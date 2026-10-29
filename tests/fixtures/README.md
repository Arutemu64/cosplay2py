# Observed response fixtures

`event_state.json`: `/api/events/get_event_state`, local browser HAR dated
2026-10-28. Role and event configuration were not independently recorded.
Only response field names, scalar types and nulls are retained; every non-null
value is replaced with a synthetic value. Request headers, URLs, identifiers and
all other capture contents are excluded. This is a historical contract example,
not evidence of current live behavior. Additional variants in unit tests are
synthetic and must not be described as captured responses.
