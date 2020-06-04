from __future__ import annotations

from dataclasses import dataclass

from jigu.core import Coins, AccAddress
from jigu.core.msg import StdMsg
from jigu.util import b64_to_dict, dict_to_b64
from jigu.util.validation import Schemas as S


@dataclass
class MsgStoreCode(StdMsg):

    type = "wasm/StoreCode"
    action = "storecode"

    __schema__ = S.OBJECT(
        type=S.STRING_WITH_PATTERN(r"^wasm/MsgStoreCode\Z"),
        value=S.OBJECT(sender=S.ACC_ADDRESS, wasm_byte_code=S.STRING),
    )

    sender: AccAddress
    wasm_byte_code: str

    @classmethod
    def from_data(cls, data: dict) -> MsgStoreCode:
        data = data["value"]
        return cls(sender=data["sender"], wasm_byte_code=data["wasm_byte_code"])


@dataclass
class MsgInstantiateContract(StdMsg):

    type = "wasm/InstantiateContract"
    action = "instantiatecontract"

    __schema__ = S.OBJECT(
        type=S.STRING_WITH_PATTERN(r"^wasm/MsgInstantiateContract\Z"),
        value=S.OBJECT(
            sender=S.ACC_ADDRESS,
            code_id=S.STRING_INTEGER,
            init_msg=S.STRING,  # b64 string
            init_coins=Coins.__schema__,
        ),
    )

    sender: AccAddress
    code_id: int
    init_msg: dict
    init_coins: Coins

    def msg_value(self) -> dict:
        return {
            "sender": self.sender,
            "code_id": str(self.code_id),
            "init_msg": dict_to_b64(self.init_msg),
            "init_coins": self.init_coins.to_data(),
        }

    @classmethod
    def from_data(cls, data: dict) -> MsgStoreCode:
        data = data["value"]
        return cls(
            sender=data["sender"],
            code_id=int(data["code_id"]),
            init_msg=b64_to_dict(data["init_msg"]),
            init_coins=Coins.from_data(data["init_coins"]),
        )


@dataclass
class MsgExecuteContract(StdMsg):

    type = "wasm/ExecuteContract"
    action = "executecontract"

    __schema__ = S.OBJECT(
        type=S.STRING_WITH_PATTERN(r"^wasm/MsgExecuteContract\Z"),
        value=S.OBJECT(
            sender=S.ACC_ADDRESS,
            contract=S.ACC_ADDRESS,
            msg=S.STRING,  # b64 string
            coins=Coins.__schema__,
        ),
    )

    sender: AccAddress
    contract: AccAddress
    msg: dict
    coins: Coins

    def msg_value(self) -> dict:
        return {
            "sender": self.sender,
            "contract": self.contract,
            "msg": dict_to_b64(self.msg),
            "coins": self.coins.to_data(),
        }

    @classmethod
    def from_data(cls, data: dict) -> MsgExecuteContract:
        data = data["value"]
        return cls(
            sender=data["sender"],
            contract=data["contract"],
            msg=b64_to_dict(data["msg"]),
            coins=Coins.fromData(data["coins"]),
        )
