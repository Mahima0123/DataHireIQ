# DataHireIQ
Job Market Intelligence & Skill Trend Analytics Platform
DataHireIQ is an end-to-end data engineering and analytics project that collects real-world job postings, processes them through an ETL pipeline, extracts in-demand skills, and visualizes hiring trends using an interactive dashboard.

It simulates a real-world data platform used for job market analysis and talent intelligence.

**It helps answer questions like:**
1. What skills are most in demand?
2. Which companies are hiring the most?
3. What locations have the highest job activity?
4. What technologies are trending in the job market?

**Key Features**
1. Data Ingestion
Fetches job postings from a public job API
Extracts structured job data (title, company, location, description, etc.)
2. ETL Pipeline
Modular pipeline
Clean separation of concerns (production-style design)
3. Skill Extraction Engine
Extracts relevant tech skills from job descriptions
Identifies Python, SQL, Kafka, Spark, AWS, Airflow, etc.
Converts unstructured text into structured analytics data
4. Data Warehouse
Built using PostgreSQL with relational schema:
5. Analytics Dashboard
Built with Streamlit:
KPI overview (jobs, companies, skills, locations)
Top skills demand visualization
Hiring company analysis
Location-based job distribution
Search + filtering system
Market insights section

**Tech Stack**
Python
PostgreSQL
Streamlit
Plotly 
Docker
Pandas 
Requests 