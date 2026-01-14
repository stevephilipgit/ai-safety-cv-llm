from langchain_ollama import OllamaLLM
from langchain_core.prompts import PromptTemplate
from typing import List, Dict

# ----------------- LLM INIT -----------------
llm = OllamaLLM(
    model="gemma:2b",
    temperature=0.2
)

# ----------------- CONTEXT PROMPT -----------------
SAFETY_CONTEXT_PROMPT = PromptTemplate(
    input_variables=["detected_ppe", "missing_ppe"],
    template="""
You are a workplace safety assistant.

A worker has been detected at a worksite.

Detected PPE:
{detected_ppe}

Missing PPE:
{missing_ppe}

Rules:
- Acknowledge PPE that is correctly worn
- Explain risks ONLY for missing PPE
- Do NOT invent violations
- Do NOT mention punishment, law, or compliance codes
- Be concise, clear, and professional

Provide:
1. Safety compliance summary
2. Why missing PPE is a safety risk
3. What should be done immediately
"""
)

# ----------------- AGGREGATED VIDEO PROMPT -----------------
AGGREGATED_PROMPT = PromptTemplate(
    input_variables=["violation", "count"],
    template="""
You are a workplace safety assistant.

Violation detected: {violation}
Occurrences across frames: {count}

Rules:
- Explain the safety risk clearly
- Explain what should be done immediately
- Do NOT mention punishment or law
- Be precise and professional
"""
)

# ----------------- IMAGE / FRAME LEVEL -----------------
def explain_safety_context(
    detected_ppe: List[str],
    missing_ppe: List[str]
) -> str:
    """
    Used for IMAGE or SINGLE VIDEO FRAME reasoning
    """

    detected = (
        "- " + "\n- ".join(detected_ppe)
        if detected_ppe else
        "None"
    )

    missing = (
        "- " + "\n- ".join(missing_ppe)
        if missing_ppe else
        "None"
    )

    prompt = SAFETY_CONTEXT_PROMPT.format(
        detected_ppe=detected,
        missing_ppe=missing
    )

    return llm.invoke(prompt).strip()


# ----------------- VIDEO SUMMARY -----------------
def explain_aggregated_violation(
    violation: str,
    frames: List[int]
) -> str:
    """
    Used for VIDEO SUMMARY (aggregated frames)
    """

    prompt = AGGREGATED_PROMPT.format(
        violation=violation,
        count=len(frames)
    )

    return llm.invoke(prompt).strip()
