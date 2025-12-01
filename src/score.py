# src/score.py
from src.models import Incident

def score_incident(incident: Incident) -> Incident:
    """
    Apply simple heuristics to assign a risk score and severity.
    """
    score = 0

    # Rule 1: Brute force burst (many failed logins)
    if incident.action == "login_failed" and incident.count >= 3:
        score += 5

    # Rule 2: Admin account targeted
    if incident.user and incident.user.lower() == "admin":
        score += 5

    # Rule 3: Port scan or privilege escalation
    if incident.action in ["port_scan", "privilege_escalation"]:
        score += 4

    # Rule 4: Suspicious external IP (non-private ranges)
    if incident.ip and not incident.ip.startswith("192.168") and not incident.ip.startswith("10."):
        score += 3

    # Assign score and severity
    incident.score = score
    if score >= 8:
        incident.severity = "high"
    elif score >= 4:
        incident.severity = "medium"
    else:
        incident.severity = "low"

    return incident
