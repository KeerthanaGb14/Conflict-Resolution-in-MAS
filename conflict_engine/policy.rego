package conflict

default allow := false

# Rule 1: Resource capacity constraint
allow if {
    input.total_resource >= total_requested
    all_valid
}

# Calculate total requested utility
# total_requested := sum([r.utility | r := input.requests[_]])

total_requested := sum([r.urgency | r := input.requests[_]])

# Ensure all requests are valid
all_valid if {
    not invalid_request
}

invalid_request if {
    some i
    input.requests[i].urgency > 10
}