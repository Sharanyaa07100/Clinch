from llm import ask_gemini


def semantic_match_skill(jd_skill, profile_evidence):
    """
    Ask Clinch whether the candidate's evidence
    is an exact, related, or missing match for a JD skill.
    """

    evidence_text = "\n".join(
        f"- {item}"
        for item in profile_evidence
    )

    prompt = f"""
You are Clinch, an AI career matching assistant.

Determine whether the candidate has evidence relevant
to the requested job skill.

JOB REQUIREMENT:
{jd_skill}

CANDIDATE EVIDENCE:
{evidence_text}

Classify the relationship as exactly one of:

EXACT
RELATED
MISSING

Definitions:

EXACT:
The candidate explicitly has the requested skill.

RELATED:
The candidate does not explicitly list the exact skill,
but their projects, technologies, education, research,
or experience demonstrate closely related knowledge.

MISSING:
There is no meaningful evidence that the candidate has
this skill.

Important rules:

- Do not invent experience.
- Do not assume that learning one technology means knowing
  every related technology.
- Do not classify something as EXACT unless there is explicit
  evidence.
- Return only valid JSON.

Return:

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
    Convert the evidence dictionary into a simple list.
    """

    flattened = []

    for skill, items in evidence.items():

        for item in items:

            flattened.append(
                f"{skill}: {item['evidence']}"
            )

    return flattened