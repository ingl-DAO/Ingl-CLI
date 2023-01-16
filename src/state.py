import json
from typing import Optional
import base58
from borsh_construct import *
from .ledger import *
from solana.keypair import Keypair
from solana.publickey import PublicKey
from solana.rpc import types
from solana.rpc.async_api import AsyncClient
from solana.transaction import Transaction
from solders.rpc.responses import SendTransactionResp
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

    TEAM_ACCOUNT_KEY = PublicKey("Team111111111111111111111111111111111111111")
    STAKE_PROGRAM_ID = PublicKey("Stake11111111111111111111111111111111111111")
    STAKE_CONFIG_PROGRAM_ID = PublicKey("StakeConfig11111111111111111111111111111111")
    VOTE_PROGRAM_ID = PublicKey("Vote111111111111111111111111111111111111111")
    BPF_LOADER_UPGRADEABLE = PublicKey("BPFLoaderUpgradeab1e11111111111111111111111")


def keypair_from_json(filepath):
    keypair = Keypair.from_secret_key(json.load(open(filepath)))
    return keypair

def pubkey_from_json(filepath): #Not Tested yet.
    return PublicKey(json.load(filepath.open()))

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

ProgramUpgradeData = CStruct(
    "validation_phrase" / U32,
    "buffer_address" / U8[32],
    "code_link" / String,
    "is_still_ongoing" / Bool,
    "votes" / HashMap(U8[32], UpgradeVote),
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
    "total_delegated" / U32,
    "last_withdraw_epoch" / U64,
    "last_total_staked" / U64,
    "is_t_stake_initialized" / Bool,
    "proposal_numeration" / U32,
    "last_feeless_redemption_date" / U32,
    "last_validated_validator_id_proposal" / U32,
    "rebalancing_data" / RebalancingData,
    "vote_rewards" / Vec(VoteReward),
)

def private_key_from_json(filepath):
    return base58.b58encode(keypair_from_json(filepath).secret_key).decode()

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

    def get_network_url(network):
        if network == "devnet":
            return rpc_url.DEVNET
        elif network == "testnet":
            return rpc_url.TESTNET
        elif network == "mainnet":
            return rpc_url.MAINNET
        else:
            raise Exception("Invalid network")



class KeypairInput:
    def __init__(self, keypair: Optional[Keypair] = None, ledger_address: Optional[int] = None, pubkey: Optional[PublicKey] = None):
        assert keypair or ledger_address, "KeypairInput must have at least one of keypair or ledger_address"
        self.keypair = keypair
        self.ledger_address = ledger_address
        self.public_key = pubkey if pubkey else keypair.public_key if keypair else None

def parse_keypair_input(str_input: String) -> KeypairInput:
    if str_input.startswith("Ledger://"):
        t_dongle = ledgerDongle()
        pub_key = t_dongle.get_address(int(str_input[9:]))
        return KeypairInput(ledger_address=int(str_input[9:]), pubkey=pub_key)
    else:
        t_keypair=keypair_from_json(str_input)
        return KeypairInput(keypair=t_keypair, pubkey=t_keypair.public_key)
class PubkeyInput:
    def __init__(self, keypair: Optional[Keypair] = None, pubkey: Optional[PublicKey] = None, ledger_address: Optional[int] = None):
        assert keypair or pubkey or ledger_address, "PubkeyInput must have at least one of keypair, pubkey or ledger_address"
        self.keypair = keypair
        self.public_key = keypair.public_key if keypair else pubkey
        self.ledger_address = ledger_address

def parse_pubkey_input(str_input: String) -> PubkeyInput:
    if str_input.startswith("Ledger://"):
        t_dongle = ledgerDongle()
        pub_key = t_dongle.get_address(int(str_input[9:]))
        return PubkeyInput(ledger_address=int(str_input[9:]), pubkey=pub_key)
    else:
        try:
            pubkey = PubkeyInput(pubkey=PublicKey(str_input))
            return pubkey
        except Exception as e:
            if 'invalid public key input:' in str(e):
                try:
                    t_keypair = keypair_from_json(str_input)
                    return PubkeyInput(keypair=t_keypair, pubkey=t_keypair.public_key)
                except Exception as new_e:
                    print("invalid public key input")
                    raise new_e
            else:
                print("invalid public key input")
                raise e

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
            # print("p_key: ", arg.public_key, "keypair: ", arg.keypair, "ledger: ", arg.ledger_address)
            if arg.keypair is not None:
                tx.sign_partial(arg.keypair)
            elif arg.ledger_address is not None:
                t_dongle = ledgerDongle()
                message = await make_message(tx, client, False)
                # print("message: ", message)
                signature = Signature.from_bytes(t_dongle.sign(message, arg.ledger_address))
                tx.add_signature(arg.public_key, signature)
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


def get_program_id() -> PublicKey:
    program_id_str = get_config('program_id')
    try:
        return PublicKey(program_id_str)
    except:
        return PublicKey("HD8kYhgqmZCJ881vyBQ3fR6a62YL7cZBnYj1P7oLw8An")

def set_program_id(program_id: str):
    set_config('program_id', program_id)

def get_network() -> str:
    network = get_config('network')
    if network == "":
        return rpc_url.get_network_url('devnet')
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
    
def set_keypair_path(keypair_path: str):
    set_config('keypair_path', keypair_path)