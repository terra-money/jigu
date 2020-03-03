from typing import Union

from jigu.client.lcd.api import ApiResponse, BaseApi, project
from jigu.core import Coins

__all__ = ["SupplyApi"]


class SupplyApi(BaseApi):
    def total(self) -> Union[ApiResponse, Coins]:
        res = self._api_get("/supply/total")
        return project(res, Coins.deserialize(res))
