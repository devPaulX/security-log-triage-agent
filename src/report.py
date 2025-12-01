# src/report.py
from datetime import datetime
from typing import List
from src.models import Incident, Report

def generate_report(incidents: List[Incident]) -> Report:
    """
    Create a triage report summarizing incidents and stats.
    """
    # Calculate stats
    stats = {"low": 0, "medium": 0, "high": 0}
    for inc in incidents:
        stats[inc.severity] += 1

    # Sort incidents by score (highest first)
    top_incidents = sorted(incidents, key=lambda x: x.score, reverse=True)[:5]

    # Recommendations (simple heuristics)
    recommendations = []
    if stats["high"] > 0:
        recommendations.append("Investigate high severity incidents immediately.")
    if stats["medium"] > 0:
        recommendations.append("Review medium severity incidents for potential escalation.")
    if stats["low"] > 0:
        recommendations.append("Low severity incidents can be monitored or ignored.")

    return Report(
        generated_at=datetime.utcnow(),
        total_events=sum(inc.count for inc in incidents),
        total_incidents=len(incidents),
        stats=stats,
        top_incidents=top_incidents,
        recommendations=recommendations
    )


def render_markdown(report: Report) -> str:
    """
    Render the Report object into Markdown text.
    """
    md = []
    md.append(f"# Security Log Triage Report")
    md.append(f"Generated at: {report.generated_at}\n")
    md.append(f"## Summary Stats")
    md.append(f"- Total Events: {report.total_events}")
    md.append(f"- Total Incidents: {report.total_incidents}")
    md.append(f"- Severity Counts: {report.stats}\n")

    md.append("## Top Incidents")
    for inc in report.top_incidents:
        md.append(f"### Incident {inc.id}")
        md.append(f"- Action: {inc.action}")
        md.append(f"- Host: {inc.host}")
        md.append(f"- User: {inc.user}")
        md.append(f"- IP: {inc.ip}")
        md.append(f"- Count: {inc.count}")
        md.append(f"- Severity: {inc.severity}")
        md.append(f"- Evidence: {inc.evidence[:3]} ...\n")

    md.append("## Recommendations")
    for rec in report.recommendations:
        md.append(f"- {rec}")

    return "\n".join(md)
