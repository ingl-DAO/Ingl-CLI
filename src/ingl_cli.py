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
import time
uasyncclient = Uasyncclient(rpc_url.target_network)

@click.group()
@click.version_option(version=CLI_VERSION)
def entry():
    pass


@click.command(name="mint")
@click.option('--keypair', '-k', default = get_keypair_path())
@click.option('--log_level', '-l', default = 2, type=int)
async def mint(keypair, log_level):
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
    t_dets = await mint_nft(payer_keypair, mint_keypair, client, log_level)
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
    try:
        print("Keypair Public Key: ", parse_keypair_input(get_keypair_path()).public_key)
    except Exception as e:
        pass
    print("\nConfig retrieved successfully.")

config.add_command(set)
config.add_command(get)

@click.command(name="init_rebalance")
@click.option('--keypair', '-k', default = get_keypair_path())
@click.option('--log_level', '-l', default = 2, type=int)
async def initialize_rebalancing(keypair, log_level):
    client = AsyncClient(rpc_url.target_network)
    client_state = await client.is_connected()
    print("Client is connected" if client_state else "Client is Disconnected")
    try:
        payer_keypair = parse_keypair_input(keypair)
    except Exception as e:
        print("Invalid Keypair Input. ")
        return
    t_dets = await init_rebalance(payer_keypair, client, log_level)
    print(t_dets)
    await client.close()

@click.command(name="finalize_rebalance")
@click.option('--keypair', '-k', default = get_keypair_path())
@click.option('--log_level', '-l', default = 2, type=int)
async def finalize_rebalancing(keypair, log_level):
    client = AsyncClient(rpc_url.target_network)
    client_state = await client.is_connected()
    print("Client is connected" if client_state else "Client is Disconnected")
    try:
        payer_keypair = parse_keypair_input(keypair)
    except Exception as e:
        print("Invalid Keypair Input. ")
        return
    t_dets = await finalize_rebalance(payer_keypair, client, log_level)
    print(t_dets)
    await client.close()

@click.command(name="init")
@click.option('--validator', '-v', default = get_keypair_path())
@click.option('--keypair', '-k', default = get_keypair_path())
@click.option('--log_level', '-l', default = 2, type=int)
async def ingl(keypair, validator, log_level):
    init_commission = click.prompt("Enter the Commission to be set for the validator: ", type=int)
    max_primary_stake = click.prompt("Enter the maximum primary stake to be set for the validator: ", type=int)
    nft_holders_share = click.prompt("Enter the NFT Holders Share to be set for the validator: ", type=int)
    initial_redemption_fee = click.prompt("Enter the Initial Redemption Fee to be set for the validator: ", type=int)
    is_validator_switchable = click.prompt("Is the validator switchable? (y/n): ", type=bool)
    unit_backing = click.prompt("Enter the Unit Backing to be set for the validator: ", type=int)
    redemption_fee_duration = click.prompt("Enter the Redemption Fee duration to be set for the validator: ", type=int)
    proposal_quorum = click.prompt("Enter the Proposal Quorum to be set for governance proposals: ", type=int)
    creator_royalty = click.prompt("Enter the Creator Royalty to be set for the validator: ", type=int)
    governance_expiration_time = click.prompt("How long should a governance take to expire? (in seconds): ", type=int)
    rarities = [100, 500, 1500, 2900, 5000]#TODO: Make this dynamic
    rarity_name = ['Mythic', 'Exalted', 'Rare', 'Uncommon', 'Common']#TODO: Make this dynamic
    twitter_handle = click.prompt("Enter the Twitter handle of the validator: ", type=str)
    discord_invite = click.prompt("Enter the Discord Invite of the validator: ", type=str)
    validator_name = click.prompt("Enter the Name of the validator: ", type=str)
    collection_uri = click.prompt("Enter the Collection URI of the validator: ", type=str)
    website = click.prompt("Enter the Website of the validator: ", type=str)


    client = AsyncClient(rpc_url.target_network)
    client_state = await client.is_connected()
    print("Client is connected" if client_state else "Client is Disconnected")
    try:
        payer_keypair = parse_keypair_input(keypair)
    except Exception as e:
        print("Invalid Keypair Input. ")
        return
    try:
        validator_key = parse_pubkey_input(validator)
    except Exception as e:
        print("Invalid Validator Input. ")
        return
        
    t_dets = await ingl_init(payer_keypair, validator_key, init_commission, max_primary_stake, nft_holders_share, initial_redemption_fee, is_validator_switchable, unit_backing, redemption_fee_duration, proposal_quorum, creator_royalty, governance_expiration_time, rarities, rarity_name, twitter_handle, discord_invite, validator_name, collection_uri, website, client, log_level,)
    print(t_dets)
    await client.close()


@click.command(name="process_rewards")
@click.option('--keypair', '-k', default = get_keypair_path())
@click.option('--log_level', '-l', default = 2, type=int)
async def process_vote_account_rewards(keypair, log_level):
    client = AsyncClient(rpc_url.target_network)
    client_state = await client.is_connected()
    print("Client is connected" if client_state else "Client is Disconnected")
    try:
        payer_keypair = parse_keypair_input(keypair) 
    except Exception as e:
        print("Invalid Keypair Input. ")
        return
    t_dets = await process_rewards(payer_keypair, client, log_level)
    print(t_dets)
    await client.close()

@click.command(name='create_vote_account')
@click.option('--val_keypair', default = get_keypair_path())
@click.option('--log_level', '-l', default = 2, type=int)
async def process_create_vote_account(val_keypair, log_level):
    client = AsyncClient(rpc_url.target_network)
    client_state = await client.is_connected()
    print("Client is connected" if client_state else "Client is Disconnected")
    try:
        payer_keypair = parse_keypair_input(f"{val_keypair}")
    except Exception as e:
        print("Invalid Keypair Input. ")
        return
    t_dets = await create_vote_account(payer_keypair, client, log_level)
    print(t_dets)
    await client.close()

@click.command(name='delegate_gem')
@click.argument('mint_id')
@click.option('--keypair', '-k', default = get_keypair_path())
@click.option('--log_level', '-l', default = 2, type=int)
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
    t_dets = await delegate_nft(payer_keypair, mint_pubkey, client, log_level)
    print(t_dets)
    await client.close()

@click.command(name = 'undelegate_gem')
@click.argument('mint_id')
@click.option('--keypair', '-k', default = get_keypair_path())
@click.option('--log_level', '-l', default = 2, type=int)
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
    t_dets = await undelegate_nft(payer_keypair, mint_pubkey, client, log_level)
    print(t_dets)
    await client.close()

@click.command(name='init_governance')
@click.argument('mint_id')
@click.option('--keypair', '-k', default = get_keypair_path())
@click.option('--log_level', '-l', default = 2, type=int)
async def process_create_governance(keypair, mint_id, log_level):
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
        print("Invalid Public Key provided for mint.")
        return

    governed = ["Validator Name", "Program Upgrade"]
    for i in range(len(governed)):
        print(f"{i} : {governed[i]}")
    numeration = click.prompt("Enter the number of the governed item", type=int)
    if numeration not in range(len(governed)):
        print("Invalid Input")
        return
    if numeration == 0:
        value = click.prompt("Enter the new validator name: ", type=str)
        t_dets = await init_governance(payer_keypair, mint_pubkey, client, config_account_type = ConfigAccountType.enum.ValidatorName(value = value), log_level = log_level)
    elif numeration == 1:
        try:
            buffer_address = parse_pubkey_input(click.prompt("Enter the buffer address: ", type=str)).public_key
        except Exception as e:
            print("Invalid Public Key provided for buffer.")
            return
        code_link = click.prompt("Enter the code link: ", type=str)

        t_dets = await init_governance(payer_keypair, mint_pubkey, client, GovernanceType.enum.ProgramUpgrade(buffer_account = buffer_address, code_link = code_link), log_level)
    print(t_dets)
    await client.close()

@click.command(name='vote_governance')
@click.argument('mint')
@click.argument('numeration', type=int)
@click.option('--vote', '-v', default='D')
@click.option('--keypair', '-k', default = get_keypair_path())
@click.option('--log_level', '-l', default = 2, type=int)
async def process_vote_governance(keypair, mint, numeration, vote, log_level):
    client = AsyncClient(rpc_url.target_network)
    client_state = await client.is_connected()
    print("Client is connected" if client_state else "Client is Disconnected")
    try:
        payer_keypair = parse_keypair_input(keypair)
    except Exception as e:
        print("Invalid Keypair Input. ")
        return
    
    try:
        mint_pubkey = parse_pubkey_input(mint)
    except Exception as e:
        print("Invalid Public Key provided for mint.")
        return
    vote = parse_vote(vote)
    t_dets = await vote_governance(payer_keypair, vote, numeration, [mint_pubkey.public_key], client, log_level)
    print(t_dets)
    await client.close()

@click.command(name='finalize_governance')
@click.argument('numeration', type=int)
@click.option('--keypair', '-k', default = get_keypair_path())
@click.option('--log_level', '-l', default = 2, type=int)
async def process_finalize_governance(keypair, numeration, log_level):
    client = AsyncClient(rpc_url.target_network)
    client_state = await client.is_connected()
    print("Client is connected" if client_state else "Client is Disconnected")
    try:
        payer_keypair = parse_keypair_input(keypair)
    except Exception as e:
        print("Invalid Keypair Input. ")
        return

    t_dets = await finalize_governance(payer_keypair, numeration, client, log_level)
    print(t_dets)
    await client.close()    

@click.command(name='execute_governance')
@click.argument('numeration', type=int)
@click.option('--keypair', '-k', default = get_keypair_path())
@click.option('--log_level', '-l', default = 2, type=int)
async def process_execute_governance(keypair, numeration, log_level):
    client = AsyncClient(rpc_url.target_network)
    client_state = await client.is_connected()
    print("Client is connected" if client_state else "Client is Disconnected")
    try:
        payer_keypair = parse_keypair_input(keypair)
    except Exception as e:
        print("Invalid Keypair Input. ")
        return

    t_dets = await execute_governance(payer_keypair, numeration, client, log_level)
    print(t_dets)
    await client.close()    

@click.command(name='upload_uris')
@click.argument('json_path')
@click.option('--keypair', '-k', default = get_keypair_path())
@click.option('--log_level', '-l', default = 2, type=int)
async def process_upload_uris(keypair, json_path, log_level):
    client_state = uasyncclient.is_connected()
    client = AsyncClient(rpc_url.target_network)
    print("Client is connected" if client_state else "Client is Disconnected")
    try:
        payer_keypair = parse_keypair_input(keypair)
    except Exception as e:
        print("Invalid Keypair Input, ", e)
        return
    try:
        f = open(f"{json_path}", "r")
        json_data = json.load(f)
        f.close()
    except Exception as e:
        print("Invalid Json Path. ")
        return
    uris = json_data["uris"]
    txs = []
    for cnt, rarity in enumerate(uris):
        z = 0
        while z < len(rarity):
            txs.append(upload_uris(payer_keypair, rarity[z:z+11], cnt, uasyncclient, log_level).value)
            z += 11
        # print(txs)
        await client.confirm_transaction(txs[-1], commitment='finalized')
        print("Done with Rarity: ", json_data["rarity_names"][cnt])
        time.sleep(3)
    for i in txs:
        print(f"Transaction Id: [link=https://explorer.solana.com/tx/{str(i)+rpc_url.get_explorer_suffix()}]{str(i)}[/link]")
    await client.close()

@click.command(name='reset_uris')
@click.option('--keypair', '-k', default = get_keypair_path())
@click.option('--log_level', '-l', default = 2, type=int)
async def process_reset_uris(keypair, log_level):
    client = AsyncClient(rpc_url.target_network)
    client_state = await client.is_connected()
    print("Client is connected" if client_state else "Client is Disconnected")
    try:
        payer_keypair = parse_keypair_input(keypair)
    except Exception as e:
        print("Invalid Keypair Input, ", e)
        return
    t_dets = await reset_uris(payer_keypair, client, log_level)
    print(t_dets)
    await client.close()




entry.add_command(mint)
entry.add_command(initialize_rebalancing)
entry.add_command(finalize_rebalancing)
entry.add_command(ingl)
entry.add_command(process_create_vote_account)
entry.add_command(process_delegate_gem)
entry.add_command(process_undelegate_gem)
entry.add_command(process_create_governance)
entry.add_command(process_vote_governance)
entry.add_command(process_finalize_governance)
entry.add_command(process_execute_governance)
entry.add_command(process_vote_account_rewards)
entry.add_command(config)
entry.add_command(process_upload_uris)
entry.add_command(process_reset_uris)
if __name__ == '__main__':
    entry()