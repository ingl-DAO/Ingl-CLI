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
import os
uasyncclient = Uasyncclient(rpc_url.target_network)

@click.group()
@click.version_option(version=CLI_VERSION)
def entry():
    pass

@click.group(name="mint")
async def mint():
    pass

async def mint_helper(keypair, log_level, class_enum):
    client = AsyncClient(rpc_url.target_network)
    client_state = await client.is_connected()
    print("Client is connected" if client_state else "Client is Disconnected")
    try:
        payer_keypair = parse_keypair_input(keypair)
    except Exception as e:
        print("Invalid Keypair Input. ")
        return
    mint_keypair = KeypairInput(keypair = Keypair())
    print("Mint_Id: ", mint_keypair.public_key)
    t_dets = await mint_nft(payer_keypair, mint_keypair, class_enum, client, log_level)
    print(t_dets)
    await client.close()

@click.command(name="Benitoite")
@click.option('--keypair', '-k', default = get_keypair_path())
@click.option('--log_level', '-l', default = '2', type=int)
async def Benitoite(keypair, log_level):
    await mint_helper(keypair, log_level, ClassEnum.enum.Benitoite())

@click.command(name="Serendibite")
@click.option('--keypair', '-k', default = get_keypair_path())
@click.option('--log_level', '-l', default = '2', type=int)
async def Serendibite(keypair, log_level):
    await mint_helper(keypair, log_level, ClassEnum.enum.Serendibite())

@click.command(name="Sapphire")
@click.option('--keypair', '-k', default = get_keypair_path())
@click.option('--log_level', '-l', default = '2', type=int)
async def Sapphire(keypair, log_level):
    await mint_helper(keypair, log_level, ClassEnum.enum.Sapphire())

@click.command(name="Emerald")
@click.option('--keypair', '-k', default = get_keypair_path())
@click.option('--log_level', '-l', default = '2', type=int)
async def Emerald(keypair, log_level):
    await mint_helper(keypair, log_level, ClassEnum.enum.Emerald())

@click.command(name="Diamond")
@click.option('--keypair', '-k', default = get_keypair_path())
@click.option('--log_level', '-l', default = '2', type=int)
async def Diamond(keypair, log_level):
    await mint_helper(keypair, log_level, ClassEnum.enum.Diamond())

@click.command(name="Ruby")
@click.option('--keypair', '-k', default = get_keypair_path())
@click.option('--log_level', '-l', default = '2', type=int)
async def Ruby(keypair, log_level):
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
@click.option('--keypair', '-k', default = get_keypair_path())
@click.option('--log_level', '-l', default = '2', type=int)
async def create_val_proposal(keypair, log_level):
    client = AsyncClient(rpc_url.target_network)
    client_state = await client.is_connected()
    print("Client is connected" if client_state else "Client is Disconnected")
    try:
        payer_keypair = parse_keypair_input(keypair)
    except Exception as e:
        print("Invalid Keypair Input. ")
        return
    global_gem_pubkey, _global_gem_bump = PublicKey.find_program_address([bytes(ingl_constants.GLOBAL_GEM_KEY, 'UTF-8')], get_program_id())
    gem_info = await client.get_account_info(global_gem_pubkey)
    numeration = GlobalGems.parse(gem_info.value.data).proposal_numeration
    t_dets = await create_validator_proposal(payer_keypair, numeration, client, log_level)
    print(t_dets)
    await client.close()

@click.group(name="config")
async def config():
    pass

@click.command(name = "set")
@click.option("--program_id", "-p")
@click.option("--url", "-u")
@click.option("--keypair", "-k")
def set(program_id, url, keypair):
    assert program_id or url or keypair, "No options specified. Use --help for more information."
    if program_id:
        try:
            program_pubkey = parse_pubkey_input(program_id)
        except Exception as e:
            print("Invalid Public Key provided.")
            return
        set_program_id(program_pubkey.public_key.__str__())
        print("Program ID set to: ", program_pubkey.public_key)
    if url:
        if url.lower() == "mainnet" or url.lower() == "testnet" or url.lower() == "devnet":
            url = rpc_url.get_network_url(url)
        set_network(url)
        print("Network set to: ", url)
    if keypair:
        set_keypair_path(keypair)
        print("Keypair set to: ", keypair)
    if not program_id and not url and not keypair:
        print("No options specified. Use --help for more information.")
        return
    print("Config set successfully.")

@click.command(name = "get")
def get():
    print("\nProgram ID: ", get_program_id())
    print("Network: ", get_network())
    print("Keypair: ", get_keypair_path())
    print("\nConfig retrieved successfully.")

config.add_command(set)
config.add_command(get)

'''
Now Deprecated, do not use. Use create_vote_account instead.
'''
@click.command(name="finalize_proposal")
@click.option('--keypair', '-k', default = get_keypair_path())
@click.option('--log_level', '-l', default = '2', type=int)
async def finalize_validator_proposal(keypair, log_level):

    # client = AsyncClient(rpc_url.target_network)
    # client_state = await client.is_connected()
    # print("Client is connected" if client_state else "Client is Disconnected")
    # try:
    #     payer_keypair = parse_keypair_input(keypair)
    # except Exception as e:
    #     print("Invalid Keypair Input. ")
    #     return

    # global_gem_pubkey, _global_gem_bump = PublicKey.find_program_address([bytes(ingl_constants.GLOBAL_GEM_KEY, 'UTF-8')], get_program_id())
    # gem_info = await client.get_account_info(global_gem_pubkey)
    # global_gems = GlobalGems.parse(gem_info.value.data)
    # numeration = global_gems.proposal_numeration
    # t_dets = await finalize_proposal(payer_keypair, client, log_level)
    # print(t_dets)
    # client.close()
    print("Instruction has been deprecated. Use 'create_vote_account' instead.")

@click.command(name="allocate_gem")
@click.argument('mint_id')
@click.option('--keypair', '-k', default = get_keypair_path())
@click.option('--log_level', '-l', default = '2', type=int)
async def process_allocate_gem(mint_id, keypair, log_level):
    client = AsyncClient(rpc_url.target_network)
    client_state = await client.is_connected()
    print("Client is connected" if client_state else "Client is Disconnected")
    try:
        payer_keypair = parse_keypair_input(keypair)
    except Exception as e:
        print("Invalid Keypair Input. ")
        return
    try:
        mint_pubkey = parse_pubkey_input(mint_id)
    except Exception as e:
        print("Invalid Public Key provided.")
        return
    t_dets = await allocate_sol(payer_keypair, mint_pubkey, client, log_level)
    print(t_dets)
    await client.close()

@click.command(name="deallocate_gem")
@click.argument('mint_id')
@click.option('--keypair', '-k', default = get_keypair_path())
@click.option('--log_level', '-l', default = '2', type=int)
async def process_deallocate_gem(mint_id, keypair, log_level):
    client = AsyncClient(rpc_url.target_network)
    client_state = await client.is_connected()
    print("Client is connected" if client_state else "Client is Disconnected")
    try:
        payer_keypair = parse_keypair_input(keypair)
    except Exception as e:
        print("Invalid Keypair Input. ")
        return
    try:
        mint_pubkey = parse_pubkey_input(mint_id)
    except Exception as e:
        print("Invalid Public Key provided.")
        return
    t_dets = await deallocate_sol(payer_keypair, mint_pubkey, client, log_level)
    print(t_dets)
    await client.close()



@click.command(name='register_validator')
@click.argument('validator_keypair')
@click.option('--log_level', '-l', default = '2', type=int)
async def reg_validator(validator_keypair, log_level):
    client = AsyncClient(rpc_url.target_network)
    client_state = await client.is_connected()
    print("Client is connected" if client_state else "Client is Disconnected")
    try:
        validator_keypair = parse_keypair_input(f"{validator_keypair}")
    except Exception as e:
        print("Invalid Keypair Input. ")
        return
    print("Validator Key: ", validator_keypair.public_key)
    t_dets = await register_validator_id(validator_keypair, client, log_level)
    print(t_dets)
    await client.close()

@click.command(name="init_rebalance")
@click.argument('vote_key')
@click.option('--keypair', '-k', default = get_keypair_path())
@click.option('--log_level', '-l', default = '2', type=int)
async def initialize_rebalancing(vote_key, keypair, log_level):
    client = AsyncClient(rpc_url.target_network)
    client_state = await client.is_connected()
    print("Client is connected" if client_state else "Client is Disconnected")
    try:
        payer_keypair = parse_keypair_input(keypair)
    except Exception as e:
        print("Invalid Keypair Input. ")
        return
    try:
        vote_account_id = parse_pubkey_input(vote_key)
    except Exception as e:
        print("Invalid Public Key provided.")
        return
    t_dets = await init_rebalance(payer_keypair, vote_account_id, client, log_level)
    print(t_dets)
    await client.close()

@click.command(name="finalize_rebalance")
@click.argument('vote_key')
@click.option('--keypair', '-k', default = get_keypair_path())
@click.option('--log_level', '-l', default = '2', type=int)
async def finalize_rebalancing(vote_key, keypair, log_level):
    client = AsyncClient(rpc_url.target_network)
    client_state = await client.is_connected()
    print("Client is connected" if client_state else "Client is Disconnected")
    try:
        payer_keypair = parse_keypair_input(keypair)
    except Exception as e:
        print("Invalid Keypair Input. ")
        return
    try:
        vote_account_id = parse_pubkey_input(vote_key)
    except Exception as e:
        print("Invalid Public Key provided.")
        return
    t_dets = await finalize_rebalance(payer_keypair, vote_account_id, client, log_level)
    print(t_dets)
    await client.close()

@click.command(name="init")
@click.option('--keypair', '-k', default = get_keypair_path())
@click.option('--log_level', '-l', default = '2', type=int)
async def ingl(keypair, log_level):
    client = AsyncClient(rpc_url.target_network)
    client_state = await client.is_connected()
    print("Client is connected" if client_state else "Client is Disconnected")
    try:
        payer_keypair = parse_keypair_input(keypair)
    except Exception as e:
        print("Invalid Keypair Input. ")
        return
    t_dets = await ingl_init(payer_keypair, client, log_level)
    print(t_dets)
    await client.close()

@click.command(name="close_proposal")
@click.option('--keypair', '-k', default = get_keypair_path())
@click.option('--log_level', '-l', default = '2', type=int)
async def close_val_proposal(keypair, log_level):
    client = AsyncClient(rpc_url.target_network)
    client_state = await client.is_connected()
    print("Client is connected" if client_state else "Client is Disconnected")
    try:
        payer_keypair = parse_keypair_input(keypair)
    except Exception as e:
        print("Invalid Keypair Input. ")
        return
    global_gem_pubkey, _global_gem_bump = PublicKey.find_program_address([bytes(ingl_constants.GLOBAL_GEM_KEY, 'UTF-8')], get_program_id())
    gem_info = await client.get_account_info(global_gem_pubkey)
    numeration = GlobalGems.parse(gem_info.value.data).proposal_numeration
    t_dets = await close_proposal(payer_keypair, numeration-1, client, log_level)
    print(t_dets)
    await client.close()

@click.command(name="process_rewards")
@click.option('--keypair', '-k', default = get_keypair_path())
@click.argument('vote_key')
@click.option('--log_level', '-l', default = '2', type=int)
async def process_vote_account_rewards(keypair, vote_key, log_level):
    client = AsyncClient(rpc_url.target_network)
    client_state = await client.is_connected()
    print("Client is connected" if client_state else "Client is Disconnected")
    try:
        payer_keypair = parse_keypair_input(keypair) 
    except Exception as e:
        print("Invalid Keypair Input. ")
        return
    try:
        vote_account_id = parse_pubkey_input(vote_key)
    except Exception as e:
        print("Invalid Public Key provided.")
        return
    t_dets = await process_rewards(payer_keypair, vote_account_id, client, log_level)
    print(t_dets)
    await client.close()

@click.command(name='create_vote_account')
@click.option('--val_keypair', default = get_keypair_path())
@click.option('--log_level', '-l', default = '2', type=int)
async def process_create_vote_account(val_keypair, log_level):
    client = AsyncClient(rpc_url.target_network)
    client_state = await client.is_connected()
    print("Client is connected" if client_state else "Client is Disconnected")
    try:
        payer_keypair = parse_keypair_input(f"./{val_keypair}")
    except Exception as e:
        print("Invalid Keypair Input. ")
        return
    global_gem_pubkey, _global_gem_bump = PublicKey.find_program_address([bytes(ingl_constants.GLOBAL_GEM_KEY, 'UTF-8')], get_program_id())
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
@click.option('--keypair', '-k', default = get_keypair_path())
@click.option('--log_level', '-l', default = '2', type=int)
@click.argument('mint_id')
@click.argument("validator_index", type=int)
async def process_vote_validator_proposal(keypair, mint_id, validator_index, log_level):
    client = AsyncClient(rpc_url.target_network)
    client_state = await client.is_connected()
    print("Client is connected" if client_state else "Client is Disconnected")
    try:
        payer_keypair = parse_keypair_input(keypair)
    except Exception as e:
        print("Invalid Keypair Input. ")
        return
    try:
        mint_pubkey = parse_pubkey_input(mint_id)
    except Exception as e:
        print("Invalid Public Key provided.")
        return
    global_gem_pubkey, _global_gem_bump = PublicKey.find_program_address([bytes(ingl_constants.GLOBAL_GEM_KEY, 'UTF-8')], get_program_id())
    gem_info = await client.get_account_info(global_gem_pubkey)
    global_gems = GlobalGems.parse(gem_info.value.data)
    numeration = global_gems.proposal_numeration
    if not global_gems.is_proposal_ongoing:
        client.close
        print("[warning]A Validator Selection Proposal is not ongoing!!![/warning]")
    t_dets = await vote_validator_proposal(payer_keypair, numeration-1, [mint_pubkey], validator_index, client, log_level)
    print(t_dets)
    await client.close()

@click.command(name='delegate_gem')
@click.argument('mint_id')
@click.argument('vote_account')
@click.option('--keypair', '-k', default = get_keypair_path())
@click.option('--log_level', '-l', default = '2', type=int)
async def process_delegate_gem(keypair, mint_id, vote_account, log_level):
    client = AsyncClient(rpc_url.target_network)
    client_state = await client.is_connected()
    print("Client is connected" if client_state else "Client is Disconnected")
    try:
        payer_keypair = parse_keypair_input(keypair)
    except Exception as e:
        print("Invalid Keypair Input. ")
        return
    try:
        mint_pubkey = parse_pubkey_input(mint_id)
    except Exception as e:
        print("Invalid Public Key provided.")
        return
    try:
        vote_account_pubkey = parse_pubkey_input(vote_account)
    except Exception as e:
        print("Invalid Public Key provided.")
        return
    t_dets = await delegate_nft(payer_keypair, mint_pubkey, vote_account_pubkey, client, log_level)
    print(t_dets)
    await client.close()

@click.command(name = 'undelegate_gem')
@click.argument('mint_id')
@click.option('--keypair', '-k', default = get_keypair_path())
@click.option('--log_level', '-l', default = '2', type=int)
async def process_undelegate_gem(keypair, mint_id, log_level):
    client = AsyncClient(rpc_url.target_network)
    client_state = await client.is_connected()
    print("Client is connected" if client_state else "Client is Disconnected")
    try:
        payer_keypair = parse_keypair_input(keypair)
    except Exception as e:
        print("Invalid Keypair Input. ")
        return
    try:
        mint_pubkey = parse_pubkey_input(mint_id)
    except Exception as e:
        print("Invalid Public Key provided.")
        return
    gem_account_pubkey, _gem_account_bump = PublicKey.find_program_address([bytes(ingl_constants.GEM_ACCOUNT_CONST, 'UTF-8'), bytes(mint_pubkey.public_key)], get_program_id())
    gem_account = await client.get_account_info(gem_account_pubkey)
    gem_account_data = gem_account.value.data
    funds_location_data = gem_account_data[20:52]
    funds_location_pubkey = PubkeyInput(pubkey = PublicKey(funds_location_data))
    # print(funds_location_pubkey)
    t_dets = await undelegate_nft(payer_keypair, mint_pubkey, funds_location_pubkey, client, log_level)
    print(t_dets)
    await client.close()

@click.command(name='create_upgrade_proposal')
@click.argument('buffer')
@click.argument('code_link')
@click.option('--keypair', '-k', default = get_keypair_path())
@click.option('--log_level', '-l', default = '2', type=int)
async def process_create_upgrade_proposal(keypair, buffer, code_link, log_level):
    client = AsyncClient(rpc_url.target_network)
    client_state = await client.is_connected()
    print("Client is connected" if client_state else "Client is Disconnected")
    try:
        payer_keypair = parse_keypair_input(keypair)
    except Exception as e:
        print("Invalid Keypair Input. ")
        return
    try:
        buffer_address = parse_pubkey_input(buffer)
    except Exception as e:
        print("Invalid Public Key provided.")
        return

    print(f"Code_Link: [link={code_link}]{code_link}[/link]")
    global_gem_pubkey, _global_gem_bump = PublicKey.find_program_address([bytes(ingl_constants.GLOBAL_GEM_KEY, 'UTF-8')], get_program_id())
    gem_info = await client.get_account_info(global_gem_pubkey)
    numeration = GlobalGems.parse(gem_info.value.data).upgrade_proposal_numeration
    t_dets = await create_program_upgrade_proposal(payer_keypair, buffer_address, numeration, code_link, client, log_level)
    print(t_dets)
    await client.close()

@click.command(name='vote_upgrade_proposal')
@click.argument('vote')
@click.argument('proposal')
@click.argument('vote_account')
@click.option('--keypair', '-k', default = get_keypair_path())
@click.option('--log_level', '-l', default = '2', type=int)
async def process_vote_upgrade_proposal(keypair, vote, proposal, vote_account, log_level):
    client = AsyncClient(rpc_url.target_network)
    client_state = await client.is_connected()
    print("Client is connected" if client_state else "Client is Disconnected")
    try:
        payer_keypair = parse_keypair_input(keypair)
    except Exception as e:
        print("Invalid Keypair Input. ")
        return
    vote = parse_vote(vote)
    upgrade_proposal_pubkey, upgrade_proposal_numeration = parse_proposal(proposal)
    vote_account_key, vote_account_numeration = parse_proposal(vote_account)
    print(f"Vote_account: {vote_account_key}, Proposal_Account {upgrade_proposal_pubkey}, Vote: {'Approve' if vote else 'Dissaprove'} ");
    t_dets = await vote_program_upgrade_proposal(payer_keypair, vote, upgrade_proposal_pubkey, upgrade_proposal_numeration, vote_account_key, vote_account_numeration, client, log_level)
    print(t_dets)
    await client.close()

@click.command(name='finalize_upgrade_proposal')
@click.argument('proposal')
@click.option('--keypair', '-k', default = get_keypair_path())
@click.option('--log_level', '-l', default = '2', type=int)
async def process_finalize_upgrade_proposal(keypair, proposal, log_level):
    client = AsyncClient(rpc_url.target_network)
    client_state = await client.is_connected()
    print("Client is connected" if client_state else "Client is Disconnected")
    try:
        payer_keypair = parse_keypair_input(keypair)
    except Exception as e:
        print("Invalid Keypair Input. ")
        return
    upgrade_proposal_pubkey, upgrade_proposal_numeration = parse_proposal(proposal)
    print(f"Proposal_Account {upgrade_proposal_pubkey}");
    t_dets = await finalize_program_upgrade_proposal(payer_keypair, upgrade_proposal_pubkey, upgrade_proposal_numeration, client, log_level)
    print(t_dets)
    await client.close()    


@click.command(name="get_vote_pubkey")
@click.option('--numeration', '-n', default=None, type=int)
def get_vote_pubkey(numeration):
    if numeration:
        expected_vote_pubkey, _expected_vote_pubkey_nonce = PublicKey.find_program_address([bytes(ingl_constants.VOTE_ACCOUNT_KEY, "UTF-8"), (numeration-1).to_bytes(4,"big")], get_program_id())
    else:
        global_gem_pubkey, _global_gem_bump = PublicKey.find_program_address([bytes(ingl_constants.GLOBAL_GEM_KEY, 'UTF-8')], get_program_id())
        numeration = GlobalGems.parse(uasyncclient.get_account_info(global_gem_pubkey).value.data).proposal_numeration - 1 
        if numeration < 0:
            print("Please precise the Proposal numeration using the '-n' command or the  '--numeration' command ")
            return
        expected_vote_pubkey, _expected_vote_pubkey_nonce = PublicKey.find_program_address([bytes(ingl_constants.VOTE_ACCOUNT_KEY, "UTF-8"), (numeration).to_bytes(4,"big")], get_program_id())
        print("Vote account for Proposal No: ", numeration, ". You can precise the specific proposal with the '-n' option")
    print("Vote Pubkey: ", expected_vote_pubkey)

@click.command(name="find_vote_key")
@click.argument('val_pubkey')
def find_vote_key(val_pubkey):
    try:
        val_pubkey = parse_pubkey_input(val_pubkey) 
    except Exception as e:
        print("Invalid Public Key provided.")
        return
    global_gem_pubkey, _global_gem_bump = PublicKey.find_program_address([bytes(ingl_constants.GLOBAL_GEM_KEY, 'UTF-8')], get_program_id())
    numeration = GlobalGems.parse(uasyncclient.get_account_info(global_gem_pubkey).value.data).proposal_numeration
    for i in range(numeration):
        expected_vote_pubkey, _expected_vote_pubkey_nonce = PublicKey.find_program_address([bytes(ingl_constants.VOTE_ACCOUNT_KEY, "UTF-8"), (i).to_bytes(4,"big")], get_program_id())
        expected_vote_data_pubkey, _expected_vote_data_bump = PublicKey.find_program_address([bytes(ingl_constants.VOTE_DATA_ACCOUNT_KEY, 'UTF-8'), bytes(expected_vote_pubkey)], get_program_id())
        validator_id = PublicKey(InglVoteAccountData.parse(uasyncclient.get_account_info(expected_vote_data_pubkey).value.data).validator_id)
        if validator_id == val_pubkey.public_key:
            print("Vote_Pubkey: ", expected_vote_pubkey)
            print("Proposal_numeration: ", i)
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
entry.add_command(process_delegate_gem)
entry.add_command(process_undelegate_gem)
entry.add_command(process_create_upgrade_proposal)
entry.add_command(process_vote_upgrade_proposal)
entry.add_command(process_finalize_upgrade_proposal)
entry.add_command(config)
if __name__ == '__main__':
    entry()