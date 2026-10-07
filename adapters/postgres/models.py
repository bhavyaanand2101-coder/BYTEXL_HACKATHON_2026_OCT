"""
SQLAlchemy database models adhering to CampusPulse v5.0 data contract.
Compatible with PostgreSQL 15+ and SQLite.
"""

from __future__ import annotations

import datetime
import uuid
from typing import Any, Dict, List, Optional

from sqlalchemy import (
    JSON,
    BigInteger,
    Boolean,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Table,
    Text,
)
from sqlalchemy.dialects.postgresql import ARRAY, JSONB, UUID
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


def gen_uuid() -> str:
    return str(uuid.uuid4())


class Student(Base):
    __tablename__ = "students"

    id = Column(String(36), primary_key=True, default=gen_uuid)
    student_ref = Column(String(64), unique=True, nullable=False, index=True)
    roll_number = Column(String(64), unique=True, nullable=True)
    name = Column(String(128), nullable=True)
    department = Column(String(32), nullable=False, default="CSE")
    batch = Column(String(32), nullable=False, default="CSE 2029")
    section = Column(String(32), nullable=False, default="UNKNOWN_SECTION")
    advisor_id = Column(String(36), ForeignKey("advisors.id"), nullable=True)
    is_quarantined = Column(Boolean, default=False)
    quarantine_reason = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    # Relationships
    advisor = relationship("Advisor", back_populates="students")
    weekly_metrics = relationship("WeeklyMetric", back_populates="student", cascade="all, delete-orphan")
    assessment_results = relationship("AssessmentResult", back_populates="student", cascade="all, delete-orphan")
    interventions = relationship("Intervention", back_populates="student", cascade="all, delete-orphan")
    flags = relationship("HiddenRiskFlag", back_populates="student", cascade="all, delete-orphan")


class Advisor(Base):
    __tablename__ = "advisors"

    id = Column(String(36), primary_key=True, default=gen_uuid)
    display_name = Column(String(128), nullable=False)
    email = Column(String(128), unique=True, nullable=False)
    department_scope = Column(JSON, nullable=False, default=list)  # Stored as JSON list for SQLite/PG compatibility
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    students = relationship("Student", back_populates="advisor")
    interventions = relationship("Intervention", back_populates="advisor")


class RawSnapshot(Base):
    __tablename__ = "raw_snapshots"

    id = Column(Integer, primary_key=True, autoincrement=True)
    source = Column(String(64), nullable=False)
    source_file = Column(String(128), nullable=False)
    sha256 = Column(String(64), nullable=False)
    captured_at = Column(DateTime, default=datetime.datetime.utcnow)
    payload = Column(JSON, nullable=False)
    is_duplicate = Column(Boolean, default=False)
    duplicate_of_sha256 = Column(String(64), nullable=True)


class CleaningLog(Base):
    __tablename__ = "cleaning_log"

    id = Column(Integer, primary_key=True, autoincrement=True)
    source = Column(String(64), nullable=False)
    source_file = Column(String(128), nullable=False)
    raw_row = Column(JSON, nullable=False)
    issue_type = Column(String(64), nullable=False)
    resolution = Column(String(128), nullable=False)
    logged_at = Column(DateTime, default=datetime.datetime.utcnow)


class WeeklyMetric(Base):
    __tablename__ = "weekly_metrics"

    id = Column(String(36), primary_key=True, default=gen_uuid)
    student_id = Column(String(36), ForeignKey("students.id"), nullable=False, index=True)
    week_number = Column(Integer, nullable=False, index=True)

    academic_index = Column(Float, nullable=False)
    attendance_index = Column(Float, nullable=False)
    placement_index = Column(Float, nullable=False)
    lms_index = Column(Float, nullable=False)
    engagement_index = Column(Float, nullable=False)
    skills_index = Column(Float, nullable=False)
    assessment_sub_score = Column(Float, nullable=True)

    success_score = Column(Float, nullable=False)
    momentum = Column(String(16), nullable=False, default="UNKNOWN")
    momentum_delta = Column(Float, nullable=True)
    tier = Column(String(32), nullable=False, index=True)
    segment = Column(String(64), nullable=False, index=True)
    confidence = Column(String(16), nullable=False, default="High")
    priority_score = Column(Float, nullable=False, default=0.0)

    reason_codes = Column(JSON, nullable=False, default=list)
    evidence_json = Column(JSON, nullable=False, default=dict)

    config_hash = Column(String(32), nullable=False)
    targets_hash = Column(String(32), nullable=False)
    score_version = Column(String(32), nullable=False, default="v5.0")
    generated_at = Column(DateTime, default=datetime.datetime.utcnow)

    student = relationship("Student", back_populates="weekly_metrics")


class AssessmentResult(Base):
    __tablename__ = "assessment_results"

    id = Column(String(36), primary_key=True, default=gen_uuid)
    student_id = Column(String(36), ForeignKey("students.id"), nullable=False, index=True)
    source_file = Column(String(128), nullable=False)
    total_score = Column(Float, nullable=False)
    tab_switches = Column(Integer, nullable=False, default=0)
    time_spent_min = Column(Float, nullable=False, default=0.0)
    plag_avg = Column(Float, nullable=False, default=0.0)
    multi_ip = Column(Boolean, default=False)
    speed_anomaly = Column(Boolean, default=False)
    integrity_flag = Column(Boolean, default=False)
    submission_at = Column(DateTime, default=datetime.datetime.utcnow)
    ip_list = Column(JSON, nullable=False, default=list)
    is_primary = Column(Boolean, default=True, index=True)

    student = relationship("Student", back_populates="assessment_results")


class HiddenRiskFlag(Base):
    __tablename__ = "hidden_risk_flags"

    id = Column(String(36), primary_key=True, default=gen_uuid)
    student_id = Column(String(36), ForeignKey("students.id"), nullable=False, index=True)
    week_number = Column(Integer, nullable=False)
    flag_code = Column(String(64), nullable=False)
    evidence_json = Column(JSON, nullable=False, default=dict)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    student = relationship("Student", back_populates="flags")


class Intervention(Base):
    __tablename__ = "interventions"

    id = Column(String(36), primary_key=True, default=gen_uuid)
    student_id = Column(String(36), ForeignKey("students.id"), nullable=False, index=True)
    advisor_id = Column(String(36), ForeignKey("advisors.id"), nullable=False)
    action_code = Column(String(64), nullable=False)
    notes = Column(Text, nullable=True)
    status = Column(String(32), nullable=False, default="OPEN")  # OPEN, IN_PROGRESS, RESOLVED
    due_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    student = relationship("Student", back_populates="interventions")
    advisor = relationship("Advisor", back_populates="interventions")


class FeedbackSignal(Base):
    __tablename__ = "feedback_signals"

    id = Column(String(36), primary_key=True, default=gen_uuid)
    student_id = Column(String(36), ForeignKey("students.id"), nullable=False)
    week_number = Column(Integer, nullable=False)
    signal_code = Column(String(64), nullable=False)
    value = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


class AuditLog(Base):
    __tablename__ = "audit_log"

    id = Column(Integer, primary_key=True, autoincrement=True)
    actor_id = Column(String(36), nullable=True)
    actor_role = Column(String(32), nullable=False, default="system")
    action = Column(String(64), nullable=False)
    target_type = Column(String(64), nullable=False)
    target_id = Column(String(36), nullable=True)
    metadata_json = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
