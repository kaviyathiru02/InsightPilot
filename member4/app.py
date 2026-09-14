import streamlit as st

from orchestrator import build_analysis_context
from recommendation import generate_recommendation
from agent import run_insightpilot


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="InsightPilot | AI Decision Support",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
    <style>

    /* Main background */
    .stApp {
        background: #f7f9fc;
    }

    /* Main content width */
    .block-container {
        max-width: 1200px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    /* Header */
    .hero {
        padding: 1.5rem 2rem;
        border-radius: 18px;
        background: linear-gradient(135deg, #172554, #2563eb);
        color: white;
        margin-bottom: 1.5rem;
        box-shadow: 0 8px 25px rgba(37, 99, 235, 0.18);
    }

    .hero-title {
        font-size: 2.5rem;
        font-weight: 800;
        margin-bottom: 0.2rem;
    }

    .hero-subtitle {
        font-size: 1.05rem;
        opacity: 0.9;
    }

    /* Section headings */
    .section-title {
        font-size: 1.35rem;
        font-weight: 750;
        color: #172033;
        margin-top: 1.5rem;
        margin-bottom: 0.8rem;
    }

    /* KPI cards */
    .kpi-card {
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 15px;
        padding: 1.2rem;
        min-height: 125px;
        box-shadow: 0 3px 12px rgba(15, 23, 42, 0.05);
    }

    .kpi-label {
        font-size: 0.85rem;
        color: #64748b;
        margin-bottom: 0.35rem;
    }

    .kpi-value {
        font-size: 1.55rem;
        font-weight: 800;
        color: #172033;
    }

    .kpi-negative {
        color: #dc2626;
    }

    /* Root cause */
    .cause-card {
        background: white;
        border-left: 5px solid #2563eb;
        border-radius: 14px;
        padding: 1.25rem;
        box-shadow: 0 3px 12px rgba(15, 23, 42, 0.05);
    }

    .cause-label {
        color: #64748b;
        font-size: 0.85rem;
    }

    .cause-value {
        font-size: 1.4rem;
        font-weight: 800;
        color: #172033;
        margin-top: 0.3rem;
    }

    /* Evidence */
    .evidence-card {
        background: #fff7ed;
        border: 1px solid #fed7aa;
        border-radius: 14px;
        padding: 1.2rem;
    }

    .evidence-title {
        font-size: 1.1rem;
        font-weight: 750;
        color: #9a3412;
    }

    /* Finding cards */
    .finding {
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 12px;
        padding: 0.9rem 1rem;
        margin-bottom: 0.6rem;
        box-shadow: 0 2px 8px rgba(15, 23, 42, 0.04);
    }

    .finding strong {
        color: #172033;
    }

    /* Recommendation */
    .recommendation-card {
        background: white;
        border: 1px solid #dbeafe;
        border-radius: 15px;
        padding: 1.3rem;
        box-shadow: 0 4px 15px rgba(37, 99, 235, 0.08);
    }

    /* Footer */
    .footer {
        text-align: center;
        color: #64748b;
        font-size: 0.8rem;
        padding-top: 2rem;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: #ffffff;
        border-right: 1px solid #e5e7eb;
    }

    /* Buttons */
    .stButton > button {
        width: 100%;
        border-radius: 10px;
        font-weight: 700;
        min-height: 45px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.write("### 📊 InsightPilot")

    st.write(
        "AI-powered business intelligence and "
        "evidence-aware decision support."
    )

    st.write("---")

    st.write("### 🧠 Agent Pipeline")

    st.write("🔹 Member 1 — What happened?")
    st.write("🔹 Member 2 — What might have caused it?")
    st.write("🔹 Member 3 — Can we trust the cause?")
    st.write("🔹 Member 4 — What should we do?")

    st.write("---")

    st.write("### ✨ Key Capability")

    st.info(
        "InsightPilot does not treat an uncertain "
        "root cause as a confirmed fact."
    )


# =========================================================
# HERO HEADER
# =========================================================

st.markdown(
    """
    <div class="hero">
        <div class="hero-title">📊 InsightPilot</div>
        <div class="hero-subtitle">
            From Data → Evidence → Decisions
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


st.write(
    "Transform business data into understandable insights, "
    "validated causes, and actionable recommendations."
)


# =========================================================
# USER QUESTION
# =========================================================

st.markdown(
    '<div class="section-title">Ask InsightPilot</div>',
    unsafe_allow_html=True
)

question = st.text_area(
    "Business question",
    value=(
        "Why did sales decrease from May 2026 to June 2026, "
        "what are the possible causes, and what should the "
        "business do next?"
    ),
    height=110,
    label_visibility="collapsed"
)


analyze = st.button(
    "🔍 Analyze Business Performance",
    type="primary"
)


# =========================================================
# ANALYSIS
# =========================================================

if analyze:

    if not question.strip():

        st.warning("Please enter a business question.")

        st.stop()

    with st.spinner("Analyzing data and evaluating evidence..."):

        analysis = build_analysis_context()

        if not analysis["success"]:

            st.error(analysis["error"])

            st.stop()

        recommendation = generate_recommendation(
            analysis
        )

        if not recommendation["success"]:

            st.error(recommendation["error"])

            st.stop()

        response_text = run_insightpilot(
            question
        )


    # =====================================================
    # SUCCESS
    # =====================================================

    st.success(
        "✅ Analysis completed successfully"
    )


    # =====================================================
    # BUSINESS OVERVIEW
    # =====================================================

    st.markdown(
        '<div class="section-title">📈 Business Overview</div>',
        unsafe_allow_html=True
    )

    member1 = analysis["member1"]

    overall = member1.get(
        "overall_change",
        {}
    )

    previous_value = overall.get(
        "previous_value",
        0
    )

    current_value = overall.get(
        "current_value",
        0
    )

    absolute_change = overall.get(
        "absolute_change",
        0
    )

    percentage_change = overall.get(
        "percentage_change",
        0
    )

    previous_period = overall.get(
        "previous_period",
        "Previous"
    )

    current_period = overall.get(
        "current_period",
        "Current"
    )


    c1, c2, c3, c4 = st.columns(4)

    with c1:

        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-label">Sales Change</div>
                <div class="kpi-value kpi-negative">
                    ↓ {abs(percentage_change):.2f}%
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c2:

        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-label">{previous_period} Sales</div>
                <div class="kpi-value">
                    ${previous_value:,.2f}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c3:

        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-label">{current_period} Sales</div>
                <div class="kpi-value">
                    ${current_value:,.2f}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c4:

        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-label">Total Decrease</div>
                <div class="kpi-value kpi-negative">
                    ${abs(absolute_change):,.2f}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


    # =====================================================
    # ROOT CAUSE + EVIDENCE
    # =====================================================

    left, right = st.columns([1, 1])


    with left:

        st.markdown(
            '<div class="section-title">🎯 Possible Root Cause</div>',
            unsafe_allow_html=True
        )

        cause = recommendation.get(
            "candidate_cause",
            "Not identified"
        )

        st.markdown(
            f"""
            <div class="cause-card">
                <div class="cause-label">
                    Leading candidate
                </div>
                <div class="cause-value">
                    {cause}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


    with right:

        st.markdown(
            '<div class="section-title">🛡️ Evidence Validation</div>',
            unsafe_allow_html=True
        )

        validation_status = recommendation.get(
            "validation_status",
            "UNKNOWN"
        )

        reliability = recommendation.get(
            "reliability_level",
            "UNKNOWN"
        )

        score = float(
            recommendation.get(
                "reliability_score",
                0
            )
        )

        st.markdown(
            f"""
            <div class="evidence-card">
                <div class="evidence-title">
                    ⚠️ Evidence requires caution
                </div>
                <br>
                <b>Validation:</b> {validation_status}<br>
                <b>Reliability:</b> {reliability}<br>
                <b>Score:</b> {score:.1f}/100
            </div>
            """,
            unsafe_allow_html=True
        )

        st.progress(
            min(max(score / 100, 0.0), 1.0)
        )


    # =====================================================
    # IMPORTANT CAUTION
    # =====================================================

    if recommendation.get("status") == "CAUTION":

        st.warning(
            "⚠️ The possible root cause is NOT confirmed. "
            "Additional evidence should be collected before "
            "making major business decisions."
        )


    # =====================================================
    # KEY FINDINGS
    # =====================================================

    st.markdown(
        '<div class="section-title">🔎 Key Findings</div>',
        unsafe_allow_html=True
    )

    dimension_analysis = member1.get(
        "dimension_analysis",
        {}
    )


    findings = [
        ("North region", "region", "North"),
        ("South region", "region", "South"),
        ("Online channel", "channel", "Online"),
        ("Returning customers", "customer_type", "Returning"),
        ("Product B", "product", "Product B")
    ]


    for label, dimension, value in findings:

        results = dimension_analysis.get(
            dimension,
            {}
        ).get(
            "results",
            []
        )

        for item in results:

            item_value = str(
                item.get(
                    "value",
                    ""
                )
            )

            if item_value.lower() == value.lower():

                change = item.get(
                    "percentage_change",
                    0
                )

                st.markdown(
                    f"""
                    <div class="finding">
                        <strong>{label}</strong>
                        &nbsp;&nbsp;
                        <span>↓ {abs(change):.2f}%</span>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                break


    # =====================================================
    # AI RECOMMENDATION
    # =====================================================

    st.markdown(
        '<div class="section-title">🤖 Decision Support</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="recommendation-card">',
        unsafe_allow_html=True
    )

    st.text(response_text)

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )


    # =====================================================
    # NEXT STEPS
    # =====================================================

    st.markdown(
        '<div class="section-title">💡 Recommended Actions</div>',
        unsafe_allow_html=True
    )

    actions = [
        "Investigate historical inventory and stockout records.",
        "Analyze returning-customer behavior.",
        "Audit the online sales funnel.",
        "Review pricing, promotions, and seasonal demand.",
        "Check supplier delivery performance and product availability."
    ]


    for index, action in enumerate(actions, 1):

        st.markdown(
            f"""
            <div class="finding">
                <strong>{index}.</strong> {action}
            </div>
            """,
            unsafe_allow_html=True
        )


    # =====================================================
    # DECISION GUIDANCE
    # =====================================================

    st.markdown(
        '<div class="section-title">🧭 Decision Guidance</div>',
        unsafe_allow_html=True
    )

    st.info(
        "Prioritize investigation and targeted corrective "
        "actions rather than assuming inventory shortage is "
        "the sole cause of the overall sales decline."
    )


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
    <div class="footer">
        InsightPilot • AI-powered Business Decision Support
        <br>
        Evidence-aware • Explainable • Action-oriented
    </div>
    """,
    unsafe_allow_html=True
)