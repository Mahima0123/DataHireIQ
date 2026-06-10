import streamlit as st
import pandas as pd
import psycopg2
import plotly.express as px

st.set_page_config(
    page_title="DataHireIQ",
    page_icon="📊",
    layout="wide"
)


def get_connection():
    return psycopg2.connect(
        host="localhost",
        port=5434,
        database="datahireiq",
        user="datahireiq_user",
        password="datahireiq_pass"
    )


@st.cache_data
def load_data():

    conn = get_connection()

    jobs = pd.read_sql(
        "SELECT * FROM jobs",
        conn
    )

    skills = pd.read_sql(
        """
        SELECT s.skill_name,
               COUNT(*) as demand
        FROM skills s
        JOIN job_skills js
          ON s.skill_id = js.skill_id
        GROUP BY s.skill_name
        ORDER BY demand DESC
        """,
        conn
    )

    companies = pd.read_sql(
        """
        SELECT company,
               COUNT(*) as jobs
        FROM jobs
        GROUP BY company
        ORDER BY jobs DESC
        LIMIT 10
        """,
        conn
    )

    conn.close()

    return jobs, skills, companies


jobs, skills, companies = load_data()

st.title("📊 DataHireIQ")
st.subheader("Job Market Intelligence Platform")

# KPIs

col1, col2, col3 = st.columns(3)

col1.metric(
    "Total Jobs",
    len(jobs)
)

col2.metric(
    "Companies",
    jobs["company"].nunique()
)

col3.metric(
    "Skills Tracked",
    len(skills)
)

st.divider()

# Top Skills

st.subheader("🔥 Most Requested Skills")

fig1 = px.bar(
    skills.head(10),
    x="skill_name",
    y="demand"
)

st.plotly_chart(
    fig1,
    use_container_width=True
)

# Top Companies

st.subheader("🏢 Top Hiring Companies")

fig2 = px.bar(
    companies,
    x="company",
    y="jobs"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

# Raw Jobs

st.subheader("📄 Job Listings")

st.dataframe(
    jobs[
        [
            "title",
            "company",
            "location"
        ]
    ],
    use_container_width=True
)