import hashlib

def generate_explanation(decision: dict) -> str:
    return(f"Agent {decision['winner']} received {decision['target']} "
           f"because {decision['reason']}")

def hash_explanation(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()

