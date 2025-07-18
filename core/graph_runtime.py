from langgraph.graph import StateGraph
from core.utils.helper import get_llm, COMPONENT_REGISTRY
from functools import wraps

# === Build the Graph Dynamically from JSON (fully modular) ===
def merge_state_wrapper(fn):
    @wraps(fn)
    def wrapped(state, config=None):
        out = fn(state)
        if out is None:
            return dict(state)
        merged = dict(state)
        merged.update(out)
        return merged
    return wrapped

def build_graph_from_json(json_def: dict) -> StateGraph:
    graph = StateGraph(dict)

    # --- Modular: Accept nodes as list or dict ---
    nodes = json_def.get("nodes", {})
    if isinstance(nodes, list):
        nodes = {node["id"]: node for node in nodes}
    edges = json_def.get("edges", [])
    if isinstance(edges, dict):
        edges = list(edges.values())

    flow_llm_config = json_def.get("llm") or json_def.get("llm_config")

    # Build nodes with config and tools
    node_objs = {}
    for node_name, node_def in nodes.items():
        fn_name = node_def["function"]
        config = node_def.get("config") or node_def.get("data", {}).get("properties", {})

        # --- Merge flow-level llm config into agent nodes if missing ---
        if fn_name == "agent_node":
            # Only add missing keys from flow_llm_config
            if flow_llm_config:
                for k, v in flow_llm_config.items():
                    if k not in config:
                        config[k] = v

        # Instantiate the node component from the registry
        if fn_name in COMPONENT_REGISTRY:
            # Each component is now responsible for its own initialization.
            # The AgentComponent will create its own LLM instance.
            node_instance = COMPONENT_REGISTRY[fn_name](config=config)
        else:
            # Handle cases where the function might not be in the registry (e.g., legacy)
            raise ValueError(f"Component function '{fn_name}' not found in registry.")

        # Wrap all nodes to merge state automatically, except for the output node
        if fn_name != "output_node":
            node_instance = merge_state_wrapper(node_instance)
        
        node_objs[node_name] = node_instance

    # Now that all nodes are instantiated, pass the full map to agent configs
    for node_name, node_instance in node_objs.items():
        # The actual component is wrapped, so we access its config via .__wrapped__
        target_component = getattr(node_instance, '__wrapped__', node_instance)
        
        # Check class name to avoid isinstance issues with hot-reloading
        if target_component.__class__.__name__ == 'AgentComponent':
            target_component.config['flow_nodes'] = node_objs

    # Add all prepared nodes to the graph
    for node_name, node_obj in node_objs.items():
        graph.add_node(node_name, node_obj)
        
    for edge in edges:
        edge_type = edge["type"].lower() if isinstance(edge.get("type", None), str) else ""
        if edge_type == "conditional":
            # This is a simplified example; production logic would be more robust.
            # It expects the 'condition' to be a string representing a lambda function.
            path_fn = eval(edge["condition"])
            path_map = edge.get("path_map")
            graph.add_conditional_edges(edge["source"], path_fn, path_map)
        else:
            src = edge["source"] if "source" in edge else edge.get("from", "?")
            tgt = edge["target"] if "target" in edge else edge.get("to", "?")
            graph.add_edge(src, tgt)

    graph.set_entry_point(json_def["entry_point"])
    graph.set_finish_point(json_def["finish_point"])

    return graph