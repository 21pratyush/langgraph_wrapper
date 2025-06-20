import os
from typing import TypedDict, Callable
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph
from langchain_core.runnables import RunnableLambda

# === Define State Schema ===
class GraphState(TypedDict):
    user_input: str
    response: str | None

# === Utility to resolve env vars ===
def resolve_env_var(value: str) -> str:
    if value.startswith("env:"):
        return os.getenv(value.split("env:")[1])
    return value

# === LLM Factory ===
def get_llm(llm_config: dict) -> ChatGoogleGenerativeAI:
    model_name = resolve_env_var(llm_config["model"])
    api_key = resolve_env_var(llm_config["api_key"])
    return ChatGoogleGenerativeAI(model=model_name, google_api_key=api_key)

# === Node Functions ===
def input_node(state: dict) -> dict:
    # Pass through all initial state keys
    return dict(state)

def agent_node_factory(llm):
    def agent_node(state: dict) -> dict:
        # Use user_input, then uppercase, then sum, then any string/number value
        input_value = (
            state.get("user_input")
            or state.get("uppercase")
            or state.get("sum")
        )
        if input_value is None:
            # fallback: use first string/number value in state
            for v in state.values():
                if isinstance(v, (str, int, float)):
                    input_value = v
                    break
        if input_value is None:
            return {**state, "response": "No input for agent."}
        response = llm.invoke(str(input_value))
        return {**state, "response": response.content}
    return agent_node

def output_node(state: dict) -> dict:
    print("Output:", state)
    # Always return the full state
    return dict(state)

def string_uppercase_node(state: dict) -> dict:
    # Expects 'user_input' or 'input' in state
    value = state.get("user_input") or state.get("input")
    if value is None:
        return {**state, "uppercase": None}
    return {**state, "uppercase": str(value).upper()}

def math_add_node(state: dict) -> dict:
    # Expects 'a' and 'b' in state
    a = state.get("a")
    b = state.get("b")
    if a is None or b is None:
        return {**state, "sum": None}
    return {**state, "sum": a + b}

# === Build the Graph Dynamically from JSON ===
def build_graph_from_json(json_def: dict, llm=None) -> StateGraph:
    graph = StateGraph(GraphState)

    # Prepare function registry
    if llm is None:
        llm = get_llm(json_def["llm"])
    function_registry: dict[str, Callable] = {
        "input_node": input_node,
        "agent_node": agent_node_factory(llm),
        "output_node": output_node,
        "string_uppercase_node": string_uppercase_node,
        "math_add_node": math_add_node
    }

    for node_name, node_def in json_def["nodes"].items():
        fn_name = node_def["function"]
        fn = function_registry.get(fn_name)
        if not fn:
            raise ValueError(f"Function '{fn_name}' not found.")
        graph.add_node(node_name, RunnableLambda(fn))

    for edge in json_def["edges"]:
        graph.add_edge(edge["from"], edge["to"])

    graph.set_entry_point(json_def["entry_point"])
    graph.set_finish_point(json_def["finish_point"])

    return graph