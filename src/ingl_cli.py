import asyncclick as click
from .instruction import *
from .processor import *
from solders.keypair import Keypair
from solana.rpc.api import Client as Uasyncclient
from solders.pubkey import Pubkey
from borsh_construct import *
from .state import *
from .utils import *
from .state import Constants as ingl_constants
from rich import print
from solana.rpc.async_api import AsyncClient
from .cli_state import CLI_VERSION
import time

uasyncclient = Uasyncclient(get_network())


@click.group()
@click.version_option(version=CLI_VERSION)
def entry():
    pass


@click.command(
    name="mint", help="Mint a new NFT. Options: --keypair/-k, --log_level/-l"
)
@click.option(
    "--keypair",
    "-k",
    default=get_keypair_path(),
    help="Enter the path to the keypair that will be used to sign this transaction. Defaults to the set config keypair",
)
@click.option(
    "--log_level",
    "-l",
    default=2,
    type=int,
    help="Precise Log_level you want the transaction to be logged at, and above(0 -> 5). 0: All logs,  ... 5: Only Errors",
)
async def mint(keypair, log_level):
    client = AsyncClient(get_network())
    client_state = await client.is_connected()
    print("Client is connected" if client_state else "Client is Disconnected")
    try:
        payer_keypair = parse_keypair_input(keypair)
    except Exception as e:
        print("Invalid Keypair Input. ", e)
        return
    mint_keypair = KeypairInput(t_keypair=Keypair())
    print("Mint_Id: ", mint_keypair.pubkey)
    t_dets = await mint_nft(payer_keypair, mint_keypair, client, log_level)
    print(t_dets)
    await client.close()


@click.group(name="config")
async def config():
    pass


@click.command(
    name="set",
    help="Set the default config options. Options: --program_id/-p, --url/-u, --keypair/-k",
)
@click.option(
    "--program_id",
    "-p",
    help="Enter the program Id of the validator instance transactions will default to",
)
@click.option(
    "--url",
    "-u",
    help="Enter the network you want to connect to. Options: mainnet, testnet, devnet, or a custom url.",
)
@click.option(
    "--keypair",
    "-k",
    help="Enter the path to the keypair that transactions will be signed with by default.",
)
def set(program_id, url, keypair):
    assert (
        program_id or url or keypair
    ), "No options specified. Use --help for more information."
    if program_id:
        try:
            program_pubkey = parse_pubkey_input(program_id)
        except Exception as e:
            print("Invalid Public Key provided.")
            return
        set_program_id(program_pubkey.pubkey.__str__())
        print("Program ID set to: ", program_pubkey.pubkey)
    if url:
        if (
            url.lower() == "mainnet"
            or url.lower() == "testnet"
            or url.lower() == "devnet"
        ):
            url = get_network_url(url)
        set_network(url)
        print("Network set to: ", url)
    if keypair:
        if set_keypair_path(keypair):
            pass
        else:
            return
    if not program_id and not url and not keypair:
        print("No options specified. Use --help for more information.")
        return
    print("Config set successfully.")


@click.command(name="get")
def get():

    print("\nProgram ID: ", get_program_id())
    print("Network: ", get_network())
    print("Keypair: ", get_keypair_path())
    try:
        print("Keypair Public Key: ", parse_keypair_input(get_keypair_path()).pubkey)
    except Exception as e:
        pass
    print("\nConfig retrieved successfully.")


config.add_command(set)
config.add_command(get)


@click.command(
    name="init_rebalance",
    help="Initialize the rebalancing process. Options: --keypair/-k, --log_level/-l",
)
@click.option(
    "--keypair",
    "-k",
    default=get_keypair_path(),
    help="Enter the path to the keypair that will be used to sign this transaction. Defaults to the set config keypair",
)
@click.option(
    "--log_level",
    "-l",
    default=2,
    type=int,
    help="Precise Log_level you want the transaction to be logged at, and above(0 -> 5). 0: All logs,  ... 5: Only Errors",
)
async def initialize_rebalancing(keypair, log_level):
    client = AsyncClient(get_network())
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


@click.command(
    name="finalize_rebalance",
    help="Finalize the rebalancing process. Options: --keypair/-k, --log_level/-l",
)
@click.option(
    "--keypair",
    "-k",
    default=get_keypair_path(),
    help="Enter the path to the keypair that will be used to sign this transaction. Defaults to the set config keypair",
)
@click.option(
    "--log_level",
    "-l",
    default=2,
    type=int,
    help="Precise Log_level you want the transaction to be logged at, and above(0 -> 5). 0: All logs,  ... 5: Only Errors",
)
async def finalize_rebalancing(keypair, log_level):
    client = AsyncClient(get_network())
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


@click.command(
    name="init",
    help="Initialize the validator instance. Options: --keypair/-k, --log_level/-l",
)
@click.option(
    "--validator",
    "-v",
    default=get_keypair_path(),
    help="Enter the path to the validator id, or the public key of the validator id for this instance",
)
@click.option(
    "--keypair",
    "-k",
    default=get_keypair_path(),
    help="Enter the path to the keypair that will be used to sign this transaction. Defaults to the set config keypair",
)
@click.option(
    "--authorized_withdrawer",
    "-aw",
    default=get_keypair_path(),
    help="Enter the path to the authorized_withdrawer keypair of the vote account you seek to fractionalize if already created",
)
@click.option(
    "--upgrade_authority",
    "-ua",
    default=get_keypair_path(),
    help="Enter the path to the upgrade authority of the program instance in question",
)
@click.option(
    "--vote_account",
    "-va",
    default=None,
    help="Enter the path to the vote_account keypair, or the publicKey of the vote_account you seek to fractionalize",
)
@click.option(
    "--log_level",
    "-l",
    default=2,
    type=int,
    help="Precise Log_level you want the transaction to be logged at, and above(0 -> 5). 0: All logs,  ... 5: Only Errors",
)
async def ingl(
    keypair,
    validator,
    authorized_withdrawer,
    upgrade_authority,
    vote_account,
    log_level,
):

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
    try:
        upgrade_authority_keypair = parse_keypair_input(upgrade_authority)
    except Exception as e:
        print("Invalid Upgrade Authority Input. ")
        return

    if vote_account:
        try:
            authorized_withdrawer_keypair = parse_keypair_input(authorized_withdrawer)
        except Exception as e:
            print("Invalid Authorized Withdrawer Input. ")
            return

        try:
            vote_account_key = parse_pubkey_input(vote_account)
        except Exception as e:
            print("Invalid Vote Account Input. ")
            return

    init_commission = 105
    counter = 0
    while init_commission > 100 or init_commission < 0:
        if counter > 0:
            print("Invalid Input.")
        counter += 1
        init_commission = click.prompt(
            "Enter the Commission(%) to be set for the validator ( > 0, <=100)",
            type=int,
        )
    max_primary_stake = 1
    counter = 0
    while max_primary_stake < 1_030_000_000:
        if counter > 0:
            print("Invalid Input.")
        counter += 1
        max_primary_stake = click.prompt(
            "Enter the maximum primary stake(in lamports) to be set for the validator (>1,030,000,000)",
            type=int,
        )
    nft_holders_share = 105
    counter = 0
    while nft_holders_share > 100 or nft_holders_share < 50:
        if counter > 0:
            print("Invalid Input.")
        counter += 1
        nft_holders_share = click.prompt(
            "Enter the NFT Holders Share(%) to be set for the validator (>50, <=100)",
            type=int,
        )
    initial_redemption_fee = 26
    counter = 0
    while initial_redemption_fee > 25 or initial_redemption_fee < 0:
        if counter > 0:
            print("Invalid Input.")
        counter += 1
        initial_redemption_fee = click.prompt(
            "Enter the Initial Redemption Fee(%) to be set for the validator (>=0, <=25)",
            type=int,
        )
    is_validator_switchable = None
    counter = 0
    while type(is_validator_switchable) != bool:
        if counter > 0:
            print("Invalid Input.")
        counter += 1
        is_validator_switchable = click.prompt(
            "Is the validator switchable? (y/n) ", type=bool
        )
    unit_backing = 1
    counter = 0
    while unit_backing < 1_030_000_000:
        if counter > 0:
            print("Invalid Input.")
        counter += 1
        unit_backing = click.prompt(
            "Enter the Unit Backing(in lamports) to be set for the validator (>1,030,000,000) ",
            type=int,
        )
    redemption_fee_duration = 70_000_000
    counter = 0
    while redemption_fee_duration > 63_072_000:
        if counter > 0:
            print("Invalid Input.")
        counter += 1
        redemption_fee_duration = click.prompt(
            "Enter the Redemption Fee duration(in seconds) to be set for the validator (<63,072,000)",
            type=int,
        )
    proposal_quorum = 60
    counter = 0
    while proposal_quorum < 65 or proposal_quorum > 100:
        if counter > 0:
            print("Invalid Input.")
        counter += 1
        proposal_quorum = click.prompt(
            "Enter the Proposal Quorum(%) to be set for governance proposals (>=65, <=100) ",
            type=int,
        )
    creator_royalty = 300
    counter = 0
    while creator_royalty > 200 or creator_royalty < 0:
        if counter > 0:
            print("Invalid Input.")
        counter += 1
        creator_royalty = click.prompt(
            "Enter the Creator Royalty(in basis points) to be set for the validator (>=0, <200)",
            type=int,
        )
    governance_expiration_time = 1
    counter = 0
    while governance_expiration_time < 35 or governance_expiration_time > 365:
        if counter > 0:
            print("Invalid Input.")
        counter += 1
        governance_expiration_time = click.prompt(
            "How long should a governance take to expire? (in days) (>=35 days, <=365 days) ",
            type=int,
        )
    governance_expiration_time = governance_expiration_time * 86_400
    twitter_handle = click.prompt("Enter the Twitter handle of the validator", type=str)
    discord_invite = click.prompt("Enter the Discord Invite of the validator", type=str)
    validator_name = click.prompt("Enter the Name of the validator", type=str)
    website = click.prompt("Enter the Website of the validator", type=str)
    default_uri = click.prompt("Enter the Default URI of the validator", type=str)

    json_data = {}
    while "uris" not in json_data:
        json_path = click.prompt(
            "Enter the Collection path to the config json", type=str
        )
        try:
            f = open(f"{json_path}", "r")
            json_data = json.load(f)
            f.close()
        except Exception as e:
            print("Invalid Json Path. ")
            return
    collection_uri = json_data["collection_uri"]
    rarity_names = json_data["rarity_names"]
    rarities = json_data["rarities"]

    client = AsyncClient(get_network())
    client_state = await client.is_connected()
    print("Client is connected" if client_state else "Client is Disconnected")

    if vote_account:
        t_dets = await fractionalize_existing(
            payer_keypair,
            authorized_withdrawer_keypair,
            upgrade_authority_keypair,
            vote_account_key,
            validator_key,
            init_commission,
            max_primary_stake,
            nft_holders_share,
            initial_redemption_fee,
            is_validator_switchable,
            unit_backing,
            redemption_fee_duration,
            proposal_quorum,
            creator_royalty,
            governance_expiration_time,
            rarities,
            rarity_names,
            twitter_handle,
            discord_invite,
            validator_name,
            collection_uri,
            website,
            default_uri,
            client,
            log_level,
        )

    else:
        t_dets = await ingl_init(
            payer_keypair,
            upgrade_authority_keypair,
            validator_key,
            init_commission,
            max_primary_stake,
            nft_holders_share,
            initial_redemption_fee,
            is_validator_switchable,
            unit_backing,
            redemption_fee_duration,
            proposal_quorum,
            creator_royalty,
            governance_expiration_time,
            rarities,
            rarity_names,
            twitter_handle,
            discord_invite,
            validator_name,
            collection_uri,
            website,
            default_uri,
            client,
            log_level,
        )
    print(t_dets)
    await client.close()


@click.command(
    name="process_rewards",
    help="Process rewards for a vote account, Options: --keypair/-k, --log_level/-l",
)
@click.option(
    "--keypair",
    "-k",
    default=get_keypair_path(),
    help="Enter the path to the keypair that will be used to sign this transaction. Defaults to the set config keypair",
)
@click.option(
    "--log_level",
    "-l",
    default=2,
    type=int,
    help="Precise Log_level you want the transaction to be logged at, and above(0 -> 5). 0: All logs,  ... 5: Only Errors",
)
async def process_vote_account_rewards(keypair, log_level):
    client = AsyncClient(get_network())
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


@click.command(
    name="create_vote_account",
    help="Create the vote account for the validator's program instance, Options: --val_keypair/-k, --log_level/-l",
)
@click.option(
    "--val_keypair",
    default=get_keypair_path(),
    help="Enter the path to the validator id keypair json file. Defaults to the set config keypair",
)
@click.option(
    "--log_level",
    "-l",
    default=2,
    type=int,
    help="Precise Log_level you want the transaction to be logged at, and above(0 -> 5). 0: All logs,  ... 5: Only Errors",
)
async def process_create_vote_account(val_keypair, log_level):
    client = AsyncClient(get_network())
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


@click.command(
    name="delegate",
    help="Delegate an NFT to a validator, Argument: Mint_ID(Pubkey or Keypair), Options: --keypair/-k, --log_level/-l",
)
@click.argument("mint_id", type=str)
@click.option(
    "--keypair",
    "-k",
    default=get_keypair_path(),
    help="Enter the path to the keypair that will be used to sign this transaction. Defaults to the set config keypair",
)
@click.option(
    "--log_level",
    "-l",
    default=2,
    type=int,
    help="Precise Log_level you want the transaction to be logged at, and above(0 -> 5). 0: All logs,  ... 5: Only Errors",
)
async def process_delegate_gem(keypair, mint_id, log_level):
    client = AsyncClient(get_network())
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


@click.command(
    name="undelegate",
    help="Undelegate an NFT from a validator, Argument: Mint_ID(Pubkey or Keypair), Options: --keypair/-k, --log_level/-l",
)
@click.argument("mint_id", type=str)
@click.option(
    "--keypair",
    "-k",
    default=get_keypair_path(),
    help="Enter the path to the keypair that will be used to sign this transaction. Defaults to the set config keypair",
)
@click.option(
    "--log_level",
    "-l",
    default=2,
    type=int,
    help="Precise Log_level you want the transaction to be logged at, and above(0 -> 5). 0: All logs,  ... 5: Only Errors",
)
async def process_undelegate_gem(keypair, mint_id, log_level):
    client = AsyncClient(get_network())
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
    # print(payer_keypair, mint_pubkey)
    t_dets = await undelegate_nft(payer_keypair, mint_pubkey, client, log_level)
    print(t_dets)
    await client.close()


@click.command(
    name="init_governance",
    help="Initialize Governance, Arguments: Mint_Id(Pubkey or Kepair) Options: --keypair/-k, --log_level/-l",
)
@click.argument(
    "mint_id",
    type=str,
)
@click.option(
    "--keypair",
    "-k",
    default=get_keypair_path(),
    help="Enter the path to the keypair that will be used to sign this transaction. Defaults to the set config keypair",
)
@click.option(
    "--log_level",
    "-l",
    default=2,
    type=int,
    help="Precise Log_level you want the transaction to be logged at, and above(0 -> 5). 0: All logs,  ... 5: Only Errors",
)
async def process_create_governance(keypair, mint_id, log_level):
    client = AsyncClient(get_network())
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
        title = click.prompt("Enter the new Proposal's Title", type=str)
        description = click.prompt("Enter the Proposal's Description", type=str)
        t_dets = await init_governance(
            payer_keypair,
            mint_pubkey,
            client,
            title=title,
            description=description,
            governance_type=GovernanceType.enum.ConfigAccount(),
            config_account_type=ConfigAccountType.enum.ValidatorName(value=value),
            log_level=log_level,
        )
    elif numeration == 1:
        try:
            buffer_address = parse_pubkey_input(
                click.prompt("Enter the buffer address: ", type=str)
            ).pubkey
        except Exception as e:
            print("Invalid Public Key provided for buffer.")
            return
        code_link = click.prompt("Enter the code link: ", type=str)
        title = click.prompt("Enter the new Proposal's Title", type=str)
        description = click.prompt("Enter the Proposal's Description", type=str)

        t_dets = await init_governance(
            payer_keypair,
            mint_pubkey,
            client,
            title=title,
            description=description,
            governance_type=GovernanceType.enum.ProgramUpgrade(
                buffer_account=buffer_address, code_link=code_link
            ),
            log_level=log_level,
        )
    print(t_dets)
    await client.close()


@click.command(
    name="vote_governance",
    help="Vote on a Governance Proposal, Arguments: Mint_ID(Pubkey or Keypair), Numeration, Options: --vote/-v, --keypair/-k, --log_level/-l",
)
@click.argument("mint", type=str)
@click.argument(
    "numeration",
    type=int,
)
@click.option(
    "--vote",
    "-v",
    default="D",
    help="Enter the vote you want to cast. D: For 'Dissapprove', A: For 'Approve', ",
)
@click.option(
    "--keypair",
    "-k",
    default=get_keypair_path(),
    help="Enter the path to the keypair that will be used to sign this transaction. Defaults to the set config keypair",
)
@click.option(
    "--log_level",
    "-l",
    default=2,
    type=int,
    help="Precise Log_level you want the transaction to be logged at, and above(0 -> 5). 0: All logs,  ... 5: Only Errors",
)
async def process_vote_governance(keypair, mint, numeration, vote, log_level):
    client = AsyncClient(get_network())
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
    t_dets = await vote_governance(
        payer_keypair, vote, numeration, [mint_pubkey.pubkey], client, log_level
    )
    print(t_dets)
    await client.close()


@click.command(
    name="finalize_governance",
    help="Finalize a Governance Proposal, Arguments: Numeration(int), Options: --keypair/-k, --log_level/-l",
)
@click.argument(
    "numeration",
    type=int,
)
@click.option(
    "--keypair",
    "-k",
    default=get_keypair_path(),
    help="Enter the path to the keypair that will be used to sign this transaction. Defaults to the set config keypair",
)
@click.option(
    "--log_level",
    "-l",
    default=2,
    type=int,
    help="Precise Log_level you want the transaction to be logged at, and above(0 -> 5). 0: All logs,  ... 5: Only Errors",
)
async def process_finalize_governance(keypair, numeration, log_level):
    client = AsyncClient(get_network())
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


@click.command(
    name="execute_governance",
    help="Execute a Governance Proposal, Arguments: Numeration(int), Options: --keypair/-k, --log_level/-l",
)
@click.argument(
    "numeration",
    type=int,
)
@click.option(
    "--keypair",
    "-k",
    default=get_keypair_path(),
    help="Enter the path to the keypair that will be used to sign this transaction. Defaults to the set config keypair",
)
@click.option(
    "--log_level",
    "-l",
    default=2,
    type=int,
    help="Precise Log_level you want the transaction to be logged at, and above(0 -> 5). 0: All logs,  ... 5: Only Errors",
)
async def process_execute_governance(keypair, numeration, log_level):
    client = AsyncClient(get_network())
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


@click.command(
    name="upload_uris",
    help="Upload URIs for the Validator's instange NFTs, Arguments: json_path(path to uris Json file) Options: --keypair/-k, --log_level/-l",
)
@click.argument("json_path")
@click.option(
    "--keypair",
    "-k",
    default=get_keypair_path(),
    help="Enter the path to the keypair that will be used to sign this transaction. Defaults to the set config keypair",
)
@click.option(
    "--log_level",
    "-l",
    default=2,
    type=int,
    help="Precise Log_level you want the transaction to be logged at, and above(0 -> 5). 0: All logs,  ... 5: Only Errors",
)
async def process_upload_uris(keypair, json_path, log_level):
    client_state = uasyncclient.is_connected()
    client = AsyncClient(get_network())
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
            txs.append(
                upload_uris(
                    payer_keypair, rarity[z : z + 11], cnt, uasyncclient, log_level
                ).value
            )
            z += 11
        # print(txs)
        await client.confirm_transaction(txs[-1], commitment="finalized")
        print("Done with Rarity: ", json_data["rarity_names"][cnt])
        time.sleep(3)
    for i in txs:
        print(
            f"Transaction Id: [link=https://explorer.solana.com/tx/{str(i)+get_explorer_suffix(get_network())}]{str(i)}[/link]"
        )
    await client.close()


@click.command(
    name="reset_uris",
    help="Reset URIs for the Validator's instange NFTs, Options: --keypair/-k, --log_level/-l",
)
@click.option(
    "--keypair",
    "-k",
    default=get_keypair_path(),
    help="Enter the path to the keypair that will be used to sign this transaction. Defaults to the set config keypair",
)
@click.option(
    "--log_level",
    "-l",
    default=2,
    type=int,
    help="Precise Log_level you want the transaction to be logged at, and above(0 -> 5). 0: All logs,  ... 5: Only Errors",
)
async def process_reset_uris(keypair, log_level):
    client = AsyncClient(get_network())
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


@click.command(
    name="init_registry",
    help="Initialize the Governance Registry Program, Options: --keypair/-k",
)
@click.option(
    "--keypair",
    "-k",
    default=get_keypair_path(),
    help="Enter the path to the keypair that will be used to sign this transaction. Defaults to the set config keypair",
)
async def process_initialize_registry(keypair):
    client = AsyncClient(get_network())
    client_state = await client.is_connected()
    print("Client is connected" if client_state else "Client is Disconnected")
    try:
        payer_keypair = parse_keypair_input(keypair)
    except Exception as e:
        print("Invalid Keypair Input, ", e)
        return
    t_dets = await init_registry(payer_keypair, client)
    print(t_dets)
    await client.close()


@click.command(
    name="reset_registry",
    help="Reset the Governance Registry Program, Options: --keypair/-k",
)
@click.option(
    "--keypair",
    "-k",
    default=get_keypair_path(),
    help="Enter the path to the keypair that will be used to sign this transaction. Defaults to the set config keypair",
)
async def process_reset_registry(keypair):
    client = AsyncClient(get_network())
    client_state = await client.is_connected()
    print("Client is connected" if client_state else "Client is Disconnected")
    try:
        payer_keypair = parse_keypair_input(keypair)
    except Exception as e:
        print("Invalid Keypair Input, ", e)
        return
    t_dets = await reset_registry(payer_keypair, client)
    print(t_dets)
    await client.close()


@click.command(
    name="register_program",
    help="Register a Program with the Governance Registry, Options: --keypair/-k, --program_id/-p",
)
@click.option(
    "--keypair",
    "-k",
    default=get_keypair_path(),
    help="Enter the path to the keypair that will be used to sign this transaction. Defaults to the set config keypair",
)
@click.option(
    "--program_id",
    "-p",
    default=get_program_id(),
    help="Enter the program_id of the validator instance you want to register. Defaults to the set config program_id",
)
async def process_register_program(keypair, program_id):
    name = click.prompt(
        "What is the name of the program you want to register :", type=str
    )
    client = AsyncClient(get_network())
    client_state = await client.is_connected()
    print("Client is connected" if client_state else "Client is Disconnected")
    try:
        payer_keypair = parse_keypair_input(keypair)
    except Exception as e:
        print("Invalid Keypair Input, ", e)
        return
    try:
        program_pubkey = parse_pubkey_input(program_id)
    except Exception as e:
        print("Invalid Pubkey Input, ", e)
        return
    t_dets = await register_program(payer_keypair, program_pubkey.pubkey, client, name)
    print(t_dets)
    await client.close()


@click.command(
    name="get_vote_pubkey",
    help="Get the Vote Account Pubkey for the Validator's instance, Options: --program_id/-p",
)
@click.option(
    "--program_id",
    "-p",
    default=get_program_id(),
    help="Enter the program_id of the validator instance you want to get the vote account pubkey for. Defaults to the set config program_id",
)
async def process_get_vote_key(program_id):
    client = AsyncClient(get_network())
    client_state = await client.is_connected()
    print("Client is connected" if client_state else "Client is Disconnected")
    try:
        program_pubkey = parse_pubkey_input(program_id)
    except Exception as e:
        print("Invalid Pubkey Input, ", e)
        return
    print("Program_id: ", program_pubkey.pubkey)
    config_account_pubkey, _config_account_bump = Pubkey.find_program_address(
        [bytes(ingl_constants.INGL_CONFIG_SEED, "UTF-8")], program_pubkey.pubkey
    )
    config_data = ValidatorConfig.parse(
        (await client.get_account_info(config_account_pubkey)).value.data
    )
    vote_account_key = Pubkey(config_data.vote_account)
    print("Vote Account Key: ", vote_account_key)
    return


@click.command(name="inject_test")
@click.argument("num_mints", type=int)
@click.option(
    "--keypair",
    "-k",
    default=get_keypair_path(),
    help="Enter the path to the keypair that will be used to sign this transaction. Defaults to the set config keypair",
)
@click.option(
    "--log_level",
    "-l",
    default=2,
    type=int,
    help="Precise Log_level you want the transaction to be logged at, and above(0 -> 5). 0: All logs,  ... 5: Only Errors",
)
async def process_inject_test(keypair, num_mints, log_level):
    client = AsyncClient(get_network())
    client_state = await client.is_connected()
    print("Client is connected" if client_state else "Client is Disconnected")
    try:
        payer_keypair = parse_keypair_input(keypair)
    except Exception as e:
        print("Invalid Keypair Input, ", e)
        return

    mints = []
    for i in range(num_mints):
        while True:
            try:
                mints.append(
                    parse_pubkey_input(
                        click.prompt(f"Enter the Mint Address for Mint {i+1}", type=str)
                    ).pubkey
                )
                break
            except Exception as e:
                print("Invalid Mint Address, ", e)

    t_dets = await inject_testing_data(
        payer_keypair, mints, client, log_level=log_level
    )
    print(t_dets)
    await client.close()


@click.group(name="markets")
async def market():
    pass


@click.group(name="config")
async def market_config():
    pass


@click.command(
    name="set",
    help="Set the default config options. Options: --program_id/-p, --keypair/-k",
)
@click.option(
    "--program_id",
    "-p",
    help="Enter the program Id of the validator instance transactions will default to",
)
@click.option(
    "--keypair",
    "-k",
    help="Enter the path to the keypair that transactions will be signed with by default.",
)
def market_set(program_id, keypair):
    assert (
        program_id or keypair
    ), "No options specified. Use --help for more information."
    if program_id:
        try:
            program_pubkey = parse_pubkey_input(program_id)
        except Exception as e:
            print("Invalid Public Key provided.")
            return
        set_market_program_id(program_pubkey.pubkey.__str__())
        print("Program ID set to: ", program_pubkey.pubkey)
    if keypair:
        if set_market_keypair_path(keypair):
            pass
        else:
            return
    if not program_id and not keypair:
        print("No options specified. Use --help for more information.")
        return
    print("Config set successfully.")


@click.command(name="get")
def market_get():

    print("\nProgram ID: ", get_market_program_id())
    print("Network: ", get_network())
    print("Keypair: ", get_market_keypair_path())
    try:
        print(
            "Keypair Public Key: ",
            parse_keypair_input(get_market_keypair_path()).pubkey,
        )
    except Exception as e:
        pass
    print("\nConfig retrieved successfully.")


@click.command(
    name="list",
    help="Initialize the validator instance. Options: --upgrade_authority/-u, --authorized_withdrawer/-aw, --log_level/-l",
)
@click.argument("validator_json", type=str)
@click.option(
    "--upgrade_authority",
    "-u",
    default=get_market_keypair_path(),
    help="Enter the path to the program's upgrade authority. Defaults to the set config keypair",
)
@click.option(
    "--authorized_withdrawer",
    "-aw",
    default=get_market_keypair_path(),
    help="Enter the path to the authorized_withdrawer keypair of the vote account. Defaults to the set config keypair",
)
@click.option(
    "--log_level",
    "-l",
    default=2,
    type=int,
    help="Precise Log_level you want the transaction to be logged at, and above(0 -> 5). 0: All logs,  ... 5: Only Errors",
)
async def list_validator(
    validator_json, upgrade_authority, authorized_withdrawer, log_level
):
    assert log_level >= 0 and log_level <= 5, "Log level must be between 0 and 5"
    client = AsyncClient(get_network())
    client_state = await client.is_connected()
    print("Client is connected" if client_state else "Client is Disconnected")
    try:
        upgrade_authority = parse_keypair_input(upgrade_authority)
        authorized_withdrawer = parse_keypair_input(authorized_withdrawer)
    except Exception as e:
        print("Invalid keypair provided.")
        return
    try:
        json_file = open(validator_json)
        validator_json = json.load(json_file)
        json_file.close()
    except Exception as e:
        print("Invalid JSON provided.")
        return

    try:
        vote_account = parse_pubkey_input(validator_json["vote_account"])
    except Exception as e:
        print("Invalid vote account provided.")
        return

    try:
        authorized_withdrawer_cost = int(validator_json["authorized_withdrawer_cost"])
        mediatable_date = int(
            time.time() + 86400 * int(validator_json["mediation_wait_days"])
        )
        description = validator_json["description"]
        validator_name = validator_json["validator_name"]
        validator_logo_url = validator_json["validator_logo_url"]
        secondary_items = validator_json["secondary_items"]
    except Exception as e:
        print(f"Invalid JSON provided: {e}")
        return

    t_dets = await process_list_validator(
        authorized_withdrawer,
        upgrade_authority,
        vote_account,
        authorized_withdrawer_cost,
        mediatable_date,
        secondary_items,
        description,
        validator_name,
        validator_logo_url,
        client=client,
        log_level=log_level,
    )
    await client.close()
    print(t_dets)


@click.command(
    name="delist",
    help="Delist the validator instance. Options: --keypair/-k, --log_level/-l",
)
@click.option(
    "-k",
    "--keypair",
    default=get_market_keypair_path(),
    help="Enter the path to the authorized_withdrawer keypair of the sales instance. Defaults to the set config keypair",
)
@click.option(
    "-l",
    "--log_level",
    default=2,
    type=int,
    help="Precise Log_level you want the transaction to be logged at, and above(0 -> 5). 0: All logs,  ... 5: Only Errors",
)
async def delist(keypair, log_level):
    assert log_level >= 0 and log_level <= 5, "Log level must be between 0 and 5"
    client = AsyncClient(get_network())
    client_state = await client.is_connected()
    print("Client is connected" if client_state else "Client is Disconnected")
    try:
        authorized_withdrawer = parse_keypair_input(keypair)
    except Exception as e:
        print("Invalid keypair provided.")
        return
    t_dets = await process_delist_validator(
        authorized_withdrawer, client=client, log_level=log_level
    )
    await client.close()
    print(t_dets)


@click.command(
    name="buy",
    help="Buy the validator instance. Options: --keypair/-k, --log_level/-l",
)
@click.option(
    "-k",
    "--keypair",
    default=get_market_keypair_path(),
    help="Enter the path to the payer keypair. Defaults to the set config keypair",
)
@click.option(
    "-l",
    "--log_level",
    default=2,
    type=int,
    help="Precise Log_level you want the transaction to be logged at, and above(0 -> 5). 0: All logs,  ... 5: Only Errors",
)
async def buy(keypair, log_level):
    assert log_level >= 0 and log_level <= 5, "Log level must be between 0 and 5"
    client = AsyncClient(get_network())
    client_state = await client.is_connected()
    print("Client is connected" if client_state else "Client is Disconnected")
    try:
        payer = parse_keypair_input(keypair)
    except Exception as e:
        print("Invalid keypair provided.")
        return
    t_dets = await process_buy_validator(payer, client=client, log_level=log_level)
    await client.close()
    print(t_dets)


@click.command(
    name="withraw_rewards",
    help="withdraw rewards from the running validator. Options: --keypair/-k, --log_level/-l",
)
@click.option(
    "-k",
    "--keypair",
    default=get_market_keypair_path(),
    help="Enter the path to the payer keypair. Defaults to the set config keypair",
)
async def withdraw_rewards(keypair, log_level):
    assert log_level >= 0 and log_level <= 5, "Log level must be between 0 and 5"
    client = AsyncClient(get_network())
    client_state = await client.is_connected()
    print("Client is connected" if client_state else "Client is Disconnected")
    try:
        authorized_withdrawer = parse_keypair_input(keypair)
    except Exception as e:
        print("Invalid keypair provided.")
        return
    t_dets = await process_withdraw_rewards(
        authorized_withdrawer, client=client, log_level=log_level
    )
    await client.close()
    print(t_dets)


@click.command(
    name="request_mediation",
    help="request mediation for the running validator. Options: --keypair/-k, --log_level/-l",
)
@click.option(
    "-k",
    "--keypair",
    default=get_market_keypair_path(),
    help="Enter the path to the payer keypair. Defaults to the set config keypair",
)
@click.option(
    "-l",
    "--log_level",
    default=2,
    type=int,
    help="Precise Log_level you want the transaction to be logged at, and above(0 -> 5). 0: All logs,  ... 5: Only Errors",
)
async def request_mediation(keypair, log_level):
    assert log_level >= 0 and log_level <= 5, "Log level must be between 0 and 5"
    client = AsyncClient(get_network())
    client_state = await client.is_connected()
    print("Client is connected" if client_state else "Client is Disconnected")
    try:
        payer = parse_keypair_input(keypair)
    except Exception as e:
        print("Invalid keypair provided.")
        return
    t_dets = await process_request_mediation(payer, client=client, log_level=log_level)
    await client.close()
    print(t_dets)


@click.command(
    name="mediate",
    help="Mediate a conflict during a sale. Options: --keypair/-k, --log_level/-l",
)
@click.option(
    "-k",
    "--keypair",
    default=get_market_keypair_path(),
    help="Enter the path to the payer keypair. Defaults to the set config keypair",
)
@click.option(
    "-l",
    "--log_level",
    default=2,
    type=int,
    help="Precise Log_level you want the transaction to be logged at, and above(0 -> 5). 0: All logs,  ... 5: Only Errors",
)
async def mediate(keypair, log_level):
    assert log_level >= 0 and log_level <= 5, "Log level must be between 0 and 5"
    mediation_shares = {}
    mediation_shares["buyer"] = click.prompt(
        "Enter the buyer's mediation share", type=int
    )
    mediation_shares["seller"] = click.prompt(
        "Enter the seller's mediation share", type=int
    )
    mediation_shares["team"] = click.prompt(
        "Enter the team's mediation share", type=int
    )

    assert (
        sum([v for v in mediation_shares.values()]) == 100
    ), "Mediation shares must add up to 100"

    client = AsyncClient(get_network())
    client_state = await client.is_connected()
    print("Client is connected" if client_state else "Client is Disconnected")
    try:
        payer = parse_keypair_input(keypair)
    except Exception as e:
        print("Invalid keypair provided.")
        return
    t_dets = await process_mediate(payer, client=client, log_level=log_level)
    await client.close()
    print(t_dets)


@click.command(
    name="validate_secondary_item",
    help="Validate a secondary item sale completion. Options: --keypair/-k, --log_level/-l",
)
@click.option(
    "-k",
    "--keypair",
    default=get_market_keypair_path(),
    help="Enter the path to the payer keypair. Defaults to the set config keypair",
)
@click.option(
    "-l",
    "--log_level",
    default=2,
    type=int,
    help="Precise Log_level you want the transaction to be logged at, and above(0 -> 5). 0: All logs,  ... 5: Only Errors",
)
@click.argument(
    "secondary_item",
    type=int,
    # help="Enter the index of the secondary item to be validated.",
)
async def validate_secondary_item(keypair, log_level, secondary_item):
    assert log_level >= 0 and log_level <= 5, "Log level must be between 0 and 5"
    client = AsyncClient(get_network())
    client_state = await client.is_connected()
    print("Client is connected" if client_state else "Client is Disconnected")
    try:
        payer = parse_keypair_input(keypair)
    except Exception as e:
        print("Invalid keypair provided.")
        return
    t_dets = await process_validate_secondary_item_transfers(
        payer, secondary_item, client=client, log_level=log_level
    )
    await client.close()
    print(t_dets)


market_config.add_command(market_set)
market_config.add_command(market_get)

market.add_command(market_config)
market.add_command(list_validator)
market.add_command(delist)
market.add_command(buy)
market.add_command(withdraw_rewards)
market.add_command(request_mediation)
market.add_command(mediate)
market.add_command(validate_secondary_item)


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
entry.add_command(market)
entry.add_command(process_upload_uris)
entry.add_command(process_reset_uris)
entry.add_command(process_initialize_registry)
entry.add_command(process_get_vote_key)
entry.add_command(process_inject_test)
entry.add_command(process_reset_registry)
entry.add_command(process_register_program)
if __name__ == "__main__":

    entry()
