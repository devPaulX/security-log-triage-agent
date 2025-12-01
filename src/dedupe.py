from typing import List, Dict
from src.models import Event, Incident
from datetime import datetime
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

def group_events(events: List[Event]) -> List[Incident]:
    """
    Group similar events into incidents based on key fields.
    """
    logging.info(f"Starting grouping for {len(events)} events")
    incidents: Dict[str, Incident] = {}

    for event in events:
        # Build a grouping key (action + host + user + ip + bucket)
        key = f"{event.action}|{event.host}|{event.user}|{event.ip}|{event.bucket}"

        if key not in incidents:
            logging.debug(f"Creating new incident for key: {key}")
            incidents[key] = Incident(
                id=key,
                action=event.action,
                host=event.host,
                user=event.user,
                ip=event.ip,
                source=event.source,
                first_seen=event.timestamp,
                last_seen=event.timestamp,
                count=1,
                entities={"ip": [event.ip], "user": [event.user]},
                evidence=[event.raw],
            )
        else:
            inc = incidents[key]
            inc.count += 1
            inc.last_seen = max(inc.last_seen, event.timestamp)
            inc.evidence.append(event.raw)
            logging.debug(f"Updated incident {key}: count={inc.count}")

    logging.info(f"Generated {len(incidents)} incidents")
    return list(incidents.values())
