from borsh_construct import *
from solana.publickey import PublicKey
from solana.transaction import TransactionInstruction, AccountMeta
from .state import ClassEnum


InstructionEnum = Enum(
    "MintNft",
    "InglInit" / CStruct("log_level"/U8),
    "Redeem" / CStruct("log_level"/U8),
    "ImprintRarity" / CStruct("log_level"/U8),
    "AllocateNFT" / CStruct("log_level"/U8),
    "DeAllocateNFT" / CStruct("log_level"/U8),
    "CreateVoteAccount" / CStruct("log_level"/U8),
    "ChangeVoteAccountsValidatorIdentity" / CStruct("log_level"/U8),
    "DelegateNFT" / CStruct("log_level"/U8),
    "UnDelegateNFT" / CStruct("log_level"/U8),
    "InitRarityImprint" / CStruct("log_level"/U8),
    "RegisterValidatorId" / CStruct("log_level"/U8),
    "CreateValidatorSelectionProposal" / CStruct("log_level"/U8),
    "VoteValidatorProposal" / CStruct("num_nfts" /U8, "validator_index"/U32, "log_level"/U8),
    "FinalizeProposal" / CStruct("log_level"/U8),
    "ValidatorWithdraw" / CStruct("log_level"/U8),
    "NFTWithdraw" / CStruct("cnt" / U32, "log_level"/U8),
    "ProcessRewards" / CStruct("log_level"/U8),
    "CloseProposal" / CStruct("log_level"/U8),
    "InitRebalance" / CStruct("log_level"/U8),
    "FinalizeRebalance" / CStruct("log_level"/U8),
    "InjectTestingData" / CStruct("num_nfts" / U32, "log_level"/U8),
    "CreateProgramUpgradeProposal" / CStruct("code_link" / String, "log_level"/U8),
    "VoteProgramUpgradeProposal" / CStruct("numeration"/ U32, "vote"/ Bool, "validator_proposal_numeration"/ U32, "log_level"/U8),
    "FinalizeProgramUpgradeProposal" / CStruct("proposal_numeration" / U32, "log_level"/U8),
    
    enum_name = "InstructionEnum",
)

def build_instruction(instruction: InstructionEnum.enum, mint_class: ClassEnum = None, log_level: int = None):
    if instruction == InstructionEnum.enum.MintNft():
        return InstructionEnum.build(instruction) +  ClassEnum.build(mint_class) + (log_level).to_bytes(1, "big")
    else:
        return InstructionEnum.build(instruction)


class ComputeBudgetInstruction:
    def __init__(self):
        self.InstructionEnum = Enum(
            "RequestUnitsDeprecated" / CStruct("units" / U32, "additional_fee"/U32),
            "RequestHeapFrame"/ CStruct("value" / U32),
            "SetComputeUnitLimit" / CStruct("value" / U32),
            "SetComputeUnitPrice" / CStruct("value" / U64),

            enum_name = 'InstructionEnum',
        )
        self.program_id = PublicKey("ComputeBudget111111111111111111111111111111")

    def request_heap_frame(self, total_bytes, payer) -> TransactionInstruction:
        instruction_bytes = self.InstructionEnum.build(self.InstructionEnum.enum.RequestHeapFrame(total_bytes))
        return TransactionInstruction(keys = [AccountMeta(payer, True, False)], program_id=self.program_id, data=instruction_bytes)

    def set_compute_unit_limit(self, units, payer) -> TransactionInstruction:
        instruction_bytes = self.InstructionEnum.build(self.InstructionEnum.enum.SetComputeUnitLimit(units))
        return TransactionInstruction(keys = [AccountMeta(payer, True, False)], program_id=self.program_id, data=instruction_bytes)

    def set_compute_unit_price(self, micro_lamports, payer) -> TransactionInstruction:
        instruction_bytes = self.InstructionEnum.build(self.InstructionEnum.enum.SetComputeUnitPrice(micro_lamports))
        return TransactionInstruction(keys = [AccountMeta(payer, True, False)], program_id=self.program_id, data=instruction_bytes)
