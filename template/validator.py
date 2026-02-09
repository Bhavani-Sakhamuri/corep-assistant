def validate_corep(output):

    errors = []

    # ---------- Validate Total Own Funds ----------
    expected_total = (
        output.cet1_capital
        + output.at1_capital
        + output.tier2_capital
    )

    if abs(output.total_own_funds - expected_total) > 0.01:
        errors.append("Total own funds mismatch")

    # ---------- Validate Total Capital Ratio ----------
    if output.rwa > 0:
        expected_total_ratio = round(
            (expected_total / output.rwa) * 100, 2
        )
    else:
        expected_total_ratio = 0

    if abs(output.total_capital_ratio - expected_total_ratio) > 0.01:
        errors.append("Total capital ratio mismatch")

    # ---------- Regulatory Threshold Checks ----------
    if output.total_capital_ratio < 8:
        errors.append("Capital ratio below regulatory minimum (8%)")

    if output.rwa <= 0:
        errors.append("Invalid RWA value")

    if output.cet1_ratio < 4.5:
        errors.append("CET1 ratio below CRR minimum (4.5%)")

    return output, errors
