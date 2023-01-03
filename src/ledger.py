from ledgerblue.comm import getDongle
import struct
from solana.rpc.commitment import Finalized
from solana.publickey import PublicKey
from solana.transaction import *
from solana.sysvar import *
from solana.rpc.async_api import AsyncClient

SOL_DERIVATION_PATH = "44'/501'/"

INS_GET_PUBKEY = 0x05;
INS_SIGN_MESSAGE = 0x06;

P1_NON_CONFIRM = 0x00;
P1_CONFIRM = 0x01;

P2_EXTEND = 0x01;
P2_MORE = 0x02;

MAX_CHUNK_SIZE = 255;

LEDGER_CLA = 0xe0;


BIP32_HARDENED_BIT = ((1 << 31) >> 0)
def _harden(n):
    return (n | BIP32_HARDENED_BIT) >>0 


def _extend_and_serialize_derivations_path(derivations_path: bytes):
    return (1).to_bytes(1, byteorder='little') + derivations_path

async def make_message(tx: Transaction, asyncclient: AsyncClient, find_blockhash = True):
    if find_blockhash:
        blockhash_resp = await asyncclient.get_latest_blockhash(Finalized)
        recent_blockhash = asyncclient._process_blockhash_resp(blockhash_resp, used_immediately=True)
        tx.recent_blockhash = recent_blockhash
    return tx.serialize_message()

class ledgerDongle:
    def __init__(self):
        self.dongle = getDongle(debug=False)

    def get_derive_path(self, account = None, change = None):
        length = 0
        if type(account) == int:
            if type(change) == int:
                length = 4
            else:
                length = 3
        else:
            length = 2
        derivation_path = length.to_bytes(1, byteorder='big')
        derivation_path += _harden(44).to_bytes(4, 'big')
        derivation_path += _harden(501).to_bytes(4, 'big')
        if length > 2:
            derivation_path += _harden(account).to_bytes(4, 'big')
            if length == 4:
                derivation_path += _harden(change).to_bytes(4, 'big')
        return derivation_path

    def get_address(self, account = None, change = None):
        path = self.get_derive_path(account, change)
        data = struct.pack(">BBBBB", LEDGER_CLA, INS_GET_PUBKEY, P1_NON_CONFIRM, 0,len(path)) + path
        response = self.dongle.exchange(data)
        return PublicKey(response)


    def list(self, limit=5, page=0):
        return list(map(lambda offset: self.get_address(offset), range(page*limit, (page+1)*limit)))

    def sign(self, message, offset: int):
        assert len(message) <= 65535, "Message to sign is too long"
        derivation_path = self.get_derive_path(offset)
        header: bytes = _extend_and_serialize_derivations_path(derivation_path)
       
        max_size = MAX_CHUNK_SIZE - len(header)
        message_splited = [message[x:x+max_size] for x in range(0, len(message), max_size)]
        message_splited_prefixed = [header + s for s in message_splited]

        if len(message_splited_prefixed) > 1:
            final_p2 = P2_EXTEND
            for m in message_splited_prefixed[:-1]:
                data = struct.pack(">BBBBB", LEDGER_CLA, INS_SIGN_MESSAGE, P1_CONFIRM, P2_MORE | P2_EXTEND, len(m)) + m
                self.dongle.exchange(data)
        else:
            final_p2 = 0

        data = struct.pack(">BBBBB", LEDGER_CLA, INS_SIGN_MESSAGE, P1_CONFIRM, final_p2, len(message_splited_prefixed[-1])) + message_splited_prefixed[-1]
        # print(base58.b58encode(data))
        response = self.dongle.exchange(data)
        return response