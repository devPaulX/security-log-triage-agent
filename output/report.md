# Security Log Triage Report
Generated at: 2025-12-01 17:16:57.748681

## Summary Stats
- Total Events: 50
- Total Incidents: 36
- Severity Counts: {'low': 20, 'medium': 7, 'high': 9}

## Top Incidents
### Incident login_failed|server3|admin|198.51.100.23|2025-11-30 10:10
- Action: login_failed
- Host: server3
- User: admin
- IP: 198.51.100.23
- Count: 2
- Severity: high
- Evidence: ['Failed login attempt', 'Failed login attempt'] ...

### Incident login_failed|server6|eve|203.0.113.101|2025-11-30 10:40
- Action: login_failed
- Host: server6
- User: eve
- IP: 203.0.113.101
- Count: 3
- Severity: high
- Evidence: ['Failed login attempt', 'Failed login attempt', 'Failed login attempt'] ...

### Incident login_failed|server10|admin|198.51.100.23|2025-11-30 11:00
- Action: login_failed
- Host: server10
- User: admin
- IP: 198.51.100.23
- Count: 2
- Severity: high
- Evidence: ['Failed login attempt', 'Failed login attempt'] ...

### Incident login_failed|server10|admin|198.51.100.23|2025-11-30 11:10
- Action: login_failed
- Host: server10
- User: admin
- IP: 198.51.100.23
- Count: 1
- Severity: high
- Evidence: ['Failed login attempt'] ...

### Incident login_failed|server15|mike|198.51.100.99|2025-11-30 11:30
- Action: login_failed
- Host: server15
- User: mike
- IP: 198.51.100.99
- Count: 3
- Severity: high
- Evidence: ['Failed login attempt', 'Failed login attempt', 'Failed login attempt'] ...

## Recommendations
- Investigate high severity incidents immediately.
- Review medium severity incidents for potential escalation.
- Low severity incidents can be monitored or ignored.