from pydantic import BaseModel
from typing import List
from typing import Optional


class CorepOwnFunds(BaseModel):
    cet1_capital: float
    at1_capital: Optional[float] = None
    tier2_capital: Optional[float] = None
    rwa: float
    audit_references: List[str]

class CorepFinalOutput(CorepOwnFunds):
    total_own_funds: float
    cet1_ratio: float
    total_capital_ratio: float



