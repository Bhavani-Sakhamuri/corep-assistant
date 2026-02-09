# reporting/corep_template_mapper.py

def map_to_corep_template(structured_output, audit_log=None):
    """
    Convert structured COREP output into COREP-style reporting extract
    """

    template_rows = []

    template_rows.append({
        "Row": "OF.01",
        "Field": "CET1 Capital",
        "Description": "Common Equity Tier 1 Capital",
        "Value": structured_output.cet1_capital,
        "Audit_Source": audit_log.get("cet1_capital") if audit_log else "LLM Derived"
    })

    template_rows.append({
        "Row": "OF.02",
        "Field": "AT1 Capital",
        "Description": "Additional Tier 1 Capital",
        "Value": structured_output.at1_capital,
        "Audit_Source": audit_log.get("at1_capital") if audit_log else "LLM Derived"
    })

    template_rows.append({
        "Row": "OF.03",
        "Field": "Total Own Funds",
        "Description": "Sum of CET1 + AT1",
        "Value": structured_output.cet1_capital + structured_output.at1_capital,
        "Audit_Source": "Calculated"
    })

    return template_rows
