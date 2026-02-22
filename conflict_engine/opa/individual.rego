# Individual Layer
## Filters malformed requests
## Ensures urgency valid
## Ensures utility bounded
## Ensures timestamp exists

package policy.individual

default allow := false

allow if {
    valid_urgency
    valid_utility
    valid_timestamp
}

valid_urgency if {
    input.urgency >= 1
    input.urgency <= 10
}

valid_utility if {
    input.utility > 0
    input.utility <= 100
}

valid_timestamp if {
    input.timestamp > 0
}