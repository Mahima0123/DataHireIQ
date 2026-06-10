import streamlit as st
import pandas as pd
import psycopg2
import plotly.express as px

# PAGE CONFIG
st.set_page_config(
    page_title="DataHireIQ",
    page_icon="📊",
    layout="wide"
)


# CUSTOM CSS
st.markdown("""
<style>

.block-container {
    padding-top: 1rem;
}

.metric-container {
    background-color: #1f2937;
    padding: 15px;
    border-radius: 12px;
}

h1 {
    font-weight: 700;
}

</style>
""", unsafe_allow_html=True)


# DB CONNECTION
def get_connection():
    return psycopg2.connect(
        host="localhost",
        port=5434,
        database="datahireiq",
        user="datahireiq_user",
        password="datahireiq_pass"
    )


# LOAD DATA
@st.cache_data(ttl=300)
def load_data():

    conn = get_connection()

    jobs = pd.read_sql(
        """
        SELECT *
        FROM jobs
        """,
        conn
    )

    skills = pd.read_sql(
        """
        SELECT
            s.skill_name,
            COUNT(*) AS demand
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
        SELECT
            company,
            COUNT(*) AS jobs
        FROM jobs
        GROUP BY company
        ORDER BY jobs DESC
        LIMIT 15
        """,
        conn
    )

    locations = pd.read_sql(
        """
        SELECT
            location,
            COUNT(*) AS jobs
        FROM jobs
        WHERE location IS NOT NULL
        GROUP BY location
        ORDER BY jobs DESC
        LIMIT 15
        """,
        conn
    )

    conn.close()

    return jobs, skills, companies, locations

jobs, skills, companies, locations = load_data()


# SIDEBAR
st.sidebar.title("🔎 Filters")

company_filter = st.sidebar.selectbox(
    "Company",
    ["All"] + sorted(
        jobs["company"].dropna().unique().tolist()
    )
)

location_filter = st.sidebar.selectbox(
    "Location",
    ["All"] + sorted(
        jobs["location"].dropna().unique().tolist()
    )
)

search_title = st.sidebar.text_input(
    "Search Job Title"
)

filtered_jobs = jobs.copy()

if company_filter != "All":
    filtered_jobs = filtered_jobs[
        filtered_jobs["company"] == company_filter
    ]

if location_filter != "All":
    filtered_jobs = filtered_jobs[
        filtered_jobs["location"] == location_filter
    ]

if search_title:
    filtered_jobs = filtered_jobs[
        filtered_jobs["title"].str.contains(
            search_title,
            case=False,
            na=False
        )
    ]


# HEADER
st.title("DataHireIQ")
st.caption("Job Market Intelligence Platform")

st.markdown("---")


# KPI CARDS
col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "📄 Total Jobs",
    len(filtered_jobs)
)

col2.metric(
    "🏢 Companies",
    filtered_jobs["company"].nunique()
)

col3.metric(
    "📍 Locations",
    filtered_jobs["location"].nunique()
)

col4.metric(
    "🛠 Skills Tracked",
    len(skills)
)

st.markdown("---")


# TABS
tab1, tab2, tab3 = st.tabs(
    [
        "📈 Overview",
        "🛠 Skills",
        "🏢 Companies"
    ]
)


# OVERVIEW TAB
with tab1:

    left, right = st.columns(2)

    with left:

        st.subheader("🔥 Top Skills")

        fig1 = px.bar(
            skills.head(10),
            x="skill_name",
            y="demand",
            text="demand",
            title="Most Requested Skills"
        )

        st.plotly_chart(
            fig1,
            use_container_width=True
        )

    with right:

        st.subheader("🏢 Top Hiring Companies")

        fig2 = px.bar(
            companies,
            x="company",
            y="jobs",
            text="jobs",
            title="Companies with Most Openings"
        )

        st.plotly_chart(
            fig2,
            use_container_width=True
        )

    st.subheader("📄 Recent Job Listings")

    display_columns = [
        col for col in [
            "title",
            "company",
            "location",
            "employment_type"
        ]
        if col in filtered_jobs.columns
    ]

    st.dataframe(
        filtered_jobs[display_columns],
        use_container_width=True,
        height=400
    )


# SKILLS TAB
with tab2:

    st.subheader("🛠 Skill Demand Analysis")

    fig3 = px.pie(
        skills.head(10),
        names="skill_name",
        values="demand",
        title="Top Skill Share"
    )

    st.plotly_chart(
        fig3,
        use_container_width=True
    )

    st.dataframe(
        skills,
        use_container_width=True
    )


# COMPANIES TAB
with tab3:

    left, right = st.columns(2)

    with left:

        st.subheader("🏢 Hiring Companies")

        fig4 = px.bar(
            companies,
            x="company",
            y="jobs",
            text="jobs"
        )

        st.plotly_chart(
            fig4,
            use_container_width=True
        )

    with right:

        st.subheader("📍 Hiring Locations")

        fig5 = px.bar(
            locations,
            x="location",
            y="jobs",
            text="jobs"
        )

        st.plotly_chart(
            fig5,
            use_container_width=True
        )


# MARKET INSIGHTS
st.markdown("---")

st.subheader("📊 Market Insights")

if not skills.empty:
    top_skill = skills.iloc[0]["skill_name"]
    demand = skills.iloc[0]["demand"]

    st.success(
        f"Most requested skill: {top_skill.upper()} ({demand} job postings)"
    )

if not companies.empty:
    top_company = companies.iloc[0]["company"]

    st.info(
        f"Top hiring company in the current dataset: {top_company}"
    )