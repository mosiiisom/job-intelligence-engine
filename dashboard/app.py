import time
import os
import subprocess

import streamlit as st
import streamlit.components.v1 as components
import pandas as pd

# --- Paths ---
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_PATH = os.path.join(ROOT_DIR, "data", "jobs.csv")


@st.cache_data(ttl=600)
def load_data():
    if not os.path.exists(DATA_PATH):
        return pd.DataFrame()
    return pd.read_csv(DATA_PATH)

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
    df = load_data()

    if df.empty:
        st.warning("No data found. Run scraper first.")
        return

    # --- Filters ---
    st.sidebar.header("Filters")

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
    filtered_df = df.copy()

    if companies:
        filtered_df = filtered_df[filtered_df["company"].isin(companies)]

    if locations:
        filtered_df = filtered_df[filtered_df["location"].isin(locations)]

    if employment_types:
        filtered_df = filtered_df[
            filtered_df["employment_type"].isin(employment_types)
        ]

    if selected_tags:
        filtered_df = filtered_df[
            filtered_df["tags"].apply(
                lambda x: any(
                    tag in [t.strip() for t in str(x).split(",")]
                    for tag in selected_tags
                )
            )
        ]

    # --- Metrics ---
    col1, col2, col3 = st.columns(3)

    col1.metric("Total Jobs", len(df))
    col2.metric("Filtered Jobs", len(filtered_df))
    col3.metric("Companies", filtered_df["company"].nunique())

    st.subheader("💼 Jobs")

    MAX_JOBS = 50
    display_df = filtered_df.head(MAX_JOBS)

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