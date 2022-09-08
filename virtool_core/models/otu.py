from typing import List, Union, Optional

from pydantic import root_validator, Field

from virtool_core.models.basemodel import BaseModel
from virtool_core.models.enums import Molecule
from virtool_core.models.history import HistoryNested
from virtool_core.models.reference import ReferenceNested


class OTUMinimal(BaseModel):
    abbreviation: str
    id: str
    name: str
    reference: ReferenceNested
    verified: bool
    version: int


class OTURemote(BaseModel):
    id: str


class OTUSequence(BaseModel):
    accession: str
    definition: str
    host: str
    id: str
    reference: ReferenceNested
    remote: Optional[OTURemote]
    segment: Optional[str]
    sequence: str


class OTUIsolate(BaseModel):
    default: bool
    id: str
    sequences: List[OTUSequence]
    source_name: str
    source_type: str


class OTUSegment(BaseModel):
    molecule: Optional[Molecule]
    name: str
    required: bool

    @root_validator(pre=True)
    def make_molecule_nullable(cls, values):
        """
        Convert unset molecule fields from empty strings to ``None``.

        """
        if values["molecule"] == "":
            values["molecule"] = None

        return values


class OTU(OTUMinimal):
    isolates: List[OTUIsolate]
    issues: Optional[Union[dict, bool]]
    last_indexed_version: Optional[int]
    most_recent_change: HistoryNested
    otu_schema: List[OTUSegment] = Field(alias="schema")
    remote: Optional[OTURemote]
