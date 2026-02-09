from rag.retriever import get_retriever
from pipeline.run_pipeline import run_corep_pipeline

retriever = get_retriever()


def main():

    query = """
    Bank reports:
    CET1 = 120 million
    AT1 = 20 million
    Tier2 = 10 million
    RWA = 900 million
    """

    docs = retriever.invoke(query)

    output = run_corep_pipeline(query, docs)

    print("Audit log saved at:", output["audit_file"])
    print(output["review_status"])

    print("====== Compliance Results =======")
    print(output["compliance_results"])

    print("===== RISK FLAGS =====")
    print(output["risk_flags"])

    print("===== EVIDENCE TRACE =====")
    print(output["evidence"])

    print("===== COREP OUTPUT =====")
    print(output["validated_result"])

    print("\n===== EXPLAINABILITY =====")

    for metric, info in output["explanations"].items():
        print(f"\n{metric.upper()}")
        for key, value in info.items():
            print(f"{key}: {value}")


if __name__ == "__main__":
    main()
