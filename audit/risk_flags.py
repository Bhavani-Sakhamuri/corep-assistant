from config.config_loader import load_risk_config

config = load_risk_config()

LOW_THRESHOLD = config["confidence_thresholds"]["low"]
MED_THRESHOLD = config["confidence_thresholds"]["medium"]


CONFIDENCE_THRESHOLDS = {
    "warning": 0.5,
    "critical": 0.3
}


def generate_risk_flags(evidence_map):

    flags = []

    for field, evidence in evidence_map.items():

        confidence = evidence.get("confidence", 0)

        if confidence < LOW_THRESHOLD:
            flags.append({
                "field": field,
                "severity": "CRITICAL",
                "message": f"Very low confidence for {field}. Manual verification required."
            })

        elif confidence < MED_THRESHOLD:
            flags.append({
                "field": field,
                "severity": "WARNING",
                "message": f"Low confidence for {field}. Review recommended."
            })

    return flags
