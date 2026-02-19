from explain import generate_explanation, hash_explanation

decision = {
    "target": "API_X",
    "winner": "A2",
    "losers": ["A1", "A3"],
    "reason": "higher fairness score",
    "timestamp": 1710000000
}

text = generate_explanation(decision)
hash_value = hash_explanation(text)

print("Explanation:", text)
print("Hash:", hash_value)
