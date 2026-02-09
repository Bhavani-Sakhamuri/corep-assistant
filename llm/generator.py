from dotenv import load_dotenv
load_dotenv()

import os

from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq

# Schema (Extraction + Final Output)
from llm.schema import CorepOwnFunds, CorepFinalOutput

# Deterministic Calculator
from template.calculator import calculate_corep_metrics
from audit.review_router import route_for_review

# Explainability Module
from template.explainability import generate_explainability
from audit.evidence_mapper import map_evidence
from audit.risk_flags import generate_risk_flags
from audit.compliance_validator import compliance_validator
from audit.audit_logger import log_audit_trail
from config.version_config import (
    MODEL_VERSION,
    PROMPT_VERSION,
    SCHEMA_VERSION,
    PIPELINE_VERSION
)


# ---------------------------
# LLM Setup
# ---------------------------

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0,
    api_key=os.getenv("GROQ_API_KEY")
)

structured_llm = llm.with_structured_output(CorepOwnFunds)


# ---------------------------
# Prompt
# ---------------------------

prompt = PromptTemplate(
    template="""
You are a UK COREP regulatory assistant.

Extract ONLY the following values from the regulatory context:

- CET1 Capital
- AT1 Capital
- Tier 2 Capital
- Risk Weighted Assets (RWA)
- Regulatory audit references used

Return ONLY values explicitly supported by the context.
Do NOT perform any calculations.

Context:
{context}

Question:
{query}
""",
    input_variables=["context", "query"],
)


# ---------------------------
# Generator
# ---------------------------

def generate_corep_output(query, docs):
    retrieved_docs = docs
    # -----------------------
    # Build Context
    # -----------------------
    context = "\n\n".join([doc.page_content for doc in docs])

    formatted_prompt = prompt.format(context=context, query=query)

    # -----------------------
    # LLM Extraction ONLY
    # -----------------------
    extracted = structured_llm.invoke(formatted_prompt)

    # -----------------------
    # Deterministic Calculations
    # -----------------------
    calculated = calculate_corep_metrics(extracted)
    evidence_map = map_evidence(extracted, retrieved_docs)
    risk_flags = generate_risk_flags(evidence_map)



    # -----------------------
    # Final Structured Output
    # -----------------------
    final_output = CorepFinalOutput(
        **extracted.model_dump(),
        total_own_funds=calculated["total_own_funds"],
        cet1_ratio=calculated["cet1_ratio"],
        total_capital_ratio=calculated["total_capital_ratio"]
    )

    # -----------------------
    # Explainability Layer
    # -----------------------
    explanations = generate_explainability(
        extracted=extracted,
        calculated=calculated,
        final_output=final_output
    )
    compliance_results = compliance_validator(final_output, risk_flags)
    version_info ={
        "model_version": MODEL_VERSION,
        "prompt_version": PROMPT_VERSION,
        "schema_version": SCHEMA_VERSION,
        "pipeline_version": PIPELINE_VERSION
    }
    review_status = route_for_review(risk_flags, compliance_results)
    audit_file = log_audit_trail(
        query=query,
        final_output=final_output,
        explanations=explanations,
        evidence_map=evidence_map,
        risk_flags=risk_flags,
        compliance_results=compliance_results,
        retrieved_docs=docs,
        version_info=version_info,
        review_status=review_status
        
    )


    return final_output, explanations, evidence_map, risk_flags, compliance_results, audit_file
