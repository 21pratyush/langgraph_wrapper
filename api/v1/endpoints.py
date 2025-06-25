from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List, Any, Optional
import json
import os
from core.graph_runtime import build_graph_from_json
from core.utils.helper import get_llm

from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Flow Builder API", version="1.0.0")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic Models
class NodePosition(BaseModel):
    x: float
    y: float

class NodeData(BaseModel):
    label: str
    properties: Dict[str, Any] = {}

class FlowNode(BaseModel):
    id: str
    type: str
    position: NodePosition
    data: NodeData

class FlowEdge(BaseModel):
    id: str
    source: str
    target: str
    sourceHandle: Optional[str] = None
    targetHandle: Optional[str] = None
    type: str = "default"
    style: Dict[str, Any] = {}
    condition: Optional[str] = None
    path_map: Optional[Dict[str, str]] = None

class FlowDefinition(BaseModel):
    flow_id: str
    name: str
    description: str
    nodes: List[FlowNode]
    edges: List[FlowEdge]
    entry_point: str
    finish_point: str
    state_schema: Dict[str, Any]
    llm_config: Dict[str, Any]

class ExecutionRequest(BaseModel):
    initial_state: Dict[str, Any]

# In-memory storage (replace with database in production)
component_definitions = {}
flow_definitions = {}

# Load component definitions on startup
def load_component_definitions():
    try:
        with open("component_schema.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {
            "schema_version": "1.0.0",
            "component_definitions": {},
            "categories": {},
            "data_types": {}
        }

@app.on_event("startup")
async def startup_event():
    global component_definitions
    component_definitions = load_component_definitions()

# API Endpoints

@app.get("/api/components")
async def get_component_definitions():
    """Get all available component definitions for the frontend"""
    return component_definitions

@app.get("/api/components/{component_type}")
async def get_component_definition(component_type: str):
    """Get specific component definition"""
    if component_type not in component_definitions.get("component_definitions", {}):
        raise HTTPException(status_code=404, detail="Component not found")
    return component_definitions["component_definitions"][component_type]

@app.get("/api/categories")
async def get_categories():
    """Get all component categories"""
    return component_definitions.get("categories", {})

@app.get("/api/data-types")
async def get_data_types():
    """Get all supported data types"""
    return component_definitions.get("data_types", {})

@app.post("/api/flows")
async def create_flow(flow: FlowDefinition):
    """Create a new flow definition"""
    # Validate flow structure
    validation_result = validate_flow(flow)
    if not validation_result["valid"]:
        raise HTTPException(status_code=400, detail=validation_result["errors"])
    
    flow_definitions[flow.flow_id] = flow.dict()
    return {"message": "Flow created successfully", "flow_id": flow.flow_id}

@app.get("/api/flows")
async def get_flows():
    """Get all flow definitions"""
    return list(flow_definitions.values())

@app.get("/api/flows/{flow_id}")
async def get_flow(flow_id: str):
    """Get specific flow definition"""
    if flow_id not in flow_definitions:
        raise HTTPException(status_code=404, detail="Flow not found")
    return flow_definitions[flow_id]

@app.put("/api/flows/{flow_id}")
async def update_flow(flow_id: str, flow: FlowDefinition):
    """Update existing flow definition"""
    if flow_id not in flow_definitions:
        raise HTTPException(status_code=404, detail="Flow not found")
    
    validation_result = validate_flow(flow)
    if not validation_result["valid"]:
        raise HTTPException(status_code=400, detail=validation_result["errors"])
    
    flow_definitions[flow_id] = flow.dict()
    return {"message": "Flow updated successfully"}

@app.delete("/api/flows/{flow_id}")
async def delete_flow(flow_id: str):
    """Delete flow definition"""
    if flow_id not in flow_definitions:
        raise HTTPException(status_code=404, detail="Flow not found")
    
    del flow_definitions[flow_id]
    return {"message": "Flow deleted successfully"}

@app.post("/api/flows/{flow_id}/execute")
async def execute_flow(flow_id: str, request: ExecutionRequest):
    """Execute a flow with given initial state"""
    if flow_id not in flow_definitions:
        raise HTTPException(status_code=404, detail="Flow not found")
    
    flow_def = flow_definitions[flow_id]
    
    # Here you would integrate with your existing LangGraph execution logic
    # This is a placeholder for the actual execution
    try:
        result = await execute_langgraph_flow(flow_def, request.initial_state)
        print(f"Execution result: {result}")
        return {
            "status": "success",
            "result": result,
            "execution_id": f"exec_{flow_id}_{hash(str(request.initial_state))}"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Execution failed: {str(e)}")

@app.post("/api/flows/{flow_id}/validate")
async def validate_flow_endpoint(flow_id: str):
    """Validate flow structure and connections"""
    if flow_id not in flow_definitions:
        raise HTTPException(status_code=404, detail="Flow not found")
    
    flow_def = FlowDefinition(**flow_definitions[flow_id])
    validation_result = validate_flow(flow_def)
    return validation_result

@app.get("/api/flows/{flow_id}/export")
async def export_flow(flow_id: str, format: str = "json"):
    """Export flow in various formats"""
    if flow_id not in flow_definitions:
        raise HTTPException(status_code=404, detail="Flow not found")
    
    flow_def = flow_definitions[flow_id]
    
    if format == "langgraph":
        # Convert to your original LangGraph format
        return convert_to_langgraph_format(flow_def)
    elif format == "json":
        return flow_def
    else:
        raise HTTPException(status_code=400, detail="Unsupported export format")

# Helper Functions

def validate_flow(flow: FlowDefinition) -> Dict[str, Any]:
    """Validate flow structure"""
    errors = []
    
    # Check if entry and finish points exist
    node_ids = [node.id for node in flow.nodes]
    if flow.entry_point not in node_ids:
        errors.append(f"Entry point '{flow.entry_point}' not found in nodes")
    if flow.finish_point not in node_ids:
        errors.append(f"Finish point '{flow.finish_point}' not found in nodes")
    
    # Check edge connections
    for edge in flow.edges:
        if edge.source not in node_ids:
            errors.append(f"Edge source '{edge.source}' not found in nodes")
        if edge.target not in node_ids:
            errors.append(f"Edge target '{edge.target}' not found in nodes")
    
    # Check for required node types
    node_types = [node.type for node in flow.nodes]
    if "input" not in node_types:
        errors.append("Flow must contain at least one input node")
    if "output" not in node_types:
        errors.append("Flow must contain at least one output node")
    
    return {
        "valid": len(errors) == 0,
        "errors": errors
    }

async def execute_langgraph_flow(flow_def: Dict[str, Any], initial_state: Dict[str, Any]) -> Dict[str, Any]:
    """Execute the flow using LangGraph (real execution)"""
    langgraph_format = convert_to_langgraph_format(flow_def)
    llm = get_llm(langgraph_format["llm"])
    workflow = build_graph_from_json(langgraph_format, llm=llm)
    app = workflow.compile()
    print(f"Executing flow with initial state: {initial_state}")
    result = app.invoke(initial_state)
    return result

def convert_to_langgraph_format(flow_def: Dict[str, Any]) -> Dict[str, Any]:
    """Convert flow definition to original LangGraph format"""
    nodes = {}
    edges = []
    
    # Convert nodes, include config/data for runtime
    for node in flow_def["nodes"]:
        nodes[node["id"]] = {
            "type": "RunnableLambda",
            "function": f"{node['type']}_node",  # Map to function names
            "config": node.get("data", {}).get("properties", {})
        }
    
    # Convert edges
    for edge in flow_def["edges"]:
        edge_dict = edge.copy()
        # Map 'source'/'target' to 'from'/'to' for compatibility, but keep all fields
        if "source" in edge_dict:
            edge_dict["from"] = edge_dict["source"]
        if "target" in edge_dict:
            edge_dict["to"] = edge_dict["target"]
        edges.append(edge_dict)
    
    return {
        "nodes": nodes,
        "edges": edges,
        "entry_point": flow_def["entry_point"],
        "finish_point": flow_def["finish_point"],
        "state_schema": flow_def["state_schema"],
        "llm": flow_def["llm_config"]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)