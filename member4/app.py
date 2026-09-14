import streamlit as st

from orchestrator import build_analysis_context
from recommendation import generate_recommendation
from agent import run_insightpilot


# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------

st.set_page_config(
    page_title="InsightPilot",
    page_icon="📊",
    layout="wide"
)


# ---------------------------------------------------------
# TITLE
# ---------------------------------------------------------

st.write("📊 InsightPilot")
st.write("AI-powered business analysis and decision support")


st.write(
    "InsightPilot analyzes sales changes, identifies possible causes, "
    "checks evidence reliability, and provides recommended next steps."
)


# ---------------------------------------------------------
# USER QUESTION
# ---------------------------------------------------------

question = st.text_area(
    "Ask InsightPilot",
    value=(
        "Why did sales decrease from May 2026 to June 2026, "
        "what are the possible causes, and what should the business do next?"
    ),
    height=100
)


# ---------------------------------------------------------
# ANALYZE BUTTON
# ---------------------------------------------------------

if st.button("🔍 Analyze", type="primary"):

    if not question.strip():
        st.warning("Please enter a question.")
        st.stop()

    with st.spinner("Analyzing business data..."):

        # Load Member 1, Member 2 and Member 3
        analysis = build_analysis_context()

        if not analysis["success"]:
            st.error(analysis["error"])
            st.stop()

        # Generate evidence-aware recommendation
        recommendation = generate_recommendation(analysis)

        if not recommendation["success"]:
            st.error(recommendation["error"])
            st.stop()

        # Run Member 4 final response
        response_text = run_insightpilot(question)


    # -----------------------------------------------------
    # MAIN RESPONSE
    # -----------------------------------------------------

    st.success("✅ Analysis completed!")

    st.write("🤖 InsightPilot Recommendation")

    st.text(response_text)


    # -----------------------------------------------------
    # EVIDENCE SUMMARY
    # -----------------------------------------------------

    st.write("Evidence Summary")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Validation Status",
            recommendation.get(
                "validation_status",
                "UNKNOWN"
            )
        )

    with col2:
        st.metric(
            "Reliability",
            recommendation.get(
                "reliability_level",
                "UNKNOWN"
            )
        )

    with col3:
        score = recommendation.get(
            "reliability_score",
            0
        )

        st.metric(
            "Evidence Score",
            f"{score}/100"
        )


    # -----------------------------------------------------
    # CANDIDATE CAUSE
    # -----------------------------------------------------

    st.write("Possible Root Cause")

    st.info(
        recommendation.get(
            "candidate_cause",
            "No candidate cause identified."
        )
    )


    # -----------------------------------------------------
    # CAUTION
    # -----------------------------------------------------

    if recommendation.get("status") == "CAUTION":

        st.warning(
            "⚠️ The possible root cause is NOT confirmed. "
            "Additional evidence should be collected before "
            "making major business decisions."
        )

    else:

        st.success(
            "The available evidence supports the recommended action."
        )


    # -----------------------------------------------------
    # RELIABILITY BAR
    # -----------------------------------------------------

    score = float(
        recommendation.get(
            "reliability_score",
            0
        )
    )

    st.write("Evidence Reliability")

    st.progress(
        min(max(score / 100, 0.0), 1.0)
    )


# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------

st.write("---")

st.write(
    "InsightPilot | Member 4 Decision Support Agent"
)