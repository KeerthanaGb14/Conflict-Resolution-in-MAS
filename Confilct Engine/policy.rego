package conflict

default allow = false

allow {
    input.utility + input.urgency - input.guilt > 10
}
