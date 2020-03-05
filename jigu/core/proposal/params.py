from __future__ import annotations

import re
from dataclasses import dataclass, field

from jigu.core.proposal import Content
from jigu.core.sdk import Coin, Dec
from jigu.error import InvalidParamChange
from jigu.util.serdes import JiguBox, JsonDeserializable, JsonSerializable
from jigu.util.validation import Schemas as S

__all__ = ["ParameterChangeProposal"]

symbol = r"[a-zA-Z_][a-zA-Z_0-9]*"
ParamKeyPattern = re.compile(r"^(" + symbol + r")\.(" + symbol + r")$")

ParamChangeSchema = S.ONE(
    S.OBJECT(subspace=S.STRING, key=S.STRING, value=S.STRING),
    S.OBJECT(subspace=S.STRING, key=S.STRING, subkey=S.STRING, value=S.STRING),
)


class ParamChanges(JsonSerializable, JsonDeserializable):

    __schema__ = S.ARRAY(ParamChangeSchema)

    def __init__(self, changes: dict):
        self.changes = changes
        for k, v in changes.items():
            m = ParamKeyPattern.match(k)
            if not m:
                raise InvalidParamChange(
                    f"Parameter change subspace and key could not be parsed: {k}"
                )
            if isinstance(v, dict):
                for sk, sv in v.items():
                    sm = re.match(f"^{symbol}$", sk)
                    if not sm:
                        raise InvalidParamChange(
                            f"Parameter change subkey is invalid - {k}: '{sk}'"
                        )

    def __repr__(self) -> str:
        return f"<ParamChanges {self.changes!r}>"

    def to_data(self) -> list:
        param_changes = []
        for k, v in self.changes.items():
            m = ParamKeyPattern.match(k)
            subspace = m.group(1)
            key = m.group(2)
            if isinstance(v, dict):
                for sk, sv in v.items():
                    param_changes.append(
                        {
                            "subspace": subspace,
                            "key": key,
                            "subkey": sk,
                            "value": str(sv),
                        }
                    )
            else:
                param_changes.append(
                    {"subspace": subspace, "key": key, "value": str(v),}
                )
        return param_changes

    @classmethod
    def from_data(cls, data: list) -> ParamChanges:
        changes = dict()
        for p in data:
            key = p["subspace"] + "." + p["key"]
            if "subkey" in p:
                if key not in changes:
                    changes[key] = dict()
                changes[key][p["subkey"]] = p["value"]
            else:
                changes[key] = p["value"]
        return cls(changes)


@dataclass
class ParameterChangeProposal(Content):

    type = "params/ParameterChangeProposal"

    __schema__ = S.OBJECT(
        type=S.STRING_WITH_PATTERN(r"^params/ParameterChangeProposal\Z"),
        value=S.OBJECT(
            title=S.STRING, description=S.STRING, changes=ParamChanges.__schema__,
        ),
    )

    title: str
    description: str
    changes: ParamChanges = field(default_factory=ParamChanges)

    def __post_init__(self):
        # validation checks for key
        if isinstance(self.changes, dict):
            self.changes = ParamChanges(self.changes)

    @classmethod
    def from_data(cls, data: dict) -> ParameterChangeProposal:
        data = data["value"]
        return cls(
            title=data["title"],
            description=data["description"],
            changes=ParamChanges.from_data(data["changes"]),
        )

