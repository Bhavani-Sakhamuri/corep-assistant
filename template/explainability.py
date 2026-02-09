"""
Explainability module for COREP outputs.
Provides audit-friendly trace for every calculated metric.
"""


def generate_explainability(extracted, calculated, final_output):

    explanations = {}

    # -----------------------------
    # Total Own Funds Explanation
    # -----------------------------
    explanations["total_own_funds"] = {
        "formula": "CET1 + AT1 + Tier2",
        "values_used": {
            "CET1": extracted.cet1_capital,
            "AT1": extracted.at1_capital,
            "Tier2": extracted.tier2_capital,
        },
        "result": final_output.total_own_funds,
        "regulation_reference": "CRR Article 72"
    }

    # -----------------------------
    # CET1 Ratio Explanation
    # -----------------------------
    explanations["cet1_ratio"] = {
        "formula": "(CET1 / RWA) * 100",
        "values_used": {
            "CET1": extracted.cet1_capital,
            "RWA": extracted.rwa
        },
        "result": final_output.cet1_ratio,
        "regulation_reference": "CRR Article 92(1)(a)"
    }

    # -----------------------------
    # Total Capital Ratio Explanation
    # -----------------------------
    explanations["total_capital_ratio"] = {
        "formula": "(Total Own Funds / RWA) * 100",
        "values_used": {
            "Total Own Funds": calculated["total_own_funds"],
            "RWA": extracted.rwa
        },
        "result": final_output.total_capital_ratio,
        "regulation_reference": "CRR Article 92(1)(c)"
    }

    return explanations
