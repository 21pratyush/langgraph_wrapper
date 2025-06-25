import os
from typing import Any
from dotenv import load_dotenv

## Core-Tools Imports
from core.core_tools.input_component import InputComponent
from core.core_tools.agent_component import AgentComponent
from core.core_tools.output_component import OutputComponent
from core.core_tools.router_component import RouterComponent
from core.core_tools.current_year_component import CurrentYearComponent

## LLM Provider Imports
from langchain_google_genai import ChatGoogleGenerativeAI        
from langchain_openai import ChatOpenAI
from langchain_deepseek import ChatDeepSeek

load_dotenv()

# from pydantic import BaseModel
# from typing import Dict, List, Any, Optional
# from core.graph_runtime import build_graph_from_json
# from core.utils.helper import get_llm

# Pydantic Models
# class NodePosition(BaseModel):
#     x: float
#     y: float

# class NodeData(BaseModel):
#     label: str
#     properties: Dict[str, Any] = {}

# class FlowNode(BaseModel):
#     id: str
#     type: str
#     position: NodePosition
#     data: NodeData

# class FlowEdge(BaseModel):
#     id: str
#     source: str
#     target: str
#     sourceHandle: Optional[str] = None
#     targetHandle: Optional[str] = None
#     type: str = "default"
#     style: Dict[str, Any] = {}
#     condition: Optional[str] = None
#     path_map: Optional[Dict[str, str]] = None

# class FlowDefinition(BaseModel):
#     flow_id: str
#     name: str
#     description: str
#     nodes: List[FlowNode]
#     edges: List[FlowEdge]
#     entry_point: str
#     finish_point: str
#     state_schema: Dict[str, Any]
#     llm_config: Dict[str, Any]


# === LLM Provider Registry ===
def get_llm(llm_config: dict) -> Any:
    provider = llm_config.get("provider", "GoogleGenerativeAI").lower()
    model_name = resolve_env_var(llm_config.get("model", ""))
    api_key = resolve_env_var(llm_config.get("api_key", ""))
    # Add more providers as needed
    if provider == "googlegenerativeai":
        return ChatGoogleGenerativeAI(model=model_name, google_api_key=api_key)
    elif provider == "openai":
        return ChatOpenAI(model=model_name, api_key=api_key)
    elif provider == "deepseek":
        return ChatDeepSeek(model=model_name, api_key=api_key)
    else:
        raise ValueError(f"Unknown LLM provider: {provider}")
    
# === Utility to resolve env vars ===
def resolve_env_var(value: str) -> str:
    if value.startswith("env:"):
        return os.getenv(value.split("env:")[1])
    return value

# === Component Registry (modular, class-based) ===
COMPONENT_REGISTRY = {
    "input_node": InputComponent,
    "agent_node": AgentComponent,
    "output_node": OutputComponent,
    "router_node": RouterComponent,
    "current_year_node": CurrentYearComponent,
}


# Run Time Helper Functions

# def validate_flow(flow: FlowDefinition) -> Dict[str, Any]:
#     """Validate flow structure"""
#     errors = []
    
#     # Check if entry and finish points exist
#     node_ids = [node.id for node in flow.nodes]
#     if flow.entry_point not in node_ids:
#         errors.append(f"Entry point '{flow.entry_point}' not found in nodes")
#     if flow.finish_point not in node_ids:
#         errors.append(f"Finish point '{flow.finish_point}' not found in nodes")
    
#     # Check edge connections
#     for edge in flow.edges:
#         if edge.source not in node_ids:
#             errors.append(f"Edge source '{edge.source}' not found in nodes")
#         if edge.target not in node_ids:
#             errors.append(f"Edge target '{edge.target}' not found in nodes")
    
#     # Check for required node types
#     node_types = [node.type for node in flow.nodes]
#     if "input" not in node_types:
#         errors.append("Flow must contain at least one input node")
#     if "output" not in node_types:
#         errors.append("Flow must contain at least one output node")
    
#     return {
#         "valid": len(errors) == 0,
#         "errors": errors
#     }

# async def execute_langgraph_flow(flow_def: Dict[str, Any], initial_state: Dict[str, Any]) -> Dict[str, Any]:
#     """Execute the flow using LangGraph (real execution)"""
#     langgraph_format = convert_to_langgraph_format(flow_def)
#     llm = get_llm(langgraph_format["llm"])
#     workflow = build_graph_from_json(langgraph_format, llm=llm)
#     app = workflow.compile()
#     print(f"Executing flow with initial state: {initial_state}")
#     result = app.invoke(initial_state)
#     return result

# def convert_to_langgraph_format(flow_def: Dict[str, Any]) -> Dict[str, Any]:
#     """Convert flow definition to original LangGraph format"""
#     nodes = {}
#     edges = []
    
#     # Convert nodes, include config/data for runtime
#     for node in flow_def["nodes"]:
#         nodes[node["id"]] = {
#             "type": "RunnableLambda",
#             "function": f"{node['type']}_node",  # Map to function names
#             "config": node.get("data", {}).get("properties", {})
#         }
    
#     # Convert edges
#     for edge in flow_def["edges"]:
#         edge_dict = edge.copy()
#         # Map 'source'/'target' to 'from'/'to' for compatibility, but keep all fields
#         if "source" in edge_dict:
#             edge_dict["from"] = edge_dict["source"]
#         if "target" in edge_dict:
#             edge_dict["to"] = edge_dict["target"]
#         edges.append(edge_dict)
    
#     return {
#         "nodes": nodes,
#         "edges": edges,
#         "entry_point": flow_def["entry_point"],
#         "finish_point": flow_def["finish_point"],
#         "state_schema": flow_def["state_schema"],
#         "llm": flow_def["llm_config"]
#     }
