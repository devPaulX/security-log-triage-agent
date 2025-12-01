from datetime import datetime
from typing import List
from src.models import Incident, Report
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

def generate_report(incidents: List[Incident]) -> Report:
    """
    Create a triage report summarizing incidents and stats.
    """
    logging.info(f"Generating report from {len(incidents)} incidents")

    # Calculate stats
    stats = {"low": 0, "medium": 0, "high": 0}
    for inc in incidents:
        stats[inc.severity] += 1
    logging.info(f"Severity breakdown: {stats}")

    # Sort incidents by score (highest first)
    top_incidents = sorted(incidents, key=lambda x: x.score, reverse=True)[:5]
    logging.info(f"Selected top {len(top_incidents)} incidents for report")

    # Recommendations (simple heuristics)
    recommendations = []
    if stats["high"] > 0:
        recommendations.append("Investigate high severity incidents immediately.")
    if stats["medium"] > 0:
        recommendations.append("Review medium severity incidents for potential escalation.")
    if stats["low"] > 0:
        recommendations.append("Low severity incidents can be monitored or ignored.")

    logging.info("Report generation complete")

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
    logging.info("Rendering report into Markdown format")

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
        md.append(f"- Evidence: {inc.evidence[:3]} ...")
        if inc.explanation:   # ✅ Added Gemini explanation without modifying existing fields
            md.append(f"- Gemini Explanation: {inc.explanation}")
        md.append("")  # blank line

    md.append("## Recommendations")
    for rec in report.recommendations:
        md.append(f"- {rec}")

    logging.info("Markdown rendering complete")
    return "\n".join(md)
