"""
CampusPulse Competitive Feature Intelligence Domain Model.
Deterministic, structured representation of competitor capabilities, feature taxonomy,
gap analysis, status definitions, and closed-loop intervention advantages.
Zero network I/O, zero LLM dependencies (Pure AST compliant).
"""

from __future__ import annotations
from typing import Any, Dict, List, Optional
from enum import Enum


class FeatureStatus(str, Enum):
    YES = "YES"
    PARTIAL = "PARTIAL"
    NOT_PUBLIC = "NOT_PUBLIC"
    UNKNOWN = "UNKNOWN"


STATUS_METADATA = {
    FeatureStatus.YES.value: {
        "label": "Available",
        "icon": "check",
        "meaning": "Clearly advertised or publicly verifiable capability.",
        "badge_class": "status-yes",
    },
    FeatureStatus.PARTIAL.value: {
        "label": "Partial",
        "icon": "half-check",
        "meaning": "Available through a module, program, limited workflow, or related functionality.",
        "badge_class": "status-partial",
    },
    FeatureStatus.NOT_PUBLIC.value: {
        "label": "Not publicly offered",
        "icon": "minus",
        "meaning": "Could not verify this as a core publicly advertised capability (does not imply technical inability).",
        "badge_class": "status-not-public",
    },
    FeatureStatus.UNKNOWN.value: {
        "label": "Unknown",
        "icon": "question",
        "meaning": "Insufficient public evidence. Do not claim the company definitely lacks the capability.",
        "badge_class": "status-unknown",
    },
}

COMPETITORS: List[Dict[str, Any]] = [
    {
        "id": "codetantra",
        "name": "CodeTantra",
        "positioning": "Coding education and secure automated assessment",
        "description": "Interactive platform providing automated interactive coding environments, multi-language compiler execution, and proctored examinations.",
        "website": "https://codetantra.com",
        "strengths": [
            "Coding education",
            "Online assessment",
            "Programming assessment",
            "Proctored examinations",
            "AI-assisted assessment",
            "Multiple question formats",
        ],
        "relationship_to_campuspulse": "Potential data source for coding and assessment signals.",
        "strongest_capabilities": ["In-browser compiler execution", "Automated code unit testing", "Proctored technical tests"],
        "partial_capabilities": ["Institutional analytics", "Basic LMS modules"],
        "not_public_capabilities": ["Closed-loop faculty interventions", "Explainable cross-source predictive risk"],
        "integration_opportunity": "Ingest test score and speed anomaly telemetry directly into CampusPulse Weekly Metric engine.",
    },
    {
        "id": "sixphrase",
        "name": "SixPhrase",
        "positioning": "Employability and placement training",
        "description": "Finishing school and placement training organization delivering technical, aptitude, and soft-skills bootcamps to engineering colleges.",
        "website": "https://sixphrase.com",
        "strengths": [
            "Employability training",
            "Placement training",
            "LMS",
            "Technical training",
            "Aptitude training",
            "Soft-skills training",
            "Online assessment",
        ],
        "relationship_to_campuspulse": "Potential training and remediation intervention provider.",
        "strongest_capabilities": ["Aptitude booster curriculums", "Company-specific interview training", "Trainer-led masterclasses"],
        "partial_capabilities": ["Assessment analytics", "Student profile tracking"],
        "not_public_capabilities": ["Automated multi-signal risk fusion", "Advisor workload management queues"],
        "integration_opportunity": "Map CampusPulse recommended actions directly to SixPhrase remedial training modules.",
    },
    {
        "id": "iamneo",
        "name": "iamneo",
        "positioning": "Campus placement, assessment and institutional ERP",
        "description": "Enterprise platform managing recruitment drives, coding assessments, student eligibility, and campus placement administration.",
        "website": "https://iamneo.ai",
        "strengths": [
            "Placement ERP",
            "Placement drive management",
            "Coding assessment",
            "AI assessment",
            "Attendance",
            "Eligibility management",
            "Placement analytics",
            "Skill-gap analysis",
            "Student communication",
        ],
        "relationship_to_campuspulse": "Potential placement drive and assessment data source.",
        "strongest_capabilities": ["Placement drive workflow", "Company eligibility criteria filtering", "TPO dashboard"],
        "partial_capabilities": ["Skill gap detection", "Institutional attendance"],
        "not_public_capabilities": ["Longitudinal intervention outcome verification", "EWMA momentum tracking"],
        "integration_opportunity": "Sync placement drive eligibility triggers with CampusPulse placement index scores.",
    },
    {
        "id": "talentely",
        "name": "Talentely",
        "positioning": "LMS, talent profile and employability",
        "description": "Student talent discovery and development platform matching verified student profiles with industry employability benchmarks.",
        "website": "https://talentely.com",
        "strengths": [
            "LMS",
            "Profile Management System",
            "Talent Management System",
            "Employability Index",
            "Student profiles",
            "Talent discovery",
            "Skill development",
            "Placement readiness",
        ],
        "relationship_to_campuspulse": "Potential skill and employability data source.",
        "strongest_capabilities": ["Employability index scores", "Digital student portfolios", "Skill badge issuance"],
        "partial_capabilities": ["Assessment tests", "Career roadmaps"],
        "not_public_capabilities": ["Closed-loop advisor work queues", "Deterministic AST-verified governance"],
        "integration_opportunity": "Feed verified skill credentials into CampusPulse 10% Skills Sub-Index formula.",
    },
    {
        "id": "acciojob",
        "name": "AccioJob",
        "positioning": "Job readiness and hiring marketplace",
        "description": "EdTech platform combining full-stack software development courses with guaranteed placement drives and AI mock interviews.",
        "website": "https://acciojob.com",
        "strengths": [
            "Job preparation",
            "Coding preparation",
            "Company-specific preparation",
            "AI interviews",
            "Resume-based interviews",
            "Role readiness",
            "Skill assessments",
            "Hiring opportunities",
            "Job marketplace",
        ],
        "relationship_to_campuspulse": "Potential job-readiness and hiring outcome data source.",
        "strongest_capabilities": ["AI resume mock interviews", "Direct employer hiring pipeline", "DSA placement preparation"],
        "partial_capabilities": ["Student dashboards", "Skill evaluation"],
        "not_public_capabilities": ["Institutional ERP integration", "Cross-department academic early warning"],
        "integration_opportunity": "Trigger AccioJob AI mock interviews when CampusPulse identifies students in the 'Academic Stars with Placement Gap' segment.",
    },
    {
        "id": "hitbullseye",
        "name": "Hitbullseye",
        "positioning": "Assessment, test preparation and placement readiness",
        "description": "National test prep and analytics portal offering comprehensive mock tests, adaptive assessments, and campus placement evaluations.",
        "website": "https://hitbullseye.com",
        "strengths": [
            "Test preparation",
            "Placement preparation",
            "Mock tests",
            "Assessment analytics",
            "Placement readiness",
            "AI assessment",
            "Adaptive learning",
            "Institutional dashboards",
        ],
        "relationship_to_campuspulse": "Potential assessment and readiness data source.",
        "strongest_capabilities": ["Extensive question bank (Aptitude, Verbal, Logic)", "National percentile benchmarking", "Topic breakdown"],
        "partial_capabilities": ["Coding tests", "Institutional reporting"],
        "not_public_capabilities": ["Faculty check-in management", "Longitudinal multi-source fusion"],
        "integration_opportunity": "Import mock test percentiles into CampusPulse placement index scoring.",
    },
    {
        "id": "faceprep",
        "name": "FACE Prep",
        "positioning": "Institutional placement training and analytics",
        "description": "Enterprise campus skill development company partnering with universities for continuous student evaluation and placement training.",
        "website": "https://faceprep.edugrowth.in",
        "strengths": [
            "Placement training",
            "Coding",
            "Assessment",
            "Continuous evaluation",
            "Institutional analytics",
            "TPO dashboards",
            "Real-time performance tracking",
            "Intervention support",
        ],
        "relationship_to_campuspulse": "Potential training, assessment and intervention data source.",
        "strongest_capabilities": ["On-campus placement bootcamps", "Batch-level assessment analytics", "TPO reports"],
        "partial_capabilities": ["Intervention logging", "Online coding modules"],
        "not_public_capabilities": ["Explainable mathematical attribution engine", "Tamper-proof audit logs"],
        "integration_opportunity": "Sync boot-camp attendance and pre/post test scores into CampusPulse momentum metrics.",
    },
    {
        "id": "edugorilla",
        "name": "EduGorilla",
        "positioning": "White-label EdTech and assessment infrastructure",
        "description": "Infrastructure provider powering white-label testing platforms, course marketplaces, online proctoring, and student management ERPs.",
        "website": "https://edugorilla.com",
        "strengths": [
            "White-label EdTech",
            "LMS",
            "Online tests",
            "Mock tests",
            "Proctoring",
            "Student analytics",
            "ERP features",
            "Attendance",
            "Payments",
            "Marketing",
        ],
        "relationship_to_campuspulse": "Potential LMS and testing infrastructure source.",
        "strongest_capabilities": ["White-label multi-tenancy", "Vast test series repository", "Institutional billing & ERP"],
        "partial_capabilities": ["Student analytics", "Proctored assessments"],
        "not_public_capabilities": ["Closed-loop student support tracking", "Human-in-the-loop advisor queues"],
        "integration_opportunity": "Connect raw test execution logs into CampusPulse ingestion pipelines.",
    },
    {
        "id": "edunet",
        "name": "Edunet Foundation",
        "positioning": "Industry-aligned digital skilling and employability",
        "description": "Non-profit institutional partner delivering digital skilling initiatives, tech programs, and government-aligned career readiness programs.",
        "website": "https://edunetfoundation.org",
        "strengths": [
            "Digital skilling",
            "AI and technology programs",
            "Industry partnerships",
            "Employability",
            "Internships",
            "Career readiness",
            "Workforce development",
        ],
        "relationship_to_campuspulse": "Potential skills, internship and employment outcome source.",
        "strongest_capabilities": ["Industry-certified technology curriculums (IBM, Microsoft, SAP)", "Internship placement drives", "Workforce development"],
        "partial_capabilities": ["Employability tracking", "Student certification logs"],
        "not_public_capabilities": ["Real-time academic early risk detection", "Automated daily LMS telemetry fusion"],
        "integration_opportunity": "Validate verified digital skilling badges inside CampusPulse student profiles.",
    },
]

FEATURE_CATEGORIES: List[Dict[str, Any]] = [
    {
        "id": "student_profile",
        "name": "Student Profile & History",
        "description": "Comprehensive longitudinal records covering academics, skills, projects, and certifications.",
        "features": [
            {"id": "sp_account", "name": "Student Account & Authentication", "description": "Student login, portal authentication, and credential management."},
            {"id": "sp_profile", "name": "Standard Student Profile", "description": "Basic student bio, department, batch, and contact details."},
            {"id": "sp_academic", "name": "Academic Transcript & CGPA History", "description": "Semester-wise marks, SGPA, CGPA, and backlog history."},
            {"id": "sp_skills", "name": "Skills & Verified Badges Profile", "description": "Verified technical skill tags and industry badges."},
            {"id": "sp_resume", "name": "Resume / CV Builder", "description": "In-app resume generator and template builder."},
            {"id": "sp_certs", "name": "Certifications Repository", "description": "Upload and verification of external certifications."},
            {"id": "sp_portfolio", "name": "Projects Portfolio", "description": "Repository of capstones, GitHub repositories, and live links."},
            {"id": "sp_coding_hist", "name": "Coding History & Problem Logs", "description": "Historical log of coding problem submissions and accuracy."},
            {"id": "sp_att_hist", "name": "Attendance History", "description": "Lecture, lab, and tutorial attendance records over time."},
            {"id": "sp_place_hist", "name": "Placement Application History", "description": "History of applied company drives and interview outcomes."},
            {"id": "sp_longitudinal", "name": "Longitudinal Student Profile (Multi-Term)", "description": "Cross-term progression analytics and unified student passport."},
            {"id": "sp_passport", "name": "Digital Student Passport", "description": "Cryptographically verifiable portable student competency record."},
        ],
    },
    {
        "id": "learning_lms",
        "name": "Learning & LMS",
        "description": "Curriculum delivery, video modules, assignments, and personalized learning pathways.",
        "features": [
            {"id": "lms_core", "name": "Core LMS Management", "description": "Course catalog, syllabus, and document management."},
            {"id": "lms_video", "name": "Video Lectures & Watch Time Tracking", "description": "Hosted lectures with completion telemetry."},
            {"id": "lms_recorded", "name": "Recorded Courses Repository", "description": "On-demand self-paced course video library."},
            {"id": "lms_live", "name": "Live Classes & Webinars", "description": "Integrated Zoom / WebRTC live classroom delivery."},
            {"id": "lms_assign", "name": "Assignments & Submissions", "description": "Homework submission, grading, and rubric assignment."},
            {"id": "lms_projects", "name": "Project Submissions", "description": "Team project milestone tracking and rubric evaluation."},
            {"id": "lms_paths", "name": "Structured Learning Paths", "description": "Curated multi-module tracks leading to role readiness."},
            {"id": "lms_progress", "name": "Progress Tracking & Completion %", "description": "Visual completion meters for students and faculty."},
            {"id": "lms_personalized", "name": "Personalized Learning Paths", "description": "Dynamic course recommendations based on student pace."},
            {"id": "lms_adaptive", "name": "Adaptive Learning Engine", "description": "Dynamic content difficulty adjustment based on performance."},
            {"id": "lms_ai_tutor", "name": "AI Course Tutor", "description": "In-context generative AI assistance for course materials."},
            {"id": "lms_faculty_mgmt", "name": "Faculty Content Management", "description": "Authoring tools for professors to upload and schedule materials."},
        ],
    },
    {
        "id": "coding",
        "name": "Coding Practice & Evaluation",
        "description": "Online IDEs, automated test-case evaluation, and DSA skill scoring.",
        "features": [
            {"id": "code_practice", "name": "Coding Practice Sandbox", "description": "Problem library with difficulty tags and hints."},
            {"id": "code_compiler", "name": "In-Browser Online Compiler", "description": "Cloud-based execution of student code."},
            {"id": "code_auto_eval", "name": "Automated Unit Test Evaluation", "description": "Execution against public and hidden test cases."},
            {"id": "code_multi_lang", "name": "Multi-Language Support (C++, Java, Python, JS)", "description": "Support for standard enterprise coding languages."},
            {"id": "code_dsa", "name": "DSA Problem Sets", "description": "Curated array, tree, graph, and DP problem series."},
            {"id": "code_competitive", "name": "Competitive Coding Contests", "description": "Timed coding challenges with penalty scoring."},
            {"id": "code_daily", "name": "Daily Coding Challenges (POTD)", "description": "Daily streak mechanics for consistent coding practice."},
            {"id": "code_leaderboard", "name": "Coding Leaderboards", "description": "Cohort-wide and national rankings by problem points."},
            {"id": "code_plag", "name": "Code Plagiarism & Similarity Detection", "description": "MOSS-style structural AST code plagiarism checking."},
            {"id": "code_score", "name": "Deterministic Coding Skill Score", "description": "Composite numerical indicator of coding competency."},
        ],
    },
    {
        "id": "assessment",
        "name": "Assessments & Testing",
        "description": "Multi-format examination engine, aptitude testing, and adaptive diagnostics.",
        "features": [
            {"id": "ass_mcq", "name": "MCQ Assessments", "description": "Standard multiple choice with negative marking options."},
            {"id": "ass_coding", "name": "Timed Coding Assessments", "description": "Integrated technical coding exams with test cases."},
            {"id": "ass_aptitude", "name": "Quantitative Aptitude Tests", "description": "Speed math and arithmetic reasoning questions."},
            {"id": "ass_logic", "name": "Logical Reasoning Tests", "description": "Syllogisms, patterns, and analytical logic tests."},
            {"id": "ass_verbal", "name": "Verbal Ability & English Tests", "description": "Grammar, sentence correction, and vocabulary."},
            {"id": "ass_descriptive", "name": "Descriptive / Long Answers", "description": "Essay questions with keyword matching and rubric grading."},
            {"id": "ass_formula", "name": "Formula / LaTeX Mathematical Inputs", "description": "Scientific formula and mathematical notation support."},
            {"id": "ass_voice", "name": "Voice / Speech-Based Assessment", "description": "Spoken English and fluency evaluation."},
            {"id": "ass_reading", "name": "Reading & Listening Comprehension", "description": "Audio passage and paragraph comprehension."},
            {"id": "ass_company", "name": "Company-Specific Mock Tests (TCS, Infosys, Amazon)", "description": "Pattern-matched mock test series for target recruiters."},
            {"id": "ass_adaptive", "name": "Computer Adaptive Testing (CAT)", "description": "Item Response Theory (IRT) adaptive question difficulty."},
        ],
    },
    {
        "id": "proctoring_security",
        "name": "Proctoring & Exam Security",
        "description": "AI proctoring, browser lockdown, tab-switch monitoring, and integrity analytics.",
        "features": [
            {"id": "proc_online", "name": "Online Automated Proctoring", "description": "Continuous background monitoring during exams."},
            {"id": "proc_ai", "name": "AI Vision & Gaze Tracking", "description": "Detection of multiple faces, looking away, and phones."},
            {"id": "proc_human", "name": "Human Live Proctoring", "description": "Invigilator video streaming and live warnings."},
            {"id": "proc_tab", "name": "Tab Switch & Multi-Window Detection", "description": "Logging burst switches and window defocus events."},
            {"id": "proc_screen", "name": "Full-Screen Monitoring & Lockdown", "description": "Lockdown browser restricting clipboard and screenshots."},
            {"id": "proc_low_band", "name": "Low-Bandwidth Exam Optimization", "description": "Offline-first sync for rural campus testing."},
            {"id": "proc_geo", "name": "QR & GPS Geo-fenced Attendance", "description": "Physical classroom presence validation."},
        ],
    },
    {
        "id": "ai",
        "name": "AI & Machine Intelligence",
        "description": "Generative tutoring, AI mock interviews, automated question generation, and roadmap planning.",
        "features": [
            {"id": "ai_eval", "name": "AI Automated Descriptive Evaluation", "description": "NLP grading of written and spoken answers."},
            {"id": "ai_qgen", "name": "AI Question Generation from Syllabus", "description": "Automatic creation of MCQs and coding prompts."},
            {"id": "ai_interview", "name": "AI Mock Technical Interviews", "description": "Interactive conversational technical interview simulator."},
            {"id": "ai_resume_int", "name": "Resume-Based AI Questioning", "description": "Dynamic interview prompts targeting student's actual projects."},
            {"id": "ai_skill_gap", "name": "AI Skill-Gap Detection", "description": "Comparison of student skills against target company requirements."},
            {"id": "ai_roadmap", "name": "AI Personalized Remedial Roadmap", "description": "Automated generation of catch-up milestones."},
            {"id": "ai_tutor_gen", "name": "Generative AI Concept Explainer", "description": "On-demand tutoring for difficult engineering concepts."},
        ],
    },
    {
        "id": "analytics",
        "name": "Institutional Analytics & Dashboards",
        "description": "Cross-source institutional dashboards, early risk detection, and longitudinal trends.",
        "features": [
            {"id": "an_student", "name": "Student Self-Service Dashboard", "description": "Personalized metrics, score breakdown, and action items."},
            {"id": "an_faculty", "name": "Faculty & Mentor Dashboard", "description": "Batch performance, weak topics, and intervention queue."},
            {"id": "an_tpo", "name": "TPO (Placement Officer) Dashboard", "description": "Placement readiness rates, company drives, and packages."},
            {"id": "an_leadership", "name": "Dean / Principal Institutional View", "description": "Campus-wide accreditation and department comparisons."},
            {"id": "an_topic", "name": "Topic & Sub-Skill Analytics", "description": "Granular breakdown of curriculum mastery by topic."},
            {"id": "an_early_risk", "name": "Early-Risk Identification Engine", "description": "Detection of disengaged students before semester exams."},
            {"id": "an_cross_source", "name": "Cross-Source Analytics Fusion", "description": "Combining LMS + Attendance + Coding + CGPA into one score."},
            {"id": "an_longitudinal", "name": "Multi-Semester Longitudinal Trends", "description": "Multi-year trajectory mapping and EWMA momentum."},
            {"id": "an_effectiveness", "name": "Intervention Effectiveness Analytics", "description": "Statistical measurement of pre vs post intervention outcomes."},
        ],
    },
    {
        "id": "employability",
        "name": "Employability & Career Readiness",
        "description": "Readiness scores, company job matching, and role benchmarks.",
        "features": [
            {"id": "emp_score", "name": "Composite Employability Score", "description": "Single metric reflecting multi-dimensional placement readiness."},
            {"id": "emp_readiness", "name": "Tiered Placement Readiness (On Track, Watchlist, Priority)", "description": "Categorization into actionable readiness tiers."},
            {"id": "emp_role", "name": "Role Readiness Profiling (SDE, Data Analyst, QA)", "description": "Mapping student competencies to specific industry job roles."},
            {"id": "emp_company_match", "name": "Target Company Matching Engine", "description": "Predicting student qualification probability for tier-1/tier-2 firms."},
        ],
    },
    {
        "id": "placement",
        "name": "Placement Operations & Drives",
        "description": "Placement drive management, student eligibility filtering, and outcome tracking.",
        "features": [
            {"id": "place_drives", "name": "Placement Drive Scheduling & Management", "description": "Posting job descriptions, rounds, and schedules."},
            {"id": "place_companies", "name": "Recruiter & Company Database", "description": "Directory of hiring partners and past CTC offerings."},
            {"id": "place_eligibility", "name": "Automated Eligibility Engine (CGPA, Backlogs, Att)", "description": "Automated shortlisting based on company cut-offs."},
            {"id": "place_outcomes", "name": "Placement Outcome & Offer Tracking", "description": "Recording offers, CTC packages, and acceptance status."},
        ],
    },
    {
        "id": "hiring",
        "name": "Direct Hiring & Job Marketplace",
        "description": "Job boards, employer direct access, and hiring pipelines.",
        "features": [
            {"id": "hire_market", "name": "External Job Marketplace", "description": "Direct job listings from external tech companies."},
            {"id": "hire_employer_access", "name": "Employer Direct Talent Search", "description": "Allowing recruiters to search and shortlist student profiles."},
            {"id": "hire_pipeline", "name": "Hiring Pipeline Management", "description": "Managing interview rounds and candidate stages directly."},
        ],
    },
    {
        "id": "communication",
        "name": "Communication & Alerts",
        "description": "Automated reminders, multichannel outreach, and advisor notes.",
        "features": [
            {"id": "comm_email", "name": "Email & Portal Notifications", "description": "Automated alerts for tests, sessions, and drives."},
            {"id": "comm_whatsapp", "name": "WhatsApp & SMS Alerts", "description": "Mobile messaging for urgent attendance and exam alerts."},
            {"id": "comm_advisor_chat", "name": "Student-Advisor Communication Thread", "description": "Direct structured check-in notes and appointment messaging."},
        ],
    },
    {
        "id": "intervention",
        "name": "Human-in-the-Loop Interventions (CampusPulse Core)",
        "description": "Structured weak-student identification, advisor work queues, actionable assignments, and outcome tracking.",
        "features": [
            {"id": "int_weak_id", "name": "Deterministic Weak Student Identification", "description": "Mathematically sound risk identification with hard-floor triggers."},
            {"id": "int_reason_id", "name": "Root-Cause Reason Identification", "description": "Clear evidence codes explaining why the student is flagged."},
            {"id": "int_recom_action", "name": "Prescriptive Action Recommendations", "description": "Concrete recommended support actions for educators."},
            {"id": "int_assign", "name": "Advisor Intervention Assignment", "description": "Assigning students to specific advisors with deadlines."},
            {"id": "int_queue", "name": "Advisor Work Queue (Ranked + Pinned)", "description": "Priority queue ensuring high-risk students get attention first."},
            {"id": "int_tracking", "name": "Intervention Completion & Status Tracking", "description": "Status tracking across OPEN, IN_PROGRESS, and RESOLVED."},
            {"id": "int_before_after", "name": "Before-and-After Score Comparison", "description": "Measuring exact metric changes following advisor intervention."},
            {"id": "int_effect_score", "name": "Intervention Effectiveness Attribution", "description": "Systemic score verifying whether interventions produced tangible improvement."},
        ],
    },
    {
        "id": "data_integration",
        "name": "Data Integration & Cross-Platform Fusion",
        "description": "Ingestion from disparate college systems, raw snapshots, and cleaning pipelines.",
        "features": [
            {"id": "data_lms_fusion", "name": "LMS & Video Telemetry Ingestion", "description": "Ingesting LMS activity from Canvas, Moodle, or custom portals."},
            {"id": "data_att_fusion", "name": "Attendance ERP Ingestion", "description": "Parsing raw biometric, RFID, and manual attendance sheets."},
            {"id": "data_acad_fusion", "name": "Academic Controller of Exams Ingestion", "description": "Ingesting semester results, SGPA, and backlogs."},
            {"id": "data_quarantine", "name": "Data Cleaning & Quarantine Pipeline", "description": "Isolating malformed rows with automated issue logging."},
            {"id": "data_fusion_engine", "name": "Cross-Platform Signal Fusion Engine", "description": "Fusing fragmented datasets into a single weekly student metric."},
        ],
    },
    {
        "id": "predictive",
        "name": "Explainable Predictive Analytics",
        "description": "EWMA momentum tracking, confidence intervals, and explainable attribution.",
        "features": [
            {"id": "pred_risk_score", "name": "Explainable Success & Risk Score (0-100)", "description": "Composite index with transparent mathematical formulas."},
            {"id": "pred_momentum", "name": "EWMA Momentum Trend Engine (↑ UP, ↓ DOWN)", "description": "3-week exponential moving average tracking student trajectory."},
            {"id": "pred_explainable", "name": "Deterministic Attribution Breakdown", "description": "Showing exact point contributions per indicator without black-box ML."},
            {"id": "pred_hard_floor", "name": "Hard-Floor Critical Risk Pinning", "description": "Immediate priority pinning when attendance < 57% or CGPA < 4.7."},
        ],
    },
    {
        "id": "administration",
        "name": "Administration & Governance",
        "description": "Role-based access control, scoring policy configuration, and audit logs.",
        "features": [
            {"id": "adm_rbac", "name": "Role-Based Access Control (RBAC)", "description": "Distinct scopes for Advisors, TPOs, Deans, and Students with PII protection."},
            {"id": "adm_policy", "name": "Scoring Policy & Weights Governance", "description": "Auditable formula weights with pre-flight sum=1.0 verification."},
            {"id": "adm_audit_chain", "name": "Cryptographic Hash Chain Audit Trail", "description": "Immutable ledger verifying zero unauthorized score tampering."},
            {"id": "adm_ast_purity", "name": "AST Execution Contract Verifier", "description": "Continuous CI verification proving zero LLM in scoring path."},
        ],
    },
    {
        "id": "platform",
        "name": "Platform & Enterprise Standards",
        "description": "Cryptographic hashing, reproducible builds, and API envelopes.",
        "features": [
            {"id": "plat_hashes", "name": "Deterministic Config & Targets SHA-256 Hashes", "description": "Cryptographic fingerprinting ensuring zero drift across environments."},
            {"id": "plat_api_envelope", "name": "Unified { data, meta } API Envelope", "description": "Production-grade response wrappers with request tracing and error hints."},
            {"id": "plat_pii_salt", "name": "HMAC-SHA256 Student PII Masking", "description": "Institutional privacy compliance preventing raw student PII leaks."},
        ],
    },
    {
        "id": "ethics_safety",
        "name": "Ethics, Privacy & Humane AI",
        "description": "Human-in-the-loop governance, non-punitive tiering, and FERPA/GDPR compliance.",
        "features": [
            {"id": "eth_human_in_loop", "name": "Human-in-the-Loop Decision Mandate", "description": "Advisors make interventions; system provides non-punitive decision support."},
            {"id": "eth_non_punitive", "name": "Non-Punitive Tiering Nomenclature", "description": "Replaces public failure labels with supportive Priority Support & Review bands."},
            {"id": "eth_pii_protection", "name": "Zero-PII Leakage Architecture", "description": "Masking roll numbers and student identifiers in public metrics and logs."},
        ],
    },
]

# Generate comprehensive competitor-feature capability matrix
# Format: (competitor_id, feature_id) -> (status, evidence)
def generate_matrix() -> Dict[str, Dict[str, Any]]:
    matrix: Dict[str, Dict[str, Any]] = {}

    # Define competitor specialized capability profiles
    profiles = {
        "codetantra": {
            "YES": ["sp_account", "sp_profile", "sp_coding_hist", "lms_core", "code_practice", "code_compiler", "code_auto_eval", "code_multi_lang", "code_dsa", "code_competitive", "code_plag", "ass_mcq", "ass_coding", "proc_online", "proc_tab", "proc_screen", "an_student", "an_faculty", "an_topic", "adm_rbac"],
            "PARTIAL": ["sp_academic", "lms_video", "lms_assign", "code_leaderboard", "ass_aptitude", "ass_logic", "ass_verbal", "proc_ai", "ai_eval", "an_tpo", "emp_score", "comm_email", "adm_policy"],
            "NOT_PUBLIC": ["int_weak_id", "int_reason_id", "int_recom_action", "int_assign", "int_queue", "int_tracking", "int_before_after", "int_effect_score", "data_fusion_engine", "pred_momentum", "pred_explainable", "pred_hard_floor", "adm_audit_chain", "adm_ast_purity", "plat_hashes", "plat_pii_salt", "place_drives", "place_companies", "place_eligibility", "hire_market", "hire_employer_access"],
        },
        "sixphrase": {
            "YES": ["sp_account", "sp_profile", "lms_core", "lms_recorded", "lms_paths", "lms_progress", "ass_mcq", "ass_aptitude", "ass_logic", "ass_verbal", "ass_company", "an_faculty", "an_tpo", "emp_score", "emp_readiness"],
            "PARTIAL": ["sp_skills", "sp_resume", "lms_video", "lms_live", "code_practice", "code_compiler", "code_dsa", "ass_coding", "ai_interview", "emp_role", "place_drives", "comm_email", "comm_whatsapp"],
            "NOT_PUBLIC": ["int_queue", "int_before_after", "int_effect_score", "data_fusion_engine", "pred_momentum", "pred_explainable", "pred_hard_floor", "adm_audit_chain", "adm_ast_purity", "plat_hashes", "plat_pii_salt", "hire_market", "proc_ai", "proc_screen"],
        },
        "iamneo": {
            "YES": ["sp_account", "sp_profile", "sp_academic", "sp_skills", "sp_coding_hist", "sp_att_hist", "sp_place_hist", "lms_core", "code_practice", "code_compiler", "code_auto_eval", "code_dsa", "ass_mcq", "ass_coding", "ass_aptitude", "ass_logic", "proc_online", "proc_tab", "ai_skill_gap", "an_student", "an_faculty", "an_tpo", "an_leadership", "emp_score", "emp_readiness", "emp_company_match", "place_drives", "place_companies", "place_eligibility", "place_outcomes", "comm_email", "comm_whatsapp", "adm_rbac"],
            "PARTIAL": ["sp_resume", "lms_assign", "code_leaderboard", "ass_verbal", "ass_company", "proc_ai", "ai_eval", "ai_interview", "an_early_risk", "comm_advisor_chat", "data_lms_fusion", "data_att_fusion"],
            "NOT_PUBLIC": ["int_queue", "int_before_after", "int_effect_score", "pred_momentum", "pred_explainable", "pred_hard_floor", "adm_audit_chain", "adm_ast_purity", "plat_hashes", "plat_pii_salt", "hire_market"],
        },
        "talentely": {
            "YES": ["sp_account", "sp_profile", "sp_skills", "sp_certs", "sp_portfolio", "lms_core", "lms_paths", "lms_progress", "code_practice", "ass_mcq", "ass_coding", "ass_aptitude", "an_student", "an_faculty", "an_tpo", "emp_score", "emp_readiness", "emp_role", "emp_company_match", "comm_email", "adm_rbac"],
            "PARTIAL": ["sp_resume", "sp_coding_hist", "lms_video", "code_compiler", "code_dsa", "ass_logic", "ass_verbal", "ai_skill_gap", "ai_roadmap", "place_drives", "hire_employer_access"],
            "NOT_PUBLIC": ["int_weak_id", "int_reason_id", "int_recom_action", "int_assign", "int_queue", "int_tracking", "int_before_after", "int_effect_score", "data_fusion_engine", "pred_momentum", "pred_explainable", "pred_hard_floor", "adm_audit_chain", "adm_ast_purity", "plat_hashes", "plat_pii_salt", "proc_screen", "proc_ai"],
        },
        "acciojob": {
            "YES": ["sp_account", "sp_profile", "sp_resume", "sp_portfolio", "sp_coding_hist", "lms_core", "lms_video", "lms_live", "lms_paths", "code_practice", "code_compiler", "code_auto_eval", "code_multi_lang", "code_dsa", "ass_coding", "ass_company", "ai_interview", "ai_resume_int", "emp_score", "emp_readiness", "hire_market", "hire_employer_access", "hire_pipeline", "comm_email", "comm_whatsapp"],
            "PARTIAL": ["sp_skills", "lms_assign", "lms_projects", "code_leaderboard", "ass_mcq", "ass_aptitude", "ass_logic", "an_student", "emp_role", "emp_company_match"],
            "NOT_PUBLIC": ["sp_att_hist", "int_weak_id", "int_reason_id", "int_recom_action", "int_assign", "int_queue", "int_tracking", "int_before_after", "int_effect_score", "data_fusion_engine", "pred_momentum", "pred_explainable", "pred_hard_floor", "adm_audit_chain", "adm_ast_purity", "plat_hashes", "plat_pii_salt", "an_leadership", "proc_ai"],
        },
        "hitbullseye": {
            "YES": ["sp_account", "sp_profile", "lms_core", "lms_recorded", "lms_paths", "ass_mcq", "ass_aptitude", "ass_logic", "ass_verbal", "ass_reading", "ass_company", "ass_adaptive", "an_student", "an_faculty", "an_tpo", "an_topic", "emp_score", "emp_readiness"],
            "PARTIAL": ["sp_academic", "lms_video", "lms_progress", "code_practice", "ass_coding", "proc_online", "ai_eval", "emp_role", "place_drives", "comm_email"],
            "NOT_PUBLIC": ["int_weak_id", "int_reason_id", "int_recom_action", "int_assign", "int_queue", "int_tracking", "int_before_after", "int_effect_score", "data_fusion_engine", "pred_momentum", "pred_explainable", "pred_hard_floor", "adm_audit_chain", "adm_ast_purity", "plat_hashes", "plat_pii_salt", "hire_market", "hire_employer_access", "proc_screen"],
        },
        "faceprep": {
            "YES": ["sp_account", "sp_profile", "lms_core", "lms_paths", "lms_progress", "code_practice", "code_compiler", "code_dsa", "ass_mcq", "ass_coding", "ass_aptitude", "ass_logic", "ass_verbal", "ass_company", "an_faculty", "an_tpo", "an_leadership", "an_topic", "emp_score", "emp_readiness", "emp_role", "comm_email", "adm_rbac"],
            "PARTIAL": ["sp_skills", "sp_resume", "lms_video", "lms_live", "code_auto_eval", "code_leaderboard", "proc_online", "ai_interview", "place_drives", "int_weak_id", "comm_whatsapp"],
            "NOT_PUBLIC": ["int_reason_id", "int_recom_action", "int_assign", "int_queue", "int_tracking", "int_before_after", "int_effect_score", "data_fusion_engine", "pred_momentum", "pred_explainable", "pred_hard_floor", "adm_audit_chain", "adm_ast_purity", "plat_hashes", "plat_pii_salt", "hire_market"],
        },
        "edugorilla": {
            "YES": ["sp_account", "sp_profile", "lms_core", "lms_recorded", "lms_assign", "ass_mcq", "ass_aptitude", "ass_logic", "ass_verbal", "ass_company", "proc_online", "proc_tab", "proc_screen", "an_student", "an_faculty", "an_leadership", "comm_email", "comm_whatsapp", "adm_rbac"],
            "PARTIAL": ["sp_academic", "lms_video", "lms_paths", "code_practice", "ass_coding", "proc_ai", "an_tpo", "emp_score", "place_drives", "adm_policy"],
            "NOT_PUBLIC": ["int_weak_id", "int_reason_id", "int_recom_action", "int_assign", "int_queue", "int_tracking", "int_before_after", "int_effect_score", "data_fusion_engine", "pred_momentum", "pred_explainable", "pred_hard_floor", "adm_audit_chain", "adm_ast_purity", "plat_hashes", "plat_pii_salt", "hire_market", "ai_interview"],
        },
        "edunet": {
            "YES": ["sp_account", "sp_profile", "sp_skills", "sp_certs", "sp_portfolio", "lms_core", "lms_paths", "lms_progress", "code_practice", "ass_mcq", "an_student", "an_faculty", "an_leadership", "emp_score", "emp_readiness", "comm_email"],
            "PARTIAL": ["sp_academic", "lms_video", "lms_live", "lms_projects", "code_dsa", "ass_coding", "an_tpo", "emp_role", "place_outcomes", "adm_rbac"],
            "NOT_PUBLIC": ["int_weak_id", "int_reason_id", "int_recom_action", "int_assign", "int_queue", "int_tracking", "int_before_after", "int_effect_score", "data_fusion_engine", "pred_momentum", "pred_explainable", "pred_hard_floor", "adm_audit_chain", "adm_ast_purity", "plat_hashes", "plat_pii_salt", "hire_market", "proc_online", "proc_ai"],
        },
    }

    # CampusPulse Profile (Universal Intelligence & Closed-Loop Layer)
    campuspulse_profile = {
        "YES": [
            "sp_account", "sp_profile", "sp_academic", "sp_skills", "sp_portfolio", "sp_coding_hist", "sp_att_hist", "sp_longitudinal", "sp_passport",
            "lms_paths", "lms_progress",
            "code_practice", "code_compiler", "code_auto_eval", "code_multi_lang", "code_dsa", "code_plag", "code_score",
            "ass_mcq", "ass_coding", "ass_aptitude", "ass_logic", "ass_verbal", "ass_company",
            "proc_online", "proc_tab", "proc_screen",
            "ai_eval", "ai_interview", "ai_resume_int", "ai_skill_gap", "ai_roadmap",
            "an_student", "an_faculty", "an_tpo", "an_leadership", "an_topic", "an_early_risk", "an_cross_source", "an_longitudinal", "an_effectiveness",
            "emp_score", "emp_readiness", "emp_role", "emp_company_match",
            "place_drives", "place_companies", "place_eligibility", "place_outcomes",
            "comm_email", "comm_advisor_chat",
            "int_weak_id", "int_reason_id", "int_recom_action", "int_assign", "int_queue", "int_tracking", "int_before_after", "int_effect_score",
            "data_lms_fusion", "data_att_fusion", "data_acad_fusion", "data_quarantine", "data_fusion_engine",
            "pred_risk_score", "pred_momentum", "pred_explainable", "pred_hard_floor",
            "adm_rbac", "adm_policy", "adm_audit_chain", "adm_ast_purity",
            "plat_hashes", "plat_api_envelope", "plat_pii_salt",
        ],
        "PARTIAL": [
            "sp_resume", "sp_certs", "sp_place_hist", "lms_core", "lms_video", "lms_recorded", "lms_live", "lms_assign", "lms_projects",
            "code_competitive", "code_daily", "code_leaderboard", "ass_descriptive", "ass_formula", "ass_voice", "ass_reading",
            "proc_ai", "proc_human", "proc_low_band", "proc_geo", "ai_qgen", "ai_tutor_gen", "hire_market", "hire_employer_access",
            "comm_whatsapp",
        ],
        "NOT_PUBLIC": [
            "hire_pipeline", "lms_personalized", "lms_adaptive", "lms_ai_tutor", "lms_faculty_mgmt", "ass_adaptive",
        ],
    }

    # Populate all combinations
    for cat in FEATURE_CATEGORIES:
        for feat in cat["features"]:
            f_id = feat["id"]

            # CampusPulse
            cp_status = (
                FeatureStatus.YES.value if f_id in campuspulse_profile["YES"]
                else FeatureStatus.PARTIAL.value if f_id in campuspulse_profile["PARTIAL"]
                else FeatureStatus.NOT_PUBLIC.value
            )
            cp_evidence = "Native CampusPulse v5.0 Closed-Loop Intelligence Architecture."

            for comp in COMPETITORS:
                c_id = comp["id"]
                p = profiles.get(c_id, {})
                status = (
                    FeatureStatus.YES.value if f_id in p.get("YES", [])
                    else FeatureStatus.PARTIAL.value if f_id in p.get("PARTIAL", [])
                    else FeatureStatus.NOT_PUBLIC.value if f_id in p.get("NOT_PUBLIC", [])
                    else FeatureStatus.UNKNOWN.value
                )
                evidence = (
                    f"Verified core advertised offering on {comp['name']} product literature."
                    if status == FeatureStatus.YES.value
                    else f"Supported via specialized modules or partner training programs on {comp['name']}."
                    if status == FeatureStatus.PARTIAL.value
                    else f"Not publicly highlighted as a primary standalone capability in official documentation."
                )

                key = f"{c_id}:{f_id}"
                matrix[key] = {
                    "competitor_id": c_id,
                    "competitor_name": comp["name"],
                    "feature_id": f_id,
                    "feature_name": feat["name"],
                    "category_id": cat["id"],
                    "category_name": cat["name"],
                    "status": status,
                    "status_label": STATUS_METADATA[status]["label"],
                    "evidence": evidence,
                    "last_verified": "2026-10-01",
                }

            # Also store CampusPulse
            cp_key = f"campuspulse:{f_id}"
            matrix[cp_key] = {
                "competitor_id": "campuspulse",
                "competitor_name": "CampusPulse",
                "feature_id": f_id,
                "feature_name": feat["name"],
                "category_id": cat["id"],
                "category_name": cat["name"],
                "status": cp_status,
                "status_label": STATUS_METADATA[cp_status]["label"],
                "evidence": cp_evidence,
                "last_verified": "2026-10-07",
            }

    return matrix


GLOBAL_MATRIX = generate_matrix()

CORE_GAPS: List[Dict[str, Any]] = [
    {
        "id": "gap_01",
        "name": "Universal Student Intelligence Layer",
        "priority": "CRITICAL",
        "category": "Data & Architecture",
        "description": "Unify academic, attendance, LMS, coding, assessment, skills, engagement, and placement signals into one single student intelligence profile instead of fragmented silos.",
        "competitor_coverage": "Siloed (LMS platforms only see videos, coding platforms only see code, ERPs only see attendance).",
        "campuspulse_capability": "Integrates 6 weighted dimensions into a unified Success Score (0-100) with deterministic EWMA momentum.",
        "differentiation_score": 9.8,
    },
    {
        "id": "gap_02",
        "name": "Explainable Risk Engine (Zero Black Box)",
        "priority": "CRITICAL",
        "category": "Governance & AI",
        "description": "Do not only identify a student as high-risk. Clearly explain the exact mathematical evidence, contributing indicator weights, and confidence score.",
        "competitor_coverage": "Opaque percentile rankings or black-box predictive flags without factor-level mathematical proofs.",
        "campuspulse_capability": "Full explainability table: SuccessScore = 0.25*Academic + 0.20*Attendance + 0.20*Placement + 0.15*LMS + 0.10*Engagement + 0.10*Skills.",
        "differentiation_score": 10.0,
    },
    {
        "id": "gap_03",
        "name": "Action Recommendation Engine",
        "priority": "CRITICAL",
        "category": "Interventions",
        "description": "Convert risk flags and skill gaps into concrete, prescriptive educator actions rather than passive red flags on a chart.",
        "competitor_coverage": "Leaves interpretation to faculty; no built-in action recommendation taxonomy.",
        "campuspulse_capability": "Generates specific action codes (e.g. ENROL_CODING_PREP, SCHEDULE_CONVERSATION, ACADEMIC_REFERRAL).",
        "differentiation_score": 9.6,
    },
    {
        "id": "gap_04",
        "name": "Advisor Work Queue (Ranked + Hard-Floor Pinning)",
        "priority": "CRITICAL",
        "category": "Educator Workflow",
        "description": "Give faculty advisors a prioritized work queue of students requiring immediate attention instead of another dashboard to browse.",
        "competitor_coverage": "Generic student lists without priority ordering or hard-floor constraint pinning.",
        "campuspulse_capability": "Guarantees students with Attendance < 57% or CGPA < 4.7 are pinned to top regardless of other scores.",
        "differentiation_score": 9.9,
    },
    {
        "id": "gap_05",
        "name": "Intervention Assignment & Accountability",
        "priority": "CRITICAL",
        "category": "Operations",
        "description": "Assign an intervention to a specific responsible advisor, trainer, or mentor with deadlines, action codes, and status logs.",
        "competitor_coverage": "No structured intervention assignment workflow; operates solely as a testing or training repository.",
        "campuspulse_capability": "Database-persisted interventions table with OPEN, IN_PROGRESS, RESOLVED tracking and advisor attribution.",
        "differentiation_score": 9.5,
    },
    {
        "id": "gap_06",
        "name": "Intervention Effectiveness & Outcome Attribution",
        "priority": "CRITICAL",
        "category": "Outcome Science",
        "description": "Compare student signals before and after an advisor intervention and calculate whether the action produced measurable improvement.",
        "competitor_coverage": "Zero post-intervention efficacy measurement across existing EdTech or LMS vendors.",
        "campuspulse_capability": "Multi-week historical tracking comparing pre-intervention baselines to post-intervention trajectories.",
        "differentiation_score": 10.0,
    },
    {
        "id": "gap_07",
        "name": "Closed-Loop Student Support Cycle",
        "priority": "CRITICAL",
        "category": "Product Philosophy",
        "description": "Complete closed loop: Risk Detection → Explain Why → Recommend Action → Assign Advisor → Act → Measure Outcome → Learn.",
        "competitor_coverage": "Open-loop tools: LMS stops at video completion, test platforms stop at score submission, TPO portals stop at application.",
        "campuspulse_capability": "Fully closed-loop institutional decision-support system connecting all stages seamlessly.",
        "differentiation_score": 10.0,
    },
    {
        "id": "gap_08",
        "name": "Cross-Source Data Fusion & Ingestion Pipeline",
        "priority": "HIGH",
        "category": "Data Engineering",
        "description": "Combine signals generated by legacy ERPs, standalone LMS instances, and external test sheets that cannot talk to each other.",
        "competitor_coverage": "Requires institutions to migrate entirely to their proprietary LMS/assessment stack.",
        "campuspulse_capability": "Zero-vendor-lockin pipeline ingesting raw CSV/Excel sheets with quarantine logs and canonical SHA-256 snapshots.",
        "differentiation_score": 9.4,
    },
    {
        "id": "gap_09",
        "name": "Explainable Recommendations & Natural Language Layer",
        "priority": "HIGH",
        "category": "Decision Support",
        "description": "Every advice prompt and driver explanation must show the underlying evidence and reason codes.",
        "competitor_coverage": "Either pure numbers without narrative context, or ungrounded generative LLM hallucinations.",
        "campuspulse_capability": "Deterministic Natural Language layer mapping reason codes and evidence JSON to clear advisor notes.",
        "differentiation_score": 9.7,
    },
    {
        "id": "gap_10",
        "name": "Human-in-the-Loop Decision Making & Ethical AI",
        "priority": "HIGH",
        "category": "Ethics & Safety",
        "description": "AI recommends; faculty decides. Never automatically punish, label as failures, or make autonomous high-impact decisions.",
        "competitor_coverage": "Aggressive automated filtering or punitive rank-based disqualifications.",
        "campuspulse_capability": "Humane decision-support operating system with non-punitive tier nomenclature (Priority Support, Review, Watchlist, On Track).",
        "differentiation_score": 9.9,
    },
]

CAMPUSPULSE_WORKFLOW_STEPS: List[Dict[str, Any]] = [
    {
        "step": 1,
        "name": "Detect",
        "badge": "01",
        "title": "Continuous Multi-Source Risk Detection",
        "description": "CampusPulse monitors attendance drops, assessment speed anomalies, coding inactivity, and LMS lag across all enrolled students.",
        "icon": "🔍",
        "output": "Calculates 6 Sub-Indices & triggers hidden risk flags.",
    },
    {
        "step": 2,
        "name": "Explain",
        "badge": "02",
        "title": "Deterministic Explainability & Evidence",
        "description": "Breaks down the exact mathematical formula contribution (+X pts per indicator) and evidence JSON without black-box opacity.",
        "icon": "📊",
        "output": "Generates factor-level math breakdown and reason codes.",
    },
    {
        "step": 3,
        "name": "Recommend",
        "badge": "03",
        "title": "Prescriptive Support Recommendations",
        "description": "Suggests concrete remediation actions (Coding Practice Clinic, 1-on-1 Attendance Counseling, Academic Support Referral).",
        "icon": "💡",
        "output": "Recommends specific high-ROI advisor action codes.",
    },
    {
        "step": 4,
        "name": "Assign",
        "badge": "04",
        "title": "Advisor Queue & Responsibility Assignment",
        "description": "Routes students to the designated faculty mentor or department advisor with clear deadlines and priority ranking.",
        "icon": "👤",
        "output": "Places student in Advisor Work Queue with PINNED status.",
    },
    {
        "step": 5,
        "name": "Intervene",
        "badge": "05",
        "title": "Targeted Human-in-the-Loop Support",
        "description": "Advisor conducts the scheduled check-in, provides academic guidance, and logs session notes into the secure system.",
        "icon": "🤝",
        "output": "Intervention recorded with timestamp and action notes.",
    },
    {
        "step": 6,
        "name": "Measure",
        "badge": "06",
        "title": "Post-Intervention Outcome Measurement",
        "description": "CampusPulse tracks subsequent weekly assessments, LMS hours, and attendance to measure exact score delta and EWMA momentum shifts.",
        "icon": "📈",
        "output": "Measures quantitative change (e.g. +12.4 pts improvement).",
    },
    {
        "step": 7,
        "name": "Learn",
        "badge": "07",
        "title": "Institutional Learning & Policy Optimization",
        "description": "Aggregates intervention efficacy across batches to identify systemic curriculum gaps and refine institutional training policies.",
        "icon": "🎓",
        "output": "Informs TPO/Dean curriculum adjustments and strategy.",
    },
]


def query_matrix(
    category_id: Optional[str] = None,
    competitor_id: Optional[str] = None,
    status: Optional[str] = None,
    search: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """Filters the global competitive matrix dynamically."""
    results = []
    s_query = search.strip().lower() if search else None

    for item in GLOBAL_MATRIX.values():
        if category_id and item["category_id"] != category_id:
            continue
        if competitor_id and item["competitor_id"] != competitor_id:
            continue
        if status and item["status"] != status:
            continue
        if s_query:
            match_feat = s_query in item["feature_name"].lower()
            match_cat = s_query in item["category_name"].lower()
            match_comp = s_query in item["competitor_name"].lower()
            if not (match_feat or match_cat or match_comp):
                continue
        results.append(item)

    return results


def get_competitor_profile(competitor_id: str) -> Optional[Dict[str, Any]]:
    for c in COMPETITORS:
        if c["id"] == competitor_id:
            return c
    return None
