from core.core_tools.custom_component import CustomComponent
from langchain_core.messages import HumanMessage, SystemMessage
import json
import pprint
from core.utils.llm_factory import get_llm
from langsmith import traceable

class AgentComponent(CustomComponent):
    def __init__(self, config=None, tools=None):
        llm = get_llm(config) if config and config.get("model") else None
        super().__init__(llm=llm, config=config, tools=tools)

    @traceable(run_type="tool", name="agent_node")
    def __call__(self, state: dict) -> dict:
        if not self.llm:
            return {**state, "agent_output": "Agent Error: LLM not configured or initialized."}

        input_keys = self.config.get("input_keys") if self.config else None
        input_value = None
        if input_keys:
            for k in input_keys:
                if k in state:
                    input_value = state[k]
                    break
        else:
            input_value = (
                state.get("user_input")
                or state.get("uppercase")
                or state.get("sum")
            )
            if input_value is None:
                for v in state.values():
                    if isinstance(v, (str, int, float)):
                        input_value = v
                        break
        if input_value is None:
            return {**state, "agent_output": "No input for agent."}

        # Tools are now resolved at runtime using the flow_nodes map
        tool_descriptions = self.config.get("tool_descriptions", {})
        tool_names = list(tool_descriptions.keys())
        
        system_prompt = self.config.get("system_prompt", "")
        try:
            # Allow the prompt to be formatted with the current state
            system_prompt = system_prompt.format(**state)
        except KeyError:
            # If a key in the prompt is not in the state, use the original prompt.
            # This allows for optional context.
            pass
        
        # If tools are specified, let the LLM decide which one to use
        if tool_names:
            tool_desc_str = "\n".join([f"- {name}: {desc}" for name, desc in tool_descriptions.items()])
            
            system_message_content = (
                f"{system_prompt}\n"
                f"You have access to the following tools:\n{tool_desc_str}\n"
                "Based on the user's input, decide if a tool is needed. "
                "If a tool is appropriate, respond with a JSON object like this: {\"tool\": \"<tool_name>\", \"input\": <input_for_tool>}. "
                "If no tool is needed, respond with {\"tool\": null, \"input\": null}."
            )
            
            messages = [
                SystemMessage(content=system_message_content),
                HumanMessage(content=str(input_value))
            ]

            provider_name = type(self.llm).__name__
            llm_kwargs = {}
            if self.config:
                if provider_name == "ChatOpenAI" or provider_name == "ChatDeepSeek":
                    if "temperature" in self.config:
                        llm_kwargs["temperature"] = self.config["temperature"]
                    if "max_tokens" in self.config:
                        llm_kwargs["max_tokens"] = self.config["max_tokens"]
            
            llm_response = self.llm.invoke(messages, **llm_kwargs)

            try:
                tool_decision = json.loads(getattr(llm_response, "content", str(llm_response)))
            except Exception:
                tool_decision = {"tool": None, "input": None}
            
            tool_to_call = tool_decision.get("tool")
            tool_input = tool_decision.get("input")

            # Execute the chosen tool if it exists in the flow
            if tool_to_call and tool_to_call in self.config.get('flow_nodes', {}):
                # Resolve tool function from the flow_nodes map
                tool_fn = self.config['flow_nodes'][tool_to_call]
                
                # Prepare state for the tool call
                tool_state = state.copy()
                tool_state["user_input"] = tool_input
                
                # Execute the tool
                tool_result = tool_fn(tool_state)
                
                # Compose the manager's response with the tool's output
                response = f"Tool '{tool_to_call}' was used. Tool response: {tool_result.get('agent_output', tool_result)}"
                return {**state, "agent_output": response}
            else:
                # If no tool is chosen or it's invalid, return the direct LLM response
                return {**state, "agent_output": getattr(llm_response, "content", str(llm_response))}
        else:
            # No tools defined, so just run a normal LLM prompt
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=str(input_value))
            ]
            
            provider_name = type(self.llm).__name__
            if provider_name == "ChatGoogleGenerativeAI":
                response = self.llm.invoke(messages)
            else:
                llm_kwargs = {}
                if self.config:
                    if provider_name == "ChatOpenAI":
                        if "temperature" in self.config:
                            llm_kwargs["temperature"] = self.config["temperature"]
                        if "max_tokens" in self.config:
                            llm_kwargs["max_tokens"] = self.config["max_tokens"]
                    elif provider_name == "ChatDeepSeek":
                        if "temperature" in self.config:
                            llm_kwargs["temperature"] = self.config["temperature"]
                        if "max_tokens" in self.config:
                            llm_kwargs["max_tokens"] = self.config["max_tokens"]
                response = self.llm.invoke(messages, **llm_kwargs)
            return {**state, "agent_output": getattr(response, "content", str(response))}
