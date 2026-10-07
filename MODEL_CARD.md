# Model Card: CampusPulse Supervised Disagreement Detector (`ml_layer`)

---

## 📌 Model Details

- **Model Name**: CampusPulse Disagreement Detector
- **Version**: 1.0.0-disabled
- **Type**: Supervised Linear Proxy / Disagreement Classifier
- **Default Status**: **DISABLED** (Deterministic Rules Layer is the primary authority)
- **Scoring Path Separation**: The model NEVER writes to `tier`, `priority`, `segment`, or `score`. It only annotates `confidence_note` and `ml_agreement_boolean`.

---

## 🛡️ Guardrails & Governance (G1–G8)

| Guardrail ID | Description | CI Enforcement |
| :--- | :--- | :--- |
| **G1** | ML output NEVER written to tier, priority, segment, or score | Verified by unit tests and domain purity rules |
| **G2** | ML output only writes `confidence_note` + `ml_agreement` | Enforced at layer return interface |
| **G3** | On disagreement: lower confidence by one level + 'review recommended' note | Automated in `ml_layer.py` |
| **G4** | Holdout AUC threshold $\ge 0.65$ | If $\text{AUC} < 0.65$, CI auto-disables feature flag |
| **G5** | Proxy bias check: tier distribution shift $\le 5\%$ across departments | CI validation on department/section proxies |
| **G6** | Temporal split enforcement ($t_{\text{train}} \le t_{\text{eval}}$) | Property testing via hypothesis |
| **G7** | Transparent coefficient disclosure | Published below when enabled |
| **G8** | Automatic failure fallback | Any G1–G7 violation automatically reverts flag to disabled |

---

## 📊 Feature Weights & Coefficients (Offline Drafted)

*When `ml_layer` is enabled:*
- Academic Index: `0.30`
- Attendance Index: `0.25`
- Placement Index: `0.25`
- LMS Index: `0.20`

---

## 🔒 Ethical Considerations & PII Protection
- Protected attributes (gender, caste, religion, socio-economic status) are **NEVER** collected or ingested.
- Department and section are used strictly as operational proxies to detect systematic evaluation divergence.
