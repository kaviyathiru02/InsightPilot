import streamlit as st

from orchestrator import build_analysis_context
from recommendation import generate_recommendation
from agent import run_insightpilot


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="InsightPilot",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# SIMPLE CLEAN STYLING
# ============================================================

st.markdown(
    """
    <style>

    .stApp {
        background-color: #f7f9fc;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1200px;
    }

    h1, h2, h3 {
        color: #102a43 !important;
    }

    /* Question input */
    textarea {
        background-color: #ffffff !important;
        color: #102a43 !important;
        border: 2px solid #bcccdc !important;
        border-radius: 10px !important;
        font-size: 16px !important;
    }

    textarea:focus {
        border-color: #1f4e79 !important;
    }

    textarea::placeholder {
        color: #7b8794 !important;
        opacity: 1 !important;
    }

    /* Analyze button */
    div.stButton > button {
        background-color: #1f4e79 !important;
        color: #ffffff !important;
        border-radius: 8px !important;
        border: none !important;
        font-weight: 700 !important;
        min-height: 45px !important;
        padding: 8px 20px !important;
    }

    div.stButton > button:hover {
        background-color: #163a5c !important;
        color: #ffffff !important;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #102a43;
    }

    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span {
        color: #ffffff !important;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title("📊 InsightPilot")

    st.write("Evidence-Based Business Decision Support")

    st.divider()

    st.subheader("🔄 Analysis Pipeline")

    st.markdown("### ① Member 1")
    st.write("What happened?")

    st.markdown("### ② Member 2")
    st.write("What might have caused it?")

    st.markdown("### ③ Member 3")
    st.write("Can we trust the cause?")

    st.markdown("### ④ Member 4")
    st.write("What should the business do?")

    st.divider()

    st.subheader("🛡️ Safety Principle")

    st.write(
        "An uncertain cause is never presented "
        "as a confirmed cause."
    )


# ============================================================
# HEADER
# ============================================================

st.title("📊 InsightPilot")

st.write(
    "Transform business data into understandable insights, "
    "validated causes, and actionable recommendations."
)

st.divider()


# ============================================================
# LOAD MEMBER 1, 2 AND 3
# ============================================================

analysis = build_analysis_context()

if not analysis.get("success"):

    st.error(
        "Unable to load analysis data: "
        + analysis.get("error", "Unknown error.")
    )

    st.stop()


recommendation = generate_recommendation(analysis)

if not recommendation.get("success"):

    st.error(
        "Unable to generate recommendation: "
        + recommendation.get("error", "Unknown error.")
    )

    st.stop()


# ============================================================
# GET MEMBER 1 OVERALL ANALYSIS
# ============================================================

member1 = analysis["member1"]

overall_change = member1.get(
    "overall_change",
    {}
)

previous_period = overall_change.get(
    "previous_period",
    "Previous Period"
)

current_period = overall_change.get(
    "current_period",
    "Current Period"
)

previous_value = overall_change.get(
    "previous_value",
    0
)

current_value = overall_change.get(
    "current_value",
    0
)

absolute_change = overall_change.get(
    "absolute_change",
    0
)

percentage_change = overall_change.get(
    "percentage_change",
    0
)


# ============================================================
# ASK INSIGHTPILOT
# ============================================================

st.header("💬 Ask InsightPilot")

st.write(
    "Enter a business question about the current investigation."
)

question = st.text_area(
    "Business Question",
    placeholder=(
        "Example: Why did sales decrease from May 2026 "
        "to June 2026, what are the possible causes, "
        "and what should the business do next?"
    ),
    height=120
)

if st.button(
    "🔍 Analyze Business Performance",
    type="primary"
):

    if not question.strip():

        st.warning(
            "Please enter a business question first."
        )

    else:

        with st.spinner("Analyzing business data..."):

            try:

                result = run_insightpilot(
                    question.strip()
                )

                st.session_state["question"] = question.strip()
                st.session_state["result"] = result
                st.session_state["analyzed"] = True

            except Exception as error:

                st.session_state["analyzed"] = False

                st.error(
                    f"Analysis failed: {error}"
                )


# ============================================================
# SHOW SUCCESS
# ============================================================

if st.session_state.get("analyzed", False):

    st.success("✅ Analysis completed successfully.")

    st.info(
        "Question analyzed: "
        + st.session_state.get("question", "")
    )


# ============================================================
# BUSINESS OVERVIEW
# ============================================================

st.header("📈 Business Overview")

# Use two rows instead of four columns.
# This prevents values from being cut off on smaller screens.

row1_col1, row1_col2 = st.columns(2)

with row1_col1:

    st.metric(
        "Sales Change",
        f"{percentage_change:.2f}%"
    )

with row1_col2:

    st.metric(
        "Total Sales Change",
        f"${absolute_change:,.2f}"
    )


row2_col1, row2_col2 = st.columns(2)

with row2_col1:

    st.metric(
        f"{previous_period} Sales",
        f"${previous_value:,.2f}"
    )

with row2_col2:

    st.metric(
        f"{current_period} Sales",
        f"${current_value:,.2f}"
    )


# ============================================================
# CAUSE INVESTIGATION
# ============================================================

st.header("🔎 Cause Investigation")

cause_col, validation_col = st.columns(2)


candidate_cause = recommendation.get(
    "candidate_cause",
    "Unknown"
)

validation_status = recommendation.get(
    "validation_status",
    "UNKNOWN"
)

reliability_level = recommendation.get(
    "reliability_level",
    "UNKNOWN"
)

reliability_score = recommendation.get(
    "reliability_score",
    0
)


# ------------------------------------------------------------
# CANDIDATE CAUSE
# ------------------------------------------------------------

with cause_col:

    st.subheader("🎯 Leading Candidate Cause")

    st.info(
        f"**{candidate_cause}**"
    )

    st.write(
        "This candidate cause comes from the Member 2 "
        "root-cause analysis and is reviewed by Member 3."
    )


# ------------------------------------------------------------
# VALIDATION
# ------------------------------------------------------------

with validation_col:

    st.subheader("🛡️ Evidence Validation")

    if validation_status == "UNCERTAIN":

        st.warning(
            f"**{validation_status}**"
        )

    elif validation_status == "VALIDATED":

        st.success(
            f"**{validation_status}**"
        )

    else:

        st.info(
            f"**{validation_status}**"
        )

    st.write(
        f"Reliability Level: **{reliability_level}**"
    )

    st.write(
        f"Evidence Score: **{reliability_score}/100**"
    )


# ============================================================
# KEY FINDINGS
# ============================================================

st.header("📌 Key Findings")

dimension_analysis = member1.get(
    "dimension_analysis",
    {}
)

important_dimensions = [
    ("region", "Region"),
    ("channel", "Channel"),
    ("customer_type", "Customer Type"),
    ("product", "Product")
]


for dimension_key, display_name in important_dimensions:

    results = dimension_analysis.get(
        dimension_key,
        {}
    ).get(
        "results",
        []
    )

    if results:

        sorted_results = sorted(
            results,
            key=lambda item: item.get(
                "percentage_change",
                0
            )
        )

        worst = sorted_results[0]

        name = worst.get(
            "dimension_value",
            worst.get(
                "name",
                "Unknown"
            )
        )

        change = worst.get(
            "percentage_change",
            0
        )

        st.write(
            f"**{display_name}:** "
            f"{name} — **{change:.2f}%**"
        )


# ============================================================
# MEMBER 4 DECISION SUPPORT
# ============================================================

st.header("🧠 Member 4 Decision Support")

result_text = st.session_state.get(
    "result",
    ""
)

if result_text:

    st.subheader("InsightPilot Recommendation")

    st.write(result_text)

else:

    st.info(
        "Enter a business question above and click "
        "'Analyze Business Performance' to generate "
        "the decision-support response."
    )


# ============================================================
# RECOMMENDED ACTIONS
# ============================================================

st.header("🚀 Recommended Actions")

actions = [
    "Investigate historical inventory and stockout records.",
    "Analyze returning-customer behavior because returning customer sales declined substantially.",
    "Audit the online sales funnel for possible conversion or customer-experience problems.",
    "Review pricing, promotions, and seasonal demand changes.",
    "Check supplier delivery performance and product-level inventory availability."
]

for index, action in enumerate(actions, start=1):

    st.write(
        f"**{index}.** {action}"
    )


# ============================================================
# EVIDENCE-BASED DECISION GUIDANCE
# ============================================================

st.header("⚠️ Evidence-Based Decision Guidance")

st.warning(
    "Inventory shortage is a leading candidate, but it is "
    "NOT confirmed as the root cause. The evidence reliability "
    f"is {reliability_level} with a score of "
    f"{reliability_score}/100. Major operational decisions "
    "should not be based only on this candidate cause."
)


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "InsightPilot • Multi-Agent Business Intelligence & "
    "Decision Support"
)

st.caption(
    "Member 1 → Member 2 → Member 3 → Member 4"
)