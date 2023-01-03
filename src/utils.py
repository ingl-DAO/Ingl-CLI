from .state import *

def parse_vote(vote: str) -> bool:
    vote = vote.lower()
    if vote == "approve" or vote == "a" or vote == "yes" or vote == "y":
        return True
    elif vote == "dissaprove" or vote == 'd' or vote == "no" or vote == "n":
        return False
    else:
        raise ValueError("Vote can only be [a]pprove, [d]issaprove, [y]es or [n]o")

def parse_proposal(proposal: str) -> Tuple[Optional[PubkeyInput], Optional[int]]:
    try:
        num = int(proposal)
        return None, num
    except Exception as e:
        return parse_pubkey_input(proposal), None