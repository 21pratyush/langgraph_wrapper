from core.core_tools.custom_component import CustomComponent

class OutputComponent(CustomComponent):
    def __init__(self, config=None):
        super().__init__(config=config)

    def __call__(self, state: dict) -> dict:
        print("[Output Node] State:", state)
        print("[Output Node] Keys in state:", list(state.keys()))
        return dict(state)
