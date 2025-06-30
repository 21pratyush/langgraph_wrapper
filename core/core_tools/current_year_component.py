from core.core_tools.custom_component import CustomComponent
import datetime
from langsmith import traceable

class CurrentYearComponent(CustomComponent):
    """
    A component that returns the current year.
    """
    def __init__(self, llm=None, config=None, tools=None):
        super().__init__(llm=llm, config=config, tools=tools)
    @traceable(run_type="tool", name="current_year_node")
    def __call__(self, state: dict) -> dict:
        """
        Calculates the current year and adds it to the state.

        The result is stored in the `current_year` key.
        """
        print("-> CurrentYearComponent: Running")
        current_year = datetime.datetime.now().year
        response = f"The current year is {current_year} +1."
        
        # Add to state
        new_state = state.copy()
        new_state['current_year'] = current_year
        new_state['response'] = response
        
        return new_state 