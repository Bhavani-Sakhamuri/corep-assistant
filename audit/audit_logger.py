import json
from datetime import datetime
from pathlib import Path
import os


AUDIT_LOG_DIR = Path("audit_logs")
AUDIT_LOG_DIR.mkdir(exist_ok=True)


def log_audit_trail(
    query,
    final_output,
    explanations,
    evidence_map,
    risk_flags,
    compliance_results,
    retrieved_docs,
    version_info,
    review_status
):

    timestamp = datetime.utcnow().isoformat()

    audit_record = {
        "timestamp": timestamp,
        "query": query,
        "corep_output": final_output.model_dump(),
        "explanations": explanations,
        "evidence_map": evidence_map,
        "risk_flags": risk_flags,
        "compliance_results": compliance_results,
        "retrieved_docs": [doc.metadata for doc in retrieved_docs],
        "audit_metadata": version_info,
        "audit_decision": review_status
    }

    filename = AUDIT_LOG_DIR / f"audit_{timestamp.replace(':','-')}.json"

    with open(filename, "w") as f:
        json.dump(audit_record, f, indent=2)

    return str(filename)



def save_audit_log(output):

    os.makedirs("audit_logs", exist_ok=True)

    timestamp = datetime.now().isoformat().replace(":", "-")

    file_path = f"audit_logs/audit_{timestamp}.json"

    with open(file_path, "w") as f:
        json.dump(output, f, indent=4)

    print(f"Audit log saved at: {file_path}")

