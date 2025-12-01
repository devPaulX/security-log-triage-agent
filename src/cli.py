# src/cli.py
import typer
from pathlib import Path
from src.parser import load_events
from src.dedupe import group_events
from src.score import score_incident
from src.report import generate_report, render_markdown

app = typer.Typer()

@app.command()
def triage(input_file: str, output_file: str = "output/report.md"):
    """
    Run the full triage pipeline:
    parse logs -> group incidents -> score -> report.
    """
    # Step 1: Parse events
    events = load_events(input_file)

    # Step 2: Group into incidents
    incidents = group_events(events)

    # Step 3: Score incidents
    scored = [score_incident(inc) for inc in incidents]

    # Step 4: Generate report
    report = generate_report(scored)
    md_text = render_markdown(report)

    # Step 5: Save to file
    Path(output_file).write_text(md_text)
    typer.echo(f"Report generated: {output_file}")


if __name__ == "__main__":
    app()
