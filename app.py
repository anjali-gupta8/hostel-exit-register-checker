import streamlit as st
import pandas as pd
import io
from datetime import datetime

# ─── Page config ───
st.set_page_config(
    page_title="Hostel Exit Register Checker",
    page_icon="📋",
    layout="wide",
)

# ─── Expected columns ───
EXPECTED_COLUMNS = [
    "Date", "Name", "Room_No", "Reg_No",
    "Destination", "Mobile_No", "Exit_Time", "Return_Time", "Remarks",
]

REQUIRED_FIELDS = ["Date", "Name", "Room_No", "Reg_No",
                   "Destination", "Mobile_No", "Exit_Time", "Return_Time"]


# ─── Helper functions ───

def load_csv(file) -> pd.DataFrame | None:
    """Read an uploaded CSV file and return a DataFrame, or None on error."""
    try:
        raw = file.read()
        if len(raw.strip()) == 0:
            st.error("⚠️ The uploaded file is empty.")
            return None
        df = pd.read_csv(io.BytesIO(raw), dtype=str, keep_default_na=False)
        return df
    except Exception as e:
        st.error(f"⚠️ Could not read the file: {e}")
        return None


def validate_columns(df: pd.DataFrame) -> bool:
    """Check that the CSV has the expected column names."""
    missing = [c for c in EXPECTED_COLUMNS if c not in df.columns]
    if missing:
        st.error(
            f"⚠️ Missing columns: **{', '.join(missing)}**. "
            f"Expected columns are: {', '.join(EXPECTED_COLUMNS)}"
        )
        return False
    return True


def find_missing_fields(row: pd.Series) -> list[str]:
    """Return a list of field names that are blank for a given row."""
    missing = []
    for col in REQUIRED_FIELDS:
        val = str(row.get(col, "")).strip()
        if val == "":
            missing.append(col)
    return missing


def analyse(df: pd.DataFrame) -> pd.DataFrame:
    """Add analysis columns to the DataFrame."""
    df = df.copy()
    df["Missing_Fields"] = df.apply(
        lambda r: ", ".join(find_missing_fields(r)) if find_missing_fields(r) else "None",
        axis=1,
    )
    df["Missing_Count"] = df.apply(lambda r: len(find_missing_fields(r)), axis=1)
    df["Is_Complete"] = df["Missing_Count"] == 0
    return df


def to_csv_download(df: pd.DataFrame) -> bytes:
    """Convert a DataFrame to CSV bytes for download."""
    return df.to_csv(index=False).encode("utf-8")


# ─── Sidebar ───

st.sidebar.title("📋 Hostel Exit Register Checker")
st.sidebar.markdown("---")
st.sidebar.markdown(
    "A tool to help hostel security guards check "
    "their handwritten exit register for missing or incomplete entries."
)
st.sidebar.markdown("---")

upload_mode = st.sidebar.radio(
    "Data source",
    ["Use default data.csv", "Upload your own CSV"],
)

uploaded_file = None
if upload_mode == "Upload your own CSV":
    uploaded_file = st.sidebar.file_uploader("Upload a CSV file", type=["csv"])

st.sidebar.markdown("---")
st.sidebar.markdown(
    "**Built for:** Hostel security staff  \n"
    "**Data:** Real register entries  \n"
    "**By:** Anjali Gupta"
)

# ─── Main content ───

st.title("📋 Hostel Exit Register — Completeness Checker")
st.markdown(
    "This tool checks the hostel exit register for **missing fields** and "
    "**incomplete records**, helping the security guard catch gaps quickly."
)
st.markdown("---")

# Load data
df = None

if upload_mode == "Upload your own CSV" and uploaded_file is not None:
    df = load_csv(uploaded_file)
    if df is not None and not validate_columns(df):
        df = None
elif upload_mode == "Use default data.csv":
    try:
        df = pd.read_csv("data.csv", dtype=str, keep_default_na=False)
        if not validate_columns(df):
            df = None
    except FileNotFoundError:
        st.error("⚠️ Default `data.csv` not found. Place it in the same folder as app.py.")
elif upload_mode == "Upload your own CSV" and uploaded_file is None:
    st.info("👆 Upload a CSV file from the sidebar to get started.")

if df is not None:
    # Run analysis
    result = analyse(df)

    # ─── Summary cards ───
    total = len(result)
    complete = int(result["Is_Complete"].sum())
    incomplete = total - complete
    missing_exit = int(result.apply(lambda r: str(r.get("Exit_Time", "")).strip() == "", axis=1).sum())
    missing_return = int(result.apply(lambda r: str(r.get("Return_Time", "")).strip() == "", axis=1).sum())

    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Total Records", total)
    col2.metric("✅ Complete", complete)
    col3.metric("❌ Incomplete", incomplete)
    col4.metric("⏰ No Exit Time", missing_exit)
    col5.metric("🔙 No Return Time", missing_return)

    st.markdown("---")

    # ─── Completeness bar ───
    if total > 0:
        pct = round(complete / total * 100, 1)
        st.markdown(f"### Register Completeness: **{pct}%**")
        st.progress(pct / 100)
    st.markdown("")

    # ─── Missing-field breakdown ───
    st.subheader("📊 Missing Fields Breakdown")
    field_counts = {}
    for col_name in REQUIRED_FIELDS:
        count = int(result.apply(lambda r, c=col_name: str(r.get(c, "")).strip() == "", axis=1).sum())
        if count > 0:
            field_counts[col_name] = count

    if field_counts:
        breakdown_df = pd.DataFrame(
            {"Field": list(field_counts.keys()), "Missing Count": list(field_counts.values())}
        ).sort_values("Missing Count", ascending=False)
        st.bar_chart(breakdown_df.set_index("Field"))
    else:
        st.success("All fields are filled in every record! 🎉")

    st.markdown("---")

    # ─── Filters ───
    st.subheader("🔍 Filter & Search")

    filter_col1, filter_col2, filter_col3 = st.columns(3)

    with filter_col1:
        show_filter = st.selectbox(
            "Show records",
            ["All", "Complete only", "Incomplete only"],
        )

    with filter_col2:
        dates = sorted(result["Date"].unique().tolist())
        date_filter = st.selectbox("Filter by date", ["All dates"] + dates)

    with filter_col3:
        search_term = st.text_input("Search (name, room, destination)")

    # Apply filters
    filtered = result.copy()

    if show_filter == "Complete only":
        filtered = filtered[filtered["Is_Complete"]]
    elif show_filter == "Incomplete only":
        filtered = filtered[~filtered["Is_Complete"]]

    if date_filter != "All dates":
        filtered = filtered[filtered["Date"] == date_filter]

    if search_term.strip():
        term = search_term.strip().lower()
        mask = filtered.apply(
            lambda r: any(term in str(v).lower() for v in r.values), axis=1
        )
        filtered = filtered[mask]

    # ─── Records table ───
    st.subheader(f"📄 Records ({len(filtered)} shown)")

    display_cols = EXPECTED_COLUMNS + ["Missing_Fields", "Missing_Count"]

    # Include Is_Complete for styling, then hide it
    styled_df = filtered[display_cols + ["Is_Complete"]].copy()

    def highlight_row(row):
        if row["Is_Complete"]:
            return ["background-color: #d4edda"] * len(row)
        else:
            return ["background-color: #f8d7da"] * len(row)

    styled = styled_df.style.apply(highlight_row, axis=1)
    st.dataframe(styled, use_container_width=True, height=420)

    st.markdown("---")

    # ─── Detailed incomplete records ───
    if incomplete > 0:
        st.subheader("⚠️ Incomplete Records — Detail")
        inc_df = result[~result["Is_Complete"]].copy()
        for idx, row in inc_df.iterrows():
            name_label = row["Name"] if row["Name"].strip() else f"(row {idx + 1})"
            with st.expander(f"Record: {name_label} — missing {row['Missing_Count']} field(s)"):
                for col_name in REQUIRED_FIELDS:
                    val = str(row.get(col_name, "")).strip()
                    if val == "":
                        st.markdown(f"- ❌ **{col_name}**: *empty*")
                    else:
                        st.markdown(f"- ✅ **{col_name}**: {val}")

    st.markdown("---")

    # ─── Download reports ───
    st.subheader("📥 Download Reports")

    dl_col1, dl_col2, dl_col3 = st.columns(3)

    with dl_col1:
        st.download_button(
            "⬇️ Full Analysis (CSV)",
            data=to_csv_download(result[display_cols]),
            file_name="full_analysis_report.csv",
            mime="text/csv",
        )

    with dl_col2:
        inc_report = result[~result["Is_Complete"]][display_cols]
        st.download_button(
            "⬇️ Incomplete Only (CSV)",
            data=to_csv_download(inc_report),
            file_name="incomplete_records_report.csv",
            mime="text/csv",
        )

    with dl_col3:
        st.download_button(
            "⬇️ Current View (CSV)",
            data=to_csv_download(filtered[display_cols]),
            file_name="filtered_view_report.csv",
            mime="text/csv",
        )

    st.markdown("---")
    st.caption(
        "Built as part of a 1-day take-home assignment. "
        "This tool reads a CSV copy of the handwritten hostel exit register "
        "and flags missing or incomplete entries."
    )
