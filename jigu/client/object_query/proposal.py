from __future__ import annotations

import jigu.client
import jigu.client.object_query
from jigu.core import AccAddress, Proposal

__all__ = ["ProposalQuery"]


class ProposalQuery(object):
    def __init__(self, terra: jigu.client.terra.Terra, proposal_id: int):
        self.terra = terra
        self.proposal_id = proposal_id

    def __repr__(self):
        return f"ProposalQuery({self.proposal_id!r}) -> {self.terra}"

    def info(self) -> Proposal:
        return self.terra.gov.proposal(self.proposal_id)

    def proposer(self) -> AccAddress:
        return self.terra.gov.proposer_for(self.proposal_id)

    def deposits(self):
        return self.terra.gov.deposits_for(self.proposal_id)

    def votes(self):
        return self.terra.gov.votes_for(self.proposal_id)

    def tally(self):
        return self.terra.gov.tally_for(self.proposal_id)
