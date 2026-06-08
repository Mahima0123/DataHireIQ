import re

SKILLS = [
    "python",
    "sql",
    "spark",
    "kafka",
    "airflow",
    "aws",
    "azure",
    "gcp",
    "snowflake",
    "databricks",
    "docker",
    "kubernetes",
    "tableau",
    "power bi"
]


def extract_skills(description):
    description = description.lower()

    found_skills = []

    for skill in SKILLS:
        pattern = r"\b" + re.escape(skill) + r"\b"

        if re.search(pattern, description):
            found_skills.append(skill)

    return found_skills

if __name__ == "__main__":
    sample = """
    Looking for a Data Engineer with Python, SQL,
    Kafka, Airflow and AWS experience.
    """

    print(extract_skills(sample))