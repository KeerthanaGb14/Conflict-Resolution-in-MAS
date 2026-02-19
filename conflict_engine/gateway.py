REQUIRED_REQUEST_FIELDS = [
    "agent_id",
    "request_type",
    "target",
    "utility",
    "urgency",
    "timestamp"
]


def validate_conflict(conflict_json: dict) -> None:
    """
    Validates incoming conflict JSON.
    Raises ValueError if invalid.
    """

    if "conflict_id" not in conflict_json:
        raise ValueError("Missing conflict_id")

    if "target" not in conflict_json:
        raise ValueError("Missing target")

    if "requests" not in conflict_json:
        raise ValueError("Missing requests list")

    if not isinstance(conflict_json["requests"], list):
        raise ValueError("Requests must be a list")

    for request in conflict_json["requests"]:
        for field in REQUIRED_REQUEST_FIELDS:
            if field not in request:
                raise ValueError(f"Missing field in request: {field}")
