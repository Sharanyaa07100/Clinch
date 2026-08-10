from pathlib import Path

from llm import analyze_job_description


def analyze_jd(file_path):

    file_path = Path(file_path)

    with open(file_path, "r", encoding="utf-8") as file:
        text = file.read()

    return analyze_job_description(text)