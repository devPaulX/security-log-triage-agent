import typer
from pathlib import Path
from src.parser import load_events
from src.dedupe import group_events
from src.score import score_incident
from src.report import generate_report, render_markdown
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

app = typer.Typer()

@app.command()
def triage(input_file: str, output_file: str = "output/report.md"):
    """
    Run the full triage pipeline:
    parse logs -> group incidents -> score -> report.
    """
    events = load_events(input_file)
    logging.info("Step 1 complete: Events loaded")

    incidents = group_events(events)
    logging.info("Step 2 complete: Incidents grouped")

    scored = [score_incident(inc) for inc in incidents]
    logging.info("Step 3 complete: Incidents scored")

    # Metrics: average score
    avg_score = sum(inc.score for inc in scored) / len(scored) if scored else 0
    logging.info(f"Average incident score: {avg_score:.2f}")

    report = generate_report(scored)
    md_text = render_markdown(report)
    logging.info("Step 4 complete: Report generated")

    # Metrics: totals and severity breakdown
    logging.info(f"Total events: {report.total_events}")
    logging.info(f"Total incidents: {report.total_incidents}")
    logging.info(f"Severity breakdown: {report.stats}")

    Path(output_file).write_text(md_text)
    logging.info(f"Step 5 complete: Report saved to {output_file}")
    typer.echo(f"Report generated: {output_file}")

if __name__ == "__main__":
    app()
