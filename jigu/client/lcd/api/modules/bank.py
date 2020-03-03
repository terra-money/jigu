from typing import Union

from jigu.client.lcd.api import ApiResponse, BaseApi, project
from jigu.core import AccAddress, Coins
from jigu.util.validation import validate_acc_address

__all__ = ["BankApi"]


class BankApi(BaseApi):
    def balance_for(self, address: AccAddress) -> Union[ApiResponse, Coins]:
        """Get's the balance of an account by its address."""
        address = validate_acc_address(address)
        res = self._api_get(f"/bank/balances/{address}")
        return project(res, Coins.deserialize(res))
