# Individual Layer
## Filters malformed requests
## Ensures urgency valid
## Ensures utility bounded
## Ensures timestamp exists

# Collective Layer
## Requires real conflict
## Prevents duplicate agent IDs
## Prevents rapid timestamp spam
## Blocks system shutdown states
## Allows scarcity escalation
## Does NOT block overload





##################################################
# ---------------- INDIVIDUAL -------------------
##################################################

package policy.individual

default allow := false

# Individual request must be structurally valid
allow if {
    valid_urgency
    valid_utility
    valid_timestamp
}

# Urgency must be between 1 and 10
valid_urgency if {
    input.urgency >= 1
    input.urgency <= 10
}

# Utility must be positive and bounded
valid_utility if {
    input.utility > 0
    input.utility <= 100
}

# Timestamp must be positive integer
valid_timestamp if {
    input.timestamp > 0
}



##################################################
# ---------------- COLLECTIVE -------------------
##################################################

package policy.collective

default allow := false

allow if {
    not system_locked
    not resource_disabled
    valid_conflict
    valid_requests
    no_duplicate_agents
    no_rapid_repeat
    resource_exists
}

##################################################
# ----- Conflict Structural Validation ----------
##################################################

# Must be real conflict (more than one request)
valid_conflict if {
    count(input.requests) > 1
}

# Defensive validation of each request
valid_requests if {
    every r in input.requests {
        r.urgency >= 1
        r.urgency <= 10
        r.utility > 0
        r.timestamp > 0
    }
}

##################################################
# ----- Duplicate Agent Protection --------------
##################################################

no_duplicate_agents if {
    agent_ids := { r.agent_id | r := input.requests[_] }
    count(agent_ids) == count(input.requests)
}

##################################################
# ----- Rapid Repeat Protection -----------------
##################################################

# Prevent same agent submitting multiple requests
# within a very small timestamp window (e.g., 5 seconds)

no_rapid_repeat if {
    not rapid_repeat_detected
}

rapid_repeat_detected if {
    some i
    some j
    i != j
    input.requests[i].agent_id == input.requests[j].agent_id
    abs(input.requests[i].timestamp - input.requests[j].timestamp) <= 5
}

##################################################
# ----- System State Checks ---------------------
##################################################

system_locked if {
    input.system_state.locked == true
}

resource_disabled if {
    input.system_state.resource_disabled == true
}

# Resource must exist (scarcity allowed, zero resource blocked)
resource_exists if {
    input.total_resource > 0
}