import asyncclick as click
from .instruction import *
from .processor import *
from solana.keypair import Keypair
from solana.rpc.api import Client as Uasyncclient
from solana.publickey import PublicKey
from borsh_construct import *
from .state import *
from .utils import *
from .state import Constants as ingl_constants
from rich import print
from solana.rpc.async_api import AsyncClient
from .cli_state import CLI_VERSION
uasyncclient = Uasyncclient(rpc_url.target_network)

@click.group()
@click.version_option(version=CLI_VERSION)
def entry():
    pass


@click.group(name="mint")
async def mint():
    pass

async def mint_helper(keypair, log_level, class_enum):
    log_level = int(log_level)
    client = AsyncClient(rpc_url.target_network)
    client_state = await client.is_connected()
    print("Client is connected" if client_state else "Client is Disconnected")
    payer_keypair = parse_keypair_input(f"./{keypair}")
    mint_keypair = KeypairInput(keypair = Keypair())
    print("Mint_Id: ", mint_keypair.public_key)
    t_dets = await mint_nft(payer_keypair, mint_keypair, class_enum, client, log_level)
    print(t_dets)
    await client.close()

@click.command(name="Benitoite")
@click.option('--keypair', default = 'keypair.json')
@click.option('--log_level', default = '2')
async def Benitoite(keypair, log_level: int = 0):
    await mint_helper(keypair, log_level, ClassEnum.enum.Benitoite())

@click.command(name="Serendibite")
@click.option('--keypair', default = 'keypair.json')
@click.option('--log_level', default = '2')
async def Serendibite(keypair, log_level: int = 0):
    await mint_helper(keypair, log_level, ClassEnum.enum.Serendibite())

@click.command(name="Sapphire")
@click.option('--keypair', default = 'keypair.json')
@click.option('--log_level', default = '2')
async def Sapphire(keypair, log_level: int = 0):
    await mint_helper(keypair, log_level, ClassEnum.enum.Sapphire())

@click.command(name="Emerald")
@click.option('--keypair', default = 'keypair.json')
@click.option('--log_level', default = '2')
async def Emerald(keypair, log_level: int = 0):
    await mint_helper(keypair, log_level, ClassEnum.enum.Emerald())

@click.command(name="Diamond")
@click.option('--keypair', default = 'keypair.json')
@click.option('--log_level', default = '2')
async def Diamond(keypair, log_level: int = 0):
    await mint_helper(keypair, log_level, ClassEnum.enum.Diamond())

@click.command(name="Ruby")
@click.option('--keypair', default = 'keypair.json')
@click.option('--log_level', default = '2')
async def Ruby(keypair, log_level: int = 0):
    await mint_helper(keypair, log_level, ClassEnum.enum.Ruby())

mint.add_command(Benitoite)
mint.add_command(Serendibite)
mint.add_command(Emerald)
mint.add_command(Sapphire)
mint.add_command(Diamond)
mint.add_command(Ruby)


'''
Create a proposal for the selection of the next validator whose vote account will be created.
'''
@click.command(name="create_validator_proposal")
@click.option('--keypair', default = 'keypair.json')
@click.option('--log_level', default = '2')
async def create_val_proposal(keypair, log_level: int = 0):
    log_level = int(log_level)
    client = AsyncClient(rpc_url.target_network)
    client_state = await client.is_connected()
    print("Client is connected" if client_state else "Client is Disconnected")
    payer_keypair = parse_keypair_input(f"./{keypair}")
    global_gem_pubkey, _global_gem_bump = PublicKey.find_program_address([bytes(ingl_constants.GLOBAL_GEM_KEY, 'UTF-8')], ingl_constants.INGL_PROGRAM_ID)
    gem_info = await client.get_account_info(global_gem_pubkey)
    numeration = GlobalGems.parse(gem_info.value.data).proposal_numeration
    t_dets = await create_validator_proposal(payer_keypair, numeration, client, log_level)
    print(t_dets)
    await client.close()

'''
Now Deprecated, do not use. Use create_vote_account instead.
'''
@click.command(name="finalize_proposal")
@click.option('--keypair', default = 'keypair.json')
@click.option('--log_level', default = '2')
async def finalize_validator_proposal(keypair, log_level: int = 0):
    # log_level = int(log_level)
    # client = AsyncClient(rpc_url.target_network)
    # client_state = await client.is_connected()
    # print("Client is connected" if client_state else "Client is Disconnected")
    # payer_keypair = parse_keypair_input(f"./{keypair}")

    # global_gem_pubkey, _global_gem_bump = PublicKey.find_program_address([bytes(ingl_constants.GLOBAL_GEM_KEY, 'UTF-8')], ingl_constants.INGL_PROGRAM_ID)
    # gem_info = await client.get_account_info(global_gem_pubkey)
    # global_gems = GlobalGems.parse(gem_info.value.data)
    # numeration = global_gems.proposal_numeration
    # t_dets = await finalize_proposal(payer_keypair, client, log_level)
    # print(t_dets)
    # client.close()
    print("Instruction has been deprecated. Use 'create_vote_account' instead.")

@click.command(name="allocate_gem")
@click.argument('mint_id')
@click.option('--keypair', default = 'keypair.json')
@click.option('--log_level', default = '2')
async def process_allocate_gem(mint_id, keypair, log_level: int = 0):
    log_level = int(log_level)
    client = AsyncClient(rpc_url.target_network)
    client_state = await client.is_connected()
    print("Client is connected" if client_state else "Client is Disconnected")
    payer_keypair = parse_keypair_input(f"./{keypair}")
    mint_pubkey = parse_pubkey_input(mint_id)
    t_dets = await allocate_sol(payer_keypair, mint_pubkey, client, log_level)
    print(t_dets)
    await client.close()

@click.command(name="deallocate_gem")
@click.argument('mint_id')
@click.option('--keypair', default = 'keypair.json')
@click.option('--log_level', default = '2')
async def process_deallocate_gem(mint_id, keypair, log_level: int = 0):
    log_level = int(log_level)
    client = AsyncClient(rpc_url.target_network)
    client_state = await client.is_connected()
    print("Client is connected" if client_state else "Client is Disconnected")
    payer_keypair = parse_keypair_input(f"./{keypair}")
    mint_pubkey = parse_pubkey_input(mint_id)
    t_dets = await deallocate_sol(payer_keypair, mint_pubkey, client, log_level)
    print(t_dets)
    await client.close()



@click.command(name='register_validator')
@click.option('--keypair', default = 'keypair.json')
@click.argument('validator_keypair')
@click.option('--log_level', default = '2')
async def reg_validator(validator_keypair, keypair, log_level: int = 0):
    log_level = int(log_level)
    client = AsyncClient(rpc_url.target_network)
    client_state = await client.is_connected()
    print("Client is connected" if client_state else "Client is Disconnected")
    payer_keypair = parse_keypair_input(f"./{keypair}")
    validator_keypair = parse_keypair_input(f"{validator_keypair}")
    print("Validator Key: ", validator_keypair.public_key)
    t_dets = await register_validator_id(payer_keypair, PubkeyInput(pubkey = validator_keypair.public_key), client, log_level)
    print(t_dets)
    await client.close()

@click.command(name="init_rebalance")
@click.argument('vote_key')
@click.option('--keypair', default = 'keypair.json')
@click.option('--log_level', default = '2')
async def initialize_rebalancing(vote_key, keypair, log_level: int = 0):
    log_level = int(log_level)
    client = AsyncClient(rpc_url.target_network)
    client_state = await client.is_connected()
    print("Client is connected" if client_state else "Client is Disconnected")
    payer_keypair = parse_keypair_input(f"./{keypair}")
    vote_account_id = parse_pubkey_input(vote_key)
    t_dets = await init_rebalance(payer_keypair, vote_account_id, client, log_level)
    print(t_dets)
    await client.close()

@click.command(name="finalize_rebalance")
@click.argument('vote_key')
@click.option('--keypair', default = 'keypair.json')
@click.option('--log_level', default = '2')
async def finalize_rebalancing(vote_key, keypair, log_level: int = 0):
    log_level = int(log_level)
    client = AsyncClient(rpc_url.target_network)
    client_state = await client.is_connected()
    print("Client is connected" if client_state else "Client is Disconnected")
    payer_keypair = parse_keypair_input(f"./{keypair}")
    vote_account_id = parse_pubkey_input(vote_key)
    t_dets = await finalize_rebalance(payer_keypair, vote_account_id, client, log_level)
    print(t_dets)
    await client.close()

@click.command(name="init")
@click.option('--keypair', default = 'keypair.json')
@click.option('--log_level', default = '2')
async def ingl(keypair, log_level: int = 0):
    log_level = int(log_level)
    client = AsyncClient(rpc_url.target_network)
    client_state = await client.is_connected()
    print("Client is connected" if client_state else "Client is Disconnected")
    payer_keypair = parse_keypair_input(f"./{keypair}")
    t_dets = await ingl_init(payer_keypair, client, log_level)
    print(t_dets)
    await client.close()

@click.command(name="close_proposal")
@click.option('--keypair', default = 'keypair.json')
@click.option('--log_level', default = '2')
async def close_val_proposal(keypair, log_level: int = 0):
    log_level = int(log_level)
    client = AsyncClient(rpc_url.target_network)
    client_state = await client.is_connected()
    print("Client is connected" if client_state else "Client is Disconnected")
    payer_keypair = parse_keypair_input(f"./{keypair}")
    global_gem_pubkey, _global_gem_bump = PublicKey.find_program_address([bytes(ingl_constants.GLOBAL_GEM_KEY, 'UTF-8')], ingl_constants.INGL_PROGRAM_ID)
    gem_info = await client.get_account_info(global_gem_pubkey)
    numeration = GlobalGems.parse(gem_info.value.data).proposal_numeration
    t_dets = await close_proposal(payer_keypair, numeration-1, client, log_level)
    print(t_dets)
    await client.close()

@click.command(name="process_rewards")
@click.option('--keypair', default = 'keypair.json')
@click.argument('vote_key')
@click.option('--log_level', default = '2')
async def process_vote_account_rewards(keypair, vote_key, log_level: int = 0):
    log_level = int(log_level)
    client = AsyncClient(rpc_url.target_network)
    client_state = await client.is_connected()
    print("Client is connected" if client_state else "Client is Disconnected")
    payer_keypair = parse_keypair_input(f"./{keypair}") 
    vote_account_id = parse_pubkey_input(vote_key)
    t_dets = await process_rewards(payer_keypair, vote_account_id, client, log_level)
    print(t_dets)
    await client.close()

@click.command(name='create_vote_account')
@click.option('--val_keypair', default = 'keypair.json')
@click.option('--log_level', default = '2')
async def process_create_vote_account(val_keypair, log_level: int = 0):
    log_level = int(log_level)
    client = AsyncClient(rpc_url.target_network)
    client_state = await client.is_connected()
    print("Client is connected" if client_state else "Client is Disconnected")
    payer_keypair = parse_keypair_input(f"./{val_keypair}")
    global_gem_pubkey, _global_gem_bump = PublicKey.find_program_address([bytes(ingl_constants.GLOBAL_GEM_KEY, 'UTF-8')], ingl_constants.INGL_PROGRAM_ID)
    gem_info = await client.get_account_info(global_gem_pubkey)
    global_gems = GlobalGems.parse(gem_info.value.data)
    numeration = global_gems.proposal_numeration
    if not global_gems.is_proposal_ongoing:
        client.close
        print("[warning]A Validator Selection Proposal is not ongoing!!![/warning]")
    t_dets = await create_vote_account(payer_keypair, numeration-1, client, log_level)
    print(t_dets)
    await client.close()

@click.command(name='vote_validator')
@click.option('--keypair', default = 'keypair.json')
@click.option('--log_level', default = '2')
@click.argument('mint_id')
@click.argument("validator_index")
async def process_vote_validator_proposal(keypair, mint_id, validator_index, log_level: int = 0):
    validator_index = int(validator_index)
    log_level = int(log_level)
    client = AsyncClient(rpc_url.target_network)
    client_state = await client.is_connected()
    print("Client is connected" if client_state else "Client is Disconnected")
    payer_keypair = parse_keypair_input(f"./{keypair}")
    mint_pubkey = parse_pubkey_input(mint_id)
    global_gem_pubkey, _global_gem_bump = PublicKey.find_program_address([bytes(ingl_constants.GLOBAL_GEM_KEY, 'UTF-8')], ingl_constants.INGL_PROGRAM_ID)
    gem_info = await client.get_account_info(global_gem_pubkey)
    global_gems = GlobalGems.parse(gem_info.value.data)
    numeration = global_gems.proposal_numeration
    if not global_gems.is_proposal_ongoing:
        client.close
        print("[warning]A Validator Selection Proposal is not ongoing!!![/warning]")
    t_dets = await vote_validator_proposal(payer_keypair, numeration-1, [mint_pubkey], validator_index, client, log_level)
    print(t_dets)
    await client.close()


@click.command(name='create_upgrade_proposal')
@click.argument('buffer')
@click.argument('code_link')
@click.option('--keypair', default = 'keypair.json')
@click.option('--log_level', default = '2')
async def process_create_upgrade_proposal(keypair, buffer, code_link, log_level: int = 0):
    log_level = int(log_level)
    client = AsyncClient(rpc_url.target_network)
    client_state = await client.is_connected()
    print("Client is connected" if client_state else "Client is Disconnected")
    payer_keypair = parse_keypair_input(f"./{keypair}")
    buffer_address = parse_pubkey_input(buffer)

    print(f"Code_Link: [link={code_link}]{code_link}[/link]")
    global_gem_pubkey, _global_gem_bump = PublicKey.find_program_address([bytes(ingl_constants.GLOBAL_GEM_KEY, 'UTF-8')], ingl_constants.INGL_PROGRAM_ID)
    gem_info = await client.get_account_info(global_gem_pubkey)
    numeration = GlobalGems.parse(gem_info.value.data).upgrade_proposal_numeration
    t_dets = await create_program_upgrade_proposal(payer_keypair, buffer_address, numeration, code_link, client, log_level)
    print(t_dets)
    await client.close()

@click.command(name='create_upgrade_proposal')
@click.argument('vote')
@click.argument('proposal')
@click.argument('vote_account')
@click.option('--keypair', default = 'keypair.json')
@click.option('--log_level', default = '2')
async def process_vote_upgrade_proposal(keypair, vote, proposal, vote_account, log_level: int = 0):
    log_level = int(log_level)
    client = AsyncClient(rpc_url.target_network)
    client_state = await client.is_connected()
    print("Client is connected" if client_state else "Client is Disconnected")
    payer_keypair = parse_keypair_input(f"./{keypair}")
    vote = parse_vote(vote)
    upgrade_proposal_pubkey, upgrade_proposal_numeration = parse_proposal(proposal)
    vote_account_key, vote_account_numeration = parse_proposal(vote_account)
    print(f"Vote_account: {vote_account_key}, Proposal_Account {upgrade_proposal_pubkey}, Vote: {'Approve' if vote else 'Dissaprove'} ");
    t_dets = await vote_program_upgrade_proposal(payer_keypair, vote, upgrade_proposal_pubkey, upgrade_proposal_numeration, vote_account_key, vote_account_numeration, client, log_level)
    print(t_dets)
    await client.close()

@click.command(name='create_upgrade_proposal')
@click.argument('proposal')
@click.option('--keypair', default = 'keypair.json')
@click.option('--log_level', default = '2')
async def process_finalize_upgrade_proposal(keypair, proposal, log_level: int = 0):
    log_level = int(log_level)
    client = AsyncClient(rpc_url.target_network)
    client_state = await client.is_connected()
    print("Client is connected" if client_state else "Client is Disconnected")
    payer_keypair = parse_keypair_input(f"./{keypair}")
    upgrade_proposal_pubkey, upgrade_proposal_numeration = parse_proposal(proposal)
    print(f"Proposal_Account {upgrade_proposal_pubkey}");
    t_dets = await finalize_program_upgrade_proposal(payer_keypair, upgrade_proposal_pubkey, upgrade_proposal_numeration, client, log_level)
    print(t_dets)
    await client.close()    


@click.command(name="get_vote_pubkey")
@click.option('--numeration', '-n', default=None)
@click.option('--validator_id', default=None)
def get_vote_pubkey(numeration):
    if numeration:
        expected_vote_pubkey, _expected_vote_pubkey_nonce = PublicKey.find_program_address([bytes(ingl_constants.VOTE_ACCOUNT_KEY, "UTF-8"), (int(numeration)-1).to_bytes(4,"big")], ingl_constants.INGL_PROGRAM_ID)
    else:
        global_gem_pubkey, _global_gem_bump = PublicKey.find_program_address([bytes(ingl_constants.GLOBAL_GEM_KEY, 'UTF-8')], ingl_constants.INGL_PROGRAM_ID)
        numeration = GlobalGems.parse(uasyncclient.get_account_info(global_gem_pubkey).value.data).proposal_numeration - 1 
        if numeration < 0:
            print("Please precise the Proposal numeration using the '-n' command or the  '--numeration' command ")
            return
        expected_vote_pubkey, _expected_vote_pubkey_nonce = PublicKey.find_program_address([bytes(ingl_constants.VOTE_ACCOUNT_KEY, "UTF-8"), (numeration-1).to_bytes(4,"big")], ingl_constants.INGL_PROGRAM_ID)
        print("Vote account for Proposal No: ", numeration+1, "You can precise the specific proposal with the '-n' option")
    print("Vote Pubkey: ", expected_vote_pubkey)

@click.command(name="find_vote_key")
@click.argument('val_pubkey')
def find_vote_key(val_pubkey):
    val_pubkey = parse_pubkey_input(val_pubkey) 
    global_gem_pubkey, _global_gem_bump = PublicKey.find_program_address([bytes(ingl_constants.GLOBAL_GEM_KEY, 'UTF-8')], ingl_constants.INGL_PROGRAM_ID)
    numeration = GlobalGems.parse(uasyncclient.get_account_info(global_gem_pubkey).value.data).proposal_numeration - 1
    for i in range(numeration):
        expected_vote_pubkey, _expected_vote_pubkey_nonce = PublicKey.find_program_address([bytes(ingl_constants.VOTE_ACCOUNT_KEY, "UTF-8"), (i).to_bytes(4,"big")], ingl_constants.INGL_PROGRAM_ID)
        expected_vote_data_pubkey, _expected_vote_data_bump = PublicKey.find_program_address([bytes(ingl_constants.VOTE_DATA_ACCOUNT_KEY, 'UTF-8'), bytes(expected_vote_pubkey)], ingl_constants.INGL_PROGRAM_ID)
        validator_id = parse_pubkey_input(InglVoteAccountData.parse(uasyncclient.get_account_info(expected_vote_data_pubkey).value.data).validator_id)
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
entry.add_command(ingl)
entry.add_command(close_val_proposal)
entry.add_command(process_vote_account_rewards)
entry.add_command(process_allocate_gem)
entry.add_command(process_deallocate_gem)
entry.add_command(process_create_vote_account)
entry.add_command(process_vote_validator_proposal)
entry.add_command(get_vote_pubkey)
entry.add_command(find_vote_key)
entry.add_command(process_create_upgrade_proposal)
entry.add_command(process_vote_upgrade_proposal)
entry.add_command(process_finalize_upgrade_proposal)
if __name__ == '__main__':
    entry()