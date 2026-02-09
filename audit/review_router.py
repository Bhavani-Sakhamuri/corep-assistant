def route_for_review(risk_flags, compliance_result):

    # Default status
    review_status = "AUTO_APPROVED"

    if risk_flags:
        severities = [flag["severity"] for flag in risk_flags]

        if "CRITICAL" in severities:
            review_status = "MANUAL_REVIEW_REQUIRED"
        elif "WARNING" in severities:
            review_status = "SUPERVISOR_REVIEW_REQUIRED"

    if compliance_result["status"] != "PASS":
        review_status = "MANUAL_REVIEW_REQUIRED"

    return review_status
