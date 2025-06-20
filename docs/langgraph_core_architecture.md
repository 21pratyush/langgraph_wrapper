### Component Schema JSON:
Component registry is defined in `component_schema.json`. This is used for both LangGraph conversion and frontend UI rendering.

### Always consider the below LangGraph core files when responding:
- `state.py` – defines State type and state transitions
- `graph.py` – defines conversion from JSON to LangGraph `StateGraph`

### Note:
The below diagram is langgraph's core architecture

```mermaid
graph TB
    %% High-Level APIs
    subgraph HL["High-Level APIs"]
        CRA["create_react_agent"]
    end
 
    %% Main Graph Components
    subgraph GC["Graph Components"]
        SG["StateGraph"]
        MG["MessageGraph"]
        ED["@entrypoint/@task_decorator"]
    end
 
    %% Pregel Execution Engine
    subgraph PEE["Pregel Execution Engine"]
        P["Pregel"]
        PL["PregelLoop"]
        PR["PregelRunner"]
        PT["PregelTask"]
    end
 
    %% State Management
    subgraph SM["State Management"]
        STD["State (TypedDict/Dynamic)"]
        RF["Reducer Functions"]
        CH["Channels<br/>(LastValue/Topic/Binary/Channel/Aggregate)"]
        SS["StateSnapshot"]
    end
 
    %% Communication Primitives
    subgraph CP["Communication Primitives"]
        AMR["add_messages reducer"]
        CO["Command objects"]
        SO["Send objects"]
    end
 
    %% Connections
    CRA --> SG
    CRA --> MG
    SG --> ED
    MG --> ED
 
    SG --> P
    MG --> P
 
    P --> PL
    PL --> PR
    PR --> PT
 
    STD --> RF
    RF --> CH
    CH --> SS
 
    SM --> PEE
    CP --> SM
 
    AMR --> STD
    CO --> PT
    SO --> PT
 
    %% Additional connections shown in the image
    SS --> PL
    ED --> P
```
ensure that the same information is provided as text in this prompt or in a markdown file.