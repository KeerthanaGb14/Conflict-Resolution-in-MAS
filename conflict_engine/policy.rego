package conflict

default allow = false

# Example: resource capacity rule
allow {
    input.total_resource >= total_requested
}

total_requested = sum([r.utility | r := input.requests[_]])

# Example: max urgency limit
allow {
    all_valid
}

all_valid {
    not invalid_request
}

invalid_request {
    some i
    input.requests[i].urgency > 10
}