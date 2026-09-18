# Complaint Resolution Agent - LangChain Single Agent Project

A beginner-friendly project that teaches you how to build a **single agent** using **LangChain + OpenAI**. The agent takes a raw customer complaint and drafts a professional, empathetic resolution response.

## What You'll Learn

- How LangChain works (LLMs, prompts, tools, agents)
- How to create tools using the `@tool` decorator
- How an agent decides which tools to call and in what order
- How `PromptTemplate` shapes LLM output
- How the agent's tool-calling loop works (think -> act -> observe -> repeat)

## How It Works
Customer complaint + service context

[Agent thinks: "I need to analyze this complaint first"]



[Tool: analyze_customer_complaint] --> identifies issue, sentiment,
requested outcome, urgency,
missing info


[Agent thinks: "Now I should draft the resolution response"]



[Tool: draft_resolution_response] --> acknowledges the issue, explains
next steps, avoids unsupported
promises



Final resolution response returned to user
## Prerequisites

- Python 3.10 or higher
- An OpenAI API key ([get one here](https://platform.openai.com/api-keys))

## Setup

### 1. Clone the repository

```bash
git 
cd Langchain_sample_project
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it:

- **Windows (PowerShell):**
```powershell
  .venv\Scripts\Activate
```
- **macOS / Linux:**
```bash
  source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up your API key

Copy the example env file and add your real key:

```bash
cp .env.example .env
```

Open `.env` and replace the placeholder with your actual OpenAI API key:
OPENAI_API_KEY=sk-your-actual-key-here


## Run

```bash
python complaint_resolution_agent.py
```

You'll see an interactive prompt:

COMPLAINT RESOLUTION AGENT (LangChain + OpenAI)
Describe the customer complaint and service context. Type 'quit' to exit.

Customer complaint:

Type the complaint (e.g., `My order arrived 2 weeks late and the item was damaged, I want a refund`) and the agent will analyze it and draft a resolution response. You'll also see a log line for each tool the agent calls.

## Example

**Input:**
My order #4521 arrived 2 weeks late and the item was damaged. I'm really
frustrated and just want a full refund, not a replacement.

**Output:**
Subject: Re: Order #4521 - Our Sincere Apologies

Hi there,

I'm really sorry to hear that your order arrived late and damaged — that's
not the experience we want for you, and I completely understand your
frustration.

I've gone ahead and flagged your request for a full refund to our support
team, and you can expect an update on the refund status within 2 business
days. In the meantime, if you have a moment, a quick photo of the damaged
item would help us speed things up on our end.

Thank you for your patience, and again, I'm sorry for the trouble this
has caused.

Best,
Customer Care Team


## Project Structure

├── complaint_resolution_agent.py # Main agent code

├── requirements.txt # Python dependencies

├── .env.example # API key template

├── .gitignore # Keeps secrets and venv out of git

└── README.md # This file



## Tech Stack

- [LangChain](https://python.langchain.com/) - Framework for building LLM applications
- [OpenAI GPT-4.1-mini](https://platform.openai.com/) - The LLM powering the agent
- [python-dotenv](https://pypi.org/project/python-dotenv/) - Environment variable management
