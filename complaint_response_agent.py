"""Complaint Resolution Agent — a LangChain agent that analyzes a customer
complaint, then drafts a professional, empathetic resolution response.

Setup: pip install -r requirements.txt, copy .env.example to .env, add your key.
Run:   python complaint_resolution_agent.py
"""

import logging
import os
import sys

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI

# ----------------------------------------------------------------------
# Setup
# ----------------------------------------------------------------------

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("complaint_resolution")

load_dotenv()
if not os.getenv("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY").startswith("sk-your"):
    logger.error("OPENAI_API_KEY not set. Copy .env.example to .env and add your key.")
    sys.exit(1)

llm = ChatOpenAI(model="gpt-4.1-mini", temperature=0.7)

# ----------------------------------------------------------------------
# Tools
# ----------------------------------------------------------------------

ANALYZE_PROMPT = PromptTemplate(
    input_variables=["complaint"],
    template="""You are an expert customer-care analyst.

Given the following customer complaint and service context, analyze it and
produce a structured complaint analysis.

Customer complaint and context: {complaint}

Identify:
- Core issue: what specifically went wrong
- Sentiment: how the customer feels (e.g., frustrated, angry, disappointed, calm)
- Requested outcome: what the customer wants (refund, replacement, apology, fix, etc.)
- Urgency: how time-sensitive this is (low, medium, high) and why
- Missing information: anything needed to fully resolve this that wasn't provided
- Response strategy: a brief recommendation on tone and approach for the reply

Return this as a clearly labeled analysis, nothing else.""",
)

DRAFT_RESPONSE_PROMPT = PromptTemplate(
    input_variables=["analysis"],
    template="""You are an experienced customer-care lead writing a reply to a customer.

Based on the following complaint analysis, draft a ready-to-send resolution response.

Complaint analysis:
{analysis}

Rules:
- Acknowledge the specific issue and how the customer feels — sound human, not scripted
- Never blame the customer or be defensive
- Explain clear next steps, including realistic timelines where relevant
- Do NOT make unsupported promises (no guarantees you can't back up, no specific
  amounts/dates unless they were explicitly given in the analysis)
- If information is missing, politely ask for it as part of the next steps
- Keep a warm, professional, empathetic tone throughout
- Include a short subject line, greeting, body, and sign-off

Return ONLY the final customer-facing response, nothing else.""",
)


@tool
def analyze_customer_complaint(complaint: str) -> str:
    """Analyze a customer complaint and service context to identify the core issue,
    sentiment, requested outcome, urgency, and missing information. Use this FIRST."""
    logger.info("[analyze_customer_complaint] analyzing complaint")
    return llm.invoke(ANALYZE_PROMPT.format(complaint=complaint)).content


@tool
def draft_resolution_response(analysis: str) -> str:
    """Draft a professional, empathetic resolution response from a complaint analysis.
    Use AFTER analyze_customer_complaint."""
    logger.info("[draft_resolution_response] drafting resolution response")
    return llm.invoke(DRAFT_RESPONSE_PROMPT.format(analysis=analysis)).content


# ----------------------------------------------------------------------
# Agent
# ----------------------------------------------------------------------

SYSTEM_PROMPT = """Act as an experienced customer-care lead. Your job is to help
resolve customer complaints with professional, empathetic responses.

When given a customer complaint, follow these steps:
1. First, use the analyze_customer_complaint tool to identify the core issue,
   sentiment, requested outcome, urgency, and missing information.
2. Then, use the draft_resolution_response tool to acknowledge the issue,
   explain next steps, and avoid unsupported promises.
3. Return the final resolution response to the user.

Always use both tools in order: analyze first, then draft. Always sound human,
and never blame the customer."""

agent = create_agent(
    model=llm,
    tools=[analyze_customer_complaint, draft_resolution_response],
    system_prompt=SYSTEM_PROMPT,
)


def run_complaint_resolution(complaint: str) -> str:
    """Run the agent on a customer complaint and return the resolution response."""
    result = agent.invoke({"messages": [HumanMessage(content=complaint)]})
    return result["messages"][-1].content


# ----------------------------------------------------------------------
# CLI
# ----------------------------------------------------------------------

def main() -> None:
    print("\nCOMPLAINT RESOLUTION AGENT (LangChain + OpenAI)")
    print("Describe the customer complaint and service context. Type 'quit' to exit.\n")

    while True:
        complaint = input("Customer complaint: ").strip()
        if not complaint:
            continue
        if complaint.lower() in ("quit", "exit", "q"):
            break

        try:
            response = run_complaint_resolution(complaint)
            print("\n" + "=" * 60)
            print(response)
            print("=" * 60 + "\n")
        except Exception as e:
            logger.error("Agent failed: %s", e)


if __name__ == "__main__":
    main()