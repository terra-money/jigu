from typing import Dict, List, Union

from jigu.client.lcd.api import ApiResponse, BaseApi, project
from jigu.core import AccAddress, Coin, Coins, Dec, Proposal
from jigu.core.denoms import uLuna
from jigu.util.serdes import JiguBox

__all__ = ["GovApi"]


class GovApi(BaseApi):
    """Interface for interacting with the Governance API."""

    def proposals(self) -> Union[ApiResponse, List[Proposal]]:
        """Get all proposals."""
        res = self._api_get("/gov/proposals")
        print(res)
        return project(res, [Proposal.deserialize(p) for p in res])

    def proposal(self, proposal_id: int) -> Union[ApiResponse, Proposal]:
        """Get a single proposal by ID."""
        res = self._api_get(f"/gov/proposals/{proposal_id}")
        return project(res, Proposal.deserialize(res))

    def proposer_for(self, proposal_id: int) -> Union[ApiResponse, AccAddress]:
        """Gets a proposal's proposer."""
        res = self._api_get(f"/gov/proposals/{proposal_id}/proposer")
        return project(res, res["proposer"])

    def deposits_for(self, proposal_id: int) -> Union[ApiResponse, Dict[str, Coins]]:
        """Get the proposal's deposits."""
        res = self._api_get(f"/gov/proposals/{proposal_id}/deposits")
        ds = res or []
        deposits = JiguBox({})
        for d in ds:
            deposits[d["depositor"]] = Coins.deserialize(d["amount"])
        return project(res, deposits)

    def votes_for(self, proposal_id: str) -> Union[ApiResponse, dict]:
        res = self._api_get(f"/gov/proposals/{proposal_id}/votes")
        vs = res or []
        votes = JiguBox({})
        for v in vs:
            votes[v["voter"]] = v["option"]
        return project(res, votes)

    def tally_for(self, proposal_id: str) -> Union[ApiResponse, Dict[str, Coin]]:
        res = self._api_get(f"/gov/proposals/{proposal_id}/tally")
        denoms = res or []
        tally = JiguBox({})
        for denom in denoms:
            tally[denom] = Coin(uLuna, int(res[denom]))
        return project(res, JiguBox(tally))

    def params(self, key: str = None):
        """Puts all the parameters together."""
        deposit = self.deposit_params()
        voting = self.voting_params()
        tally = self.tally_params()
        p = JiguBox(
            {"deposit_params": deposit, "voting_params": voting, "tally_params": tally}
        )

        return project(  # use response information of last entry, even if there is a delay
            tally, p[key] if key else p
        )

    def deposit_params(
        self, key: str = None
    ) -> Union[ApiResponse, Dict[str, Union[int, Coins]]]:
        res = self._api_get(f"/gov/parameters/deposit")
        p = JiguBox(res)
        p["min_deposit"] = Coins.deserialize(p["min_deposit"])
        p["max_deposit_period"] = int(p["max_deposit_period"])
        return project(res, p[key] if key else p)

    def voting_params(self, key: str = None) -> Union[ApiResponse, Dict[str, int]]:
        res = self._api_get(f"/gov/parameters/voting")
        p = JiguBox(res, box_recast={"voting_period": int})
        return project(res, p[key] if key else p)

    def tally_params(self, key: str = None) -> Union[ApiResponse, Dict[str, Dec]]:
        res = self._api_get(f"/gov/parameters/tallying")
        p = JiguBox(res, box_recast={"quorum": Dec, "threshold": Dec, "veto": Dec})
        return project(res, p[key] if key else p)
