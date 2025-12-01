# src/models.py
from datetime import datetime
from typing import List, Dict, Optional
from pydantic import BaseModel, Field
from dataclasses import dataclass

class Event(BaseModel):
    """
    A single log entry, normalized to a consistent schema.
    """
    timestamp: datetime
    source: str                   # e.g., "auth", "firewall", "system"
    host: str                     # e.g., "server1"
    user: str                     # e.g., "alice" or "admin"
    ip: str                       # e.g., "192.168.1.10"
    action: str                   # e.g., "login_failed", "port_scan"
    raw: str                      # original message snippet

    # Helper: a coarse time bucket (e.g., 5 minutes) used for grouping
    bucket: Optional[str] = None  # set later by parser/deduper


class Incident(BaseModel):
    """
    A group of related events that represent one meaningful situation.
    """
    id: str                                     # stable key for the group
    action: str                                 # dominant action type
    host: str
    user: Optional[str] = None
    ip: Optional[str] = None
    source: Optional[str] = None
    first_seen: datetime
    last_seen: datetime
    count: int                                   # number of events grouped
    entities: Dict[str, List[str]] = Field(default_factory=dict)
    evidence: List[str] = Field(default_factory=list)  # short raw snippets
    score: int = 0                               # risk score (heuristics)
    severity: str = "low"                        # low/medium/high
    notes: Optional[str] = None                  # free-form summary
    explanation: str | None = None  # Gemini explanation

class Report(BaseModel):
    """
    The final triage output we’ll render to Markdown.
    """
    generated_at: datetime
    total_events: int
    total_incidents: int
    stats: Dict[str, int] = Field(default_factory=dict)  # e.g., {"low": 5, "med": 3, "high": 2}
    top_incidents: List[Incident] = Field(default_factory=list)
    recommendations: List[str] = Field(default_factory=list)  # next-step actions
