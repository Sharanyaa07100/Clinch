def normalize_skill(skill):
    """
    Normalize a skill for comparison.
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

        for skill in data_dict.get("skills", []):
            skills.add(normalize_skill(skill))

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

        # Direct skills
        for skill in data_dict.get("skills", []):

            normalized = normalize_skill(skill)

            evidence.setdefault(normalized, []).append({
                "source": file_name,
                "type": "skill",
                "evidence": skill
            })

        # Projects
        for project in data_dict.get("projects", []):

            project_name = project.get("name")

            for technology in project.get("technologies", []):

                normalized = normalize_skill(technology)

                evidence.setdefault(normalized, []).append({
                    "source": file_name,
                    "type": "project",
                    "evidence": project_name
                })

    return evidence


def match_skills(jd, profile_skills):

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