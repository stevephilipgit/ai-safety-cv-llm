from app.llm.reasoner import explain_violation

violation = {
    "type": "No Hard Hat",
    "severity": "High"
}

print(explain_violation(violation))
