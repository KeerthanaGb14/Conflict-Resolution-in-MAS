# Collective Layer
## Requires real conflict
## Prevents duplicate agent IDs
## Prevents rapid timestamp spam
## Blocks system shutdown states
## Allows scarcity escalation
## Does NOT block overload


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

valid_conflict if {
    count(input.requests) > 1
}

valid_requests if {
    every r in input.requests {
        r.urgency >= 1
        r.urgency <= 10
        r.utility > 0
        r.timestamp > 0
    }
}

no_duplicate_agents if {
    agent_ids := { r.agent_id | r := input.requests[_] }
    count(agent_ids) == count(input.requests)
}

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

system_locked if {
    input.system_state.locked == true
}

resource_disabled if {
    input.system_state.resource_disabled == true
}

resource_exists if {
    input.total_resource > 0
}