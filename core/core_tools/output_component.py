from core.core_tools.custom_component import CustomComponent
from langsmith import traceable

class OutputComponent(CustomComponent):
    def __init__(self, config=None):
        super().__init__(config=config)

    @traceable(run_type="tool", name="output_node")
    def __call__(self, state: dict) -> dict:
        """
        Processes the final state and returns a structured output.
        It prioritizes agent_output, then other known tool outputs.
        """
        print("[Output Node] Final state received:", state)
        
        output_message = "Flow completed."
        if 'agent_output' in state:
            output_message = state['agent_output']
        elif 'current_year' in state:
            output_message = f"The current year is: {state['current_year']}"
        elif 'user_input' in state:
            # Fallback if no other output is generated
            output_message = f"Processed input: {state['user_input']}"
        else:
            output_message = "Flow finished without a standard output."

        # The final return from the graph is this dictionary
        return {"output": output_message}
