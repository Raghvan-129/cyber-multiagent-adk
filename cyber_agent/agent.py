from google.adk.agents import LlmAgent
from google.adk.models import Gemini
from google.adk.tools import AgentTool


def code_security_audit(code: str) -> str:
    """
    Lightweight static security check on code.
    Looks for eval/exec, broad SELECT, and possible hardcoded secrets.
    """
    issues = []
    lower = code.lower()
    if "eval(" in lower or "exec(" in lower:
        issues.append("use of eval/exec (remote code execution risk)")
    if "select *" in lower and "where" not in lower:
        issues.append("broad SELECT without filtering (data exposure risk)")
    if "password" in lower and ("=" in lower or "hardcode" in lower):
        issues.append("possible hardcoded credential")

    if not issues:
        return (
            "No obvious pattern‑based issues detected. "
            "This does NOT replace a full manual review."
        )
    return "Detected issues: " + ", ".join(issues)


# Research / general agent
research_agent = LlmAgent(
    name="ResearchAgent",
    model=Gemini(model="gemini-2.5-flash-lite"),
    instruction=(
        "You are a research specialist and general assistant. For any topic, "
        "use your browsing and reasoning ability to give a concise, accurate "
        "answer with 3–5 key bullet points and mention important sources."
    ),
)

# Cybersecurity mentor
security_agent = LlmAgent(
    name="SecurityAgent",
    model=Gemini(model="gemini-2.5-flash-lite"),
    instruction=(
        "You are an expert cybersecurity mentor. Explain attacks, defenses, "
        "network security, web security, blue‑team and red‑team concepts, and "
        "best practices in simple steps, with practical examples."
    ),
)

# Code audit specialist
code_audit_agent = LlmAgent(
    name="CodeAuditAgent",
    model=Gemini(model="gemini-2.5-flash-lite"),
    instruction=(
        "You are a secure code reviewer. Given code or pseudo‑code, first run "
        "the code_security_audit helper to catch obvious patterns, then add a "
        "deeper analysis. Identify specific vulnerabilities and show how to fix "
        "them with concrete code changes."
    ),
    tools=[code_security_audit],
)

# Calculator / reasoning agent
calculator_agent = LlmAgent(
    name="CalculatorAgent",
    model=Gemini(model="gemini-2.5-flash-lite"),
    instruction=(
        "You are a precise math and reasoning assistant. For any calculation, "
        "show the steps and give the final numeric answer."
    ),
)

# Root coordinator agent that ADK Web UI will expose
agent = LlmAgent(
    name="CyberCoordinator",
    model=Gemini(model="gemini-2.5-flash-lite"),
    instruction=(
        "You are a friendly, independent AI assistant with deep cybersecurity "
        "expertise. The user can ask ANYTHING.\n"
        "- For pure security questions, delegate to SecurityAgent.\n"
        "- For code review or 'audit this code', delegate to CodeAuditAgent.\n"
        "- For heavy calculations, delegate to CalculatorAgent.\n"
        "- For everything else, answer directly or delegate to ResearchAgent.\n"
        "Always give clear, step‑by‑step explanations, and keep answers concise."
    ),
    tools=[
        AgentTool(agent=research_agent),
        AgentTool(agent=security_agent),
        AgentTool(agent=code_audit_agent),
        AgentTool(agent=calculator_agent),
    ],
)
