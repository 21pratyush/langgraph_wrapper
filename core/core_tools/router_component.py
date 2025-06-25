from core.core_tools.custom_component import CustomComponent

class RouterComponent(CustomComponent):
    def __init__(self, config=None, llm=None, tools=None):
        super().__init__(llm=llm, config=config, tools=tools)

    def __call__(self, state: dict) -> dict:
        routing_logic = self.config.get("routing_logic")
        if routing_logic:
            try:
                exec(routing_logic, {"state": state})
                return state
            except Exception as e:
                state["route_label"] = "error"
                state["router_error"] = str(e)
                return state
        return {**state, "route_label": "unknown"}