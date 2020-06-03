from typing import Union, Any

import json

from jigu.client.lcd.api import ApiResponse, BaseApi, project
from jigu.core import AccAddress
from jigu.util.serdes import JiguBox

__all__ = ["WasmApi"]


class WasmApi(BaseApi):
    def code_info(self, code_id: int) -> Union[ApiResponse, JiguBox]:
        res = self._api_get(f"/wasm/code/{code_id}")
        return project(res, JiguBox(res))

    def contract_info(self, contract: AccAddress) -> Union[ApiResponse, JiguBox]:
        res = self._api_get(f"/wasm/contract/{contract}")
        return project(res, JiguBox(res))

    def contract_query(
        self, contract: AccAddress, query: dict
    ) -> Union[ApiResponse, Any]:
        res = self._api_get(
            f"/wasm/contract/{contract}/store", params={"query_msg": json.dumps(query)}
        )
        return res
