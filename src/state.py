import json
from typing import Optional
import base58
from borsh_construct import *
from .ledger import *
from solders.keypair import Keypair
from solders.pubkey import Pubkey
from solana.rpc import types
from solana.rpc.async_api import AsyncClient
from solana.transaction import Transaction
from solders.rpc.responses import SendTransactionResp
from solders.signature import Signature
import os


class Constants:
    INGL_CONFIG_SEED = "ingl_config";
    URIS_ACCOUNT_SEED = "uris_account";
    GENERAL_ACCOUNT_SEED = "general_account";
    INGL_NFT_COLLECTION_KEY = "ingl_nft_collection";
    INGL_MINT_AUTHORITY_KEY = "ingl_mint_authority";
    COLLECTION_HOLDER_KEY = "collection_holder";
    VOTE_ACCOUNT_KEY = "vote_account";
    AUTHORIZED_WITHDRAWER_KEY = "authorized_withdrawer";
    STAKE_ACCOUNT_KEY = "stake_account";
    PD_POOL_ACCOUNT_KEY = "pd_pool_account";
    NFT_ACCOUNT_CONST = "nft_account";
    INGL_PROGRAM_AUTHORITY_KEY = "ingl_program_authority";
    INGL_PROPOSAL_KEY = "ingl_proposal";
    VALIDATOR_ID_SEED = "validator_ID___________________";
    T_STAKE_ACCOUNT_KEY = "t_stake_account_key";
    T_WITHDRAW_KEY = "t_withdraw_key";
    INGL_REGISTRY_CONFIG_SEED = 'config'

    TEAM_ACCOUNT_KEY = Pubkey.from_string("Team111111111111111111111111111111111111111")
    STAKE_PROGRAM_ID = Pubkey.from_string("Stake11111111111111111111111111111111111111")
    STAKE_CONFIG_PROGRAM_ID = Pubkey.from_string("StakeConfig11111111111111111111111111111111")
    VOTE_PROGRAM_ID = Pubkey.from_string("Vote111111111111111111111111111111111111111")
    BPF_LOADER_UPGRADEABLE = Pubkey.from_string("BPFLoaderUpgradeab1e11111111111111111111111")
    REGISTRY_PROGRAM_ID = Pubkey.from_string("38pfsot7kCZkrttx1THEDXEz4JJXmCCcaDoDieRtVuy5")


VoteReward = CStruct(
    "epoch_number" / U64,
    "total_reward" / U64,
    "total_stake" / U32,
    "nft_holders_reward" / U64,
)

UpgradeVote = CStruct(
    "vote" / Bool,
    "validator_id" / U8[32],
)

ValidatorConfig = CStruct(
    "validation_phrase" / U32,
    "is_validator_id_switchable" / Bool,
    "max_primary_stake" / U64,
    "nft_holders_share" / U8,
    "initial_redemption_fee" / U8,
    "unit_stake" / U64,
    "redemption_fee_duration" / U32,
    "proposal_quorum" / U8,
    "creator_royalties" / U16,
    "commission" / U8,
    "validator_id" / U8[32],
    "governance_expiration_time" / U32,
    "default_uri" / String,
    "validator_name" / String,
    "twitter_handle" / String,
    "discord_invite" / String,
    "website" / String,
)
RebalancingData = CStruct(
    "pending_validator_rewards" / U64,
    "unclaimed_validator_rewards" / U64,
    "is_rebalancing_active" / Bool,
)

GeneralData = CStruct(
    "validation_phrase" / U32,
    "mint_numeration" / U32,
    "pending_delegation_total" / U64,
    "dealloced" / U64,
    "total_delegated" / U64,
    "last_withdraw_epoch" / U64,
    "last_total_staked" / U64,
    "is_t_stake_initialized" / Bool,
    "proposal_numeration" / U32,
    "last_feeless_redemption_date" / U32,
    "last_validated_validator_id_proposal" / U32,
    "rebalancing_data" / RebalancingData,
    "vote_rewards" / Vec(VoteReward),
)
RegistryConfig  = CStruct(
    "validation_phase" / U32,
    "validator_numeration" / U32,
)

class rpc_url:
    DEVNET = "https://api.devnet.solana.com"
    TESTNET = "https://api.testnet.solana.com"
    MAINNET = "https://api.mainnet.solana.com"
    target_network = DEVNET
    
def get_explorer_suffix():
    if rpc_url.target_network == rpc_url.DEVNET:
        return "?cluster=devnet"
    elif rpc_url.target_network == rpc_url.TESTNET:
        return "?cluster=testnet"
    else:
        return ""

def get_network_url(network: str) -> str:
    if network == "devnet":
        return rpc_url.DEVNET
    elif network == "testnet":
        return rpc_url.TESTNET
    elif network == "mainnet":
        return rpc_url.MAINNET
    else:
        raise Exception("Invalid network")


def keypair_from_json(filepath):
    keypair = Keypair.from_bytes(json.load(open(filepath)))
    return keypair

class KeypairInput:
    def __init__(self, t_keypair: Optional[Keypair] = None, ledger_address: Optional[int] = None, pubkey: Optional[Pubkey] = None):
        assert t_keypair or ledger_address, "KeypairInput must have at least one of keypair or ledger_address"
        self.keypair = t_keypair
        self.ledger_address = ledger_address
        self.pubkey = pubkey if pubkey else t_keypair.pubkey() if t_keypair else Pubkey.new_unique()
    
    def __str__(self):
        return f"KeypairInput(keypair={self.keypair}, ledger_address={self.ledger_address}, pubkey={self.pubkey})"

    def __repr__(self):
        return self.__str__()

def parse_keypair_input(str_input: str) -> KeypairInput:
    if str_input.startswith("Ledger://"):
        t_dongle = ledgerDongle()
        pub_key = t_dongle.get_address(int(str_input[9:]))
        return KeypairInput(ledger_address=int(str_input[9:]), pubkey=pub_key)
    else:
        t_keypair=keypair_from_json(str_input)
        return KeypairInput(t_keypair=t_keypair)
class PubkeyInput:
    def __init__(self, t_keypair: Optional[Keypair] = None, pubkey: Optional[Pubkey] = None, ledger_address: Optional[int] = None):
        assert t_keypair or pubkey or ledger_address, "PubkeyInput must have at least one of keypair, pubkey or ledger_address"
        self.keypair = t_keypair
        self.pubkey = t_keypair.pubkey() if t_keypair else pubkey
        self.ledger_address = ledger_address
    
    def __str__(self):
        return f"PubkeyInput(keypair={self.keypair}, pubkey={self.pubkey}, ledger_address={self.ledger_address})"

    def __repr__(self):
        return self.__str__()

def parse_pubkey_input(str_input: str) -> PubkeyInput:
    if str_input.startswith("Ledger://"):
        t_dongle = ledgerDongle()
        pub_key = t_dongle.get_address(int(str_input[9:]))
        return PubkeyInput(ledger_address=int(str_input[9:]), pubkey=pub_key)
    else:
        try:
            pubkey = PubkeyInput(pubkey=Pubkey.from_string(str_input))
            return pubkey
        except Exception as e:
            try:
                t_keypair = keypair_from_json(str_input)
                return PubkeyInput(t_keypair=t_keypair)
            except Exception as new_e:
                print("invalid public key input")
                raise new_e
            
async def sign_and_send_tx(tx: Transaction, client: AsyncClient, *args) -> SendTransactionResp:
    last_valid_block_height = None
    if client.blockhash_cache:
        try:
            recent_blockhash = client.blockhash_cache.get()
        except ValueError:
            blockhash_resp = await client.get_latest_blockhash(Finalized)
            recent_blockhash = client._process_blockhash_resp(blockhash_resp, used_immediately=True)
            last_valid_block_height = blockhash_resp.value.last_valid_block_height
    else:
        blockhash_resp = await client.get_latest_blockhash(Finalized)
        recent_blockhash = client.parse_recent_blockhash(blockhash_resp)
        last_valid_block_height = blockhash_resp.value.last_valid_block_height
    tx.recent_blockhash = recent_blockhash

    # print("signing actually args: ", args)
    for arg in args:
        # print(arg)
        if isinstance(arg, KeypairInput):
            # print("p_key: ", arg.pubkey, "keypair: ", arg.keypair, "ledger: ", arg.ledger_address)
            if arg.keypair is not None:
                tx.sign_partial(arg.keypair)
            elif arg.ledger_address is not None:
                t_dongle = ledgerDongle()
                message = await make_message(tx, client, False)
                # print("message: ", message)
                signature = Signature.from_bytes(t_dongle.sign(message, arg.ledger_address))
                tx.add_signature(arg.pubkey, signature)
            else:
                raise Exception("KeypairInput is not valid")
        else:
            raise ValueError("Invalid argument expected a KeypairInput, Found -> : " + str(type(arg)))
    # print("Reached here")
    opts_to_use = types.TxOpts(preflight_commitment=client._commitment, last_valid_block_height=last_valid_block_height)
    txn_resp = await client.send_raw_transaction(tx.serialize(), opts=opts_to_use)
    if client.blockhash_cache:
        blockhash_resp = await client.get_latest_blockhash(Finalized)
        client._process_blockhash_resp(blockhash_resp, used_immediately=False)
    # print("finished")
    return txn_resp

def set_config(key: str, value: str):
    file_dir = f"{os.path.expanduser('~')}/.config/solana/ingl/"
    os.makedirs(file_dir, exist_ok=True)
    file_dir = file_dir + "config.json"
    try:
        f = open(file_dir, 'r')
        config = json.load(f)
        f.close()
    except:
        config = {}
    config[key] = value
    with open(file_dir, 'w') as f:
        json.dump(config, f)

def get_config(key: str) -> str:
    file_dir = f"{os.path.expanduser('~')}/.config/solana/ingl/"
    os.makedirs(file_dir, exist_ok=True)
    file_dir = file_dir + "config.json"
    try:
        f = open(file_dir, 'r')
        config = json.load(f)
        f.close()
        if key in config:
            return config[key]
        else:
            return ""
    except:
        return ""


def get_program_id() -> Pubkey:
    program_id_str = get_config('program_id')
    try:
        return Pubkey.from_string(program_id_str)
    except:
        return Pubkey.from_string("HD8kYhgqmZCJ881vyBQ3fR6a62YL7cZBnYj1P7oLw8An")

def set_program_id(program_id: str):
    set_config('program_id', program_id)

def get_network() -> str:
    network = get_config('network')
    if network == "":
        return get_network_url(network = 'devnet')
    else:
        return network

def set_network(network: str):
    set_config('network', network)

def get_keypair_path() -> str:
    keypair_path = get_config('keypair_path')
    if keypair_path == "":
        return f"{os.path.expanduser('~')}/.config/solana/ingl/id.json"
    else:
        return keypair_path
    
def set_keypair_path(keypair_path: str) -> bool:
    path = os.path.abspath(keypair_path)
    try:
        keypair = keypair_from_json(path)
    except:
        print("Invalid keypair path")
        return False
    set_config('keypair_path', path)
    print("Keypair path set to: ", path)
    print("Keypair Public Key: ", keypair.pubkey())
    return True