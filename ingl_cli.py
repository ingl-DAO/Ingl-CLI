import click
from instruction import keypair_from_json
from processor import *
from solana.keypair import Keypair
from solana.rpc.api import Client
from solana.publickey import PublicKey
from borsh_construct import *
from state import ClassEnum
from state import Constants as ingl_constants
from state import GlobalGems
import base64
client = Client("https://api.devnet.solana.com")

@click.group()
def entry():
    pass

@click.group(name="mint")
@click.option('--keypair', default = 'keypair.json')
def mint(keypair):
    pass

@click.command(name="Benitoite")
@click.option('--keypair', default = 'keypair.json')
def Benitoite(keypair):
    print("Client is connected" if client.is_connected() else "Client is Disconnected")
    payer_keypair = keypair_from_json(f"./{keypair}")
    mint_keypair = Keypair()
    print("Mint_Id: ", mint_keypair.public_key)
    print("Transaction ID: ", mint_nft(payer_keypair, mint_keypair, ClassEnum.enum.Benitoite(), client)['result'])

@click.command(name="Serendibite")
@click.option('--keypair', default = 'keypair.json')
def Serendibite(keypair):
    print("Client is connected" if client.is_connected() else "Client is Disconnected")
    payer_keypair = keypair_from_json(f"./{keypair}")
    mint_keypair = Keypair()
    print("Mint_Id: ", mint_keypair.public_key)
    print("Transaction ID: ", mint_nft(payer_keypair, mint_keypair, ClassEnum.enum.Serendibite(), client)['result'])

@click.command(name="Sapphire")
@click.option('--keypair', default = 'keypair.json')
def Sapphire(keypair):
    print("Client is connected" if client.is_connected() else "Client is Disconnected")
    payer_keypair = keypair_from_json(f"./{keypair}")
    mint_keypair = Keypair()
    print("Mint_Id: ", mint_keypair.public_key)
    print("Transaction ID: ", mint_nft(payer_keypair, mint_keypair, ClassEnum.enum.Sapphire(), client)['result'])

@click.command(name="Emerald")
@click.option('--keypair', default = 'keypair.json')
def Emerald(keypair):
    print("Client is connected" if client.is_connected() else "Client is Disconnected")
    payer_keypair = keypair_from_json(f"./{keypair}")
    mint_keypair = Keypair()
    print("Mint_Id: ", mint_keypair.public_key)
    print("Transaction ID: ", mint_nft(payer_keypair, mint_keypair, ClassEnum.enum.Emerald(), client)['result'])

@click.command(name="Diamond")
@click.option('--keypair', default = 'keypair.json')
def Diamond(keypair):
    print("Client is connected" if client.is_connected() else "Client is Disconnected")
    payer_keypair = keypair_from_json(f"./{keypair}")
    mint_keypair = Keypair()
    print("Mint_Id: ", mint_keypair.public_key)
    print("Transaction ID: ", mint_nft(payer_keypair, mint_keypair, ClassEnum.enum.Diamond(), client)['result'])

@click.command(name="Ruby")
@click.option('--keypair', default = 'keypair.json')
def Ruby(keypair):
    print("Client is connected" if client.is_connected() else "Client is Disconnected")
    payer_keypair = keypair_from_json(f"./{keypair}")
    mint_keypair = Keypair()
    print("Mint_Id: ", mint_keypair.public_key)
    print("Transaction ID: ", mint_nft(payer_keypair, mint_keypair, ClassEnum.enum.Ruby(), client)['result'])

mint.add_command(Benitoite)
mint.add_command(Serendibite)
mint.add_command(Emerald)
mint.add_command(Sapphire)
mint.add_command(Diamond)
mint.add_command(Ruby)


@click.command(name="create_validator_proposal")
@click.option('--keypair', default = 'keypair.json')
def create_val_proposal(keypair):
    print("Client is connected" if client.is_connected() else "Client is Disconnected")
    payer_keypair = keypair_from_json(f"./{keypair}")
    global_gem_pubkey, _global_gem_bump = PublicKey.find_program_address([bytes(ingl_constants.GLOBAL_GEM_KEY, 'UTF-8')], ingl_constants.INGL_PROGRAM_ID)
    numeration = GlobalGems.parse(base64.urlsafe_b64decode(client.get_account_info(global_gem_pubkey)['result']['value']['data'][0])).proposal_numeration
    print("Transaction ID: ", create_validator_proposal(payer_keypair, numeration, client)['result'])

@click.command(name="finalize_proposal")
@click.option('--keypair', default = 'keypair.json')
def finalize_validator_proposal(keypair):
    print("Client is connected" if client.is_connected() else "Client is Disconnected")
    payer_keypair = keypair_from_json(f"./{keypair}")

    global_gem_pubkey, _global_gem_bump = PublicKey.find_program_address([bytes(ingl_constants.GLOBAL_GEM_KEY, 'UTF-8')], ingl_constants.INGL_PROGRAM_ID)

    global_gems = GlobalGems.parse(base64.urlsafe_b64decode(client.get_account_info(global_gem_pubkey)['result']['value']['data'][0]))
    numeration = global_gems.proposal_numeration
    print("Transaction ID: ", finalize_proposal(payer_keypair, numeration-1, client)['result'])

@click.command(name='register_validator')
@click.option('--keypair', default = 'keypair.json')
@click.argument('validator_keypair')
def reg_validator(validator_keypair, keypair):
    print("Client is connected" if client.is_connected() else "Client is Disconnected")
    payer_keypair = keypair_from_json(f"./{keypair}")
    validator_keypair = keypair_from_json(f"{validator_keypair}")
    print("Validator Key: ", validator_keypair.public_key)
    print("Transaction ID: ", register_validator_id(payer_keypair, validator_keypair.public_key, client)['result'])

@click.command(name="init_rebalance")
@click.argument('vote_key')
@click.option('--keypair', default = 'keypair.json')
def initialize_rebalancing(vote_key, keypair):
    print("Client is connected" if client.is_connected() else "Client is Disconnected")
    payer_keypair = keypair_from_json(f"./{keypair}")
    vote_account_id = PublicKey(vote_key)
    print("Transaction ID: ", init_rebalance(payer_keypair, vote_account_id, client)['result'])

@click.command(name="finalize_rebalance")
@click.argument('vote_key')
@click.option('--keypair', default = 'keypair.json')
def finalize_rebalancing(vote_key, keypair):
    print("Client is connected" if client.is_connected() else "Client is Disconnected")
    payer_keypair = keypair_from_json(f"./{keypair}")
    vote_account_id = PublicKey(vote_key)
    print("Transaction ID: ", finalize_rebalance(payer_keypair, vote_account_id, client)['result'])

@click.command(name="create_collection")
@click.option('--keypair', default = 'keypair.json')
def create_new_collection(keypair):
    print("Client is connected" if client.is_connected() else "Client is Disconnected")
    payer_keypair = keypair_from_json(f"./{keypair}")
    print("Transaction ID: ", create_collection(payer_keypair, client)['result'])

@click.command(name="close_proposal")
@click.option('--keypair', default = 'keypair.json')
def close_val_proposal(keypair):
    print("Client is connected" if client.is_connected() else "Client is Disconnected")
    payer_keypair = keypair_from_json(f"./{keypair}")
    global_gem_pubkey, _global_gem_bump = PublicKey.find_program_address([bytes(ingl_constants.GLOBAL_GEM_KEY, 'UTF-8')], ingl_constants.INGL_PROGRAM_ID)
    numeration = GlobalGems.parse(base64.urlsafe_b64decode(client.get_account_info(global_gem_pubkey)['result']['value']['data'][0])).proposal_numeration
    print("Transaction ID: ", close_proposal(payer_keypair, numeration-1, client)['result'])

@click.command(name="process_rewards")
@click.option('--keypair', default = 'keypair.json')
@click.argument('vote_key')
def process_vote_account_rewards(keypair, vote_key):
    print("Client is connected" if client.is_connected() else "Client is Disconnected")
    payer_keypair = keypair_from_json(f"./{keypair}") 
    vote_account_id = PublicKey(vote_key)
    print("Transaction ID: ", process_rewards(payer_keypair, vote_account_id, client)['result'])

@click.command(name='create_vote_account')
@click.argument('val_keypair')
def process_create_vote_account(val_keypair):
    print("Client is connected" if client.is_connected() else "Client is Disconnected")
    payer_keypair = keypair_from_json(f"./{val_keypair}")
    global_gem_pubkey, _global_gem_bump = PublicKey.find_program_address([bytes(ingl_constants.GLOBAL_GEM_KEY, 'UTF-8')], ingl_constants.INGL_PROGRAM_ID)
    numeration = GlobalGems.parse(base64.urlsafe_b64decode(client.get_account_info(global_gem_pubkey)['result']['value']['data'][0])).proposal_numeration
    print("Transaction Id: ", create_vote_account(payer_keypair, numeration-1, client)['result'])

@click.command(name="get_vote_pubkey")
@click.option('--numeration', '-n', default=None)
def get_vote_pubkey(numeration):
    if numeration:
        expected_vote_pubkey, _expected_vote_pubkey_nonce = PublicKey.find_program_address([bytes(ingl_constants.VOTE_ACCOUNT_KEY, "UTF-8"), int(numeration-1).to_bytes(4,"big")], ingl_constants.INGL_PROGRAM_ID)
    else:
        global_gem_pubkey, _global_gem_bump = PublicKey.find_program_address([bytes(ingl_constants.GLOBAL_GEM_KEY, 'UTF-8')], ingl_constants.INGL_PROGRAM_ID)
        numeration = GlobalGems.parse(base64.urlsafe_b64decode(client.get_account_info(global_gem_pubkey)['result']['value']['data'][0])).proposal_numeration - 1 
        if numeration < 0:
            print("Please precise the Proposal numeration using the '-n' command or the  '--numeration' command ")
            return
        expected_vote_pubkey, _expected_vote_pubkey_nonce = PublicKey.find_program_address([bytes(ingl_constants.VOTE_ACCOUNT_KEY, "UTF-8"), (numeration-1).to_bytes(4,"big")], ingl_constants.INGL_PROGRAM_ID)
        print("Vote account for Proposal No: ", numeration+1, "You can precise the specific proposal with the '-n' option")
    print("Vote Pubkey: ", expected_vote_pubkey)

@click.command(name="find_vote_key")
@click.argument('val_pubkey')
def find_vote_key(val_pubkey):
    val_pubkey = PublicKey(val_pubkey) 
    global_gem_pubkey, _global_gem_bump = PublicKey.find_program_address([bytes(ingl_constants.GLOBAL_GEM_KEY, 'UTF-8')], ingl_constants.INGL_PROGRAM_ID)
    numeration = GlobalGems.parse(base64.urlsafe_b64decode(client.get_account_info(global_gem_pubkey)['result']['value']['data'][0])).proposal_numeration - 1
    for i in range(numeration):
        expected_vote_pubkey, _expected_vote_pubkey_nonce = PublicKey.find_program_address([bytes(ingl_constants.VOTE_ACCOUNT_KEY, "UTF-8"), (i).to_bytes(4,"big")], ingl_constants.INGL_PROGRAM_ID)
        expected_vote_data_pubkey, _expected_vote_data_bump = PublicKey.find_program_address([bytes(ingl_constants.VOTE_DATA_ACCOUNT_KEY, 'UTF-8'), bytes(expected_vote_pubkey)], ingl_constants.INGL_PROGRAM_ID)
        validator_id = PublicKey(InglVoteAccountData.parse(base64.urlsafe_b64decode(client.get_account_info(expected_vote_data_pubkey)['result']['value']['data'][0])).validator_id)
        if validator_id == val_pubkey:
            print("Vote_Pubkey: ", expected_vote_pubkey)
            print("Proposal_numeration: ", i+1)
            return
    print("Couldn't find a vote account with the specified authorized validator.")
    print("Check to see if validator Was winner of the latest proposal")

entry.add_command(mint)
entry.add_command(reg_validator)
entry.add_command(create_val_proposal)
entry.add_command(finalize_validator_proposal)
entry.add_command(reg_validator)
entry.add_command(initialize_rebalancing)
entry.add_command(finalize_rebalancing)
entry.add_command(create_new_collection)
entry.add_command(close_val_proposal)
entry.add_command(process_vote_account_rewards)
entry.add_command(process_create_vote_account)
entry.add_command(get_vote_pubkey)
entry.add_command(find_vote_key)
if __name__ == '__main__':
    entry()