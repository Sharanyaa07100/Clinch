from llm import ask_gemini


def semantic_match_skill(jd_skill, profile_evidence):
    """
    Determine whether candidate evidence is an exact,
    related, or missing match for a JD skill.

    This function is intentionally conservative.
    It must not upgrade related evidence to EXACT.
    """

    evidence_text = "\n".join(
        f"- {item}"
        for item in profile_evidence
    )

    prompt = f"""
You are Clinch, an AI career matching assistant.

Your job is to determine whether the candidate has evidence
for a specific job requirement.

JOB REQUIREMENT:
{jd_skill}

CANDIDATE EVIDENCE:
{evidence_text}

Classify the requirement into exactly ONE of:

EXACT
RELATED
MISSING

========================
STRICT CLASSIFICATION RULES
========================

EXACT:

Use EXACT ONLY when the candidate evidence explicitly contains
the requested skill or a clearly equivalent standardized name.

Examples:

JD: Python
Evidence: Python
=> EXACT

JD: Machine Learning
Evidence: Machine Learning
=> EXACT

JD: Scikit-learn
Evidence: Scikit-learn
=> EXACT

JD: Continuous Integration / Continuous Deployment
Evidence: CI/CD
=> EXACT

Do NOT infer EXACT merely because the candidate demonstrates
the concept.

========================

RELATED:

Use RELATED when the exact requested skill is NOT explicitly
present, but the candidate has strong and meaningful evidence
of closely related knowledge.

Example:

JD: Machine Learning

Evidence:
- Supervised Learning
- Deep Learning
- XGBoost
- LightGBM
- CatBoost
- Scikit-learn

=> RELATED

Another example:

JD: Machine Learning

Evidence:
- AI
- Deep Learning

=> RELATED

Another example:

JD: Kubernetes

Evidence:
- Docker
- GitLab CI/CD
- DevOps

=> RELATED

========================

MISSING:

Use MISSING when there is no meaningful evidence that the
candidate has the requested skill.

Example:

JD: Kubernetes

Evidence:
- Python
- SQL
- Tableau

=> MISSING

========================
CRITICAL RULE
========================

DO NOT classify a skill as EXACT based on inference.

The following do NOT prove an EXACT match for Machine Learning:

- AI
- Artificial Intelligence
- Deep Learning
- Supervised Learning
- Neural Networks
- XGBoost
- LightGBM
- CatBoost
- Scikit-learn

These may support a RELATED classification.

Only explicit "Machine Learning" or a clearly equivalent
standardized term should produce EXACT.

Similarly, do not assume that one technology automatically
means another technology.

Never invent skills or experience.

========================
OUTPUT
========================

Return ONLY valid JSON.

Use this exact structure:

{{
    "skill": "{jd_skill}",
    "status": "EXACT | RELATED | MISSING",
    "confidence": 0.0,
    "reason": "short explanation"
}}
"""

    response = ask_gemini(prompt)

    return response

def flatten_evidence(evidence):
    """
    Convert the evidence dictionary into a simple list
    for semantic matching.
    """

    flattened = []

    for skill, items in evidence.items():

        for item in items:

            flattened.append(
                f"{skill}: {item['evidence']}"
            )

    return flattened