from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

from jigu.core.proposal import Content
from jigu.util.serdes import JiguBox
from jigu.util.validation import Schemas as S

ParamChangeSchema = S.OBJECT(subspace=S.STRING, key=S.STRING, value=S.STRING)

__all__ = ["ParameterChangeProposal"]


@dataclass
class ParameterChangeProposal(Content):

    type = "params/ParameterChangeProposal"

    __schema__ = S.OBJECT(
        type=S.STRING_WITH_PATTERN(r"^params/ParameterChangeProposal\Z"),
        value=S.OBJECT(
            title=S.STRING, description=S.STRING, changes=S.ARRAY(ParamChangeSchema),
        ),
    )

    title: str
    description: str
    changes: List[JiguBox] = field(default_factory=list)

    @classmethod
    def from_data(cls, data: dict) -> ParameterChangeProposal:
        data = data["value"]
        return cls(
            title=data["title"],
            description=data["description"],
            changes=[JiguBox(change) for change in data["changes"]],
        )
