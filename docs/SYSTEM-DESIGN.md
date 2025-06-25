# System Design & PRD: Modular AI Flow Builder

## 1. Overview
This project is a modular, node-based flow builder for conversational AI and data processing. It enables users to visually or programmatically define workflows (flows) as graphs of components (nodes) and connections (edges), supporting both standard and conditional logic. The backend is built with FastAPI and uses LangGraph as the workflow engine.

---

## 2. High-Level Architecture

```mermaid
graph TD
    A[API (FastAPI)] -->|Flow CRUD/Execution| B(Runtime: graph_runtime.py)
    B -->|Builds| C[LangGraph StateGraph]
    C -->|Invokes| D[Component Registry]
    D -->|Implements| E[Node Classes (core/core_tools/)]
    C -->|Executes| F[Flow State]
    B -->|Reads| G[Flow JSON]
    G -.->|Frontend| A
```

---

## 3. Flow Definition & Execution
- **Flows** are defined as JSON with:
  - `nodes`: List of components (type, function, config, etc.)
  - `edges`: List of connections (source, target, type, etc.)
  - `entry_point`/`finish_point`: Start and end nodes
  - `state_schema`: State keys/types
- **Execution**:
  1. API receives a request to execute a flow with an initial state.
  2. `graph_runtime.py` builds a LangGraph StateGraph from the JSON.
  3. Nodes are registered from the component registry.
  4. Edges are added (including conditional/branching logic).
  5. The compiled graph is invoked with the initial state.

---

## 4. Component (Node) System
- Components are Python classes/functions in `core/core_tools/`.
- Registered in `COMPONENT_REGISTRY` in `core/utils/helper.py`.
- Each node type (e.g., input, agent, output, transform, conditional) implements a callable interface.
- To add a new component:
  1. Implement the class/function in `core/core_tools/`.
  2. Register it in `COMPONENT_REGISTRY`.
  3. Add its schema to `component_schema.json`.

---

## 5. Edge System
- **Standard Edges**: Direct connections between nodes.
- **Conditional Edges**: Use LangGraph's `add_conditional_edges` for router/branching logic.
- **JSON Example for Conditional Edge**:
```json
{
  "source": "router_1",
  "type": "conditional",
  "condition": "lambda state: 'true' if state['flag'] else 'false'",
  "path_map": {"true": "node_a", "false": "node_b"}
}
```
- **Implementation**: In `graph_runtime.py`, parse edges and use `add_conditional_edges` for conditional types.

---

## 6. Runtime Logic & LangGraph Integration
- `core/graph_runtime.py` builds the runtime graph:
  - Uses `StateGraph(dict)` for dynamic state.
  - StateGraph(dict) dict is used for flexibility and not binding the graph state with pydantic or typed dict. Make sure the api and core follows dict for graph state management.
  - Adds nodes from the registry.
  - Adds edges (standard and conditional).
  - Compiles and invokes the graph.
- **If LangGraph or runtime logic changes**:
  - Update `build_graph_from_json` to match new APIs.
  - Review node signatures and state handling.
  - Update component registration if needed.

---

## 7. Extensibility & Upgrade Path
- **To add new node types**: Implement in `core/core_tools/`, register, and update schema.
- **To add new edge types**: Extend JSON schema and edge parsing logic in `graph_runtime.py`.
- **On LangGraph/package upgrade**:
  - Review `core/graph_runtime.py` for API changes.
  - Update node/component signatures if state or config handling changes.
  - Test all flows using `tests/test_api.py`.

---

## 8. Testing & Validation
- Use `tests/test_api.py` for API and flow execution tests.
- Validate flows via `/api/flows/{flow_id}/validate` endpoint.
- Add new tests for new node/edge types as needed.

---

## 10. File/Folder Impact for Runtime Changes or Upgrades
- **core/graph_runtime.py**: Main runtime logic, node/edge parsing, LangGraph integration.
- **core/utils/helper.py**: Component registry, LLM provider logic.
- **core/core_tools/**: Node/component implementations.
- **core/core_tools/custom_component.py**: Base component of any existing or new component registry, it will help for testing and maintainance of apps and tools integration in the application.
- **component_schema.json**: Node type definitions for frontend/backend.
- **api/v1/endpoints.py**: API endpoints for flow CRUD and execution.
- **tests/test_api.py**: Test coverage for flows and runtime.

---

## 11. Upgrade/Refactor Checklist
- Review LangGraph release notes for breaking changes.
- Update `build_graph_from_json` and node registration logic.
- Update or migrate node/component classes as needed.
- Update tests and validate all flows.
- Update documentation in `docs/` as needed.

---

## 12. References
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Project README]
