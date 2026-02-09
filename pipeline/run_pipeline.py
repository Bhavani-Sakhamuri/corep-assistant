from llm.generator import generate_corep_output
from template.validator import validate_corep
from audit.review_router import route_for_review
from reporting.corep_template_mapper import map_to_corep_template



def run_corep_pipeline(query, docs):

    (
        result,
        explanations,
        evidence,
        risk_flags,
        compliance_results,
        audit_file
    ) = generate_corep_output(query, docs)

    review_status = route_for_review(risk_flags, compliance_results)

    validated_result, errors = validate_corep(result)
    corep_extract = map_to_corep_template(
        structured_output=result,
        audit_log=result.audit_log if hasattr(result, "audit_log") else None
    )

    return {
        "validated_result": validated_result,
        "explanations": explanations,
        "evidence": evidence,
        "risk_flags": risk_flags,
        "compliance_results": compliance_results,
        "audit_file": audit_file,
        "review_status": review_status,
        "errors": errors,
        "corep_template": corep_extract
    }
