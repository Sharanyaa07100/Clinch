from knowledge_base import load_knowledge
from matcher import collect_evidence
from semantic_matcher import (
    semantic_match_skill,
    flatten_evidence
)


documents = load_knowledge()

evidence = collect_evidence(documents)

candidate_evidence = flatten_evidence(evidence)

result = semantic_match_skill(
    "Machine Learning",
    candidate_evidence
)

print("\n===== CLINCH SEMANTIC MATCH =====\n")

print(result)