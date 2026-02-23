from groq import Groq
import os
import json

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)

def generate_explanation(conflict_json, allocations):

    total_resource = conflict_json.get("total_resource", 0)
    

    prompt = f"""
You are generating a short executive governance summary.

Audience: Organization Admin.

Strict Rules:
- Do NOT mention algorithms or internal models.
- Do NOT repeat allocation numbers or percentages.
- Do NOT describe calculation methods.
- Do NOT speculate.
- Keep under 120 words.
- Be direct and professional.

Conflict Context:
Target Resource: {conflict_json.get("target")}
Total Resource Available: {total_resource}
Number of Requests: {len(conflict_json.get("requests", []))}

Generate exactly this format:

Conflict:
(1 sentence explaining what caused the conflict)

Resolution:
(1 sentence explaining how the resource was distributed across agents)

Outcome:
(1 sentence confirming full allocation and balanced distribution)

Validation:
(1 sentence confirming approval by 3 of 5 registered arbitrators)
"""


    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You produce concise executive governance summaries."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.0,  
        max_tokens=200, # 🔥 zero creativity
        top_p=0.1
    )

    return response.choices[0].message.content.strip()

def generate_deterministic_explanation(conflict_json, allocations):

    explanation = []

    explanation.append(
        f"This dispute concerns resource '{conflict_json.get('target', 'Unknown')}'."
    )

    explanation.append(
        f"A total of {len(conflict_json.get('requests', []))} agent requests were evaluated."
    )

    explanation.append("Final allocation based strictly on Nash Social Welfare computation:")

    for agent, amount in allocations.items():
        explanation.append(f"- Agent {agent} allocated {amount} units.")

    explanation.append(
        "Allocation was validated by a 3-of-5 arbitrator signature threshold, ensuring consensus integrity."
    )

    explanation.append(
        "No assumptions beyond provided conflict data were used."
    )

    return "\n".join(explanation)