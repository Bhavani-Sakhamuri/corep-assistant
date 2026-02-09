FIELD_KEYWORDS = {
    "cet1_capital": ["CET1", "Common Equity Tier 1"],
    "at1_capital": ["AT1", "Additional Tier 1"],
    "tier2_capital": ["Tier 2"],
    "rwa": ["Risk weighted", "RWA"]
}


def map_evidence(extracted, retrieved_docs):

    evidence_map = {}

    for field, keywords in FIELD_KEYWORDS.items():

        best_match = None
        best_score = 0

        for doc in retrieved_docs:

            content = doc.page_content.lower()

            score = sum(
                content.count(keyword.lower()) for keyword in keywords
            )

            if score > best_score:
                best_score = score
                best_match = doc

        if best_match:
            evidence_map[field] = {
                "value": getattr(extracted, field),
                "source": best_match.metadata.get("source"),
                "page": best_match.metadata.get("page_label"),
                "confidence": round(best_score / 5, 2),  # simple normalization
                "snippet": best_match.page_content[:400]
            }

    return evidence_map
