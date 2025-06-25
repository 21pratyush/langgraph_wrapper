class CustomComponent:
    def __init__(self, llm=None, config=None, tools=None):
        self.llm = llm
        self.config = config or {}
        self.tools = tools or []

    def __call__(self, state: dict) -> dict:
        raise NotImplementedError("Subclasses must implement __call__ method.")