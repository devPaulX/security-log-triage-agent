from src.models import Incident
from src.gemini import explain_incident
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

def score_incident(incident: Incident) -> Incident:
    """
    Apply simple heuristics to assign a risk score and severity.
    """
    logging.info(f"Scoring incident {incident.id} (action={incident.action}, user={incident.user}, count={incident.count}, ip={incident.ip})")

    score = 0

    # Rule 1: Brute force burst (many failed logins)
    if incident.action == "login_failed" and incident.count >= 3:
        score += 5
        logging.debug(f"Rule 1 applied: login_failed burst → +5")

    # Rule 2: Admin account targeted
    if incident.user and incident.user.lower() == "admin":
        score += 5
        logging.debug(f"Rule 2 applied: admin targeted → +5")

    # Rule 3: Port scan or privilege escalation
    if incident.action in ["port_scan", "privilege_escalation"]:
        score += 4
        logging.debug(f"Rule 3 applied: {incident.action} → +4")

    # Rule 4: Suspicious external IP (non-private ranges)
    if incident.ip and not incident.ip.startswith("192.168") and not incident.ip.startswith("10."):
        score += 3
        logging.debug(f"Rule 4 applied: external IP {incident.ip} → +3")

    # Assign score and severity
    incident.score = score
    if score >= 8:
        incident.severity = "high"
    elif score >= 4:
        incident.severity = "medium"
    else:
        incident.severity = "low"

    # Attach Gemini explanation for high severity
    if incident.severity == "high":
        try:
            incident.explanation = explain_incident(incident)
        except Exception as e:
            logging.error(f"Gemini explanation failed: {e}")
            incident.explanation = "Explanation unavailable due to API error."

    logging.info(f"Incident {incident.id} scored={incident.score}, severity={incident.severity}")
    return incident
