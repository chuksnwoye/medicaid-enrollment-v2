# Predicting Medicaid Coverage at Interview

This portfolio project uses CPS-ASEC microdata to predict reported Medicaid coverage at interview among respondents ages 18–64 screened at or below 138% of the federal poverty guideline. The target is [CAIDNW](https://cps.ipums.org/cps-action/variables/CAIDNW). The model estimates coverage for a historical survey population. Legal Medicaid eligibility is determined separately.

[Open the executed notebook](Medicaid_Enrollment_ML_V2.ipynb) to see the evaluation tables, calibration plot, and permutation importance.

## Data and cohort

Use a local copy of the prepared Stata source `Maindata1.dta` with all fields listed in the notebook's data-loading cell. The source contains the IPUMS CPS ASEC fields for 2019–2020. An extract with different identification, family, or label coding may produce different results. The input is your responsibility to obtain and store locally. [IPUMS CPS](https://cps.ipums.org/cps/)

The final cohort restores adults who reported a disability and people coded as Armed Forces. The income screen uses prior-year family income and guideline year with interview-time family size and state. The main model uses interview demographics, employment, health, family composition, and state. Prior-year personal income is evaluated separately.

## Evaluation

The model compares a prevalence baseline, Logistic Regression, Random Forest, and Histogram Gradient Boosting. Related households and people stay together. The 2019 validation groups determine the model and threshold. The 2020 wave provides the held-out test. The notebook reports ROC-AUC, Brier score, precision, recall, F1, balanced accuracy, calibration, and validation permutation importance. It also reports a civilian test subset and ASEC-weighted estimates. The two-wave design and 2020 survey nonresponse limit generalization. [Census Bureau nonresponse study](https://www.census.gov/content/dam/Census/library/working-papers/2020/demo/sehsd-wp2020-10.pdf)

### Results

The selected Histogram Gradient Boosting model achieved 0.7710 ROC-AUC and 0.1894 Brier score on 2019 validation. The validation threshold was 0.35.

| 2020 holdout (14,979 records) | Value |
|---|---:|
| ROC-AUC | 0.7429 |
| Precision | 0.5709 |
| Recall | 0.7785 |
| F1 | 0.6588 |
| Balanced accuracy | 0.6751 |
| Brier score | 0.2021 |

The ASEC-weighted holdout ROC-AUC was 0.7544 and its Brier score was 0.1960. The earlier restricted-cohort benchmark reported 0.7361 ROC-AUC and 0.2001 Brier score on a different set of 12,645 test records. These evaluations describe different cohorts.

The evaluation fit and deployment fit are separate. The deployment pipeline refits the selected model on the combined 2019 development cohort after evaluation and preserves the validation-selected threshold.

## Run locally

From this folder, create and activate a local Python environment, then install the dependencies listed in requirements.txt.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
$env:MEDICAID_ASEC_DATA = 'C:\temp\Maindata1.dta'
python -m jupyterlab Medicaid_Enrollment_ML_V2.ipynb
```

Alternatively, place the source in `data/Maindata1.dta`. Run all notebook cells from this folder. The last cell creates and verifies `artifacts/medicaid_caidnw.joblib`. Load only locally generated or trusted joblib artifacts.

```powershell
python -m streamlit run app_v2.py
```

Raw data, virtual environments, caches, and generated model artifacts are excluded from Git.
