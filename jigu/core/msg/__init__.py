from __future__ import annotations

import abc
from typing import Any, Dict

from jigu.util.serdes import JsonDeserializable, JsonSerializable
from jigu.util.validation import Schemas as S

# __all__ exports all messages


class StdMsg(JsonSerializable, JsonDeserializable, metaclass=abc.ABCMeta):

    __schema__ = S.OBJECT(type=S.STRING, value={"type": "object"})

    @property
    @abc.abstractmethod
    def type(self):
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def action(self):
        raise NotImplementedError

    def msg_value(self) -> Dict[str, Any]:
        return dict(self.__dict__)

    def to_data(self) -> Dict[str, Any]:
        return {"type": self.type, "value": self.msg_value()}


from .bank import MsgSend, MsgMultiSend  # isort:skip
from .distribution import (  # isort:skip
    MsgModifyWithdrawAddress,
    MsgWithdrawDelegationReward,
    MsgWithdrawValidatorCommission,
)
from .gov import MsgSubmitProposal, MsgVote, MsgDeposit  # isort:skip
from .market import MsgSwap  # isort:skip
from .staking import (  # isort:skip
    MsgBeginRedelegate,
    MsgDelegate,
    MsgUndelegate,
    MsgEditValidator,
    MsgCreateValidator,
)
from .slashing import MsgUnjail  # isort:skip
from .oracle import (  # isort:skip
    MsgDelegateFeedConsent,
    MsgExchangeRatePrevote,
    MsgExchangeRateVote,
)

MSG_TYPES = {
    "bank/MsgSend": MsgSend,
    "bank/MsgMultiSend": MsgMultiSend,
    "distribution/MsgModifyWithdrawAddress": MsgModifyWithdrawAddress,
    "distribution/MsgWithdrawDelegationReward": MsgWithdrawDelegationReward,
    "distribution/MsgWithdrawValidatorCommission": MsgWithdrawValidatorCommission,
    "oracle/MsgExchangeRatePrevote": MsgExchangeRatePrevote,
    "oracle/MsgExchangeRateVote": MsgExchangeRateVote,
    "oracle/MsgDelegateFeedConsent": MsgDelegateFeedConsent,
    "gov/MsgSubmitProposal": MsgSubmitProposal,
    "gov/MsgDeposit": MsgDeposit,
    "gov/MsgVote": MsgVote,
    "market/MsgSwap": MsgSwap,
    "staking/MsgBeginRedelegate": MsgBeginRedelegate,
    "staking/MsgDelegate": MsgDelegate,
    "staking/MsgUndelegate": MsgUndelegate,
    "staking/MsgEditValidator": MsgEditValidator,
    "staking/MsgCreateValidator": MsgCreateValidator,
    "cosmos/MsgUnjail": MsgUnjail,
}
