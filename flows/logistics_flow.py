# logistics_flow.py
from crewai.flow.flow import Flow, start, router, listen, and_
from models.state import LogisticsState
from tools.inventory_tool import InventoryAnalyticsTool
from tools.delivery_tool import DeliveryAnalyticsTool
from tools.geo_tool import GeoAnalyticsTool

from crews.inventory_crew import run_inventory_crew
from crews.route_crew import run_route_crew
from crews.strategy_crew import run_strategy_crew
from crews.critique_crew import run_critique_crew
from crews.revision_crew import run_revision_crew

from memory.strategy_store import StrategyMemory
from utils.normalize_output import normalize_output
from utils.event_logger import EventLogger  # Thread-safe tracker

# Centralized dataset tracking
DATA_PATH = "data/DataCoSupplyChainDatasetRefined_First_5000.csv"


class LogisticsFlow(Flow[LogisticsState]):

    def __init__(self, logger: EventLogger = None):
        super().__init__()
        # Fallback to a blank instance if run without a UI to avoid NoneType attribute errors
        self.logger = logger if logger else EventLogger()

    # =====================================================================
    # 🏁 STAGE 1: ENTRY POINT & ROUTING
    # =====================================================================

    @start()
    def initialize(self):
        print("\n=== [STAGE 1] PIPELINE INITIALIZED ===")
        self.logger.log("Pipeline Engine Initialized. Commencing optimization run...")
        
        product_name = (
            self.state.products[0]
            if self.state.products
            else "unknown"
        )
        self.logger.log(f"Target Product Profile Mapped: '{product_name}'")
        
        # Load historical entries from memory database
        self.logger.log("🧠 Querying SQLite long-term storage ledger...")
        memory = StrategyMemory()
        history = memory.get_product_history(product_name)
        
        # Format and save historical strategies into active state context
        formatted_history = []
        if history:
            import json
            for row in history:
                timestamp, final_strat_str = row
                try:
                    strat_dict = json.loads(final_strat_str) if isinstance(final_strat_str, str) else final_strat_str
                    if strat_dict:  # Ignore empty runs
                        formatted_history.append({
                            "timestamp": timestamp,
                            "strategy": strat_dict
                        })
                except Exception:
                    continue
                    
        self.state.memory_context = formatted_history
        self.logger.log(f"Memory Matrix Hydrated: Found {len(formatted_history)} historical runs for this item.")
        
        if formatted_history:
            print(f"✅ Found {len(formatted_history)} historical runs for '{product_name}'. Injecting memory context.")
        else:
            print(f"ℹ️ No history found for '{product_name}'. Running on pristine baseline metrics.")
            
        return self.state

    @router(initialize)
    def route_evaluation(self):
        print("\n=== [ROUTER] DETERMINING EVALUATION PATH ===")
        opt_type = getattr(self.state, "optimization_type", "full").lower()
        self.logger.log(f"Junction Gate reached. Dispatching workflows for: '{opt_type.upper()}'")
        return opt_type

    # =====================================================================
    # 📋 STAGE 2: SINGLE-TRACK PIPELINES (Isolated Branch Mode)
    # =====================================================================

    @listen("inventory")
    def inventory_pipeline(self):
        print("\n📥 Running Isolated Inventory Analytics Layer...")
        self.logger.log("📋 Activating Isolated Inventory Analyst Crew... Scanning stock velocity.")
        
        product_name = [self.state.products[0] if self.state.products else "unknown"]
        tool = InventoryAnalyticsTool(dataset_path=DATA_PATH)
        tool_output = tool.run(product_name)
        
        insights = run_inventory_crew(tool_output)
        self.state.inventory_insights = normalize_output(insights)
        
        print("✅ Single-Track Inventory Processing Concluded.")
        self.logger.log("✅ Isolated Inventory Analytics processed and finalized.")
        return "complete"

    @listen("delivery")
    def delivery_pipeline(self):
        print("\n📥 Running Isolated Logistics & Geospatial Analytics Layers...")
        self.logger.log("🚚 Activating Isolated Route Analyst Crew... Compiling transit matrices.")
        
        product_name = [self.state.products[0] if self.state.products else "unknown"]
        del_tool = DeliveryAnalyticsTool(dataset_path=DATA_PATH)
        geo_tool = GeoAnalyticsTool(dataset_path=DATA_PATH)
        
        del_output = del_tool.run(product_name)
        geo_output = geo_tool.run(product_name)
        
        insights = run_route_crew(del_output, geo_output)
        self.state.delivery_insights = normalize_output(insights)
        
        print("✅ Single-Track Delivery Processing Concluded.")
        self.logger.log("✅ Isolated Geospatial Route Insights successfully captured.")
        return "complete"

    # =====================================================================
    # 🔄 STAGE 3: PARALLEL BRANCHES (Full Mode Execution)
    # =====================================================================

    @listen("full")
    def full_inventory_branch(self):
        print("\n🔄 [Parallel Branch A] Starting Inventory Analytics Stream...")
        self.logger.log("📋 Parallel Branch A: Launching Inventory Multi-threading Engine...")
        
        product_name = [self.state.products[0] if self.state.products else "unknown"]
        tool = InventoryAnalyticsTool(dataset_path=DATA_PATH)
        tool_output = tool.run(product_name)
        
        insights = run_inventory_crew(tool_output)
        self.state.inventory_insights = normalize_output(insights)
        
        print("✅ Parallel Branch A Context Hydrated.")
        self.logger.log("✅ Parallel Branch A (Inventory Metrics) Synchronized.")
        return "inventory_done"

    @listen("full")
    def full_delivery_branch(self):
        print("\n🔄 [Parallel Branch B] Starting Delivery & Geo Analytics Stream...")
        self.logger.log("🚚 Parallel Branch B: Launching Geospatial Routing Systems...")
        
        product_name = [self.state.products[0] if self.state.products else "unknown"]
        del_tool = DeliveryAnalyticsTool(dataset_path=DATA_PATH)
        geo_tool = GeoAnalyticsTool(dataset_path=DATA_PATH)
        
        del_output = del_tool.run(product_name)
        geo_output = geo_tool.run(product_name)
        
        insights = run_route_crew(del_output, geo_output)
        self.state.delivery_insights = normalize_output(insights)
        
        print("✅ Parallel Branch B Context Hydrated.")
        self.logger.log("✅ Parallel Branch B (Route Matrices) Synchronized.")
        return "route_done"

    # =====================================================================
    # ⚡ STAGE 4: SYNCHRONIZATION AND STRATEGY DRAFTING
    # =====================================================================

    @listen(and_(full_inventory_branch, full_delivery_branch))
    def strategy_stage(self):
        print("\n🎯 [Junction Sync] Both analytical streams resolved. Activating Strategist...")
        self.logger.log("⚡ Parallel Streams Synchronized. Engaging regional Strategist Crew...")
        
        strategy = run_strategy_crew(
            self.state.inventory_insights,
            self.state.delivery_insights,
            self.state.memory_context
        )
        self.state.strategy = normalize_output(strategy)
        
        print("🎯 Strategy Draft Generated with Delta Reasoning Context.")
        self.logger.log("✍️ Strategic Playbook draft generated. Handing over to validation loop...")
        return "strategy_complete"

    # =====================================================================
    # ⚖️ STAGE 5: CRITIQUE AND EVOLUTIONARY LOOP MANAGEMENT
    # =====================================================================

    @listen(strategy_stage)
    def critique_stage(self):
        print("\n🕵️ Passing Strategy Payload to Senior Risk Critic for Evaluation...")
        self.logger.log("⚖️ Critic Crew activated. Performing risk-mitigation and compliance audit...")
        
        critique = run_critique_crew(self.state.strategy)
        self.state.critique = normalize_output(critique)
        
        status = "revise"
        if isinstance(self.state.critique, dict):
            status = self.state.critique.get("approval_status", "revise").lower()
        elif isinstance(self.state.critique, str) and "APPROVED" in self.state.critique.upper():
            status = "approved"
            
        self.state.approval_status = status.upper()
        print(f"✅ Critique Analysis Concluded. Status: {self.state.approval_status}")
        return "critique_complete"

    @router(critique_stage)
    def reflection_router(self):
        status = self.state.approval_status.lower()
        print(f"🧠 [Reflection Router] Critic Evaluation Status Determined: '{status.upper()}'")
        
        if status == "approved":
            self.logger.log("✅ Strategy verified with high-confidence by Critic. Bypassing revisions.")
            return "complete"
        else:
            self.logger.log(f"⚠️ Critic flagged optimization flaws. Triggering Revision Loop (Run #{self.state.revision_count + 1}).")
            return "revise"

    # =====================================================================
    # 💾 STAGE 6: MEMORY STORAGE AND REVERSION LIFECYCLES
    # =====================================================================

    def save_to_memory(self, override_strategy=None):
        """Helper sequence to append results securely to SQLite database"""
        memory = StrategyMemory()
        product_name = self.state.products[0] if self.state.products else "unknown"
        strategy_payload = override_strategy if override_strategy is not None else self.state.final_strategy

        memory.save_strategy(
            product_name,
            self.state.inventory_insights,
            self.state.delivery_insights,
            self.state.strategy,
            self.state.critique,
            strategy_payload
        )

    @listen("revise")
    def revision_stage(self):
        print("\n🔄 [Loop Triggered] Hardening Strategy Playbook using Critic Insights...")
        self.logger.log("🔄 Revision loop running. Refining playbook against targeted critique parameters...")
        
        final_strategy = run_revision_crew(self.state.strategy, self.state.critique)
        parsed_strategy = normalize_output(final_strategy)
        
        self.state.final_strategy = parsed_strategy
        self.state.revision_count += 1
        
        # Save to SQLite
        self.save_to_memory(override_strategy=parsed_strategy)
        
        print("🏁 Strategy Hardened, Finalized & Saved to Memory.")
        self.logger.log("🏁 Operational strategy hardened, signed off, and stored to SQLite instance.")
        
        # 🔑 FIX: Return the fully formatted strategy payload structure directly!
        return parsed_strategy

    @listen("complete")
    def complete(self):
        print("\n🏁 Pristine Strategy Fast-Tracked. No Revisions Required.")
        
        parsed_strategy = normalize_output(self.state.strategy)
        self.state.final_strategy = parsed_strategy
        
        # Save to SQLite
        self.save_to_memory(override_strategy=parsed_strategy)
        
        print("🏁 Final Strategy Saved directly to memory storage layers.")
        self.logger.log("🏁 Pristine strategy saved directly to local database structures.")
        
        # 🔑 FIX: Return the fully formatted strategy payload structure directly!
        return parsed_strategy