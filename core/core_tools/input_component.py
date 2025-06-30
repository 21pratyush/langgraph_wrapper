from core.core_tools.custom_component import CustomComponent
from langsmith import traceable

class InputComponent(CustomComponent):
    def __init__(self, config=None):
        super().__init__(config=config)

    @traceable(run_type="tool", name="input_node")
    def __call__(self, state: dict) -> dict:
        print("[Input Node] State:", state)
        print("[Input Node] Keys in state:", list(state.keys()))
        return dict(state)
