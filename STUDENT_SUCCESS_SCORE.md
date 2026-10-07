# Student Success Score & Risk Identification Framework
> **Technical & Methodology Note — CampusPulse v5.0**  
> **KPMG in India Hackathon Deliverable**

---

## 1. Executive Summary & Philosophy

The **Student Success Score** is a composite metric designed to transition higher education institutions from passive observation to proactive, humane intervention. 

### Core Tenets:
1. **Support, Not Surveillance**: The framework isolates actionable barriers (e.g. low LMS participation or coding gaps) to recommend faculty coaching pathways.
2. **Deterministic & Explainable**: The scoring pipeline uses zero black-box runtime LLMs. Every point earned is a direct linear decomposition of auditable student achievements.
3. **CI-Audited Governance**: System parameters are calibrated against frozen baseline targets (`TARGETS.yaml`) with cryptographic SHA-256 integrity verification.

---

## 2. Key Indicators & Sub-Index Mathematics

The overall Student Success Score integrates six distinct dimensions:

$$\text{Success Score} = 0.25 \cdot I_{\text{academic}} + 0.20 \cdot I_{\text{attendance}} + 0.20 \cdot I_{\text{placement}} + 0.15 \cdot I_{\text{lms}} + 0.10 \cdot I_{\text{engagement}} + 0.10 \cdot I_{\text{skills}}$$

### Sub-Index Formulations:

| Indicator | Weight | Mathematical Formulation | Rationale |
| :--- | :---: | :--- | :--- |
| **Academic** ($I_{\text{acad}}$) | $25\%$ | $\text{clamp}(\text{CGPA} \times 10 - 3 \times \min(\text{backlogs}, 5), 0, 100)$ | Core academic baseline penalized for active backlog drag. |
| **Attendance** ($I_{\text{att}}$) | $20\%$ | $\text{clamp}(\mu_{\text{att}} - 5 \times N_{\text{sub} < 60\%}, 0, 100)$ | Penalizes localized subject absenteeism even if overall attendance seems acceptable. |
| **Placement** ($I_{\text{place}}$) | $20\%$ | $0.35 \cdot \text{Aptitude} + 0.40 \cdot \text{Coding} + 0.25 \cdot \text{MockInterview}$ | Direct placement readiness signal. Fallback to assessment sub-score when coding logs are absent. |
| **LMS Engagement** ($I_{\text{lms}}$) | $15\%$ | $0.50 \cdot \text{CompletionPct} + 0.50 \cdot \text{ScaledLogins}$ | Measures self-directed continuous learning habits. |
| **Campus Engagement** ($I_{\text{eng}}$) | $10\%$ | $\text{clamp}\left(\frac{\text{WinsorizedSum}(\text{events}, \text{clubs}, \text{hackathons}, \text{certs})}{20} \times 100, 0, 100\right)$ | Extracurricular differentiation winsorized at 95th percentile to prevent extreme outlier skew. |
| **Skills Profile** ($I_{\text{skills}}$) | $10\%$ | $0.60 \cdot \text{TechnicalAssessment} + 0.40 \cdot \text{SoftSkills}$ | Balanced technical competency and interpersonal readiness. |

---

## 3. Tier Decision Order & Hard Floor Protection

To ensure high-risk students never get lost in aggregate averages, tier classification follows a strict decision order:

1. **Hard Floor Trigger**:
   $$\text{Attendance} < 57\% \quad \lor \quad \text{CGPA} < 4.7 \quad \lor \quad \text{Backlogs} \ge 3 \implies \mathbf{Priority\ Support\ [PINNED]}$$
2. **Review Band**:
   $$57\% \le \text{Attendance} \le 63\% \quad \lor \quad 4.7 \le \text{CGPA} \le 5.3 \implies \mathbf{Review}$$
3. **Score Bands**:
   $$\begin{cases} 
   \text{Score} \ge 60 \implies \mathbf{On\ Track} \\
   40 \le \text{Score} < 60 \implies \mathbf{Watchlist} \\
   \text{Score} < 40 \implies \mathbf{Priority\ Support}
   \end{cases}$$

---

## 4. Exclusive Student Segmentation

Students are assigned to **exactly one mutually exclusive segment** per week following strict precedence:

1. **Struggling on All Fronts**: Tier = `priority_support` with $\ge 4$ sub-indices below cohort $p_{25}$.
2. **Academic Stars with Placement Gap**: High academic performance ($I_{\text{acad}} \ge 75$) but low coding/placement readiness ($I_{\text{place}} \le p_{25}$).
3. **Hustlers at Academic Risk**: High engagement ($I_{\text{eng}} \ge 75$) but academic index falling below cohort quartile ($I_{\text{acad}} < p_{25}$).
4. **Quietly Disengaged**: Adequate attendance ($I_{\text{att}} \ge 60\%$) but low LMS and engagement activity ($I_{\text{lms}}, I_{\text{eng}} < p_{25}$).
5. **Balanced**: Standard progression fulfilling institutional milestones.

---

## 5. Priority Action Ranking for Faculty Advisors

The advisor action list ranks students using a multi-factor urgency index:

$$\text{Priority Score} = (0.50 \cdot \text{Severity} + 0.25 \cdot \text{Actionability} + 0.25 \cdot \text{Urgency}) \times \text{MomentumBoost}$$

- **Pinned Hard-Floor Students**: Always guaranteed inclusion at the top of the advisor queue.
- **Actionability**: Rewards students whose primary risk factor corresponds to a concrete faculty intervention template (e.g., Attendance Check-in or Coding Practice Clinic).
- **Sub-30-Second Workflow**: Advisors see the student tier, top risk driver, and one-click intervention logging button immediately.
