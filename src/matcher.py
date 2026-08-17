from semantic_matcher import semantic_match_skill, flatten_evidence


def normalize_skill(skill):
    """
    Normalize a skill for consistent comparison.
    """

    skill = skill.lower().strip()

    replacements = {
        "python programming": "python",
        "python development": "python",
        "sql programming": "sql",
        "ml": "machine learning",
        "artificial intelligence": "ai",
        "ci/cd pipelines": "ci/cd",
        "continuous integration/continuous deployment": "ci/cd",
        "scikit learn": "scikit-learn",
    }

    return replacements.get(skill, skill)


def collect_profile_skills(documents):
    """
    Collect all skills and technologies from career knowledge.
    """

    skills = set()

    for document in documents:

        data = document.get("data")

        if not data:
            continue

        data_dict = (
            data
            if isinstance(data, dict)
            else data.model_dump()
        )

        # Direct skills
        for skill in data_dict.get("skills", []):
            skills.add(normalize_skill(skill))

        # Project technologies
        for project in data_dict.get("projects", []):

            for technology in project.get("technologies", []):
                skills.add(normalize_skill(technology))

    return skills


def collect_evidence(documents):
    """
    Build an index showing where each skill appears.
    """

    evidence = {}

    for document in documents:

        data = document.get("data")

        if not data:
            continue

        data_dict = (
            data
            if isinstance(data, dict)
            else data.model_dump()
        )

        file_name = document.get("file_name")

        # -------------------------------------------------
        # Direct skills
        # -------------------------------------------------

        for skill in data_dict.get("skills", []):

            normalized = normalize_skill(skill)

            evidence.setdefault(normalized, []).append({
                "source": file_name,
                "type": "skill",
                "evidence": skill
            })

        # -------------------------------------------------
        # Project technologies
        # -------------------------------------------------

        for project in data_dict.get("projects", []):

            project_name = project.get("name")

            for technology in project.get("technologies", []):

                normalized = normalize_skill(technology)

                evidence.setdefault(normalized, []).append({
                    "source": file_name,
                    "type": "project",
                    "evidence": project_name
                })

        # -------------------------------------------------
        # Experience
        # -------------------------------------------------

        for experience in data_dict.get("experience", []):

            company = experience.get("company")
            role = experience.get("role")

            responsibilities = experience.get(
                "responsibilities",
                []
            )

            for responsibility in responsibilities:

                # Store the responsibility as searchable
                # evidence without pretending it is a skill.
                evidence.setdefault(
                    "__experience__",
                    []
                ).append({
                    "source": file_name,
                    "type": "experience",
                    "evidence": (
                        f"{company} — {role}: "
                        f"{responsibility}"
                    )
                })

    return evidence


def match_skills(jd, profile_skills):
    """
    Perform basic exact skill matching against a JD.
    """

    required = [
        normalize_skill(skill)
        for skill in jd.required_skills
    ]

    preferred = [
        normalize_skill(skill)
        for skill in jd.preferred_skills
    ]

    matched_required = []
    missing_required = []

    for skill in required:

        if skill in profile_skills:
            matched_required.append(skill)

        else:
            missing_required.append(skill)

    matched_preferred = []
    missing_preferred = []

    for skill in preferred:

        if skill in profile_skills:
            matched_preferred.append(skill)

        else:
            missing_preferred.append(skill)

    return {
        "matched_required": matched_required,
        "missing_required": missing_required,
        "matched_preferred": matched_preferred,
        "missing_preferred": missing_preferred
    }


def match_jd_skills(jd_skills, evidence):
    """
    Match JD skills using a two-stage approach:

    1. Exact matching using the local knowledge base.
    2. Semantic matching using Clinch/Gemini only when
       an exact match cannot be found.
    """

    results = []

    # Convert our evidence dictionary into a list
    # that can be provided to the semantic matcher.
    candidate_evidence = flatten_evidence(evidence)

    for skill in jd_skills:

        # Normalize the JD skill before comparison.
        normalized_skill = normalize_skill(skill)

        # -------------------------------------------------
        # Stage 1: Exact match
        # -------------------------------------------------

        if normalized_skill in evidence:

            results.append({
                "skill": skill,
                "status": "EXACT",
                "confidence": 1.0,
                "reason": (
                    "Exact skill found in the "
                    "candidate knowledge base."
                ),
                "evidence": evidence[normalized_skill]
            })

            continue

        # -------------------------------------------------
        # Stage 2: Semantic fallback
        # -------------------------------------------------

        result = semantic_match_skill(
            skill,
            candidate_evidence
        )

        results.append(result)

    return results