import os
import sys
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd

# --- Paths ---
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from storage.repositories.job_queries import filter_jobs

@st.cache_data(ttl=300)
def load_data():
    from storage.repositories.job_queries import get_all_jobs
    return get_all_jobs(200)

def main():
    st.set_page_config(
        page_title="Job Intelligence Dashboard",
        layout="wide"
    )

    st.title("🚀 Job Intelligence Dashboard")

    st.markdown("""
        <div style="
            padding:12px;
            border-radius:10px;
            background:#1e1e1e;
            border:1px solid #333;
            margin-bottom:15px;
            color:#ddd;
        ">
        🚧 <b>Early Stage Project</b><br>
        Jobs are collected automatically every 1 hour via GitHub Actions.<br>
        This dashboard only visualizes pre-collected data.
        </div>
        """, unsafe_allow_html=True)

    # --- Sidebar ---
    st.sidebar.header("Controls")

    # --- Load Data ---
    jobs = load_data()

    if not jobs:
        st.warning("No data found. Run scraper first.")
        return

    df = pd.DataFrame(jobs)

    # --- Filters ---
    st.sidebar.header("Filters")

    keyword = st.sidebar.text_input("Search")

    companies = st.sidebar.multiselect(
        "Company",
        sorted(df["company"].dropna().unique())
    )

    locations = st.sidebar.multiselect(
        "Location",
        sorted(df["location"].dropna().unique())
    )

    employment_types = st.sidebar.multiselect(
        "Employment Type",
        sorted(df["employment_type"].dropna().unique())
    )

    # --- Tags ---
    all_tags = set()
    for tags in df["tags"].dropna():
        all_tags.update(tag.strip() for tag in tags.split(",") if tag.strip())

    selected_tags = st.sidebar.multiselect(
        "Tags",
        sorted(all_tags)
    )

    # --- Apply Filters ---
    filtered_jobs = filter_jobs(
        companies=companies,
        locations=locations,
        employment_types=employment_types,
        tags=selected_tags,
        limit=200
    )


    if keyword:
        filtered_jobs = [
            job for job in filtered_jobs
            if keyword.lower() in (
                    job["title"] + job["company"] + job["tags"]
            ).lower()
        ]

    filtered_df = pd.DataFrame(filtered_jobs)

    # --- Metrics ---
    col1, col2, col3 = st.columns(3)

    if filtered_df.empty:
        companies_count = 0
    else:
        companies_count = filtered_df["company"].nunique()

    all_jobs = load_data()
    col1.metric("Total Jobs", len(all_jobs))
    col2.metric("Filtered Jobs", len(filtered_df))
    col3.metric("Companies", companies_count)

    st.subheader("💼 Jobs")

    MAX_JOBS = 50
    display_df = filtered_df.head(MAX_JOBS)

    if filtered_df.empty:
        st.warning("No jobs match your filters 😅 Try removing some filters")
        return

    for _, row in display_df.iterrows():

        tags_html = ""
        if pd.notna(row["tags"]):
            tags = [t.strip() for t in str(row["tags"]).split(",")]
            tags_html = "".join(
                [f'<span class="tag">{tag}</span>' for tag in tags]
            )

        components.html(f"""
        <style>
        .job-card {{
            background: #1e1e1e;
            padding: 20px;
            border-radius: 12px;
            margin-bottom: 15px;
            border: 1px solid #2c2c2c;
            transition: all 0.25s ease;
            color: white;
            line-height:1.6;
        }}

        .job-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0px 8px 25px rgba(0,0,0,0.4);
        }}

        .job-title {{
            font-size: 18px;
            font-weight: bold;
        }}

        .job-company {{
            color: #bbb;
            font-size: 14px;
        }}

        .tag {{
            display: inline-block;
            background: #2a2a2a;
            padding: 5px 10px;
            margin: 5px 5px 0 0;
            border-radius: 6px;
            font-size: 12px;
        }}

        .job-link {{
            display: inline-block;
            margin-top: 10px;
            padding: 8px 12px;
            background: #4CAF50;
            color: white;
            text-decoration: none;
            border-radius: 6px;
        }}
        </style>

        <div class="job-card">
            <div class="job-title">{row['title']}</div>
            <div class="job-company">{row['company']} · {row['location']}</div>

            <div>
                🕒 {row['employment_type']} | 🌐 {row['work_type']}
            </div>

            <div>{tags_html}</div>

            <a href="{row['url']}" target="_blank" class="job-link">
                🔗 More Details
            </a>
        </div>
        """, height=220)


if __name__ == "__main__":
    main()