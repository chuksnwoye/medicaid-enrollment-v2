from pathlib import Path

import joblib
import pandas as pd
import streamlit as st


ARTIFACT = Path(__file__).resolve().parent / "artifacts" / "medicaid_caidnw.joblib"
LABELS = {
    "statefip": "State of residence", "empstat": "Employment status",
    "health": "Self-rated health", "sex": "Sex recorded by CPS", "race": "Race",
    "hispan": "Hispanic origin", "nativity": "Nativity", "marst": "Marital status",
    "educ": "Educational attainment", "citizen": "Citizenship",
    "age": "Age", "famsize": "Family size", "nchild": "Own children in household",
}


@st.cache_resource
def load_artifact():
    return joblib.load(ARTIFACT)


st.set_page_config(page_title="Medicaid Coverage Estimator")
st.title("Medicaid Coverage Estimator")
st.write("Estimate the probability of reported Medicaid coverage at interview.")
st.caption(
    "The model uses historical 2019 CPS-ASEC data for adults ages 18–64 "
    "screened at or below 138% of the federal poverty guideline using prior-year "
    "family income. Predictions are statistical estimates. Medicaid eligibility "
    "is determined separately by the program."
)

if not ARTIFACT.is_file():
    st.error("Run Medicaid_Enrollment_ML_V2.ipynb to create the local model artifact.")
    st.stop()

artifact = load_artifact()
with st.form("coverage"):
    entry = {}
    for field, options in artifact["choices"].items():
        entry[field] = st.selectbox(
            LABELS[field], list(options), format_func=options.__getitem__
        )
    entry["age"] = st.number_input(LABELS["age"], 18, 64, 40)
    entry["famsize"] = st.number_input(LABELS["famsize"], 1, 30, 1)
    entry["nchild"] = st.number_input(LABELS["nchild"], 0, 9, 0)
    submitted = st.form_submit_button("Estimate probability")

if submitted:
    row = pd.DataFrame([entry], columns=artifact["features"])
    probability = artifact["pipeline"].predict_proba(row)[0, 1]
    st.metric("Estimated coverage probability", f"{probability:.1%}")
    threshold = artifact["threshold"]
    classification = "Above threshold" if probability >= threshold else "Below threshold"
    st.caption(f"{classification} at the validation-selected cutoff of {threshold:.0%}.")
