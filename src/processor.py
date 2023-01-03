import solana
from solana.publickey import PublicKey
from solana import system_program
from solana.transaction import *
from spl.token import constants as spl_constants
from spl.token import instructions as assoc_instructions
from .instruction import *
from .state import *
from .state import Constants as ingl_constants
from solana.rpc.async_api import AsyncClient
from rich import print

async def ingl_init(payer_keypair: KeypairInput, client: AsyncClient, log_level: int = 0) -> str:
    mint_pubkey, _mint_pubkey_bump = PublicKey.find_program_address([bytes(ingl_constants.INGL_NFT_COLLECTION_KEY, 'UTF-8')], get_program_id())
    mint_authority_pubkey, _mint_authority_pubkey_bump = PublicKey.find_program_address([bytes(ingl_constants.INGL_MINT_AUTHORITY_KEY, 'UTF-8')], get_program_id())
    collection_holder_pubkey, _collection_holder_pubkey_bump = PublicKey.find_program_address([bytes(ingl_constants.COLLECTION_HOLDER_KEY, 'UTF-8')], get_program_id())
    mint_associated_account_pubkey = assoc_instructions.get_associated_token_address(collection_holder_pubkey, mint_pubkey)
    metaplex_program_id = PublicKey("metaqbxxUerdq28cj1RbAWkYQm3ybzjb6a8bt518x1s")
    metadata_pda, _metadata_pda_bump = PublicKey.find_program_address([b"metadata", bytes(metaplex_program_id), bytes(mint_pubkey)], metaplex_program_id)
    master_edition_pda, _master_edition_bump = PublicKey.find_program_address([b"metadata", bytes(metaplex_program_id), bytes(mint_pubkey), b"edition"], metaplex_program_id)
    global_gem_pubkey, _global_gem_bump = PublicKey.find_program_address([bytes(ingl_constants.GLOBAL_GEM_KEY, 'UTF-8')], get_program_id())


    payer_account_meta = AccountMeta(payer_keypair.public_key, True, True)
    collection_holder_meta = AccountMeta(collection_holder_pubkey, False, True) #This might be the cause of a Writable escalated permission error.
    mint_account_meta = AccountMeta(mint_pubkey, False, True)
    mint_authority_meta = AccountMeta(mint_authority_pubkey, False, False)
    mint_associated_meta = AccountMeta(mint_associated_account_pubkey, False, True)
    spl_program_meta = AccountMeta(spl_constants.TOKEN_PROGRAM_ID, False, False)
    sysvar_rent_account_meta = AccountMeta(solana.sysvar.SYSVAR_RENT_PUBKEY, False, False)
    system_program_meta = AccountMeta(system_program.SYS_PROGRAM_ID, False, False)
    token_metadata_meta = AccountMeta(metadata_pda, False, True)
    metadata_program_id = AccountMeta(metaplex_program_id, False, False)
    associated_program_meta = AccountMeta(spl_constants.ASSOCIATED_TOKEN_PROGRAM_ID, False, False)
    global_gem_meta = AccountMeta(global_gem_pubkey, False, True)
    edition_meta = AccountMeta(master_edition_pda, False, True)

    accounts = [
        payer_account_meta, 
        collection_holder_meta,
        mint_account_meta,
        mint_authority_meta,
        mint_associated_meta, 
        token_metadata_meta, 
        global_gem_meta,
        edition_meta,
        spl_program_meta,
        sysvar_rent_account_meta, 
        system_program_meta,

        system_program_meta, 
        spl_program_meta,
        associated_program_meta,
        associated_program_meta,
        spl_program_meta, 
        metadata_program_id,
        metadata_program_id,
        system_program_meta,
    ]
    # print(accounts)
    data = build_instruction(InstructionEnum.enum.InglInit(log_level = log_level))
    transaction = Transaction()
    transaction.add(ComputeBudgetInstruction().set_compute_unit_limit(250_000, payer_keypair.public_key))
    transaction.add(TransactionInstruction(accounts, get_program_id(), data))
   

    try:
        t_dets = await sign_and_send_tx(transaction, client, payer_keypair)
        await client.confirm_transaction(tx_sig = t_dets.value, commitment= "finalized", sleep_seconds = 0.4, last_valid_block_height = None)
        return f"Transaction Id: [link=https://explorer.solana.com/tx/{str(t_dets.value)+rpc_url.get_explorer_suffix()}]{str(t_dets.value)}[/link]"
    except Exception as e:
        return(f"[warning]Error: {e}[/warning]")

async def mint_nft(payer_keypair: KeypairInput, mint_keypair: KeypairInput, mint_class: ClassEnum.enum, client: AsyncClient, log_level: int = 0) -> str:
    mint_authority_pubkey, _mint_authority_pubkey_bump = PublicKey.find_program_address([bytes(ingl_constants.INGL_MINT_AUTHORITY_KEY, 'UTF-8')], get_program_id())
    collection_mint_pubkey, _collection_mint_pubkey_bump = PublicKey.find_program_address([bytes(ingl_constants.INGL_NFT_COLLECTION_KEY, 'UTF-8')], get_program_id())
    minting_pool_pubkey, _minting_pool_pubkey_bump = PublicKey.find_program_address([bytes(ingl_constants.INGL_MINTING_POOL_KEY, 'UTF-8')], get_program_id())
    mint_associated_account_pubkey = assoc_instructions.get_associated_token_address(payer_keypair.public_key, mint_keypair.public_key)
    metaplex_program_id = PublicKey("metaqbxxUerdq28cj1RbAWkYQm3ybzjb6a8bt518x1s")
    metadata_pda, _metadata_pda_bump = PublicKey.find_program_address([b"metadata", bytes(metaplex_program_id), bytes(mint_keypair.public_key)], metaplex_program_id)
    global_gem_pubkey, _global_gem_bump = PublicKey.find_program_address([bytes(ingl_constants.GLOBAL_GEM_KEY, 'UTF-8')], get_program_id())
    collection_master_edition_pda, _master_edition_bump = PublicKey.find_program_address([b"metadata", bytes(metaplex_program_id), bytes(collection_mint_pubkey), b"edition"], metaplex_program_id)
    mint_edition_pda, _mint_edition_bump = PublicKey.find_program_address([b"metadata", bytes(metaplex_program_id), bytes(mint_keypair.public_key), b"edition"], metaplex_program_id)
    collection_account_pda, _collection_account_bump = PublicKey.find_program_address([b"metadata", bytes(metaplex_program_id), bytes(collection_mint_pubkey)], metaplex_program_id)
    gem_account_pubkey, _gem_account_bump = PublicKey.find_program_address([bytes(ingl_constants.GEM_ACCOUNT_CONST, 'UTF-8'), bytes(mint_keypair.public_key)], get_program_id())
    payer_account_meta = AccountMeta(payer_keypair.public_key, True, True)
    mint_account_meta = AccountMeta(mint_keypair.public_key, True, True)
    minting_pool_meta = AccountMeta(minting_pool_pubkey, False, True)
    mint_authority_meta = AccountMeta(mint_authority_pubkey, False, True)
    mint_associated_meta = AccountMeta(mint_associated_account_pubkey, False, True)
    spl_program_meta = AccountMeta(spl_constants.TOKEN_PROGRAM_ID, False, False)
    sysvar_rent_account_meta = AccountMeta(solana.sysvar.SYSVAR_RENT_PUBKEY, False, False)
    system_program_meta = AccountMeta(system_program.SYS_PROGRAM_ID, False, False)
    token_metadata_meta = AccountMeta(metadata_pda, False, True)
    metadata_program_id = AccountMeta(metaplex_program_id, False, False)
    associated_program_meta = AccountMeta(spl_constants.ASSOCIATED_TOKEN_PROGRAM_ID, False, False)
    global_gem_meta = AccountMeta(global_gem_pubkey, False, True)
    gem_account_meta = AccountMeta(gem_account_pubkey, False, True)
    collection_master_edition_meta = AccountMeta(collection_master_edition_pda, False, True)
    mint_edition_meta = AccountMeta(mint_edition_pda, False, True)
    collection_mint_meta = AccountMeta(collection_mint_pubkey, False, True)
    collection_account_meta = AccountMeta(collection_account_pda, False, True)


    accounts = [
        payer_account_meta,
        mint_account_meta,
        mint_authority_meta,
        mint_associated_meta,
        spl_program_meta,
        sysvar_rent_account_meta,
        system_program_meta,
        token_metadata_meta,
        minting_pool_meta,
        global_gem_meta,
        gem_account_meta,
        collection_master_edition_meta,
        mint_edition_meta,
        collection_mint_meta,
        collection_account_meta,

        system_program_meta,
        spl_program_meta,
        system_program_meta,
        spl_program_meta,
        associated_program_meta,
        spl_program_meta,
        metadata_program_id,
        metadata_program_id,
        spl_program_meta,
        metadata_program_id,
    ]

    instruction_data = build_instruction(InstructionEnum.enum.MintNft(), log_level = log_level, mint_class = mint_class)
    transaction = Transaction()
    transaction.add(ComputeBudgetInstruction().set_compute_unit_limit(400_000, payer_keypair.public_key))
    transaction.add(TransactionInstruction(accounts, get_program_id(), instruction_data))
    try: 
        t_dets = await sign_and_send_tx(transaction, client, payer_keypair, mint_keypair)
        await client.confirm_transaction(tx_sig = t_dets.value, commitment= "finalized", sleep_seconds = 0.4, last_valid_block_height = None)
        return f"Transaction Id: [link=https://explorer.solana.com/tx/{str(t_dets.value)+rpc_url.get_explorer_suffix()}]{str(t_dets.value)}[/link]"
    except Exception as e:
        return(f"[warning]Error: {e}[/warning]")

async def allocate_sol(payer_keypair: KeypairInput, mint_pubkey: PubkeyInput, client: AsyncClient, log_level: int = 0) -> str:
    minting_pool_pubkey, _minting_pool_pubkey_bump = PublicKey.find_program_address([bytes(ingl_constants.INGL_MINTING_POOL_KEY, 'UTF-8')], get_program_id())
    pd_pool_pubkey, _pd_pool_pubkey_bump = PublicKey.find_program_address([bytes(ingl_constants.PD_POOL_KEY, 'UTF-8')], get_program_id())
    gem_account_pubkey, _gem_account_bump = PublicKey.find_program_address([bytes(ingl_constants.GEM_ACCOUNT_CONST, 'UTF-8'), bytes(mint_pubkey.public_key)], get_program_id())
    global_gem_pubkey, _global_gem_bump = PublicKey.find_program_address([bytes(ingl_constants.GLOBAL_GEM_KEY, 'UTF-8')], get_program_id())
    mint_associated_account_pubkey = assoc_instructions.get_associated_token_address(payer_keypair.public_key, mint_pubkey.public_key)

    
    payer_account_meta = AccountMeta(payer_keypair.public_key, True, True)
    mint_account_meta = AccountMeta(mint_pubkey.public_key, False, True)
    gem_account_meta = AccountMeta(gem_account_pubkey, False, True)
    mint_associated_meta = AccountMeta(mint_associated_account_pubkey, False, True)
    global_gem_meta = AccountMeta(global_gem_pubkey, False, True)
    pd_pool_meta = AccountMeta(pd_pool_pubkey, False, True)
    minting_pool_meta = AccountMeta(minting_pool_pubkey, False, True)
    system_program_meta = AccountMeta(system_program.SYS_PROGRAM_ID, False, False)


    accounts = [
        payer_account_meta,
        mint_account_meta,
        gem_account_meta,
        mint_associated_meta,
        global_gem_meta,
        pd_pool_meta,
        minting_pool_meta,
        # sysvar_clock_meta,

        system_program_meta
    ]

    # print(accounts)
    instruction_data = build_instruction(InstructionEnum.enum.AllocateNFT(log_level = log_level, ))
    transaction = Transaction()
    transaction.add(TransactionInstruction(accounts, get_program_id(), instruction_data))
    try:
        t_dets = await sign_and_send_tx(transaction, client, payer_keypair)
        await client.confirm_transaction(tx_sig = t_dets.value, commitment= "finalized", sleep_seconds = 0.4, last_valid_block_height = None)
        return f"Transaction Id: [link=https://explorer.solana.com/tx/{str(t_dets.value)+rpc_url.get_explorer_suffix()}]{str(t_dets.value)}[/link]"
    except Exception as e:
        return(f"[warning]Error: {e}[/warning]")

async def deallocate_sol(payer_keypair: KeypairInput, mint_pubkey: PubkeyInput, client: AsyncClient, log_level: int = 0) -> str:
    minting_pool_pubkey, _minting_pool_pubkey_bump = PublicKey.find_program_address([bytes(ingl_constants.INGL_MINTING_POOL_KEY, 'UTF-8')], get_program_id())
    pd_pool_pubkey, _pd_pool_pubkey_bump = PublicKey.find_program_address([bytes(ingl_constants.PD_POOL_KEY, 'UTF-8')], get_program_id())
    gem_account_pubkey, _gem_account_bump = PublicKey.find_program_address([bytes(ingl_constants.GEM_ACCOUNT_CONST, 'UTF-8'), bytes(mint_pubkey.public_key)], get_program_id())
    global_gem_pubkey, _global_gem_bump = PublicKey.find_program_address([bytes(ingl_constants.GLOBAL_GEM_KEY, 'UTF-8')], get_program_id())
    mint_associated_account_pubkey = assoc_instructions.get_associated_token_address(payer_keypair.public_key, mint_pubkey.public_key)

    
    payer_account_meta = AccountMeta(payer_keypair.public_key, True, True)
    mint_account_meta = AccountMeta(mint_pubkey.public_key, False, True)
    gem_account_meta = AccountMeta(gem_account_pubkey, False, True)
    mint_associated_meta = AccountMeta(mint_associated_account_pubkey, False, True)
    global_gem_meta = AccountMeta(global_gem_pubkey, False, True)
    pd_pool_meta = AccountMeta(pd_pool_pubkey, False, True)
    minting_pool_meta = AccountMeta(minting_pool_pubkey, False, True)
    # sysvar_clock_meta = AccountMeta(solana.sysvar.SYSVAR_CLOCK_PUBKEY, False, False)
    system_program_meta = AccountMeta(system_program.SYS_PROGRAM_ID, False, False)


    accounts = [
        payer_account_meta,
        mint_account_meta,
        gem_account_meta,
        mint_associated_meta,
        global_gem_meta,
        pd_pool_meta,
        minting_pool_meta,
        # sysvar_clock_meta,

        system_program_meta
    ]

    # print(accounts)
    instruction_data = build_instruction(InstructionEnum.enum.DeAllocateNFT(log_level = log_level, ))
    transaction = Transaction()
    transaction.add(TransactionInstruction(accounts, get_program_id(), instruction_data))
    try:
        t_dets = await sign_and_send_tx(transaction, client, payer_keypair)
        await client.confirm_transaction(tx_sig = t_dets.value, commitment= "finalized", sleep_seconds = 0.4, last_valid_block_height = None)
        return f"Transaction Id: [link=https://explorer.solana.com/tx/{str(t_dets.value)+rpc_url.get_explorer_suffix()}]{str(t_dets.value)}[/link]"
    except Exception as e:
        return(f"[warning]Error: {e}[/warning]")

async def register_validator_id(validator_keypair: KeypairInput, client: AsyncClient, log_level: int = 0) -> str:
    team_account_pubkey, _team_account_pubkey_bump = PublicKey.find_program_address([bytes(ingl_constants.INGL_TEAM_ACCOUNT, 'UTF-8')], get_program_id())
    global_gem_pubkey, _global_gem_bump = PublicKey.find_program_address([bytes(ingl_constants.GLOBAL_GEM_KEY, 'UTF-8')], get_program_id())

    dupkey, dup_bump = PublicKey.find_program_address([ingl_constants.DUPKEYBYTES, bytes(validator_keypair.public_key)], get_program_id());

    
    validator_meta = AccountMeta(validator_keypair.public_key, True, True)
    global_gem_meta = AccountMeta(global_gem_pubkey, False, True)
    system_program_meta = AccountMeta(system_program.SYS_PROGRAM_ID, False, False)
    mint_authority_meta = AccountMeta(team_account_pubkey, False, True)
    dup_meta = AccountMeta(dupkey, False, True)

    accounts = [
        validator_meta,
        global_gem_meta,
        mint_authority_meta,
        dup_meta,

        system_program_meta,
        system_program_meta,
    ]

    instruction_data = build_instruction(InstructionEnum.enum.RegisterValidatorId(log_level = log_level, ))
    transaction = Transaction()
    transaction.add(TransactionInstruction(accounts, get_program_id(), instruction_data))
    try:
        t_dets = await sign_and_send_tx(transaction, client, validator_keypair)
        await client.confirm_transaction(tx_sig = t_dets.value, commitment= "finalized", sleep_seconds = 0.4, last_valid_block_height = None)
        return f"Transaction Id: [link=https://explorer.solana.com/tx/{str(t_dets.value)+rpc_url.get_explorer_suffix()}]{str(t_dets.value)}[/link]"
    except Exception as e:
        return(f"[warning]Error: {e}[/warning]")

async def create_validator_proposal(payer_keypair: KeypairInput, proposal_numeration: int, client: AsyncClient, log_level: int = 0) -> str:
    global_gem_pubkey, _global_gem_bump = PublicKey.find_program_address([bytes(ingl_constants.GLOBAL_GEM_KEY, 'UTF-8')], get_program_id())
    proposal_pubkey, _proposal_bump = PublicKey.find_program_address([bytes(ingl_constants.PROPOSAL_KEY, 'UTF-8'), proposal_numeration.to_bytes(4,"big")], get_program_id())
    
    payer_account_meta = AccountMeta(payer_keypair.public_key, True, True)
    global_gem_meta = AccountMeta(global_gem_pubkey, False, True)
    proposal_meta = AccountMeta(proposal_pubkey, False, True)
    system_program_meta = AccountMeta(system_program.SYS_PROGRAM_ID, False, False)
    print(f"Proposal_id: {proposal_pubkey}")
    accounts = [
        payer_account_meta,
        global_gem_meta,
        proposal_meta,

        system_program_meta,
    ]

    instruction_data = build_instruction(InstructionEnum.enum.CreateValidatorSelectionProposal(log_level = log_level, ))
    transaction = Transaction()
    transaction.add(TransactionInstruction(accounts, get_program_id(), instruction_data))
    try:
        t_dets = await sign_and_send_tx(transaction, client, payer_keypair)
        await client.confirm_transaction(tx_sig = t_dets.value, commitment= "finalized", sleep_seconds = 0.4, last_valid_block_height = None)
        return f"Transaction Id: [link=https://explorer.solana.com/tx/{str(t_dets.value)+rpc_url.get_explorer_suffix()}]{str(t_dets.value)}[/link]"
    except Exception as e:
        return(f"[warning]Error: {e}[/warning]")

async def vote_validator_proposal(payer_keypair: KeypairInput, proposal_numeration: int, mint_pubkeys: List[PubkeyInput], val_index:int, client: AsyncClient, log_level: int = 0) -> str:
    proposal_pubkey, _proposal_bump = PublicKey.find_program_address([bytes(ingl_constants.PROPOSAL_KEY, 'UTF-8'), proposal_numeration.to_bytes(4,"big")], get_program_id())
    global_gem_pubkey, _global_gem_bump = PublicKey.find_program_address([bytes(ingl_constants.GLOBAL_GEM_KEY, 'UTF-8')], get_program_id())

    
    payer_account_meta = AccountMeta(payer_keypair.public_key, True, True)
    proposal_meta = AccountMeta(proposal_pubkey, False, True)
    global_gem_meta = AccountMeta(global_gem_pubkey, False, True)
    system_program_meta = AccountMeta(system_program.SYS_PROGRAM_ID, False, False)

    accounts = [
        payer_account_meta,
        proposal_meta,
        global_gem_meta,
        ]

    for mint in mint_pubkeys:
        gem_account_pubkey, _ = PublicKey.find_program_address([bytes(ingl_constants.GEM_ACCOUNT_CONST, 'UTF-8'), bytes(mint.public_key)], get_program_id())
        accounts.append(AccountMeta(mint.public_key, False, False))
        accounts.append(AccountMeta(assoc_instructions.get_associated_token_address(payer_keypair.public_key, mint.public_key), False, False))
        accounts.append(AccountMeta(gem_account_pubkey, False, True))
    
    accounts.append(system_program_meta)




    instruction_data = build_instruction(InstructionEnum.enum.VoteValidatorProposal(log_level = log_level, num_nfts = len(mint_pubkeys), validator_index = val_index))
    transaction = Transaction()
    transaction.add(TransactionInstruction(accounts, get_program_id(), instruction_data))
    try:
        t_dets = await sign_and_send_tx(transaction, client, payer_keypair)
        await client.confirm_transaction(tx_sig = t_dets.value, commitment= "finalized", sleep_seconds = 0.4, last_valid_block_height = None)
        return f"Transaction Id: [link=https://explorer.solana.com/tx/{str(t_dets.value)+rpc_url.get_explorer_suffix()}]{str(t_dets.value)}[/link]"
    except Exception as e:
        return(f"[warning]Error: {e}[/warning]")

async def finalize_proposal(payer_keypair: KeypairInput, client: AsyncClient, log_level: int = 0) -> str:
    global_gem_pubkey, _global_gem_bump = PublicKey.find_program_address([bytes(ingl_constants.GLOBAL_GEM_KEY, 'UTF-8')], get_program_id())
    
    data = await client.get_account_info(global_gem_pubkey)
    global_gems = GlobalGems.parse(data.value.data)
    proposal_numeration = global_gems.proposal_numeration - 1
    proposal_pubkey, _proposal_bump = PublicKey.find_program_address([bytes(ingl_constants.PROPOSAL_KEY, 'UTF-8'), proposal_numeration.to_bytes(4,"big")], get_program_id())

    global_gem_meta = AccountMeta(global_gem_pubkey, False, True)
    payer_account_meta = AccountMeta(payer_keypair.public_key, True, True)
    proposal_meta = AccountMeta(proposal_pubkey, False, True)

    accounts = [
        payer_account_meta,
        proposal_meta,
        global_gem_meta,
    ]

    instruction_data = build_instruction(InstructionEnum.enum.FinalizeProposal(log_level = log_level, ))
    transaction = Transaction()
    transaction.add(TransactionInstruction(accounts, get_program_id(), instruction_data))
    try:
        t_dets = await sign_and_send_tx(transaction, client, payer_keypair)
        await client.confirm_transaction(tx_sig = t_dets.value, commitment= "finalized", sleep_seconds = 0.4, last_valid_block_height = None)
        return f"Transaction Id: [link=https://explorer.solana.com/tx/{str(t_dets.value)+rpc_url.get_explorer_suffix()}]{str(t_dets.value)}[/link]"
    except Exception as e:
        return(f"[warning]Error: {e}[/warning]")

async def delegate_nft(payer_keypair: KeypairInput, mint_pubkey: PubkeyInput, expected_vote_pubkey: PubkeyInput, client: AsyncClient, log_level: int = 0) -> str:
    gem_account_pubkey, _gem_account_bump = PublicKey.find_program_address([bytes(ingl_constants.GEM_ACCOUNT_CONST, 'UTF-8'), bytes(mint_pubkey.public_key)], get_program_id())
    global_gem_pubkey, _global_gem_bump = PublicKey.find_program_address([bytes(ingl_constants.GLOBAL_GEM_KEY, 'UTF-8')], get_program_id())
    mint_associated_account_pubkey = assoc_instructions.get_associated_token_address(payer_keypair.public_key, mint_pubkey.public_key)
    expected_vote_data_pubkey, _expected_vote_data_bump = PublicKey.find_program_address([bytes(ingl_constants.VOTE_DATA_ACCOUNT_KEY, 'UTF-8'), bytes(expected_vote_pubkey.public_key)], get_program_id())

    
    payer_account_meta = AccountMeta(payer_keypair.public_key, True, True)
    mint_account_meta = AccountMeta(mint_pubkey.public_key, False, True)
    gem_account_meta = AccountMeta(gem_account_pubkey, False, True)
    mint_associated_meta = AccountMeta(mint_associated_account_pubkey, False, True)
    global_gem_meta = AccountMeta(global_gem_pubkey, False, True)
    ingl_vote_data_account_meta = AccountMeta(expected_vote_data_pubkey, False, True)
    
    vote_account_meta = AccountMeta(expected_vote_pubkey.public_key, False, True)
    sysvar_clock_meta = AccountMeta(solana.sysvar.SYSVAR_CLOCK_PUBKEY, False, False)
    stake_config_program_meta = AccountMeta(ingl_constants.STAKE_CONFIG_PROGRAM_ID, False, False)


    accounts = [
        payer_account_meta,
        vote_account_meta,
        ingl_vote_data_account_meta,
        mint_account_meta,
        gem_account_meta,
        mint_associated_meta,
        global_gem_meta,
        sysvar_clock_meta,
        stake_config_program_meta,
    ]

    # print(accounts)
    instruction_data = build_instruction(InstructionEnum.enum.DelegateNFT(log_level = log_level, ))
    transaction = Transaction()
    transaction.add(TransactionInstruction(accounts, get_program_id(), instruction_data))
    try:
        t_dets = await sign_and_send_tx(transaction, client, payer_keypair)
        await client.confirm_transaction(tx_sig = t_dets.value, commitment= "finalized", sleep_seconds = 0.4, last_valid_block_height = None)
        return f"Transaction Id: [link=https://explorer.solana.com/tx/{str(t_dets.value)+rpc_url.get_explorer_suffix()}]{str(t_dets.value)}[/link]"
    except Exception as e:
        return(f"[warning]Error: {e}[/warning]")

async def undelegate_nft(payer_keypair: KeypairInput, mint_pubkey: PubkeyInput, expected_vote_pubkey: PubkeyInput, client: AsyncClient, log_level: int = 0) -> str: #TODO: Need to include the 3 new accounts: Authorized_withdrawer, validator_info, and the system program in this instruction, without which instruction will consistently fail
    pd_pool_pubkey, _pd_pool_pubkey_bump = PublicKey.find_program_address([bytes(ingl_constants.PD_POOL_KEY, 'UTF-8')], get_program_id())
    gem_account_pubkey, _gem_account_bump = PublicKey.find_program_address([bytes(ingl_constants.GEM_ACCOUNT_CONST, 'UTF-8'), bytes(mint_pubkey.public_key)], get_program_id())
    global_gem_pubkey, _global_gem_bump = PublicKey.find_program_address([bytes(ingl_constants.GLOBAL_GEM_KEY, 'UTF-8')], get_program_id())
    mint_associated_account_pubkey = assoc_instructions.get_associated_token_address(payer_keypair.public_key, mint_pubkey.public_key)
    expected_vote_data_pubkey, _expected_vote_data_bump = PublicKey.find_program_address([bytes(ingl_constants.VOTE_DATA_ACCOUNT_KEY, 'UTF-8'), bytes(expected_vote_pubkey.public_key)], get_program_id())
    authorized_withdrawer_key, _authorized_withdrawer_bump = PublicKey.find_program_address([bytes(ingl_constants.AUTHORIZED_WITHDRAWER_KEY, 'UTF-8'), bytes(expected_vote_pubkey.public_key) ], get_program_id())
    
    data = await client.get_account_info(expected_vote_data_pubkey)
    validator_id = PublicKey(InglVoteAccountData.parse(data.value.data).validator_id)

    
    payer_account_meta = AccountMeta(payer_keypair.public_key, True, True)
    mint_account_meta = AccountMeta(mint_pubkey.public_key, False, True)
    gem_account_meta = AccountMeta(gem_account_pubkey, False, True)
    mint_associated_meta = AccountMeta(mint_associated_account_pubkey, False, True)
    global_gem_meta = AccountMeta(global_gem_pubkey, False, True)
    pd_pool_meta = AccountMeta(pd_pool_pubkey, False, True)
    ingl_vote_data_account_meta = AccountMeta(expected_vote_data_pubkey, False, True)
    stake_program_meta  = AccountMeta(ingl_constants.STAKE_PROGRAM_ID, False, False)
    
    vote_account_meta = AccountMeta(expected_vote_pubkey.public_key, False, True)
    authorized_withdrawer_meta = AccountMeta(authorized_withdrawer_key, False, True)
    validator_account_meta =  AccountMeta(validator_id, False, False)
    system_program_meta = AccountMeta(system_program.SYS_PROGRAM_ID, False, False)


    accounts = [
        payer_account_meta,
        pd_pool_meta,
        vote_account_meta,
        ingl_vote_data_account_meta,
        mint_account_meta,
        gem_account_meta,
        mint_associated_meta,
        global_gem_meta,
        system_program_meta,
        authorized_withdrawer_meta,

        system_program_meta,
        stake_program_meta,
    ]

    # print(accounts)
    instruction_data = build_instruction(InstructionEnum.enum.UnDelegateNFT(log_level = log_level, ))
    transaction = Transaction()
    transaction.add(TransactionInstruction(accounts, get_program_id(), instruction_data))
    try:
        t_dets = await sign_and_send_tx(transaction, client, payer_keypair)
        await client.confirm_transaction(tx_sig = t_dets.value, commitment= "finalized", sleep_seconds = 0.4, last_valid_block_height = None)
        return f"Transaction Id: [link=https://explorer.solana.com/tx/{str(t_dets.value)+rpc_url.get_explorer_suffix()}]{str(t_dets.value)}[/link]"
    except Exception as e:
        return(f"[warning]Error: {e}[/warning]")

async def create_vote_account(validator_keypair: KeypairInput, proposal_numeration: int, client: AsyncClient, log_level: int = 0) -> str:
    global_gem_pubkey, _global_gem_bump = PublicKey.find_program_address([bytes(ingl_constants.GLOBAL_GEM_KEY, 'UTF-8')], get_program_id())
    proposal_pubkey, _proposal_bump = PublicKey.find_program_address([bytes(ingl_constants.PROPOSAL_KEY, 'UTF-8'), proposal_numeration.to_bytes(4,"big")], get_program_id())
    expected_vote_pubkey, _expected_vote_pubkey_nonce = PublicKey.find_program_address([bytes(ingl_constants.VOTE_ACCOUNT_KEY, "UTF-8"), (proposal_numeration).to_bytes(4,"big")], get_program_id())
    expected_vote_data_pubkey, _expected_vote_data_bump = PublicKey.find_program_address([bytes(ingl_constants.VOTE_DATA_ACCOUNT_KEY, 'UTF-8'), bytes(expected_vote_pubkey)], get_program_id())
    expected_stake_key, _expected_stake_bump = PublicKey.find_program_address([bytes(ingl_constants.STAKE_ACCOUNT_KEY, 'UTF-8'), bytes(expected_vote_pubkey)], get_program_id())
    pd_pool_pubkey, _pd_pool_bump = PublicKey.find_program_address([bytes(ingl_constants.PD_POOL_KEY, 'UTF-8')], get_program_id())
    
    print(f"Vote_Account: {expected_vote_pubkey}")

    rent_account_meta = AccountMeta(solana.sysvar.SYSVAR_RENT_PUBKEY, False, False)
    sysvar_clock_meta = AccountMeta(solana.sysvar.SYSVAR_CLOCK_PUBKEY, False, False)
    stake_config_meta = AccountMeta(ingl_constants.STAKE_CONFIG_PROGRAM_ID, False, False)
    sysvar_stake_history_meta = AccountMeta(solana.sysvar.SYSVAR_STAKE_HISTORY_PUBKEY, False, False)
    validator_meta = AccountMeta(validator_keypair.public_key, True, True)
    vote_account_meta = AccountMeta(expected_vote_pubkey, False, True)
    sys_program_meta = AccountMeta(system_program.SYS_PROGRAM_ID, False, False)
    vote_program_meta = AccountMeta(ingl_constants.VOTE_PROGRAM_ID, False, False)
    global_gem_meta = AccountMeta(global_gem_pubkey, False, True)
    proposal_meta = AccountMeta(proposal_pubkey, False, True)
    spl_program_meta = AccountMeta(spl_constants.TOKEN_PROGRAM_ID, False, False)
    ingl_vote_data_account_meta = AccountMeta(expected_vote_data_pubkey, False, True)
    stake_account_meta = AccountMeta(expected_stake_key, False, True)
    pd_pool_meta = AccountMeta(pd_pool_pubkey, False, True)
    stake_program_meta = AccountMeta(ingl_constants.STAKE_PROGRAM_ID, False, False)


    accounts = [
        validator_meta,
        vote_account_meta,
        rent_account_meta,
        sysvar_clock_meta,
        global_gem_meta,
        proposal_meta,
        sys_program_meta,
        spl_program_meta,
        ingl_vote_data_account_meta,
        stake_account_meta,
        pd_pool_meta,
        sysvar_stake_history_meta,
        stake_config_meta,

        
        sys_program_meta,
        vote_program_meta,
        vote_program_meta,
        sys_program_meta,
        stake_program_meta,
    ]

    data = InstructionEnum.build(InstructionEnum.enum.CreateVoteAccount(log_level = log_level, ))
    transaction = Transaction()
    transaction.add(TransactionInstruction(accounts, get_program_id(), data))
    try: 
        t_dets = await sign_and_send_tx(transaction, client, validator_keypair)
        await client.confirm_transaction(tx_sig = t_dets.value, commitment= "finalized", sleep_seconds = 0.4, last_valid_block_height = None)
        return f"Transaction Id: [link=https://explorer.solana.com/tx/{str(t_dets.value)+rpc_url.get_explorer_suffix()}]{str(t_dets.value)}[/link]"
    except Exception as e:
        return(f"[warning]Error: {e}[/warning]")

async def close_proposal(payer_keypair: KeypairInput, proposal_numeration: int, client: AsyncClient, log_level: int = 0) -> str:
    global_gem_pubkey, _global_gem_bump = PublicKey.find_program_address([bytes(ingl_constants.GLOBAL_GEM_KEY, 'UTF-8')], get_program_id())
    expected_vote_pubkey, _expected_vote_pubkey_nonce = PublicKey.find_program_address([bytes(ingl_constants.VOTE_ACCOUNT_KEY, "UTF-8"), (proposal_numeration).to_bytes(4,"big")], get_program_id())
    expected_vote_data_pubkey, _expected_vote_data_bump = PublicKey.find_program_address([bytes(ingl_constants.VOTE_DATA_ACCOUNT_KEY, 'UTF-8'), bytes(expected_vote_pubkey)], get_program_id())
    
    data = await client.get_account_info(global_gem_pubkey)
    global_gems = GlobalGems.parse(data.value.data)
    proposal_numeration = global_gems.proposal_numeration - 1
    proposal_pubkey, _proposal_bump = PublicKey.find_program_address([bytes(ingl_constants.PROPOSAL_KEY, 'UTF-8'), proposal_numeration.to_bytes(4,"big")], get_program_id())


    payer_account_meta = AccountMeta(payer_keypair.public_key, True, True)
    global_gem_meta = AccountMeta(global_gem_pubkey, False, True)
    ingl_vote_data_account_meta = AccountMeta(expected_vote_data_pubkey, False, True)
    proposal_meta = AccountMeta(proposal_pubkey, False, False)

    accounts = [
        payer_account_meta,
        global_gem_meta,
        ingl_vote_data_account_meta,
        proposal_meta,
    ]

    data = InstructionEnum.build(InstructionEnum.enum.CloseProposal(log_level = log_level, ))
    transaction = Transaction()
    transaction.add(TransactionInstruction(accounts, get_program_id(), data))
    try:
        t_dets = await sign_and_send_tx(transaction, client, payer_keypair)
        await client.confirm_transaction(tx_sig = t_dets.value, commitment= "finalized", sleep_seconds = 0.4, last_valid_block_height = None)
        return f"Transaction Id: [link=https://explorer.solana.com/tx/{str(t_dets.value)+rpc_url.get_explorer_suffix()}]{str(t_dets.value)}[/link]"
    except Exception as e:
        return(f"[warning]Error: {e}[/warning]")

async def init_rebalance(payer_keypair: KeypairInput, vote_account_pubkey: PubkeyInput, client: AsyncClient, log_level: int = 0) -> str:
    global_gem_pubkey, _global_gem_bump = PublicKey.find_program_address([bytes(ingl_constants.GLOBAL_GEM_KEY, 'UTF-8')], get_program_id())
    expected_vote_pubkey = vote_account_pubkey.public_key
    expected_vote_data_pubkey, _expected_vote_data_bump = PublicKey.find_program_address([bytes(ingl_constants.VOTE_DATA_ACCOUNT_KEY, 'UTF-8'), bytes(expected_vote_pubkey)], get_program_id())
    expected_stake_key, _expected_stake_bump = PublicKey.find_program_address([bytes(ingl_constants.STAKE_ACCOUNT_KEY, 'UTF-8'), bytes(expected_vote_pubkey)], get_program_id())
    t_stake_key, _t_stake_bump = PublicKey.find_program_address([bytes(ingl_constants.T_STAKE_ACCOUNT_KEY, 'UTF-8'), bytes(expected_vote_pubkey)], get_program_id())
    t_withdraw_key, _t_withdraw_bump = PublicKey.find_program_address([bytes(ingl_constants.T_WITHDRAW_KEY, 'UTF-8'), bytes(expected_vote_pubkey)], get_program_id())
    pd_pool_pubkey, _pd_pool_bump = PublicKey.find_program_address([bytes(ingl_constants.PD_POOL_KEY, 'UTF-8')], get_program_id())
    data = await client.get_account_info(expected_vote_data_pubkey)
    validator_id = PublicKey(InglVoteAccountData.parse(data.value.data).validator_id)
    print(f"Validator_Id: {validator_id}")

    payer_account_meta = AccountMeta(payer_keypair.public_key, True, True)
    rent_account_meta = AccountMeta(solana.sysvar.SYSVAR_RENT_PUBKEY, False, False)
    sysvar_clock_meta = AccountMeta(solana.sysvar.SYSVAR_CLOCK_PUBKEY, False, False)
    validator_meta = AccountMeta(validator_id, True, True)
    vote_account_meta = AccountMeta(expected_vote_pubkey, False, True)
    sys_program_meta = AccountMeta(system_program.SYS_PROGRAM_ID, False, False)
    global_gem_meta = AccountMeta(global_gem_pubkey, False, True)
    ingl_vote_data_account_meta = AccountMeta(expected_vote_data_pubkey, False, True)
    stake_account_meta = AccountMeta(expected_stake_key, False, True)
    t_stake_meta = AccountMeta(t_stake_key, False, True)
    t_withdraw_meta = AccountMeta(t_withdraw_key, False, True)
    pd_pool_meta = AccountMeta(pd_pool_pubkey, False, True)
    stake_program_meta = AccountMeta(ingl_constants.STAKE_PROGRAM_ID, False, False)

    accounts = [
        payer_account_meta,
        vote_account_meta,
        validator_meta,
        t_stake_meta,
        pd_pool_meta,
        global_gem_meta,
        ingl_vote_data_account_meta,
        sysvar_clock_meta,
        rent_account_meta,
        stake_account_meta,
        t_withdraw_meta,

        sys_program_meta,
        stake_program_meta,
        sys_program_meta,
        sys_program_meta,
        stake_program_meta,
        stake_program_meta,
    ]
    print(accounts)
    data = InstructionEnum.build(InstructionEnum.enum.InitRebalance(log_level = log_level, ))
    transaction = Transaction()
    transaction.add(TransactionInstruction(accounts, get_program_id(), data))
    try:
        t_dets = await sign_and_send_tx(transaction, client, payer_keypair)
        await client.confirm_transaction(tx_sig = t_dets.value, commitment= "finalized", sleep_seconds = 0.4, last_valid_block_height = None)
        return f"Transaction Id: [link=https://explorer.solana.com/tx/{str(t_dets.value)+rpc_url.get_explorer_suffix()}]{str(t_dets.value)}[/link]"
    except Exception as e:
        return(f"[warning]Error: {e}[/warning]")

async def finalize_rebalance(payer_keypair: KeypairInput, vote_account_pubkey: PubkeyInput, client: AsyncClient, log_level: int = 0) -> str:
    expected_vote_pubkey = vote_account_pubkey.public_key
    expected_vote_data_pubkey, _expected_vote_data_bump = PublicKey.find_program_address([bytes(ingl_constants.VOTE_DATA_ACCOUNT_KEY, 'UTF-8'), bytes(expected_vote_pubkey)], get_program_id())
    expected_stake_key, _expected_stake_bump = PublicKey.find_program_address([bytes(ingl_constants.STAKE_ACCOUNT_KEY, 'UTF-8'), bytes(expected_vote_pubkey)], get_program_id())
    t_stake_key, _t_stake_bump = PublicKey.find_program_address([bytes(ingl_constants.T_STAKE_ACCOUNT_KEY, 'UTF-8'), bytes(expected_vote_pubkey)], get_program_id())
    t_withdraw_key, _t_withdraw_bump = PublicKey.find_program_address([bytes(ingl_constants.T_WITHDRAW_KEY, 'UTF-8'), bytes(expected_vote_pubkey)], get_program_id())
    pd_pool_pubkey, _pd_pool_bump = PublicKey.find_program_address([bytes(ingl_constants.PD_POOL_KEY, 'UTF-8')], get_program_id())
    data = await client.get_account_info(expected_vote_data_pubkey)
    validator_id = PublicKey(InglVoteAccountData.parse(data.value.data).validator_id)
    print(f"Validator_Id: {validator_id}")

    payer_account_meta = AccountMeta(payer_keypair.public_key, True, True)
    sysvar_clock_meta = AccountMeta(solana.sysvar.SYSVAR_CLOCK_PUBKEY, False, False)
    validator_meta = AccountMeta(validator_id, True, True)
    vote_account_meta = AccountMeta(expected_vote_pubkey, False, True)
    ingl_vote_data_account_meta = AccountMeta(expected_vote_data_pubkey, False, True)
    stake_account_meta = AccountMeta(expected_stake_key, False, True)
    t_stake_meta = AccountMeta(t_stake_key, False, True)
    t_withdraw_meta = AccountMeta(t_withdraw_key, False, True)
    pd_pool_meta = AccountMeta(pd_pool_pubkey, False, True)
    stake_program_meta = AccountMeta(ingl_constants.STAKE_PROGRAM_ID, False, False)
    sysvar_stake_history_meta = AccountMeta(solana.sysvar.SYSVAR_STAKE_HISTORY_PUBKEY, False, False)

    accounts = [
        payer_account_meta,
        vote_account_meta,
        validator_meta,
        t_stake_meta,
        pd_pool_meta,
        ingl_vote_data_account_meta,
        sysvar_clock_meta,
        stake_account_meta,
        t_withdraw_meta,
        sysvar_stake_history_meta,
        
        
        stake_program_meta,
        stake_program_meta,
        stake_program_meta,
    ]

    data = InstructionEnum.build(InstructionEnum.enum.FinalizeRebalance(log_level = log_level, ))
    transaction = Transaction()
    transaction.add(TransactionInstruction(accounts, get_program_id(), data))
    try:
        t_dets = await sign_and_send_tx(transaction, client, payer_keypair)
        await client.confirm_transaction(tx_sig = t_dets.value, commitment= "finalized", sleep_seconds = 0.4, last_valid_block_height = None)
        return f"Transaction Id: [link=https://explorer.solana.com/tx/{str(t_dets.value)+rpc_url.get_explorer_suffix()}]{str(t_dets.value)}[/link]"
    except Exception as e:
        return(f"[warning]Error: {e}[/warning]")

async def process_rewards(payer_keypair: KeypairInput, vote_account_id: PubkeyInput, client: AsyncClient, log_level: int = 0) -> str:
    ingl_team_account_pubkey, _ita_bump = PublicKey.find_program_address([bytes(ingl_constants.INGL_TEAM_ACCOUNT, 'UTF-8')], get_program_id())
    expected_vote_data_pubkey, _expected_vote_data_bump = PublicKey.find_program_address([bytes(ingl_constants.VOTE_DATA_ACCOUNT_KEY, 'UTF-8'), bytes(vote_account_id.public_key)], get_program_id())
    data = await client.get_account_info(expected_vote_data_pubkey)
    validator_id = PublicKey(InglVoteAccountData.parse(data.value.data).validator_id)
    authorized_withdrawer_key, _authorized_withdrawer_bump = PublicKey.find_program_address([bytes(ingl_constants.AUTHORIZED_WITHDRAWER_KEY, 'UTF-8'), bytes(vote_account_id.public_key) ], get_program_id())
    treasury_key, _treasury_bump = PublicKey.find_program_address([bytes(ingl_constants.TREASURY_ACCOUNT_KEY, 'UTF-8')], get_program_id())
    print(f"Validator_Id: {validator_id}")

    treasury_meta = AccountMeta(treasury_key, False, True)
    payer_account_meta = AccountMeta(payer_keypair.public_key, True, True)
    validator_meta = AccountMeta(validator_id, False, True)
    vote_account_meta = AccountMeta(vote_account_id.public_key, False, True)
    sys_program_meta = AccountMeta(system_program.SYS_PROGRAM_ID, False, False)
    vote_program_meta = AccountMeta(ingl_constants.VOTE_PROGRAM_ID, False, False)
    mint_authority_meta = AccountMeta(ingl_team_account_pubkey, False, True)
    ingl_vote_data_account_meta = AccountMeta(expected_vote_data_pubkey, False, True)
    authorized_withdrawer_meta = AccountMeta(authorized_withdrawer_key, False, True)


    accounts = [
        payer_account_meta,
        validator_meta,
        vote_account_meta,
        ingl_vote_data_account_meta,
        authorized_withdrawer_meta,
        mint_authority_meta,
        treasury_meta,
        
        
        vote_program_meta,
        sys_program_meta,
        sys_program_meta,
        sys_program_meta,
    ]
    # print(accounts)
    data = InstructionEnum.build(InstructionEnum.enum.ProcessRewards(log_level = log_level, ))
    transaction = Transaction()
    transaction.add(TransactionInstruction(accounts, get_program_id(), data))
    try:
        t_dets = await sign_and_send_tx(transaction, client, payer_keypair)
        await client.confirm_transaction(tx_sig = t_dets.value, commitment= "finalized", sleep_seconds = 0.4, last_valid_block_height = None)
        return f"Transaction Id: [link=https://explorer.solana.com/tx/{str(t_dets.value)+rpc_url.get_explorer_suffix()}]{str(t_dets.value)}[/link]"
    except Exception as e:
        return(f"[warning]Error: {e}[/warning]")

async def nft_withdraw(payer_keypair: KeypairInput, mints: List[PublicKey], vote_account_id: PubkeyInput, client: AsyncClient, log_level: int = 0) -> str:
    expected_vote_data_pubkey, _expected_vote_data_bump = PublicKey.find_program_address([bytes(ingl_constants.VOTE_DATA_ACCOUNT_KEY, 'UTF-8'), bytes(vote_account_id)], get_program_id())
    data = await client.get_account_info(expected_vote_data_pubkey)
    validator_id = PublicKey(InglVoteAccountData.parse(data.value.data).validator_id)
    authorized_withdrawer_key, _authorized_withdrawer_bump = PublicKey.find_program_address([bytes(ingl_constants.AUTHORIZED_WITHDRAWER_KEY, 'UTF-8'), bytes(vote_account_id.public_key) ], get_program_id())

    payer_account_meta = AccountMeta(payer_keypair.public_key, True, True)
    validator_meta = AccountMeta(validator_id, False, True)
    vote_account_meta = AccountMeta(vote_account_id, False, True)
    sys_program_meta = AccountMeta(system_program.SYS_PROGRAM_ID, False, False)
    authorized_withdrawer_meta = AccountMeta(authorized_withdrawer_key, False, True)
    ingl_vote_data_account_meta = AccountMeta(expected_vote_data_pubkey, False, True)

    accounts = [
        payer_account_meta,
        vote_account_meta,
        validator_meta,
        ingl_vote_data_account_meta,
        authorized_withdrawer_meta,
        
    ]

    for mint_pubkey in mints:
        mint_associated_account_pubkey = assoc_instructions.get_associated_token_address(payer_keypair.public_key, mint_pubkey.public_key)
        accounts.append(AccountMeta(mint_associated_account_pubkey, False, False))
        accounts.append(AccountMeta(mint_pubkey.public_key, False, False))
        gem_account_pubkey, _gem_account_bump = PublicKey.find_program_address([bytes(ingl_constants.GEM_ACCOUNT_CONST, 'UTF-8'), bytes(mint_pubkey.public_key)], get_program_id())
        accounts.append(AccountMeta(gem_account_pubkey, False, True))




    accounts.append(sys_program_meta)
    # print(accounts)
    data = InstructionEnum.build(InstructionEnum.enum.NFTWithdraw(log_level = log_level, cnt = len(mints)))
    transaction = Transaction()
    transaction.add(TransactionInstruction(accounts, get_program_id(), data))
    try:
        t_dets = await sign_and_send_tx(transaction, client, payer_keypair)
        await client.confirm_transaction(tx_sig = t_dets.value, commitment= "finalized", sleep_seconds = 0.4, last_valid_block_height = None)
        return f"Transaction Id: [link=https://explorer.solana.com/tx/{str(t_dets.value)+rpc_url.get_explorer_suffix()}]{str(t_dets.value)}[/link]"
    except Exception as e:
        return(f"[warning]Error: {e}[/warning]")

async def inject_testing_data(payer_keypair: KeypairInput, mints: List[PublicKey], vote_account_id: PubkeyInput, client: AsyncClient, log_level: int = 0) -> str:
    expected_vote_data_pubkey, _expected_vote_data_bump = PublicKey.find_program_address([bytes(ingl_constants.VOTE_DATA_ACCOUNT_KEY, 'UTF-8'), bytes(vote_account_id.public_key)], get_program_id())
    authorized_withdrawer_key, _authorized_withdrawer_bump = PublicKey.find_program_address([bytes(ingl_constants.AUTHORIZED_WITHDRAWER_KEY, 'UTF-8'), bytes(vote_account_id.public_key) ], get_program_id())

    payer_account_meta = AccountMeta(payer_keypair.public_key, True, True)
    vote_account_meta = AccountMeta(vote_account_id.public_key, False, True)
    sys_program_meta = AccountMeta(system_program.SYS_PROGRAM_ID, False, False)
    ingl_vote_data_account_meta = AccountMeta(expected_vote_data_pubkey, False, True)
    authorized_withdrawer_meta = AccountMeta(authorized_withdrawer_key, False, True)

    accounts = [
        payer_account_meta,
        vote_account_meta,
        ingl_vote_data_account_meta,
        authorized_withdrawer_meta,
        
    ]

    for mint_pubkey in mints:
        accounts.append(AccountMeta(mint_pubkey.public_key, False, False))
        gem_account_pubkey, _gem_account_bump = PublicKey.find_program_address([bytes(ingl_constants.GEM_ACCOUNT_CONST, 'UTF-8'), bytes(mint_pubkey.public_key)], get_program_id())
        accounts.append(AccountMeta(gem_account_pubkey, False, True))




    accounts.append(sys_program_meta)
    # print(accounts)
    data = InstructionEnum.build(InstructionEnum.enum.InjectTestingData(log_level = log_level, num_nfts = len(mints)))
    transaction = Transaction()
    transaction.add(TransactionInstruction(accounts, get_program_id(), data))
    try:
        t_dets = await sign_and_send_tx(transaction, client, payer_keypair)
        await client.confirm_transaction(tx_sig = t_dets.value, commitment= "finalized", sleep_seconds = 0.4, last_valid_block_height = None)
        return f"Transaction Id: [link=https://explorer.solana.com/tx/{str(t_dets.value)+rpc_url.get_explorer_suffix()}]{str(t_dets.value)}[/link]"
    except Exception as e:
        return(f"[warning]Error: {e}[/warning]")

async def create_program_upgrade_proposal(payer_keypair: KeypairInput, buffer_address: PubkeyInput, proposal_numeration: int, code_link: String,  client: AsyncClient, log_level: int = 0) -> str:
    ingl_team_account_pubkey, _ita_bump = PublicKey.find_program_address([bytes(ingl_constants.INGL_TEAM_ACCOUNT, 'UTF-8')], get_program_id())
    proposal_account_pubkey, _proposal_account_pubkey_bump = PublicKey.find_program_address([bytes(ingl_constants.UPGRADE_PROPOSAL_KEY, 'UTF-8'), (proposal_numeration).to_bytes(4, "big")], get_program_id())
    global_gem_pubkey, _global_gem_bump = PublicKey.find_program_address([bytes(ingl_constants.GLOBAL_GEM_KEY, 'UTF-8')], get_program_id())

    
    payer_account_meta = AccountMeta(pubkey = payer_keypair.public_key, is_signer = True, is_writable = True)
    buffer_address_meta = AccountMeta(pubkey = buffer_address.public_key, is_signer= False, is_writable =True)
    global_gem_meta = AccountMeta(pubkey = global_gem_pubkey, is_signer = False, is_writable = True)
    proposal_account_meta = AccountMeta(pubkey = proposal_account_pubkey, is_signer = False, is_writable = True)
    ingl_team_account_meta = AccountMeta(pubkey = ingl_team_account_pubkey, is_signer = False, is_writable = True)
    system_program_meta = AccountMeta(pubkey = system_program.SYS_PROGRAM_ID, is_signer = False, is_writable = False)


    accounts = [
        payer_account_meta,
        ingl_team_account_meta,
        buffer_address_meta,
        proposal_account_meta,
        global_gem_meta,

        system_program_meta,
        system_program_meta,
    ]

    # print(accounts)
    instruction_data = build_instruction(InstructionEnum.enum.CreateProgramUpgradeProposal(log_level = log_level, code_link = code_link))
    transaction = Transaction()
    transaction.add(TransactionInstruction(accounts, get_program_id(), instruction_data))
    try:
        t_dets = await sign_and_send_tx(transaction, client, payer_keypair)
        await client.confirm_transaction(tx_sig = t_dets.value, commitment= "finalized", sleep_seconds = 0.4, last_valid_block_height = None)
        return f"Transaction Id: [link=https://explorer.solana.com/tx/{str(t_dets.value)+rpc_url.get_explorer_suffix()}]{str(t_dets.value)}[/link]"
    except Exception as e:
        return(f"[warning]Error: {e}[/warning]")

async def vote_program_upgrade_proposal(payer_keypair: KeypairInput, vote: Bool, upgrade_proposal_pubkey: Optional[PubkeyInput], upgrade_numeration: Optional[int], vote_account_proposal_pubkey: Optional[PubkeyInput],  vote_account_numeration: Optional[int], client: AsyncClient, log_level: int = 0) -> str:
    global_gem_pubkey, _global_gem_bump = PublicKey.find_program_address([bytes(ingl_constants.GLOBAL_GEM_KEY, 'UTF-8')], get_program_id())
    
    data = await client.get_account_info(global_gem_pubkey)
    global_gems = GlobalGems.parse(data.value.data)
    cnt = global_gems.upgrade_proposal_numeration
    proposal_account_pubkey, proposal_numeration =  parse_upgrade_proposal_id(upgrade_proposal_pubkey.public_key, upgrade_numeration, cnt)
    vote_account_pubkey, vote_account_numeration = parse_validator_proposal_id(vote_account_proposal_pubkey.public_key, vote_account_numeration, global_gems.validator_proposal_numeration)
    expected_vote_data_pubkey, _expected_vote_data_bump = PublicKey.find_program_address([bytes(ingl_constants.VOTE_DATA_ACCOUNT_KEY, 'UTF-8'), bytes(vote_account_pubkey)], get_program_id())
    
    
    payer_account_meta = AccountMeta(pubkey = payer_keypair.public_key, is_signer = True, is_writable = True) # payer is the validator ID.
    proposal_account_meta = AccountMeta(pubkey = proposal_account_pubkey, is_signer = False, is_writable = True)
    ingl_vote_data_account_meta = AccountMeta(pubkey = expected_vote_data_pubkey, is_signer = False, is_writable = False)
    vote_account_meta = AccountMeta(pubkey = vote_account_pubkey, is_signer = False, is_writable = False)


    accounts = [
        proposal_account_meta,
        vote_account_meta,
        payer_account_meta,
        ingl_vote_data_account_meta,
        

    ]

    # print(accounts)
    instruction_data = build_instruction(InstructionEnum.enum.VoteProgramUpgradeProposal(log_level = log_level, numeration = proposal_numeration, vote=vote, validator_proposal_numeration = vote_account_numeration))
    transaction = Transaction()
    transaction.add(TransactionInstruction(accounts, get_program_id(), instruction_data))
    try:
        t_dets = await sign_and_send_tx(transaction, client, payer_keypair)
        await client.confirm_transaction(tx_sig = t_dets.value, commitment= "finalized", sleep_seconds = 0.4, last_valid_block_height = None)
        return f"Transaction Id: [link=https://explorer.solana.com/tx/{str(t_dets.value)+rpc_url.get_explorer_suffix()}]{str(t_dets.value)}[/link]"
    except Exception as e:
        return(f"[warning]Error: {e}[/warning]")

async def finalize_program_upgrade_proposal(payer_keypair: KeypairInput, upgrade_proposal_pubkey: Optional[PubkeyInput], upgrade_numeration: Optional[int], client: AsyncClient, log_level: int = 0) -> str:
    ingl_team_account_pubkey, _ita_bump = PublicKey.find_program_address([bytes(ingl_constants.INGL_TEAM_ACCOUNT, 'UTF-8')], get_program_id())
    global_gem_pubkey, _global_gem_bump = PublicKey.find_program_address([bytes(ingl_constants.GLOBAL_GEM_KEY, 'UTF-8')], get_program_id())
    
    programdata_id, _bump = PublicKey.find_program_address([bytes(get_program_id())], ingl_constants.BPF_LOADER_KEY)
    pda_authority_key = PublicKey.find_program_address([b"authority", bytes(get_program_id())], get_program_id())[0]
    data = await client.get_account_info(global_gem_pubkey)
    global_gems = GlobalGems.parse(data.value.data)
    cnt = global_gems.upgrade_proposal_numeration
    proposal_account_pubkey, proposal_numeration =  parse_upgrade_proposal_id(upgrade_proposal_pubkey.public_key, upgrade_numeration, cnt)

    proposal_data = await client.get_account_info(proposal_account_pubkey)
    proposal_data = ProgramUpgradeData.parse(data.value.data)
    buffer_address = proposal_data.buffer_address
    
    payer_account_meta = AccountMeta(pubkey = payer_keypair.public_key, is_signer = True, is_writable = True) # payer is the validator ID.
    proposal_account_meta = AccountMeta(pubkey = proposal_account_pubkey, is_signer = False, is_writable = True)
    global_gem_meta = AccountMeta(pubkey = global_gem_pubkey, is_signer = False, is_writable = True)
    programdata_meta = AccountMeta(pubkey=programdata_id, is_signer=False, is_writable=True)
    upgraded_program_meta = AccountMeta(pubkey=get_program_id(), is_signer=False, is_writable=True)
    buffer_address_meta = AccountMeta(pubkey=buffer_address, is_signer=False, is_writable=True)
    spilling_address_info_meta = AccountMeta(pubkey=ingl_team_account_pubkey, is_signer=True, is_writable=True)
    sysvar_rent_account_meta = AccountMeta(pubkey = SYSVAR_RENT_PUBKEY, is_signer = False, is_writable = False)
    sysvar_clock_account_meta = AccountMeta(pubkey = SYSVAR_CLOCK_PUBKEY, is_signer = False, is_writable = False)
    authority_meta = AccountMeta(pubkey = pda_authority_key, is_signer = False, is_writable = True)
    bpf_loader_meta = AccountMeta(pubkey = ingl_constants.BPF_LOADER_KEY, is_signer = False, is_writable = True)


    accounts = [
        payer_account_meta,
        upgraded_program_meta,
        buffer_address_meta,
        authority_meta,
        spilling_address_info_meta,
        programdata_meta,
        sysvar_rent_account_meta,
        sysvar_clock_account_meta,
        proposal_account_meta,
        global_gem_meta,


        bpf_loader_meta,
    ]

    # print(accounts)
    instruction_data = build_instruction(InstructionEnum.enum.FinalizeProgramUpgradeProposal(log_level = log_level, proposal_numeration = proposal_numeration))
    transaction = Transaction()
    transaction.add(TransactionInstruction(accounts, get_program_id(), instruction_data))
    try:
        t_dets = await sign_and_send_tx(transaction, client, payer_keypair)
        await client.confirm_transaction(tx_sig = t_dets.value, commitment= "finalized", sleep_seconds = 0.4, last_valid_block_height = None)
        return f"Transaction Id: [link=https://explorer.solana.com/tx/{str(t_dets.value)+rpc_url.get_explorer_suffix()}]{str(t_dets.value)}[/link]"
    except Exception as e:
        return(f"[warning]Error: {e}[/warning]")