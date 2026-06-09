import json
from models.state import LogisticsState
from flows.logistics_flow import LogisticsFlow  # Change to 'from logistics_flow' if in root

def run_integration_test():
    print("======================================================================")
    # 1. Instantiate the asynchronous State-driven Flow
    print("🚀 Instantiating Enterprise Logistics Flow Machine...")
    flow = LogisticsFlow()
    
    # 2. Inject initial test telemetry into the state layer (Clean inputs)
    flow.state.products = ["Nike Men's CJ Elite 2 TD Football Cleat"]
    flow.state.optimization_type = "full"
    flow.state.revision_count = 0
    
    print(f"📊 Test Target: Product List -> {flow.state.products}")
    print(f"⚙️  Execution Profile: Optimization Type -> '{flow.state.optimization_type}'")
    print("======================================================================")
    
    # 3. Kick off the workflow lifecycle
    print("\n🔥 Activating CrewAI Flow Engine. Initializing threads...")
    final_output = flow.kickoff()
    
    # 4. Generate Post-Execution Audit Report
    print("\n======================= POST-FLOW LIFECYCLE REPORT =======================")
    print(f"🔄 Total Reflection Loops Executed: {flow.state.revision_count}")
    print(f"🧠 Final Internal Approval Status:  {flow.state.approval_status}")
    
    print("\n📋 Final Strategy Playbook Payload:")
    # Since default_factory=dict, an empty dictionary {} is falsy.
    if flow.state.final_strategy:
        # Enforced as a pure dictionary by normalize_output, no hasattr check required
        print(json.dumps(flow.state.final_strategy, indent=2))
    else:
        print("❌ Warning: No final strategy asset populated in the state tree.")
    print("==========================================================================")

    # 5. Architecture Verification Assertions
    print("\n🔍 Verifying Orchestration Integrity:")
    if flow.state.optimization_type == "full":
        # Ensure metrics from both parallel paths exist
        has_inventory_metrics = len(flow.state.inventory_metrics) > 0
        has_delivery_metrics = len(flow.state.delivery_metrics) > 0
        
        print(f" -> Parallel Branch A (Inventory Tools) Resolved: {has_inventory_metrics}")
        print(f" -> Parallel Branch B (Delivery/Geo Tools) Resolved: {has_delivery_metrics}")
        
        if has_inventory_metrics and has_delivery_metrics:
            print(" ✅ SUCCESS: and_() Barrier Synchronization functioned perfectly.")
        else:
            print(" ❌ FAILURE: Parallel streams failed to synchronize state variables correctly.")
            
    if flow.state.revision_count > 0:
        print(" ✅ SUCCESS: Conditional Router successfully identified a 'Revise' state and engaged reflection loops.")
    else:
        print(" ℹ️  INFO: Strategy bypassed revision (Pristine path execution or crews currently mocked).")

if __name__ == "__main__":
    run_integration_test()