from typing import Optional
from borsh_construct import *
from solders.pubkey import Pubkey
from solders.instruction import Instruction, AccountMeta
from .state import get_market_program_id


InitStruct = CStruct(
    "log_level" / U8,
    "init_commission" / U8,
    "max_primary_stake" / U64,
    "nft_holders_share" / U8,
    "initial_redemption_fee" / U8,
    "is_validator_id_switchable" / Bool,
    "unit_backing" / U64,
    "redemption_fee_duration" / U32,
    "proposal_quorum" / U8,
    "creator_royalties" / U16,
    "governance_expiration_time" / U32,
    "rarities" / Vec(U16),
    "rarity_names" / Vec(String),
    "twitter_handle" / String,
    "discord_invite" / String,
    "validator_name" / String,
    "collection_uri" / String,
    "website" / String,
    "default_uri" / String,
)

InstructionEnum = Enum(
    "MintNft"
    / CStruct("switchboard_state_bump" / U8, "permission_bump" / U8, "log_level" / U8),
    "ImprintRarity" / CStruct("log_level" / U8),
    "Init" / InitStruct,
    "Redeem" / CStruct("log_level" / U8),
    "NFTWithdraw" / CStruct("cnt" / U8, "log_level" / U8),
    "ProcessRewards" / CStruct("log_level" / U8),
    "InitRebalance" / CStruct("log_level" / U8),
    "FinalizeRebalance" / CStruct("log_level" / U8),
    "UploadUris" / CStruct("uris" / Vec(String), "rarity" / U8, "log_level" / U8),
    "ResetUris" / CStruct("log_level" / U8),
    "UnDelegateNFT" / CStruct("log_level" / U8),
    "DelegateNFT" / CStruct("log_level" / U8),
    "CreateVoteAccount" / CStruct("log_level" / U8),
    "InitGovernance",
    "VoteGovernance"
    / CStruct("numeration" / U32, "vote" / Bool, "cnt" / U8, "log_level" / U8),
    "FinalizeGovernance" / CStruct("numeration" / U32, "log_level" / U8),
    "ExecuteGovernance" / CStruct("numeration" / U32, "log_level" / U8),
    "InjectTestingData" / CStruct("num_mints" / U8, "log_level" / U8),
    "FractionalizeExisting" / InitStruct,
    enum_name="InstructionEnum",
)

GovernanceType = Enum(
    "ConfigAccount",
    "ProgramUpgrade" / CStruct("buffer_account" / U8[32], "code_link" / String),
    "VoteAccountGovernance",
    enum_name="GovernanceType",
)

ConfigAccountType = Enum(
    "MaxPrimaryStake" / CStruct("value" / U64),
    "NftHolderShare" / CStruct("value" / U8),
    "InitialRedemptionFee" / CStruct("value" / U8),
    "RedemptionFeeDuration" / CStruct("value" / U32),
    "ValidatorName" / CStruct("value" / String),
    "TwitterHandle" / CStruct("value" / String),
    "DiscordInvite" / CStruct("value" / String),
    enum_name="ConfigAccountType",
)

VoteAccountGovernance = Enum(
    "ValidatorId" / CStruct("value" / U8[32]),
    "Commission" / CStruct("value" / U8),
    enum_name="VoteAccountGovernance",
)

RegistryEnum = Enum(
    "InitConfig",
    "AddProgram",
    "RemovePrograms" / CStruct("program_count" / U8),
    "AddMarketplaceProgram",
    "Reset",
    "Blank",
    enum_name="RegistryEnum",
)


SecondaryItem = CStruct(
    "cost" / U64,
    "name" / String,
    "description" / String,
)


MediationShares = CStruct(
    "buyer" / U8,
    "seller" / U8,
    "team" / U8,
)

MarketInstructionEnum = Enum(
    "List"
    / CStruct(
        "log_level" / U8,
        "authorized_withdrawer_cost" / U64,
        "mediatable_date" / U32,
        "secondary_items" / Vec(SecondaryItem),
        "description" / String,
        "validator_name" / String,
        "validator_logo_url" / String,
    ),
    "Delist"
    / CStruct(
        "log_level" / U8,
    ),
    "Buy"
    / CStruct(
        "log_level" / U8,
    ),
    "WithdrawRewards"
    / CStruct(
        "log_level" / U8,
    ),
    "RequestMediation"
    / CStruct(
        "log_level" / U8,
    ),
    "Mediate"
    / CStruct(
        "log_level" / U8,
        "mediation_shares" / MediationShares,
    ),
    "ValidateSecondaryItemsTransfers"
    / CStruct(
        "log_level" / U8,
        "item_index" / U32,
    ),
    enum_name="InstructionEnum",
)


def build_market_instruction(
    instruction: MarketInstructionEnum.enum, accounts: list[AccountMeta]
) -> Instruction:
    return Instruction(
        program_id=get_market_program_id(),
        data=MarketInstructionEnum.build(instruction),
        accounts=accounts,
    )


Purchase = CStruct(
    "buyer" / U8[32],
    "date" / U32,
    "date_finalized" / Option(U32),
)

StoredSecondaryItem = CStruct(
    "cost" / U64,
    "name" / String,
    "description" / String,
    "date_validated" / Option(U32),
)

Storage = CStruct(
    "validation_phrase" / U32,
    "authorized_withdrawer" / U8[32],
    "vote_account" / U8[32],
    "authorized_withdrawer_cost" / U64,
    "mediatable_date" / U32,
    "purchase" / Option(Purchase),
    "request_mediation_date" / Option(U32),
    "mediation_date" / Option(U32),
    "mediation_shares" / Option(MediationShares),
    "secondary_items" / Vec(StoredSecondaryItem),
    "description" / String,
    "validator_name" / String,
    "validator_logo_url" / String,
)


def build_governance_type(
    governance_type: GovernanceType.enum,
    config_account_type: Optional[ConfigAccountType.enum] = None,
    vote_account_governance: Optional[VoteAccountGovernance.enum] = None,
):
    if governance_type == GovernanceType.enum.ConfigAccount():
        return GovernanceType.build(governance_type) + ConfigAccountType.build(
            config_account_type
        )
    elif governance_type == GovernanceType.enum.VoteAccountGovernance():
        return GovernanceType.build(governance_type) + VoteAccountGovernance.build(
            vote_account_governance
        )
    else:
        return GovernanceType.build(governance_type)


def build_instruction(
    instruction: InstructionEnum.enum,
    title: Optional[str] = None,
    description: Optional[str] = None,
    governance_type: Optional[GovernanceType.enum] = None,
    config_account_type: Optional[ConfigAccountType.enum] = None,
    vote_account_governance: Optional[VoteAccountGovernance.enum] = None,
    log_level: int = 0,
):
    if instruction == InstructionEnum.enum.InitGovernance():
        return (
            InstructionEnum.build(instruction)
            + build_governance_type(
                governance_type,
                config_account_type=config_account_type,
                vote_account_governance=vote_account_governance,
            )
            + String.build(title)
            + String.build(description)
            + (log_level).to_bytes(1, "big")
        )
    else:
        return InstructionEnum.build(instruction)


class ComputeBudgetInstruction:
    def __init__(self):
        self.InstructionEnum = Enum(
            "RequestUnitsDeprecated" / CStruct("units" / U32, "additional_fee" / U32),
            "RequestHeapFrame" / CStruct("value" / U32),
            "SetComputeUnitLimit" / CStruct("value" / U32),
            "SetComputeUnitPrice" / CStruct("value" / U64),
            enum_name="InstructionEnum",
        )
        self.program_id = Pubkey.from_string(
            "ComputeBudget111111111111111111111111111111"
        )

    def request_heap_frame(self, total_bytes, payer) -> Instruction:
        instruction_bytes = self.InstructionEnum.build(
            self.InstructionEnum.enum.RequestHeapFrame(total_bytes)
        )
        return Instruction(
            accounts=[AccountMeta(payer, True, False)],
            program_id=self.program_id,
            data=instruction_bytes,
        )

    def set_compute_unit_limit(self, units, payer) -> Instruction:
        instruction_bytes = self.InstructionEnum.build(
            self.InstructionEnum.enum.SetComputeUnitLimit(units)
        )
        return Instruction(
            accounts=[AccountMeta(payer, True, False)],
            program_id=self.program_id,
            data=instruction_bytes,
        )

    def set_compute_unit_price(self, micro_lamports, payer) -> Instruction:
        instruction_bytes = self.InstructionEnum.build(
            self.InstructionEnum.enum.SetComputeUnitPrice(micro_lamports)
        )
        return Instruction(
            accounts=[AccountMeta(payer, True, False)],
            program_id=self.program_id,
            data=instruction_bytes,
        )
