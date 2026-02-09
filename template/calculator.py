"""
Performs deterministic COREP metric calculations.
LLM is restricted to extraction only.
"""


def calculate_corep_metrics(extracted_output):
    at1 = extracted_output.at1_capital or 0
    tier2 = extracted_output.tier2_capital or 0
    total_own_funds = (
        extracted_output.cet1_capital
        + at1
        + tier2
    )

    rwa = extracted_output.rwa

    if rwa > 0:
        cet1_ratio = round((extracted_output.cet1_capital / rwa) * 100, 2)
        total_capital_ratio = round((total_own_funds / rwa) * 100, 2)
    else:
        cet1_ratio = 0
        total_capital_ratio = 0

    return {
        "total_own_funds": total_own_funds,
        "cet1_ratio": cet1_ratio,
        "total_capital_ratio": total_capital_ratio
    }

