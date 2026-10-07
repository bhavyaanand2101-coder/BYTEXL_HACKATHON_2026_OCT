"""
Pydantic API request and response schemas for CampusPulse v5.0.
"""

from __future__ import annotations

import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class ResponseMeta(BaseModel):
    config_hash: Optional[str] = None
    targets_hash: Optional[str] = None
    generated_at: str = Field(default_factory=lambda: datetime.datetime.utcnow().isoformat())
    request_id: Optional[str] = None


class ApiResponse(BaseModel):
    data: Any
    meta: ResponseMeta


class ErrorDetail(BaseModel):
    code: str
    message: str
    hint: Optional[str] = None


class ErrorEnvelope(BaseModel):
    error: ErrorDetail


class InterventionCreate(BaseModel):
    student_ref: str
    action_code: str
    notes: Optional[str] = None
    due_at: Optional[datetime.datetime] = None


class InterventionUpdate(BaseModel):
    status: Optional[str] = None
    notes: Optional[str] = None


class WhatIfOverride(BaseModel):
    indicator: str  # 'academic', 'attendance', 'placement', 'lms', 'engagement', 'skills'
    delta: Optional[float] = 0.0
    value: Optional[float] = None


class WhatIfRequest(BaseModel):
    student_ref: str
    overrides: List[WhatIfOverride]


class ChatRequest(BaseModel):
    query: str
    advisor_id: Optional[str] = None
