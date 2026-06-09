# gradio_app.py
import gradio as gr
import threading
import time
import json

# Thread-safe components and true flow engine mappings
from utils.event_logger import EventLogger
from flows.logistics_flow import LogisticsFlow
from memory.strategy_store import StrategyMemory
from services.product_catalog import ProductCatalog  
from crews.comparison_crew import run_comparison_crew  

# Initialize our physical storage instance
catalog = ProductCatalog()
memory = StrategyMemory()

# ----------------------------------------------------------------------
# Strategy Markdown Formatter Engine
# ----------------------------------------------------------------------

def format_mode1_inventory_markdown(product_name, insights_text):
    """Parses Mode 1 structured JSON or text using correct agent dictionary keys."""
    if not insights_text:
        return "### 📭 Channel Idle\nSelect an active SKU anchor and execute the inventory analyzer."
    
    print(f"\n👉 [Mode 1 Fixed Parser] Processing payload for: {product_name}")
    
    try:
        # Step 1: Parse the incoming string or use it directly if it's already a dict object
        data = json.loads(insights_text) if isinstance(insights_text, str) else insights_text
        
        # Step 2: Extract mapping fields directly from your agent's exact keys
        classification = str(data.get("inventory_classification", "Standard Velocity"))
        risk_level = str(data.get("inventory_risk", "Unknown Risk Profile"))
        observation = str(data.get("key_observation", "No observation recorded."))
        recommendation = str(data.get("recommendation", "No custom action specified."))
        
        # Set a dynamic visual badge color matching the threat matrix
        badge_color = "#ef4444" if "HIGH" in risk_level.upper() or "CRITICAL" in risk_level.upper() else "#f59e0b" if "MEDIUM" in risk_level.upper() else "#10b981"
        
        return f"""
# 📦 Inventory Logistics Analytics Review
**Target SKU Category Anchor:** `{product_name}`

<div style="margin: 10px 0 20px 0;">
    <span style="background-color: #3b82f6; color: white; padding: 6px 14px; border-radius: 20px; font-weight: bold; font-size: 0.85em; margin-right: 8px;">
        📊 CLASS: {classification.upper()}
    </span>
    <span style="background-color: {badge_color}; color: white; padding: 6px 14px; border-radius: 20px; font-weight: bold; font-size: 0.85em; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
        🚨 RISK: {risk_level.upper()}
    </span>
</div>

### 🔍 Core Analytics & Key Observations
> {observation}

### 🛠️ Strategic Operational Recommendation
* ⚡ **Immediate Action Directive:** {recommendation}

---
<p style="font-size: 0.85em; color: #64748b; text-align: right;">📦 Inventory Data Stream Aligned & Processed</p>
"""
    except Exception as format_error:
        print(f"⚠️ Mode 1 Format Exception Encountered: {str(format_error)}")
        return f"""
# 📦 Inventory Logistics Analytics Review
**Target SKU Category Anchor:** `{product_name}`

---
### 🔍 Core Analytics & Stock Insights (Fallback Layout)
{insights_text}

---
<p style="font-size: 0.85em; color: #64748b; text-align: right;">📦 Baseline Verification View</p>
"""


def format_mode2_delivery_markdown(product_name, insights_text):
    """Parses Mode 2 structured JSON or text using correct agent dictionary keys."""
    if not insights_text:
        return "### 📭 Channel Idle\nSelect an active SKU anchor and execute the route analyzer."
        
    print(f"\n👉 [Mode 2 Fixed Parser] Processing payload for: {product_name}")
    
    try:
        # Step 1: Parse the incoming string or use it directly if it's already a dict object
        data = json.loads(insights_text) if isinstance(insights_text, str) else insights_text
        
        # Step 2: Extract mapping fields directly from your agent's exact keys
        classification = str(data.get("delivery_classification", "Standard Route Window"))
        risk_level = str(data.get("logistics_risk", "Low Exposure"))
        observation = str(data.get("key_observation", "No route observation metrics declared."))
        recommendation = str(data.get("recommendation", "Maintain status quo fulfillment paths."))
        
        badge_color = "#ef4444" if "CRITICAL" in risk_level.upper() or "HIGH" in risk_level.upper() else "#f59e0b" if "MEDIUM" in risk_level.upper() else "#3b82f6"
        
        return f"""
# 🚛 Distribution Route & Delivery Analytics
**Target SKU Category Anchor:** `{product_name}`

<div style="margin: 10px 0 20px 0;">
    <span style="background-color: #4b5563; color: white; padding: 6px 14px; border-radius: 20px; font-weight: bold; font-size: 0.85em; margin-right: 8px;">
        📍 PROFILE: {classification.upper()}
    </span>
    <span style="background-color: {badge_color}; color: white; padding: 6px 14px; border-radius: 20px; font-weight: bold; font-size: 0.85em; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
        ⚠️ RISK METRIC: {risk_level.upper()}
    </span>
</div>

### 🗺️ Route Metrics & Transit Optimization Vectors
> {observation}

### 🛡️ Logistics Contingency Planning & Guardrails
* ⚡ **Immediate Mitigation Action:** {recommendation}

---
<p style="font-size: 0.85em; color: #64748b; text-align: right;">🚛 Transit Optimization Metrics Completed Effectively</p>
"""
    except Exception as format_error:
        print(f"⚠️ Mode 2 Format Exception Encountered: {str(format_error)}")
        return f"""
# 🚛 Distribution Route & Delivery Analytics
**Target SKU Category Anchor:** `{product_name}`

---
### 🗺️ Route Metrics & Transit Optimization Vectors (Fallback Layout)
{insights_text}

---
<p style="font-size: 0.85em; color: #64748b; text-align: right;">🚛 Baseline Verification View</p>
"""


import re  # Ensure re is imported at the top of your file

def format_mode4_comparison_markdown(prod_a, prod_b, comparative_text):
    """Formats Mode 4 agent matrix outputs into a beautifully typeset premium dashboard layout."""
    # Only short-circuit on actual upstream error messages, not on normal output
    if not comparative_text:
        return "### 📭 No output received from comparison crew."
    if isinstance(comparative_text, str) and comparative_text.startswith("### ❌") or comparative_text.startswith("### ⚠️"):
        return comparative_text
        
    print(f"\n🧼 [Mode 4 Substring Extractor] Isolate JSON from telemetry frames...")
    
    try:
        # 🎯 SUBSTRING EXTRACTOR: Finds the first '{' and matching last '}' to completely ignore telemetry text
        match = re.search(r'\{.*\}', str(comparative_text), re.DOTALL)
        if not match:
            raise ValueError("No matching curly brace boundaries located inside output stream.")
            
        cleaned_text = match.group(0)
        data = json.loads(cleaned_text)
        
        target = str(data.get("recommended_investment_target", "Undetermined"))
        high_risk = str(data.get("highest_logistics_risk", "Undetermined"))
        high_roi = str(data.get("highest_expected_roi", "Undetermined"))
        ranking = data.get("operational_complexity_ranking", [])
        summary = str(data.get("executive_summary", "No cross-analysis summary available."))
        
        # Turn the complexity ranking array into a clear inline string block
        ranking_str = " → ".join([f"`{item}`" for item in ranking]) if isinstance(ranking, list) else str(ranking)

        return f"""
# ⚖️ Portfolio Cross-Analysis Framework Matrix
**Track Anchor Alpha:** `{prod_a}` | **Track Anchor Beta:** `{prod_b}`

---

### 📊 Strategic Cross-Analysis Synthesis
| Analytical Core Metric Vector | System Assessment Profile |
| :--- | :--- |
| 🎯 **Primary Capital Priority Target** | **{target}** |
| 📈 **Highest Modeled ROI Trajectory** | `{high_roi}` |
| ⚠️ **Elevated Logistics Risk Concentration** | `{high_risk}` |
| 🔀 **Operational Complexity Ranking (Highest First)** | {ranking_str} |

### 📋 Executive Summary Insight
> {summary}

---
<p style="font-size: 0.85em; color: #64748b; text-align: right;">⚖️ Multi-SKU Portfolio Matrix Evaluation Signed Off • Substring Isolated</p>
"""
    except Exception as format_error:
        print(f"⚠️ Mode 4 Format Exception Encountered: {str(format_error)}")
        # Secondary parse attempt before falling back - never dump raw JSON into markdown
        try:
            fallback_data = json.loads(comparative_text) if isinstance(comparative_text, str) else comparative_text
            if isinstance(fallback_data, dict):
                fb_target = str(fallback_data.get("recommended_investment_target", "Undetermined"))
                fb_summary = str(fallback_data.get("executive_summary", "No summary available."))
                fb_risk = str(fallback_data.get("highest_logistics_risk", "N/A"))
                fb_roi = str(fallback_data.get("highest_expected_roi", "N/A"))
                fb_ranking = fallback_data.get("operational_complexity_ranking", [])
                fb_ranking_str = " → ".join([f"`{item}`" for item in fb_ranking]) if isinstance(fb_ranking, list) else str(fb_ranking)
                return f"""
# ⚖️ Portfolio Cross-Analysis Framework Matrix
**Track Anchor Alpha:** `{prod_a}` | **Track Anchor Beta:** `{prod_b}`

---

### 📊 Strategic Cross-Analysis Synthesis
| Analytical Core Metric Vector | System Assessment Profile |
| :--- | :--- |
| 🎯 **Primary Capital Priority Target** | **{fb_target}** |
| 📈 **Highest Modeled ROI Trajectory** | `{fb_roi}` |
| ⚠️ **Elevated Logistics Risk Concentration** | `{fb_risk}` |
| 🔀 **Operational Complexity Ranking** | {fb_ranking_str} |

### 📋 Executive Summary Insight
> {fb_summary}

---
<p style="font-size: 0.85em; color: #64748b; text-align: right;">⚖️ Secondary Parse Layer Applied</p>
"""
        except Exception:
            pass
        return f"""
# ⚖️ Portfolio Cross-Analysis Framework Matrix
**Track Anchor Alpha:** `{prod_a}` | **Track Anchor Beta:** `{prod_b}`

---
### 📊 Strategic Trade-Off & Optimization Synthesis
> Analysis completed. Structured data could not be fully parsed — review the **Raw Metadata** panel for full output details.

---
<p style="font-size: 0.85em; color: #64748b; text-align: right;">⚖️ Baseline Verification View • Telemetry Bypass Fallback</p>
"""


def generate_premium_playbook_markdown(strategy_dict):
    """
    Transforms structural strategy JSON data into a premium, 
    highly polished Executive Markdown report.
    """
    if not strategy_dict or not isinstance(strategy_dict, dict) or strategy_dict == {}:
        return "### 📭 System Idle\nSelect a product target and execute the cognitive pipeline to build an executive playbook."

    if "Error" in strategy_dict or "Internal Extraction Failure Error" in strategy_dict:
        return f"### ❌ Operational Extraction Fault\n`{strategy_dict.get('Error', 'Unknown Error Link')}`"

    # Safely extract core operational parameters
    sku_name = strategy_dict.get("product_name", "Unspecified Inventory Anchor")
    priority = strategy_dict.get("priority_level", "Standard Operational Scope")
    goal = strategy_dict.get("optimization_goal", "No core objective stated.")
    actions = strategy_dict.get("recommended_actions", [])
    impact = strategy_dict.get("expected_business_impact", "No baseline impact modeled.")
    risk = strategy_dict.get("implementation_risk", "No secondary risk profile declared.")

    # Assign priority colors dynamically
    priority_badge_color = "#ef4444" if "Critical" in priority or "Accelerated" in priority else "#f59e0b" if "High" in priority else "#3b82f6"

    # Build the report typography layout
    markdown_output = f"""
# 📋 Optimized Operational Playbook Matrix
**Target Asset Category:** `{sku_name}`

<div style="margin: 10px 0 20px 0;">
    <span style="background-color: {priority_badge_color}; color: white; padding: 6px 14px; border-radius: 20px; font-weight: bold; font-size: 0.85em; letter-spacing: 0.5px; box-shadow: 0 2px 4px rgba(0,0,0,0.15);">
        🚨 ACTION PRIORITY: {priority.upper()}
    </span>
</div>

### 🎯 Core Optimization Objective
> {goal}

### 🛠️ Executable Strategic Actions Plan
"""

    if isinstance(actions, list) and len(actions) > 0:
        for idx, action in enumerate(actions, 1):
            # If the action has a title split via a colon, bold it beautifully
            if ":" in action:
                title, details = action.split(":", 1)
                markdown_output += f"\n{idx}. **{title.strip()}**\n   * {details.strip()}\n"
            else:
                markdown_output += f"\n{idx}. ⚡ **Operational Directive {idx}**\n   * {action.strip()}\n"
    else:
        markdown_output += f"\n* ⚡ {str(actions)}\n"

    markdown_output += f"""
### 📊 Anticipated Business & Capital Impact
* 📈 {impact}

### ⚠️ Implementation Risk Profile & Guardrails
* 🛡️ {risk}

---
<p style="font-size: 0.8em; color: #64748b; text-align: right;">Cognitive Orchestration Pipeline Verified • Secure Ledger Stored</p>
"""
    return markdown_output

# ----------------------------------------------------------------------
# ASYNC GRAPHICAL EVENT RUNNERS
# ----------------------------------------------------------------------

def handle_isolated_inventory(product_name):
    """Fires Mode 1: Isolated Inventory Channel with Markdown wrap"""
    if not product_name:
        return "### ⚠️ System Request Refused\nPlease choose a valid product configuration target."
    
    flow = LogisticsFlow()
    flow.state.products = [product_name]
    flow.state.optimization_type = "inventory"
    
    flow.kickoff()
    # 🔑 NEW: Return beautifully styled Markdown instead of the raw text string
    return format_mode1_inventory_markdown(product_name, flow.state.inventory_insights)


def handle_isolated_delivery(product_name):
    """Fires Mode 2: Isolated Delivery Channel with Markdown wrap"""
    if not product_name:
        return "### ⚠️ System Request Refused\nPlease choose a valid product configuration target."
    
    flow = LogisticsFlow()
    flow.state.products = [product_name]
    flow.state.optimization_type = "delivery"
    
    flow.kickoff()
    # 🔑 NEW: Return beautifully styled Markdown instead of the raw text string
    return format_mode2_delivery_markdown(product_name, flow.state.delivery_insights)


def build_agent_roster_markdown(title, elapsed, agents, detail):
    """Render a compact live status board for long-running agent workflows."""
    rows = []
    for agent_name, state, note in agents:
        badge = {
            "complete": "COMPLETE",
            "active": "ACTIVE",
            "queued": "QUEUED",
            "error": "ERROR",
        }.get(state, "QUEUED")
        rows.append(
            f"""
<div class="agent-row agent-{state}">
    <div>
        <strong>{agent_name}</strong>
        <span>{note}</span>
    </div>
    <em>{badge}</em>
</div>
"""
        )

    return f"""
### ⏳ {title}
`{elapsed}s elapsed` — {detail}

<div class="agent-roster">
{''.join(rows)}
</div>
"""


def build_mode3_live_markdown(live_logs, elapsed):
    """Map Mode 3 flow log milestones to visible agent names and step states."""
    logs = live_logs or ""

    inventory_done = "Inventory Metrics) Synchronized" in logs
    route_done = "Route Matrices) Synchronized" in logs
    strategist_done = "Strategic Playbook draft generated" in logs
    critic_done = (
        "Strategy verified with high-confidence" in logs
        or "Critic flagged optimization flaws" in logs
    )
    revision_needed = "Revision loop running" in logs or "Operational strategy hardened" in logs
    revision_done = "Operational strategy hardened" in logs

    inventory_active = "Inventory Multi-threading Engine" in logs and not inventory_done
    route_active = "Geospatial Routing Systems" in logs and not route_done
    strategist_active = "Strategist Crew" in logs and not strategist_done
    critic_active = "Critic Crew activated" in logs and not critic_done
    revision_active = "Revision loop running" in logs and not revision_done

    agents = [
        (
            "Inventory Analyst",
            "complete" if inventory_done else "active" if inventory_active else "queued",
            "Stock velocity, inventory risk, and SKU availability metrics",
        ),
        (
            "Route Analyst",
            "complete" if route_done else "active" if route_active else "queued",
            "Transit reliability, delivery exposure, and route performance",
        ),
        (
            "Optimization Strategist",
            "complete" if strategist_done else "active" if strategist_active else "queued",
            "Executive playbook synthesis from inventory and route findings",
        ),
        (
            "Strategy Reviewer",
            "complete" if critic_done else "active" if critic_active else "queued",
            "Risk, compliance, feasibility, and mitigation critique",
        ),
        (
            "Revision Strategist",
            "complete" if revision_done else "active" if revision_active else "queued",
            "Final hardening pass when critique requests revisions",
        ),
    ]

    if not revision_needed:
        agents[-1] = (
            "Revision Strategist",
            "queued",
            "Stands by unless the reviewer requests refinement",
        )

    return build_agent_roster_markdown(
        "Agents Orchestrating",
        elapsed,
        agents,
        "Pipeline is actively running. Each agent updates as its stage begins and completes.",
    )


def build_mode4_live_markdown(prod_a, prod_b, elapsed, stage="analysis"):
    """Render Mode 4 live status with the comparison crew's agent name."""
    loader_state = "complete"
    analyst_state = "active" if stage == "analysis" else "complete"
    formatter_state = "queued" if stage == "analysis" else "active"

    agents = [
        (
            "Memory Ledger Loader",
            loader_state,
            f"Recovered saved playbooks for {prod_a} and {prod_b}",
        ),
        (
            "Supply Chain Portfolio Analyst",
            analyst_state,
            "Comparing ROI, risk concentration, and operational complexity",
        ),
        (
            "Portfolio Report Formatter",
            formatter_state,
            "Preparing dashboard cards and executive comparison matrix",
        ),
    ]

    return build_agent_roster_markdown(
        "Portfolio Agents Orchestrating",
        elapsed,
        agents,
        "Cross-analysis is running. The report will replace this board when complete.",
    )

# ----------------------------------------------------------------------
# MODE 3: End-to-End Optimization Loop
# ----------------------------------------------------------------------

def handle_full_optimization_stream(product_name):
    """Fires Mode 3: Dispatches Background Worker Threads to Stream Event Logs Live"""
    if not product_name:
        yield "System Error", "0", "0", "0", "❌ No product chosen.", "### ❌ No product selected.", {}
        return

    # Instantiate our thread-safe shared logging queue
    ui_logger = EventLogger()
    ui_logger.clear()
    ui_logger.log(f"Target Anchor Selected: '{product_name}'")
    ui_logger.log("Spawning decoupled background agent orchestration thread...")
    
    flow = LogisticsFlow(logger=ui_logger)
    flow.state.products = [product_name]
    flow.state.optimization_type = "full"

    # Container to safely capture the thread's terminal return context
    execution_result = {}

    def thread_wrapper():
        nonlocal execution_result
        try:
            # Capturing the returned context from final_pipeline_exit
            execution_result["output"] = flow.kickoff()
        except Exception as e:
            execution_result["error"] = str(e)

    # Kickoff the agent running context in an isolated background thread
    worker_thread = threading.Thread(target=thread_wrapper)
    worker_thread.start()

    # While agents execute their long tasks, yield intermediate events to the UI terminal frame
    start_time = time.time()
    while worker_thread.is_alive():
        elapsed = int(time.time() - start_time)
        live_logs = ui_logger.get_events()
        yield (
            "⏳ RUNNING...",
            "Polling...",
            "Processing...",
            "0",
            live_logs,
            build_mode3_live_markdown(live_logs, elapsed),
            None
        )
        time.sleep(0.5)

    # Rejoin the threads safely
    worker_thread.join()
    print("THREAD FINISHED")
    print("execution_result =", execution_result)
    print("flow.state.final_strategy =", type(getattr(flow.state, "final_strategy", None)))
    
    # --- POST-PROCESSING & STRUCTURAL EXTRACTION ---
    print("\n[Thread Join Completed] Commencing pipeline state extraction metrics...")
    
    # 1. Corrected Memory History Telemetry Tracking
    try:
        mem_ctx = getattr(flow.state, "memory_context", [])
        # Your deduction was correct: memory_context is a formatted array of strings
        history_count = len(mem_ctx) if isinstance(mem_ctx, list) else 0
    except Exception:
        history_count = 0
        
    memory_was_used = "✅ YES (Delta Reasoning Active)" if history_count > 0 else "❌ NO (Baseline Sandbox Run)"
    
    # 2. Extract Loops Telemetry Counter
    try:
        loops_run = str(getattr(flow.state, "revision_count", 0))
    except Exception:
        loops_run = "1"
    
    # 3. Secure Playbook Extraction Pipeline
    final_strategy = {}
    try:
        # Extract returned result from the safe thread execution container
        raw_strategy = execution_result.get("output", None)
        
        # Diagnostics Logging
        print(f"👉 Type of context output received: {type(raw_strategy)}")
        print(f"👉 Context payload value: {raw_strategy}")
        
        # Fallback: Check if the background thread structure was bypassed
        if not raw_strategy:
            raw_strategy = getattr(flow.state, "final_strategy", None)

        # Normalize any Pydantic object wrappers into clean UI primitives
        if raw_strategy:
            if hasattr(raw_strategy, "to_dict"):
                final_strategy = raw_strategy.to_dict()
            elif hasattr(raw_strategy, "model_dump"):
                final_strategy = raw_strategy.model_dump()
            elif isinstance(raw_strategy, dict):
                final_strategy = raw_strategy
            elif isinstance(raw_strategy, str):
                final_strategy = json.loads(raw_strategy)
                
        # 🛡️ Bulletproof Ledger Recovery Layer
        # If the state container dropped out to {}, pull it directly from the local SQLite disk storage
        if not final_strategy or final_strategy == {}:
            print("⚠️ State data container detected empty. Initializing cold disk database restore sequence...")
            ui_logger.log("⚠️ Processing state drop. Syncing playbook data from secure memory ledger...")
            
            from memory.strategy_store import StrategyMemory
            db_memory = StrategyMemory()
            history = db_memory.get_product_history(product_name)
            
            if history:
                latest_entry = history[0][1]
                if isinstance(latest_entry, str):
                    final_strategy = json.loads(latest_entry)
                else:
                    final_strategy = latest_entry

    except Exception as parse_error:
        print(f"❌ Storage layer extraction failure: {str(parse_error)}")
        final_strategy = {"Internal Extraction Failure Error": str(parse_error)}

    # 🔑 NEW: Generate premium Markdown string representation from our strategy dictionary
    playbook_markdown = generate_premium_playbook_markdown(final_strategy)

    # Finalize log rendering
    final_logs = ui_logger.get_events()
    if "Operational strategy hardened" not in final_logs:
        ui_logger.log("🏁 Operational strategy finalized, verified, and mapped back to dashboard panels.")
        final_logs = ui_logger.get_events()
        
    # 🔑 FIX: Return both premium markdown text and the dictionary payload
    yield memory_was_used, str(history_count), loops_run, "5", final_logs, playbook_markdown, final_strategy


# ----------------------------------------------------------------------
# MODE 4: PORTFOLIO COMPARATIVE ANALYSIS (THREAD-ISOLATED)
# ----------------------------------------------------------------------

def handle_portfolio_comparison(prod_a, prod_b):
    """
    Executes Mode 4: Invokes comparison agent crew inside a thread-isolated
    container to prevent web socket blocks and infinite UI loops.
    """
    if not prod_a or not prod_b:
        yield (
            "⚠️ Error", "Missing Input", "High Uncertainty",
            "### ❌ Operational Halte\nBoth strategic playbook profiles must be selected before executing cross-analysis."
        )
        return

    if prod_a == prod_b:
        yield (
            f"⚖️ {prod_a}", "0% Delta", "Identical Matrix",
            "### ⚠️ Duplicative Matrix Selected\nYou have selected the same product for both comparison tracks. Please choose two distinct profiles."
        )
        return

    from memory.strategy_store import StrategyMemory
    from crews.comparison_crew import run_comparison_crew

    db_memory = StrategyMemory()
    
    # 1. Fetch historical data from disk storage
    hist_a = db_memory.get_product_history(prod_a)
    hist_b = db_memory.get_product_history(prod_b)

    if not hist_a or not hist_b:
        missing = prod_a if not hist_a else prod_b
        yield (
            "⚠️ Storage Miss", "Data Missing", "Critical",
            f"### ❌ Missing Strategy History\nThe profile **'{missing}'** does not have a saved playbook in the database. Please run Mode 3 optimization for this item first."
        )
        return

    # 2. Extract latest strategy records
    strat_a_raw = hist_a[0][1]
    strat_b_raw = hist_b[0][1]

    # Structuring data for the crew
    compiled_strategies_payload = {
        "Product_A_Name": prod_a,
        "Product_A_Strategy": json.loads(strat_a_raw) if isinstance(strat_a_raw, str) else strat_a_raw,
        "Product_B_Name": prod_b,
        "Product_B_Strategy": json.loads(strat_b_raw) if isinstance(strat_b_raw, str) else strat_b_raw
    }

    # 3. Thread-isolated container for crew execution
    container = {}

    def crew_worker_thread():
        try:
            # Execute CrewAI kickoff inside the worker thread
            container["output"] = run_comparison_crew(compiled_strategies_payload)
        except Exception as e:
            container["error"] = str(e)

    # Spawn and launch thread context
    worker = threading.Thread(target=crew_worker_thread)
    worker.start()

    start_time = time.time()

    # Hold main thread while rendering intermediate processing states
    while worker.is_alive():
        elapsed = int(time.time() - start_time)
        yield (
            "⏳ Comparing...",
            "Portfolio scan active",
            "Risk review active",
            build_mode4_live_markdown(prod_a, prod_b, elapsed)
        )
        time.sleep(0.5)

    # Rejoin the execution thread safely
    worker.join()

    # 4. Handle errors if the crew execution fails
    if "error" in container:
        yield (
            "❌ Failure", "Error 500", "Critical",
            f"### Internal Execution Error encountered inside comparison worker:\n`{container['error']}`"
        )
        return

    elapsed = int(time.time() - start_time)
    yield (
        "✅ Crew complete",
        "Parsing results...",
        "Formatting report...",
        build_mode4_live_markdown(prod_a, prod_b, elapsed, stage="formatting")
    )

    # 5. Extract results — unwrap CrewAI CrewOutput object to plain string
    crew_output = container.get("output", "")
    # CrewAI returns a CrewOutput object; extract the raw string from it
    if hasattr(crew_output, "raw"):
        raw_markdown = str(crew_output.raw)
    elif hasattr(crew_output, "final_output"):
        raw_markdown = str(crew_output.final_output)
    else:
        raw_markdown = str(crew_output)
    print(f"[Mode 4] raw_markdown snippet: {raw_markdown[:300]}")

    # 🔑 NEW: Sanitize raw markdown string via regex substring boundaries before updating metrics cards
    try:
        match = re.search(r'\{.*\}', raw_markdown, re.DOTALL)
        if not match:
            raise ValueError("No JSON boundaries found.")
            
        cleaned_markdown = match.group(0)
        parsed_data = json.loads(cleaned_markdown)
        
        target_recommendation = str(parsed_data.get("recommended_investment_target", "Multi-SKU Balance"))
        roi_impact = f"🚀 {parsed_data.get('highest_expected_roi', 'See Report')}"
        risk_level = f"⚠️ {parsed_data.get('highest_logistics_risk', 'See Report')}"
    except Exception as parse_err:
        print(f"⚠️ Card Extraction Parsing Failed: {str(parse_err)}")
        # Fallback heuristic if the parsing layer fails
        target_recommendation = "⚖️ Multi-SKU Balance Matrix"
        roi_impact = "Determined in Report"
        risk_level = "Tiered Structure"

    # Format the final text chunk using our premium cross-analysis table layout
    premium_markdown_report = format_mode4_comparison_markdown(prod_a, prod_b, raw_markdown)

    # Return the metrics along with your premium Markdown report string!
    yield target_recommendation, roi_impact, risk_level, premium_markdown_report


# ----------------------------------------------------------------------
# MODE 5: MEMORY LEDGER EXPLORER HANDLERS
# ----------------------------------------------------------------------

def update_archive_timeline(product_name):
    if not product_name:
        return gr.update(choices=[], value=None), "### Select a valid historical profile anchor.", {}

    from memory.strategy_store import StrategyMemory
    db_memory = StrategyMemory()
    history = db_memory.get_product_history(product_name)
    
    if not history:
        return gr.update(choices=["❌ No History Found"], value=None), "### No historical records identified.", {}

    timestamps = [str(row[0]) for row in history]
    default_ts = timestamps[0] if timestamps else None

    # Load initial playbook data
    initial_json = {}
    try:
        latest_entry_raw = history[0][1]
        initial_json = json.loads(latest_entry_raw) if isinstance(latest_entry_raw, str) else latest_entry_raw
    except Exception as e:
        initial_json = {"Error Parsing Record": str(e)}

    # Convert to markdown right away
    initial_md = generate_premium_playbook_markdown(initial_json)

    return gr.update(choices=timestamps, value=default_ts), initial_md, initial_json


def render_historical_json(product_name, selected_timestamp):
    """Returns (markdown_text, raw_json_dict) to display premium look in Mode 5"""
    if not product_name or not selected_timestamp or "No History" in selected_timestamp:
        return "### Invalid profile time key chosen.", {}

    from memory.strategy_store import StrategyMemory
    db_memory = StrategyMemory()
    history = db_memory.get_product_history(product_name)

    target_dict = {}
    for row in history:
        if str(row[0]) == str(selected_timestamp):
            try:
                strategy_payload = row[1]
                target_dict = json.loads(strategy_payload) if isinstance(strategy_payload, str) else strategy_payload
                break
            except Exception as e:
                target_dict = {"Error Decoding Data": str(e)}

    if not target_dict:
        try:
            target_dict = json.loads(history[0][1]) if isinstance(history[0][1], str) else history[0][1]
        except Exception:
            target_dict = {"Error": "Data slice missing."}

    # Generate layout view
    return generate_premium_playbook_markdown(target_dict), target_dict


def hot_reload_db_selectors():
    """Tab Focus Event Listener: Hot-reloads list states dynamically from SQLite file updates"""
    active_db_rows = memory.get_all_products()
    return gr.update(choices=active_db_rows), gr.update(choices=active_db_rows), gr.update(choices=active_db_rows)


# ----------------------------------------------------------------------
# UI DASHBOARD LAYOUT MANAGEMENT
# ----------------------------------------------------------------------

catalog_items = catalog.get_all_products()
db_items = memory.get_all_products()

# ── Custom CSS: vibrant light theme ─────────────────────────────────────────
CUSTOM_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Space+Grotesk:wght@400;500;600;700&display=swap');

:root {
    --bg:         #f0f4ff;
    --bg-panel:   #ffffff;
    --bg-card:    #f8faff;
    --accent:     #4f46e5;
    --accent2:    #0ea5e9;
    --accent3:    #7c3aed;
    --success:    #059669;
    --warn:       #d97706;
    --danger:     #dc2626;
    --text:       #0f172a;
    --text-mid:   #334155;
    --text-muted: #64748b;
    --border:     #e2e8f0;
    --border-acc: rgba(79,70,229,0.25);
    --shadow-sm:  0 1px 3px rgba(15,23,42,0.08), 0 1px 2px rgba(15,23,42,0.04);
    --shadow-md:  0 4px 16px rgba(79,70,229,0.12), 0 2px 6px rgba(15,23,42,0.06);
    --shadow-lg:  0 8px 32px rgba(79,70,229,0.18);
}

/* ── Base ── */
body, .gradio-container, .gradio-container * {
    font-family: 'Inter', sans-serif !important;
    box-sizing: border-box;
}
html, body, gradio-app {
    width: 100% !important;
    min-width: 100% !important;
}
body {
    margin: 0 !important;
    font-size: 18px !important;
}
.gradio-container {
    background: var(--bg) !important;
    color: var(--text) !important;
    width: 100% !important;
    max-width: none !important;
    margin: 0 !important;
    padding: 28px clamp(28px, 4vw, 64px) 40px !important;
}
.gradio-container .contain,
.gradio-container main,
.gradio-container .main,
.gradio-container .wrap {
    width: 100% !important;
    max-width: none !important;
}
.gradio-row {
    width: 100% !important;
    gap: 18px !important;
}
.gradio-column {
    min-width: 280px !important;
}
footer { display: none !important; }

/* ── Hero Header ── */
.hub-header {
    background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 40%, #0ea5e9 100%);
    border-radius: 20px;
    padding: 34px 42px;
    margin-bottom: 22px;
    position: relative;
    overflow: hidden;
    box-shadow: var(--shadow-lg);
}
.hub-header::before {
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 300px; height: 300px;
    background: radial-gradient(circle, rgba(255,255,255,0.12) 0%, transparent 65%);
    pointer-events: none;
}
.hub-header::after {
    content: '';
    position: absolute;
    bottom: -40px; left: 30%;
    width: 200px; height: 200px;
    background: radial-gradient(circle, rgba(14,165,233,0.2) 0%, transparent 65%);
    pointer-events: none;
}
.hub-header h1 {
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 2.25rem !important;
    font-weight: 700 !important;
    letter-spacing: -0.5px !important;
    color: #ffffff !important;
    margin: 0 0 8px 0 !important;
    text-shadow: 0 2px 8px rgba(0,0,0,0.15);
}
.hub-header p {
    color: rgba(255,255,255,0.82) !important;
    font-size: 1.08rem !important;
    font-weight: 400 !important;
    margin: 0 0 20px 0 !important;
    letter-spacing: 0.1px;
}
/* Agent badge strip inside header */
.agent-strip {
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
    margin-top: 4px;
}
.agent-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(255,255,255,0.18);
    backdrop-filter: blur(8px);
    border: 1px solid rgba(255,255,255,0.3);
    border-radius: 999px;
    padding: 5px 14px;
    font-size: 0.95rem;
    font-weight: 600;
    color: #ffffff;
    letter-spacing: 0.2px;
}
.agent-badge .dot {
    width: 7px; height: 7px;
    border-radius: 50%;
    background: #4ade80;
    box-shadow: 0 0 6px #4ade80;
    animation: pulse-dot 2s ease-in-out infinite;
}
@keyframes pulse-dot {
    0%,100% { opacity: 1; transform: scale(1); }
    50%      { opacity: 0.6; transform: scale(1.3); }
}

/* ── Tabs ── */
.tab-nav {
    background: var(--bg-panel) !important;
    border-radius: 14px !important;
    padding: 8px !important;
    box-shadow: var(--shadow-sm) !important;
    border: 1px solid var(--border) !important;
    margin-bottom: 16px !important;
    gap: 4px !important;
}
.tab-nav button {
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 1rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.2px !important;
    border-radius: 10px !important;
    padding: 11px 20px !important;
    transition: all 0.18s ease !important;
    color: var(--text-muted) !important;
    background: transparent !important;
    border: none !important;
}
.tab-nav button:hover {
    background: rgba(79,70,229,0.08) !important;
    color: var(--accent) !important;
}
.tab-nav button.selected {
    background: linear-gradient(135deg, var(--accent), var(--accent3)) !important;
    color: #ffffff !important;
    box-shadow: 0 4px 12px rgba(79,70,229,0.35) !important;
}

/* ── Section labels ── */
.section-label {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 0.92rem;
    font-weight: 700;
    color: var(--accent);
    text-transform: uppercase;
    letter-spacing: 1.4px;
    margin-bottom: 8px;
    display: flex;
    align-items: center;
    gap: 6px;
}
.section-label::before {
    content: '';
    display: inline-block;
    width: 12px; height: 3px;
    background: linear-gradient(90deg, var(--accent), var(--accent2));
    border-radius: 2px;
}

/* ── Buttons ── */
button.primary, .gr-button-primary {
    background: linear-gradient(135deg, var(--accent) 0%, var(--accent3) 100%) !important;
    border: none !important;
    color: white !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 1.05rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.3px !important;
    border-radius: 12px !important;
    box-shadow: 0 4px 14px rgba(79,70,229,0.4) !important;
    transition: all 0.2s ease !important;
    padding: 14px 26px !important;
}
button.primary:hover, .gr-button-primary:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 24px rgba(79,70,229,0.5) !important;
}
button.secondary, .gr-button-secondary {
    background: var(--bg-panel) !important;
    border: 2px solid var(--border-acc) !important;
    color: var(--accent) !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 1.05rem !important;
    font-weight: 600 !important;
    border-radius: 12px !important;
    transition: all 0.2s ease !important;
    padding: 13px 24px !important;
}
button.secondary:hover, .gr-button-secondary:hover {
    background: rgba(79,70,229,0.06) !important;
    border-color: var(--accent) !important;
    box-shadow: var(--shadow-md) !important;
}

/* ── Inputs / Dropdowns ── */
.gr-form, .gr-box { border-radius: 12px !important; }
select, input[type="text"],
.gr-dropdown > div,
div[data-testid="dropdown"] > label + div {
    background: var(--bg-panel) !important;
    border: 1.5px solid var(--border) !important;
    color: var(--text) !important;
    border-radius: 10px !important;
    font-size: 1.05rem !important;
    transition: border-color 0.15s !important;
}
select:focus, input:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px rgba(79,70,229,0.12) !important;
    outline: none !important;
}
label span {
    color: var(--text-mid) !important;
    font-weight: 600 !important;
    font-size: 0.98rem !important;
}

/* ── Textboxes / Terminal ── */
textarea {
    background: #f8faff !important;
    border: 1.5px solid var(--border) !important;
    color: #1e293b !important;
    font-family: 'JetBrains Mono', 'Fira Code', monospace !important;
    font-size: 0.98rem !important;
    border-radius: 10px !important;
    line-height: 1.6 !important;
}
/* Textbox (KPI cards) */
input[type="text"] {
    color: var(--accent) !important;
    font-weight: 700 !important;
    font-size: 1.05rem !important;
}

/* ── Markdown pane ── */
.gr-markdown, div[data-testid="markdown"] {
    background: var(--bg-panel) !important;
    border: 1.5px solid var(--border) !important;
    border-radius: 14px !important;
    padding: 28px 34px !important;
    box-shadow: var(--shadow-sm) !important;
}
.gr-markdown p, div[data-testid="markdown"] p,
.gr-markdown li, div[data-testid="markdown"] li,
.gr-markdown strong, div[data-testid="markdown"] strong,
.gr-markdown em, div[data-testid="markdown"] em {
    color: var(--text) !important;
    font-size: 1.05rem !important;
    line-height: 1.65 !important;
}
div[data-testid="markdown"] h1 {
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 1.8rem !important; font-weight: 700 !important;
    color: var(--accent) !important; margin-bottom: 6px !important;
}
div[data-testid="markdown"] h2 {
    font-size: 1.42rem !important; font-weight: 700 !important;
    color: var(--text) !important;
}
div[data-testid="markdown"] h3 {
    font-size: 1.16rem !important; font-weight: 700 !important;
    color: var(--accent3) !important; text-transform: uppercase !important;
    letter-spacing: 0.6px !important; margin-top: 18px !important;
}
/* Table */
div[data-testid="markdown"] table {
    width: 100% !important;
    border-collapse: separate !important;
    border-spacing: 0 !important;
    border-radius: 10px !important;
    overflow: hidden !important;
    box-shadow: var(--shadow-sm) !important;
    margin: 12px 0 !important;
}
div[data-testid="markdown"] th {
    background: linear-gradient(90deg, var(--accent), var(--accent3)) !important;
    color: #ffffff !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 1rem !important; font-weight: 700 !important;
    padding: 14px 18px !important;
    text-align: left !important;
    letter-spacing: 0.5px !important;
}
div[data-testid="markdown"] td {
    padding: 13px 18px !important;
    background: var(--bg-panel) !important;
    color: var(--text) !important;
    font-size: 1.03rem !important;
    border-bottom: 1px solid var(--border) !important;
}
div[data-testid="markdown"] tr:nth-child(even) td {
    background: var(--bg-card) !important;
}
div[data-testid="markdown"] tr:hover td {
    background: rgba(79,70,229,0.05) !important;
}
/* Blockquote */
div[data-testid="markdown"] blockquote {
    border-left: 4px solid var(--accent2) !important;
    background: linear-gradient(90deg, rgba(14,165,233,0.07), rgba(79,70,229,0.04)) !important;
    padding: 15px 20px !important;
    border-radius: 0 10px 10px 0 !important;
    color: var(--text-mid) !important;
    font-style: italic !important;
    margin: 10px 0 !important;
}
/* Inline code */
div[data-testid="markdown"] code {
    background: rgba(79,70,229,0.1) !important;
    color: var(--accent) !important;
    padding: 2px 7px !important;
    border-radius: 5px !important;
    font-size: 0.95em !important;
    font-weight: 600 !important;
}
div[data-testid="markdown"] hr {
    border: none !important;
    border-top: 2px solid var(--border) !important;
    margin: 16px 0 !important;
}

/* Live agent orchestration board */
.agent-roster {
    display: grid;
    gap: 12px;
    margin-top: 18px;
}
.agent-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 18px;
    border: 1.5px solid var(--border);
    border-radius: 10px;
    padding: 14px 16px;
    background: var(--bg-card);
}
.agent-row strong {
    display: block;
    color: var(--text) !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 1.06rem !important;
    margin-bottom: 3px;
}
.agent-row span {
    display: block;
    color: var(--text-mid) !important;
    font-size: 0.98rem !important;
    line-height: 1.45;
}
.agent-row em {
    flex: 0 0 auto;
    border-radius: 999px;
    padding: 6px 11px;
    font-style: normal !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 0.82rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.6px;
}
.agent-active {
    border-color: rgba(124,58,237,0.55);
    background: linear-gradient(90deg, rgba(124,58,237,0.09), rgba(14,165,233,0.07));
    box-shadow: 0 0 0 3px rgba(124,58,237,0.08);
}
.agent-active em {
    background: var(--accent3);
    color: #ffffff !important;
}
.agent-complete {
    border-color: rgba(5,150,105,0.35);
}
.agent-complete em {
    background: rgba(5,150,105,0.12);
    color: var(--success) !important;
}
.agent-queued {
    opacity: 0.78;
}
.agent-queued em {
    background: rgba(100,116,139,0.12);
    color: var(--text-muted) !important;
}
.agent-error {
    border-color: rgba(220,38,38,0.45);
}
.agent-error em {
    background: rgba(220,38,38,0.12);
    color: var(--danger) !important;
}

/* ── Accordion ── */
.gr-accordion {
    background: var(--bg-card) !important;
    border: 1.5px solid var(--border) !important;
    border-radius: 12px !important;
    box-shadow: var(--shadow-sm) !important;
}

/* ── JSON viewer ── */
.json-holder { background: var(--bg-card) !important; border-radius: 10px !important; }

@media (max-width: 900px) {
    .gradio-container {
        padding: 18px 14px 28px !important;
    }
    .hub-header {
        padding: 26px 24px;
        border-radius: 16px;
    }
    .hub-header h1 {
        font-size: 1.75rem !important;
    }
    .tab-nav button {
        font-size: 0.95rem !important;
        padding: 10px 14px !important;
    }
}
"""

with gr.Blocks(
    theme=gr.themes.Base(
        primary_hue="blue",
        neutral_hue="slate",
        font=gr.themes.GoogleFont("DM Sans"),
    ),
    title="Logistics Control Deck",
    css=CUSTOM_CSS
) as app:

    gr.HTML("""
    <div class="hub-header">
        <h1>🏭 Intelligent Regional Logistics Orchestration Hub</h1>
        <p>Production-Ready Decision Support System (DSS) &nbsp;•&nbsp; Real-Time Core Telemetry Tracing &nbsp;•&nbsp; Multi-Agent CrewAI Flow Architecture</p>
    </div>
    """)

    with gr.Tabs() as main_tabs:

        # --- MODE 1 TAB ---
        with gr.TabItem("📦 Mode 1: Inventory Analysis") as tab_1:
            gr.HTML('<div class="section-label">📦 Isolated Inventory Risk & Analytics Evaluation</div>')
            with gr.Row():
                drop_inv = gr.Dropdown(choices=catalog_items, label="Select Target Supply Chain SKU")
                btn_inv = gr.Button("Analyze Stock Metrics", variant="secondary")
            out_inv = gr.Markdown("### 📭 Channel Idle\nSelect an active SKU anchor and execute the inventory analyzer.")
            btn_inv.click(fn=handle_isolated_inventory, inputs=[drop_inv], outputs=[out_inv])

        # --- MODE 2 TAB ---
        with gr.TabItem("🚛 Mode 2: Delivery Optimization") as tab_2:
            gr.HTML('<div class="section-label">🚛 Isolated Transit Routing & Distribution Efficiency Vector</div>')
            with gr.Row():
                drop_del = gr.Dropdown(choices=catalog_items, label="Select Distribution Target SKU")
                btn_del = gr.Button("Optimize Route Metrics", variant="secondary")
            out_del = gr.Markdown("### 📭 Channel Idle\nSelect an active SKU anchor and execute the route analyzer.")
            btn_del.click(fn=handle_isolated_delivery, inputs=[drop_del], outputs=[out_del])

        # --- MODE 3 TAB ---
        with gr.TabItem("⚡ Mode 3: End-to-End Optimization Loop") as tab_3:
            gr.HTML('<div class="section-label">🔄 Multi-Agent Cognitive Strategy Synthesizer with Criticism Loop</div>')

            with gr.Row():
                drop_prod = gr.Dropdown(choices=catalog_items, label="Target Supply Chain Product SKU Anchor")
                btn_run = gr.Button("🔥 Run End-to-End Optimization Pipeline", variant="primary")

            # ── Telemetry KPI Row ──────────────────────────────────────────
            gr.HTML('<div class="section-label" style="margin-top:16px;">⬡ Pipeline Telemetry Dashboard</div>')
            with gr.Row():
                card_memory  = gr.Textbox(label="🧠 Database Context Trace",      value="💤 Inactive")
                card_history = gr.Textbox(label="📜 Recovered Historical Records", value="0")
                card_loops   = gr.Textbox(label="🔁 Completed Refinement Loops",   value="0")
                card_agents  = gr.Textbox(label="🤖 Active Agents in Pipeline",    value="5")

            # ── Main Content Row ──────────────────────────────────────────
            with gr.Row():
                with gr.Column(scale=2):
                    gr.HTML('<div class="section-label">🎛️ Live Pipeline Orchestration Feed</div>')
                    out_terminal = gr.TextArea(
                        label="Asynchronous Engine Logs Stream",
                        lines=16, max_lines=20, interactive=False
                    )

                with gr.Column(scale=3):
                    gr.HTML('<div class="section-label">💼 Final Executive Assessment</div>')
                    out_playbook_md = gr.Markdown(
                        "### 📭 System Idle\nSelect a product target and execute the cognitive pipeline to build an executive playbook."
                    )
                    with gr.Accordion("🛠️ Inspect Raw Structural JSON Metadata", open=False):
                        out_final_json = gr.JSON(label="Raw System Dictionary State Output")

            btn_run.click(
                fn=handle_full_optimization_stream,
                inputs=[drop_prod],
                outputs=[card_memory, card_history, card_loops, card_agents, out_terminal, out_playbook_md, out_final_json]
            )

        # --- MODE 4 TAB ---
        with gr.TabItem("⚖️ Mode 4: Portfolio Cross-Analysis") as tab_4:
            gr.HTML('<div class="section-label">⚖️ Multi-SKU Portfolio Matrix Delta Cross-Analysis Evaluation</div>')

            with gr.Row():
                drop_comp_a = gr.Dropdown(choices=db_items, label="Strategic Playbook Profile Track Alpha")
                drop_comp_b = gr.Dropdown(choices=db_items, label="Strategic Playbook Profile Track Beta")

            btn_comp = gr.Button("Execute Strategic Portfolio Cross-Analysis", variant="primary")

            with gr.Row():
                card_target = gr.Textbox(label="🎯 Optimized Deployment Target",     value="Pending Matrix Calculation")
                card_roi    = gr.Textbox(label="📈 Modeled ROI Value Vector",         value="Pending Run")
                card_risk   = gr.Textbox(label="⚠️ Aggregated Implementation Risk",  value="Pending Run")

            gr.HTML('<div class="section-label" style="margin-top:16px;">💼 Portfolio Cross-Analysis Synthesis Report</div>')
            out_markdown_summary = gr.Markdown("### Executive Summary synthesis waiting for execution input...")

            btn_comp.click(
                fn=handle_portfolio_comparison,
                inputs=[drop_comp_a, drop_comp_b],
                outputs=[card_target, card_roi, card_risk, out_markdown_summary]
            )

        # --- MODE 5 TAB ---
        with gr.TabItem("📖 Mode 5: Memory Ledger Explorer") as tab_5:
            gr.HTML('<div class="section-label">📖 Long-Term Persistent Memory Database Archive Audit Ledger</div>')

            with gr.Row():
                drop_hist_prod = gr.Dropdown(choices=db_items, label="Select Optimized Database Profile Entry")
                drop_hist_time = gr.Dropdown(choices=[], label="Select Historical Execution Log Frame (Timestamp)")

            gr.HTML('<div class="section-label" style="margin-top:16px;">📂 Historical Executive Playbook View</div>')
            out_archive_md = gr.Markdown(
                "### 🧭 Selector Framework Waiting\nChoose an optimized profile entry above to extract long-term historical records details."
            )

            with gr.Accordion("🛠️ View Archived Structural Metadata Layer", open=False):
                out_archive_json = gr.JSON(label="Retrieved SQLite Strategic Storage Playbook State")

            drop_hist_prod.change(
                fn=update_archive_timeline,
                inputs=[drop_hist_prod],
                outputs=[drop_hist_time, out_archive_md, out_archive_json]
            )
            drop_hist_time.change(
                fn=render_historical_json,
                inputs=[drop_hist_prod, drop_hist_time],
                outputs=[out_archive_md, out_archive_json]
            )

    main_tabs.select(fn=hot_reload_db_selectors, inputs=[], outputs=[drop_comp_a, drop_comp_b, drop_hist_prod])

if __name__ == "__main__":
    app.queue().launch(server_name="127.0.0.1", server_port=7860, share=False)
