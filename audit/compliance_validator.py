from config.config_loader import load_risk_config
config = load_risk_config()

min_cet1 = config["compliance_thresholds"]["min_cet1_ratio"]
min_total = config["compliance_thresholds"]["min_total_capital_ratio"]



def compliance_validator(corep_output, risk_flags):
    validation_results = []

    if corep_output.cet1_ratio < min_cet1:
        validation_results.append({
            "metric": "CET1_RATIO",
            "status": "BREACH",
            "message": "CET1 ratio below regulatory minimum (4.5%)"
        })
    else:
        validation_results.append({
            "metric": "CET1_RATIO",
            "status": "PASS",
            "value": corep_output.cet1_ratio
        })

    if corep_output.total_capital_ratio < min_total:
        validation_results.append({
            "metric": "TOTAL_CAPITAL_RATIO",
            "status": "BREACH",
            "message": "Total capital ratio below regulatory minimum (8%)"
        })
    else:
        validation_results.append({
            "metric": "TOTAL_CAPITAL_RATIO",
            "status": "PASS",
            "value": corep_output.total_capital_ratio
        })

    manual_review_required = any(
        flag["severity"] == "CRITICAL" for flag in risk_flags
    )

    compliance_status = "COMPLIANT"

    if validation_results:
        compliance_status = "BREACH"

    if manual_review_required:
        compliance_status = "MANUAL_REVIEW_REQUIRED"

    return {
        "status": compliance_status,
        "validation_results": validation_results
    }
