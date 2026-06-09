# Logistics Decision Intelligence Platform

> A **CrewAI Flow-powered multi-agent logistics decision system** for inventory, delivery, geospatial, and portfolio optimization. The platform combines deterministic supply-chain analytics, multi-LLM agent orchestration, reflection-based strategy validation, persistent SQLite memory, historical learning, product comparison, and a Gradio executive control deck.

---

## Project Snapshot

This project is an agentic decision-support platform for logistics operations. It uses a refined DataCo supply chain dataset to analyze inventory performance, delivery risk, route bottlenecks, and geospatial delay patterns, then converts those metrics into structured executive strategy playbooks through specialized CrewAI agents.

Unlike a conventional dashboard, the system does not stop at descriptive analytics. It generates recommendations, critiques them, revises them when needed, stores historical strategies, and compares product-level investment opportunities across saved runs.

---

## Architecture Diagram

![Logistics Decision Intelligence Platform Architecture](Architecture%20Diagram.png)

The diagram captures the full system design:

- Gradio control deck with five execution modes.
- CrewAI Flow engine with state initialization and routing.
- Parallel inventory and delivery/geospatial analytics branches.
- Synchronization barrier before strategic synthesis.
- Memory-aware strategist, critic agent, reflection router, and revision strategist.
- SQLite memory layer for persistent historical strategy storage.
- Comparison agent for portfolio-level investment analysis.
- Live telemetry and multi-LLM execution tiers.

---

## Screenshots And Deliverables

### Gradio Control Deck

> Five-mode decision interface for inventory analysis, delivery analysis, full optimization, product comparison, and historical memory exploration.

### Live Agent Telemetry

> Mode 3 and Mode 4 stream execution state with visible agent names, status badges, elapsed time, and live pipeline logs.

### Executive Playbook Output

> Final strategy reports include priority level, optimization goal, recommended actions, expected business impact, implementation risk, and stored JSON metadata.

### Architecture And Report

> The project includes a dedicated architecture diagram and a project report: `Project report- Logistics Decision Intelligence Platform.docx`.

---

## High-Level Workflow

```text
User selects product and mode
        |
        v
Gradio Control Deck
        |
        v
CrewAI Flow Engine
        |
        v
State Initialization
  - product selection
  - optimization type
  - memory context hydration
        |
        v
Router Node
  - inventory mode
  - delivery mode
  - full optimization mode
        |
        +------------------------------+
        |                              |
        v                              v
Inventory Analytics Branch      Delivery + Geo Branch
  - sales velocity                - shipping delays
  - profitability                 - late delivery risk
  - product performance           - route distance
  - category metrics              - affected regions
        |                              |
        v                              v
Inventory Analyst Agent          Route Analyst Agent
        |                              |
        +--------------+---------------+
                       |
                       v
             Synchronization Barrier
                       |
                       v
           Memory-Aware Strategist Agent
                       |
                       v
                 Critic Agent
                       |
                       v
              Reflection Router
               /             \
              /               \
      Approved                 Needs Revision
          |                         |
          v                         v
   Save Strategy             Revision Strategist
          |                         |
          +------------+------------+
                       |
                       v
              SQLite Memory Layer
                       |
                       v
             Executive Gradio Report
```

---

## Application Modes

| Mode | Name | Purpose |
|---|---|---|
| Mode 1 | Inventory Analysis | Isolated SKU inventory analytics, sales velocity, profitability, and inventory risk interpretation |
| Mode 2 | Delivery Optimization | Delivery delay, late shipment, route, and geospatial risk analysis |
| Mode 3 | Full Optimization | End-to-end strategy generation with parallel branches, memory, critique, revision, and final storage |
| Mode 4 | Product Comparison | Compare two saved product playbooks for ROI, risk, investment priority, and complexity |
| Mode 5 | Historical Explorer | Browse saved strategy runs and inspect archived JSON strategy records |

---

## Core Features

- **CrewAI Flow orchestration** - stateful flow with start node, router node, branch listeners, synchronization barrier, conditional reflection, and final persistence.
- **Multi-agent workflow** - specialized agents for inventory, route analysis, strategy synthesis, critique, revision, and portfolio comparison.
- **Multi-LLM architecture** - different LLM tiers are assigned to extraction, logistics reasoning, strategic synthesis, and validation workloads.
- **Deterministic analytics before LLM reasoning** - Pandas tools calculate concrete business metrics before agents generate narrative recommendations.
- **Parallel branch execution** - inventory and delivery/geospatial streams run as separate branches in full optimization mode.
- **Reflection and revision loop** - strategy drafts are reviewed by a critic agent and revised if the reflection router detects weaknesses.
- **Persistent memory** - SQLite stores every final strategy with product name, timestamp, insights, critique, and final playbook.
- **Delta reasoning** - historical strategies are loaded into future runs so recommendations can evolve instead of repeating baseline advice.
- **Portfolio comparison** - saved strategies can be compared across products for investment priority, ROI, implementation risk, and complexity.
- **Live execution telemetry** - Gradio displays running logs, elapsed time, and visible agent status during long workflows.
- **Structured outputs** - Pydantic models define the expected schema for metrics, insights, strategies, critiques, and comparisons.
- **Executive reporting UI** - results are formatted into readable Gradio markdown reports with final JSON available for inspection.

---

## Multi-LLM Cognitive Architecture

| Tier | Responsibility | Agent | Model Configured |
|---|---|---|---|
| Tier 1 | Analytical extraction and inventory interpretation | Inventory Analyst | `groq/llama-3.3-70b-versatile` |
| Tier 2 | Logistics reasoning and route interpretation | Route Analyst | `gemini/gemma-4-26b-a4b-it` |
| Tier 3 | Strategic synthesis and portfolio reasoning | Strategist / Revision / Comparison | `gemini/gemma-4-31b-it` |
| Tier 4 | Validation, critique, and risk detection | Critic Agent | `gemini/gemini-3.1-flash-lite` |

This division makes the architecture more realistic than a single-model system: lighter or cheaper models handle narrower analytical tasks, while stronger reasoning models handle synthesis and trade-off decisions.

---

## Analytics Layer

### InventoryAnalyticsTool

Calculates:

- Total units sold.
- Total sales.
- Average profit.
- Sales velocity.
- Product category.

### DeliveryAnalyticsTool

Calculates:

- Average actual shipping days.
- Average scheduled shipping days.
- Average delay days.
- Delay rate.
- High-risk shipment count.
- Shipment count.

### GeoAnalyticsTool

Calculates:

- Top delay region.
- Top delay country.
- Delayed shipment count.
- Average route distance using the Haversine formula.
- High-risk route percentage.

---

## Agent Responsibilities

| Agent | Role |
|---|---|
| Inventory Analyst | Converts inventory metrics into inventory classification, risk profile, observations, and recommendations |
| Route Analyst | Interprets delivery and geospatial metrics into logistics risk and route recommendations |
| Optimization Strategist | Synthesizes inventory, route, and memory context into an executive playbook |
| Strategy Reviewer | Critiques the strategy for weaknesses, missing assumptions, risk, and feasibility |
| Revision Strategist | Refines the strategy using critic feedback when revision is required |
| Supply Chain Portfolio Analyst | Compares saved product strategies and recommends where to invest resources |

---

## Data And Memory

### Dataset

The project uses:

```text
data/DataCoSupplyChainDatasetRefined_First_5000.csv
```

The project report describes the refined dataset as:

- 4,999 records.
- 58 features.
- 80 products.
- 41 categories.
- Inventory, delivery, and geospatial fields.

### SQLite Memory Layer

Saved strategy runs are stored in:

```text
memory/logistics_memory.db
```

Each memory record includes:

- Product name.
- Timestamp.
- Inventory insights.
- Delivery insights.
- Strategy draft.
- Critique.
- Final strategy.

---

## Tech Stack

| Component | Technology |
|---|---|
| Frontend | Gradio |
| Workflow Orchestration | CrewAI Flow |
| Agent Framework | CrewAI |
| Data Processing | Pandas, NumPy |
| Structured Schemas | Pydantic |
| Memory Store | SQLite |
| Environment Management | python-dotenv |
| Inventory LLM | Groq Llama 3.3 70B Versatile |
| Route LLM | Gemini / Gemma route reasoning model |
| Strategy LLM | Gemini / Gemma strategic synthesis model |
| Critic LLM | Gemini Flash Lite validation model |
| Language | Python |

---

## Project Structure

```text
logistics_optimizer/
|
|-- gradio_app.py        # Gradio control deck and UI event handlers
|-- README.md            # Project documentation
|-- requirements.txt     # Python dependencies
|-- run_integration_test.py
|-- test.py
|-- test_memory.py
|
|-- agents/              # CrewAI agent definitions
|   |-- inventory_analyst.py
|   |-- route_analyst.py
|   |-- strategist.py
|   |-- critic.py
|   |-- comparison_agent.py
|
|-- crews/               # Crew assembly wrappers
|   |-- inventory_crew.py
|   |-- route_crew.py
|   |-- strategy_crew.py
|   |-- critique_crew.py
|   |-- revision_crew.py
|   |-- comparison_crew.py
|
|-- flows/
|   |-- logistics_flow.py # CrewAI Flow router, branches, reflection, memory save
|
|-- tasks/               # Prompt/task definitions for each crew
|-- tools/               # Deterministic analytics tools
|-- models/              # Pydantic state and output schemas
|-- memory/              # SQLite strategy store
|-- services/            # Product catalog loader
|-- utils/               # Event logging and output normalization
|-- config/              # LLM configuration
|-- data/                # Refined DataCo supply chain dataset
```

---

## Getting Started

### 1. Create and activate a virtual environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 2. Install dependencies

```powershell
pip install -r requirements.txt
```

### 3. Configure environment variables

Create a `.env` file in the project root.

```env
GROQ_API_KEY=your_groq_api_key_here
GOOGLE_API_KEY=your_google_or_gemini_api_key_here
```

Depending on your CrewAI and LiteLLM provider setup, model names or environment variable names may need to be adjusted in `config/llms.py`.

### 4. Run the Gradio app

```powershell
python gradio_app.py
```

Open:

```text
http://127.0.0.1:7860
```

---

## Running Project Scripts

Run the full flow integration test:

```powershell
python run_integration_test.py
```

Inspect catalog and memory helpers:

```powershell
python test.py
```

Run portfolio comparison over saved strategies:

```powershell
python test_memory.py
```

---

## How The Reflection Loop Works

The project uses a strategist-critic-revision pattern:

1. The strategist creates an initial optimization playbook from inventory, route, geo, and memory context.
2. The critic reviews the strategy for weaknesses, hidden risks, missing considerations, and feasibility gaps.
3. The reflection router checks the approval status.
4. If approved, the strategy is saved directly.
5. If revision is needed, the revision strategist updates the playbook using critic feedback.
6. The final strategy is saved to SQLite and displayed in the dashboard.

This makes the system more robust than a single-pass LLM recommendation engine.

---

## How Memory-Aware Delta Reasoning Works

Before full optimization starts, the flow checks SQLite for prior strategy runs for the selected product.

If history exists, it is injected into the strategy task so the strategist can:

- Avoid repeating previous recommendations.
- Build on already suggested operational actions.
- Contrast current findings with earlier runs.
- Produce a more evolved recommendation over time.

This is one of the most important design choices in the project because it gives the platform a sense of historical continuity.

---

## Why This Project Is Useful

The platform is useful because it bridges the gap between analytics and executive action. Traditional dashboards show metrics; this system interprets those metrics, creates recommendations, challenges its own output, stores the result, and allows comparison across product opportunities.

Strong use cases include:

- Inventory risk triage.
- Delivery performance review.
- SKU-level logistics optimization.
- Regional bottleneck identification.
- Strategy review and revision.
- Historical strategy audit.
- Product investment prioritization.
- Executive decision support demos.

---

## Implementation Quality

This project demonstrates several mature implementation choices:

- Modular architecture across agents, tools, tasks, crews, flow, memory, services, and UI.
- Deterministic metric calculation before generative AI interpretation.
- Typed Pydantic contracts for key outputs.
- CrewAI Flow routing instead of a flat script.
- Parallel branch design for full optimization.
- Persistent memory and historical retrieval.
- Live UI telemetry for observability.
- Dedicated portfolio comparison mode.
- Separate project report and architecture diagram for presentation.

---

## Current Limitations

- The project is a prototype, not a production deployment.
- LLM model IDs and provider keys are configured directly in `config/llms.py`.
- Automated test coverage is still light.
- Recommendation quality is not benchmarked against human expert labels.
- The dataset is static and local rather than connected to a live ERP, WMS, or TMS.
- Error handling around missing API keys and unavailable model providers can be improved.
- Export features for PDF, Excel, or dashboard snapshots are not yet implemented.

---

## Future Roadmap

- Add `.env.example` and stronger startup validation.
- Add automated tests for analytics tools and memory behavior.
- Add dataset schema validation.
- Add charts for sales velocity, delay rate, route risk, and strategy history.
- Add report export to PDF, Markdown, JSON, and Excel.
- Add Docker support.
- Add deployment instructions.
- Add human approval gates for high-impact recommendations.
- Add confidence scores and recommendation evaluation metrics.
- Connect the system to live logistics data sources.

---

## Project Report

A companion project report is included:

```text
Project report- Logistics Decision Intelligence Platform.docx
```

The report describes:

- Problem statement.
- Dataset details.
- Flow-oriented multi-agent architecture.
- Multi-LLM cognitive architecture.
- Analytics layer.
- Reflection loop.
- Persistent memory.
- Product comparison.
- Executive reporting.

---

## Project Status

This is a functional applied-AI prototype and a strong portfolio project. It is especially compelling because it combines real analytics, agentic reasoning, memory, critique, revision, and an executive UI into one coherent logistics decision platform.

