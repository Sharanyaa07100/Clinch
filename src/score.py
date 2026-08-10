def calculate_skill_score(matched, total):
    """
    Calculate percentage of matched skills.
    """

    if total == 0:
        return 0.0

    return round((matched / total) * 100, 2)


def calculate_ats_score(match_result):
    """
    Calculate the initial Clinch ATS match score.

    Required skills are weighted more heavily than
    preferred skills.
    """

    matched_required = len(match_result["matched_required"])
    missing_required = len(match_result["missing_required"])

    matched_preferred = len(match_result["matched_preferred"])
    missing_preferred = len(match_result["missing_preferred"])

    total_required = matched_required + missing_required
    total_preferred = matched_preferred + missing_preferred

    required_score = calculate_skill_score(
        matched_required,
        total_required
    )

    preferred_score = calculate_skill_score(
        matched_preferred,
        total_preferred
    )

    # Required skills matter more.
    if total_preferred > 0:

        overall_score = (
            required_score * 0.70
            + preferred_score * 0.30
        )

    else:

        overall_score = required_score

    return {
        "overall_score": round(overall_score, 2),
        "required_score": required_score,
        "preferred_score": preferred_score
    }