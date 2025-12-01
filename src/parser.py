# src/parser.py
import pandas as pd
from datetime import datetime
from typing import List
from src.models import Event

def load_events(file_path: str) -> List[Event]:
    """
    Load CSV logs and convert each row into an Event object.
    """
    df = pd.read_csv(file_path)

    events = []
    for _, row in df.iterrows():
        # Convert timestamp string to datetime
        ts = datetime.fromisoformat(row["timestamp"].replace("Z", "+00:00"))

        # Create Event object
        event = Event(
            timestamp=ts,
            source=row["source"],
            host=row["host"],
            user=row["user"],
            ip=row["ip"],
            action=row["action"],
            raw=row["raw"]
        )

        # Add coarse time bucket (5‑minute window)
        bucket = ts.strftime("%Y-%m-%d %H:%M")[:-1] + "0"
        event.bucket = bucket

        events.append(event)

    return events
