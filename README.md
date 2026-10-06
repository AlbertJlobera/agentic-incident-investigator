# Agentic Incident Investigator

An agentic AI system for investigating technical incidents in portfolio executions using **LangGraph**, LLM tool calling, log analysis, and technical documentation retrieval.

The project simulates an incident investigation workflow in which an AI agent autonomously decides which information it needs, analyzes execution history and logs, determines whether an incident exists, validates the suspected root cause against technical documentation, and generates a structured technical report.

## Overview

The system receives a portfolio investigation request and uses tools to inspect recent executions and their associated logs.

Instead of sending all available information to a single LLM call, the investigation is implemented as a **stateful LangGraph workflow**.

The agent can:

- Retrieve portfolio execution history.
- Inspect execution logs.
- Decide whether more information is required.
- Determine whether there is evidence of an incident.
- Stop early when the portfolio or logs cannot be found.
- Retrieve relevant technical documentation when an incident is detected.
- Validate the suspected root cause against known incidents and system documentation.
- Generate a structured final investigation report.

## Why LangGraph?

The investigation is not implemented as a single prompt containing executions, logs, and documentation.

LangGraph provides explicit control over the investigation workflow while maintaining state across the different steps.

This allows the system to separate:

- Agent reasoning and tool selection.
- Deterministic workflow decisions.
- Data retrieval.
- Incident classification.
- Documentation retrieval.
- Final report generation.

The graph structure also makes each stage easier to test, observe, debug, and evolve independently.

## Workflow

```text
START
  |
  v
AGENT <--------------------+
  |                        |
  | tool call              |
  v                        |
TOOLS ---------------------+
  |
  | investigation continues
  v
AGENT
  |
  +---- NO_INCIDENT ----------------------> END
  |
  +---- PORTFOLIO_NOT_FOUND --------------> END
  |
  +---- LOGS_NOT_FOUND -------------------> END
  |
  +---- INCIDENT_FOUND
            |
            v
   DOCUMENTATION_VALIDATION
            |
            v
      FINAL_SYNTHESIS
            |
            v
           END
```

The LLM agent controls which investigation tools should be called, while LangGraph controls the possible transitions between investigation states.

## Investigation States

The workflow currently supports the following states:

```text
INVESTIGATING
PORTFOLIO_NOT_FOUND
LOGS_NOT_FOUND
NO_INCIDENT
INCIDENT_FOUND
```

Some states are determined directly by tools when objective information is available, while the agent is responsible for determining whether the collected evidence indicates an incident.

## Tools

The agent currently has access to two tools:

### `get_portfolio_executions`

Retrieves recent executions associated with a portfolio.

Execution data includes information such as:

- Portfolio ID
- Execution ID
- Execution timestamp
- Execution status
- Engine
- Execution result

### `get_execution_logs`

Retrieves the technical logs associated with a specific execution.

The agent can inspect multiple executions and compare their logs before deciding whether an incident exists.

## Documentation Retrieval

When an incident is detected, the workflow generates a technical search query based on the investigation history.

Technical documentation is split by Markdown sections and indexed using a **BM25 retriever**.

The system retrieves the most relevant documentation related to the suspected root cause.

Documentation currently contains:

- Known incidents
- Equity engine behavior
- Troubleshooting procedures

This stage is intentionally separated from the agent tools because documentation validation is a mandatory workflow step after an incident has been detected.

## Final Report

When an incident is confirmed, the final synthesis node produces a structured technical investigation report containing:

### Probable Root Cause

The most likely explanation based on the collected evidence.

### Execution Evidence

Concrete evidence discovered during the investigation, including execution IDs, instruments, dates, warnings, and relevant values.

### Documentation Validation

Whether the retrieved technical documentation supports the suspected root cause.

### Recommended Next Action

Technical actions recommended to investigate or resolve the incident.

## Example

One of the simulated scenarios contains an equity valuation incident.

The agent identifies that:

```text
Requested valuation date: 2026-10-05
Received market price date: 2026-10-03
```

The execution logs show that the equity engine applied its configured fallback price and that the resulting portfolio valuation differed **18.7% from the previous close**.

The documentation retrieval stage finds a known incident related to stale market prices, allowing the final report to connect the execution evidence with the documented system behavior.

## Project Structure

```text
.
├── data/
│   ├── portfolio_executions.json
│   ├── execution_logs.txt
│   └── documentation/
│       ├── equity_engine.md
│       ├── known_incidents.md
│       └── troubleshooting.md
│
├── notebooks/
│   └── 01_agentic_incident_investigator.ipynb
│
├── src/
│   ├── libs/
│   │   ├── constants.py
│   │   └── utils.py
│   │
│   ├── prompts/
│   │   └── incident_prompts.py
│   │
│   ├── state.py
│   ├── tools.py
│   ├── llm.py
│   ├── nodes.py
│   ├── routers.py
│   └── graph.py
│
├── tests/
│   └── test_graph.py
│
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## Technologies

The project uses:

- Python
- LangGraph
- LangChain
- OpenAI API
- BM25 retrieval
- Pytest
- Markdown-based technical documentation

## Installation

Clone the repository and create a virtual environment:

```bash
python -m venv .venv
```

Activate the environment.

Windows:

```bash
.venv\Scripts\activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file based on `.env.example`:

```text
OPENAI_API_KEY=your_openai_api_key_here
```

## Testing

The project includes integration tests covering the main workflow paths.

Run:

```bash
pytest tests/test_graph.py -v
```

Current scenarios:

```text
PORT-483 -> INCIDENT_FOUND
PORT-221 -> NO_INCIDENT
PORT-999 -> PORTFOLIO_NOT_FOUND
PORT-555 -> LOGS_NOT_FOUND
```

The four workflow paths are validated through automated integration tests.

## Current Limitations

This is the first version of the project and intentionally keeps several components simple.

Current limitations include:

- Local simulated execution and log data.
- BM25-only documentation retrieval.
- Text-based incident classification contract between the LLM and the workflow.
- No persistent LangGraph checkpoints.
- No human-in-the-loop approval step.
- No production API or user interface.
- No evaluation or observability pipeline yet.

These limitations provide clear areas for future iterations of the project.

## Roadmap

Future versions may introduce:

- Structured LLM outputs.
- More advanced LangGraph state management.
- Human-in-the-loop workflows.
- Checkpointing and persistence.
- Improved error handling.
- Semantic or hybrid documentation retrieval.
- Agent evaluation and observability.
- LangSmith integration.
- Additional investigation tools.
- Production-oriented API deployment.

## Project Purpose

This project was developed as part of a practical learning path focused on **Agentic AI Engineering**.

The goal is not only to demonstrate LLM usage, but to explore how agentic systems can combine:

**LLM reasoning + tool calling + deterministic workflows + state management + retrieval + testing**

to solve multi-step technical investigation problems.