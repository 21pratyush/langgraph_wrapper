from core.core_tools.custom_component import CustomComponent
from langsmith import traceable

class RouterComponent(CustomComponent):
    def __init__(self, config=None, llm=None, tools=None):
        super().__init__(llm=llm, config=config, tools=tools)

    @traceable(run_type="tool", name="router_node")
    def __call__(self, state: dict) -> dict:
        routing_logic = self.config.get("routing_logic")
        
        if not routing_logic:
            state["route_label"] = "unknown"
            return state

        # Wrap the user-provided logic in a function for safe execution
        func_code = "def get_route(state):\n"
        for line in routing_logic.strip().split('\n'):
            func_code += f"    {line}\n"

        local_scope = {}
        try:
            # Define the function in the local scope
            exec(func_code, {}, local_scope)
            route_fn = local_scope['get_route']
            
            # Call the function and get the route label
            route_label = route_fn(state)
            state["route_label"] = route_label
            
        except Exception as e:
            print(f"❌ Error executing router logic: {e}")
            state["route_label"] = "error"
            state["router_error"] = str(e)
            
        return state