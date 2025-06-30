import asyncio
from core.graph_runtime import build_graph_from_json

# --- Flow Definitions ---

# Flow 1: Simple Greeting Agent
GREETING_FLOW = {
    "nodes": {
        "input": {"function": "input_node"},
        "agent": {
            "function": "agent_node",
            "config": {
                "system_prompt": "You are a friendly greeting bot. Your job is to greet the user warmly.",
                "model": "gemini-2.0-flash"
            },
        },
        "output": {"function": "output_node"},
    },
    "edges": [
        {"source": "input", "target": "agent"},
        {"source": "agent", "target": "output"},
    ],
    "entry_point": "input",
    "finish_point": "output",
}

# Flow 2: Coding Assistant
CODING_FLOW = {
    "nodes": {
        "input": {"function": "input_node"},
        "agent": {
            "function": "agent_node",
            "config": {
                "system_prompt": "You are an expert coding assistant. Provide clear, concise, and accurate answers to programming questions.",
                "model": "gemini-2.0-flash"
            },
        },
        "output": {"function": "output_node"},
    },
    "edges": [
        {"source": "input", "target": "agent"},
        {"source": "agent", "target": "output"},
    ],
    "entry_point": "input",
    "finish_point": "output",
}

# Flow 3: Tool-based Year Fetcher
CURRENT_YEAR_FLOW = {
    "nodes": {
        "input": {"function": "input_node"},
        "get_year": {"function": "current_year_node"},
        "output": {"function": "output_node"},
    },
    "edges": [
        {"source": "input", "target": "get_year"},
        {"source": "get_year", "target": "output"},
    ],
    "entry_point": "input",
    "finish_point": "output",
}

# Flow 4: Multi-Agent Router
ROUTER_FLOW = {
    "llm_config": {"model": "gemini-2.0-flash"},
    "nodes": {
        "input": {"function": "input_node"},
        "router": {
            "function": "router_node",
            "config": {
                "routing_logic": """
user_input = state.get('user_input', '').strip().lower()
if any(word in user_input for word in ['code', 'python', 'function', 'script', 'program']):
    return 'coding'
elif any(greet in user_input for greet in ['hi', 'hello', 'hey', 'greetings']):
    return 'greeting'
else:
    return 'conversation'
"""
            }
        },
        "greeting_agent": {
            "function": "agent_node",
            "config": {
                "system_prompt": "You are a greeting bot. Only respond to greetings. If the input is not a greeting, reply: 'I am only a greeting agent.'"
            }
        },
        "coding_agent": {
            "function": "agent_node",
            "config": {
                "system_prompt": "You are a coding assistant. Only answer programming/code-related questions."
            }
        },
        "conversation_agent": {
            "function": "agent_node",
            "config": {
                "system_prompt": "You are a general conversation assistant. Do not answer greetings or code questions."
            }
        },
        "output": {"function": "output_node"},
    },
    "edges": [
        {"source": "input", "target": "router"},
        {
            "source": "router",
            "type": "conditional",
            "condition": "lambda state: state.get('route_label', 'conversation')",
            "path_map": {
                "greeting": "greeting_agent",
                "coding": "coding_agent",
                "conversation": "conversation_agent"
            }
        },
        {"source": "greeting_agent", "target": "output"},
        {"source": "coding_agent", "target": "output"},
        {"source": "conversation_agent", "target": "output"},
    ],
    "entry_point": "input",
    "finish_point": "output",
}

# Flow 5: Grounded Q&A with Dynamic Routing
GROUNDED_QA_FLOW = {
    "llm_config": {"model": "gemini-2.0-flash"},
    "nodes": {
        "input": {"function": "input_node"},
        "router": {
            "function": "router_node",
            "config": {
                "routing_logic": """
user_input = state.get('user_input', '').strip().lower()
if any(word in user_input for word in ['year', 'date', 'current', 'today']):
    return 'get_year_route'
else:
    return 'general_route'
"""
            }
        },
        "get_year": {"function": "current_year_node"},
        "synthesis_agent": {
            "function": "agent_node",
            "config": {
                "system_prompt": "You are a helpful assistant. The user's question is: '{user_input}'. The current year is: {current_year}. Use this information to form a clear and accurate answer."
            }
        },
        "general_agent": {
            "function": "agent_node",
            "config": {
                "system_prompt": "You are a helpful general assistant. Answer the user's question directly and concisely."
            }
        },
        "output": {"function": "output_node"},
    },
    "edges": [
        {"source": "input", "target": "router"},
        {
            "source": "router", "type": "conditional",
            "condition": "lambda state: state.get('route_label', 'general_route')",
            "path_map": {
                "get_year_route": "get_year",
                "general_route": "general_agent"
            }
        },
        {"source": "get_year", "target": "synthesis_agent"},
        {"source": "synthesis_agent", "target": "output"},
        {"source": "general_agent", "target": "output"},
    ],
    "entry_point": "input",
    "finish_point": "output",
}

# Flow 6: Manager/Worker Agent Pipeline
MANAGER_WORKER_FLOW = {
    "llm_config": {"model": "gemini-2.0-flash"},
    "nodes": {
        "input": {"function": "input_node"},
        "manager_agent": {
            "function": "agent_node",
            "config": {
                "system_prompt": "You are a manager. Your task is to analyze the user's request and break it down into a single, clear, and simple instruction for your worker. Do not answer the request, only provide the instruction."
            }
        },
        "worker_agent": {
            "function": "agent_node",
            "config": {
                "input_keys": ["agent_output"],
                "system_prompt": "You are a worker. Your only task is to execute the following instruction precisely and concisely."
            }
        },
        "output": {"function": "output_node"},
    },
    "edges": [
        {"source": "input", "target": "manager_agent"},
        {"source": "manager_agent", "target": "worker_agent"},
        {"source": "worker_agent", "target": "output"},
    ],
    "entry_point": "input",
    "finish_point": "output",
}

# Flow 7: Manager + Specialist Agents with Conditional Routing
MANAGER_SPECIALIST_FLOW = {
    "llm_config": {"model": "gemini-2.0-flash"},
    "nodes": {
        "input": {"function": "input_node"},
        "manager_router": {
            "function": "agent_node",
            "config": {
                "system_prompt": (
                    "You are a manager. Analyze the user's query: '{user_input}'. "
                    "If it asks for all perspectives, reply with: 'all'. "
                    "If it's HR-related, reply with: 'hr'. "
                    "If it's Finance-related, reply with: 'finance'. "
                    "If it's Tech-related, reply with: 'tech'. "
                    "If multiple, reply with a comma-separated list (e.g., 'hr,tech'). "
                    "Reply ONLY with the keyword(s)."
                )
            }
        },
        "hr_agent": {
            "function": "agent_node",
            "config": {
                "system_prompt": "You are an HR expert. Give a concise answer to: '{user_input}'."
            }
        },
        "finance_agent": {
            "function": "agent_node",
            "config": {
                "system_prompt": "You are a finance expert. Give a concise answer to: '{user_input}'."
            }
        },
        "tech_agent": {
            "function": "agent_node",
            "config": {
                "system_prompt": "You are a tech expert. Give a concise answer to: '{user_input}'."
            }
        },
        "synthesis_agent": {
            "function": "agent_node",
            "config": {
                "system_prompt": (
                    "You are a manager. Summarize the following specialist responses in a short, conversational way. "
                    "HR: '{agent_output}', Finance: '{agent_output}', Tech: '{agent_output}'. "
                    "Only include the sections that are present."
                ),
                "input_keys": ["agent_output"]
            }
        },
        "output": {"function": "output_node"},
    },
    "edges": [
        {"source": "input", "target": "manager_router"},
        # Conditional routing to specialists
        {
            "source": "manager_router",
            "type": "conditional",
            "condition": "lambda state: state.get('agent_output', 'all').replace(' ', '').split(',')",
            "path_map": {
                "hr": "hr_agent",
                "finance": "finance_agent",
                "tech": "tech_agent",
                "all": "hr_agent"  # Start with HR, then chain to others
            }
        },
        # HR path
        {"source": "hr_agent", "target": "finance_agent", "condition": "lambda state: 'all' in state.get('agent_output', '') or 'finance' in state.get('agent_output', '')"},
        {"source": "finance_agent", "target": "tech_agent", "condition": "lambda state: 'all' in state.get('agent_output', '') or 'tech' in state.get('agent_output', '')"},
        # Synthesis
        {"source": "hr_agent", "target": "synthesis_agent"},
        {"source": "finance_agent", "target": "synthesis_agent"},
        {"source": "tech_agent", "target": "synthesis_agent"},
        {"source": "synthesis_agent", "target": "output"},
    ],
    "entry_point": "input",
    "finish_point": "output",
}

# --- Execution Logic ---

FLOWS = {
    "1": ("Greeting Flow", GREETING_FLOW),
    "2": ("Coding Flow", CODING_FLOW),
    "3": ("Current Year Flow", CURRENT_YEAR_FLOW),
    "4": ("Multi-Agent Router Flow", ROUTER_FLOW),
    "5": ("Grounded Q&A Flow", GROUNDED_QA_FLOW),
    "6": ("Manager/Worker Pipeline Flow", MANAGER_WORKER_FLOW),
    "7": ("Manager + Specialist Conditional Routing Flow", MANAGER_SPECIALIST_FLOW),
}

async def run_flow(flow_def: dict, user_input: str):
    """Builds and executes a graph from a flow definition."""
    try:
        graph = build_graph_from_json(flow_def)
        app = graph.compile()
        initial_state = {"user_input": user_input}
        
        print(f"\n🚀 Executing flow...")
        final_state = await app.ainvoke(initial_state)
        
        # The output node is designed to return the final message.
        # It now returns a dictionary containing the final state.
        if isinstance(final_state, dict) and "output" in final_state:
             print(f"✅ Final Output: {final_state['output']}")
        else:
             print(f"✅ Final State: {final_state}")
             
    except Exception as e:
        print(f"❌ Error executing flow: {e}")

async def main():
    """Main CLI loop to select and run flows."""
    while True:
        print("\n--- Available Flows ---")
        for key, (name, _) in FLOWS.items():
            print(f"  {key}: {name}")
        print("  q: Quit")
        
        choice = input("\nSelect a flow to run: ").strip()
        
        if choice == 'q':
            break
        
        if choice not in FLOWS:
            print("Invalid choice, please try again.")
            continue
            
        name, flow_def = FLOWS[choice]
        print(f"\n--- Running: {name} ---")
        user_input = input("Enter your message: ").strip()
        
        await run_flow(flow_def, user_input)

if __name__ == "__main__":
    asyncio.run(main()) 