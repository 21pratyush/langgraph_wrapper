import requests
import json
import datetime

BASE_URL = "http://localhost:8000"

def test_api():
    print("🧪 Testing Flow Builder API")
    
    # Test 1: Get components
    # print("\n1. Testing GET /api/components")
    # response = requests.get(f"{BASE_URL}/api/components")
    # print(f"Status: {response.status_code}")
    # if response.status_code == 200:
    #     data = response.json()
    #     print(f"Found {len(data.get('component_definitions', {}))} components")
    
    # # Test 2: Get categories
    # print("\n2. Testing GET /api/categories")
    # response = requests.get(f"{BASE_URL}/api/categories")
    # print(f"Status: {response.status_code}")
    # if response.status_code == 200:
    #     categories = response.json()
    #     print(f"Found {len(categories)} categories")
    
    # Test 3: Create a flow
    # print("\n3. Testing POST /api/flows")
    # test_flow = {
    #     "flow_id": "test_chatbot_flow",
    #     "name": "Test Chatbot Flow",
    #     "description": "A simple test flow",
    #     "version": "1.0.0",
    #     "created_at": "2024-01-20T10:00:00Z",
    #     "updated_at": "2024-01-20T10:00:00Z",
    #     "metadata": {
    #         "author": "Test User",
    #         "tags": ["test", "chatbot"],
    #         "complexity": "simple"
    #     },
    #     "nodes": [
    #         {
    #             "id": "input_1",
    #             "type": "input",
    #             "function": "input_node",
    #             "position": {"x": 100, "y": 200},
    #             "data": {
    #                 "label": "User Input",
    #                 "properties": {
    #                     "placeholder": "Enter your message..."
    #                 }
    #             }
    #         },
    #         {
    #             "id": "agent_1",
    #             "type": "agent",
    #             "function": "agent_node",
    #             "position": {"x": 400, "y": 200},
    #             "data": {
    #                 "label": "AI Agent",
    #                 "properties": {
    #                     "model": "gemini-2.0-flash",
    #                     "temperature": 0.7,
    #                 }
    #             }
    #         },
    #         {
    #             "id": "output_1",
    #             "type": "output",
    #             "function": "output_node",
    #             "position": {"x": 700, "y": 200},
    #             "data": {
    #                 "label": "Response Output",
    #                 "properties": {}
    #             }
    #         }
    #     ],
    #     "edges": [
    #         {
    #             "id": "edge_1",
    #             "source": "input_1",
    #             "target": "agent_1"
    #         },
    #         {
    #             "id": "edge_2",
    #             "source": "agent_1",
    #             "target": "output_1"
    #         }
    #     ],
    #     "entry_point": "input_1",
    #     "finish_point": "output_1",
    #     "state_schema": {
    #         "user_input": {
    #             "type": "string",
    #             "required": True
    #         },
    #         "response": {
    #             "type": "string",
    #             "required": False
    #         }
    #     },
    #     "llm_config": {
    #         "provider": "GoogleGenerativeAI",
    #         "model": "gemini-2.0-flash",
    #         "api_key": "env:GOOGLE_API_KEY"
    #     },
    #     "environment": {
    #         "variables": [
    #             {
    #                 "key": "GOOGLE_API_KEY",
    #                 "type": "secret",
    #                 "required": True,
    #                 "description": "Google API key"
    #             }
    #         ]
    #     },
    #     "validation": {
    #         "required_nodes": ["input", "output"],
    #         "max_nodes": 50,
    #         "max_edges": 100,
    #         "allowed_cycles": False
    #     }
    # }
    
    # response = requests.post(f"{BASE_URL}/api/flows", json=test_flow)
    # print(f"Status: {response.status_code}")
    # if response.status_code == 200:
    #     print("✅ Flow created successfully!")
    # else:
    #     print(f"❌ Error: {response.text}")
    
    # Test 4: Get all flows
    # print("\n4. Testing GET /api/flows")
    # response = requests.get(f"{BASE_URL}/api/flows")
    # print(f"Status: {response.status_code}")
    # if response.status_code == 200:
    #     flows = response.json()
    #     print(f"Found {len(flows)} flows")
    
    # Test 5: Validate flow
    # print("\n5. Testing POST /api/flows/{flow_id}/validate")
    # response = requests.post(f"{BASE_URL}/api/flows/test_chatbot_flow/validate")
    # print(f"Status: {response.status_code}")
    # if response.status_code == 200:
    #     result = response.json()
    #     print(f"Validation result: {'✅ Valid' if result['valid'] else '❌ Invalid'}")
    #     if not result['valid']:
    #         print(f"Errors: {result['errors']}")
    
    # Test 6: Export flow
    # print("\n6. Testing GET /api/flows/{flow_id}/export")
    # response = requests.get(f"{BASE_URL}/api/flows/test_chatbot_flow/export?format=langgraph")
    # print(f"Status: {response.status_code}")
    # if response.status_code == 200:
    #     exported = response.json()
    #     print("✅ Flow exported to LangGraph format")
    #     print(f"Nodes: {list(exported.get('nodes', {}).keys())}")
    
    # Test 7: Execute flow
    # print("\n7. Testing POST /api/flows/{flow_id}/execute")
    # execution_payload = {
    #     "flow_id": "test_chatbot_flow",
    #     "initial_state": {
    #         "user_input": "Hello, how are you?",
    #         "response": None
    #     }
    # }
    # response = requests.post(f"{BASE_URL}/api/flows/test_chatbot_flow/execute", json=execution_payload)
    # print(f"Status: {response.status_code}")
    # if response.status_code == 200:
    #     result = response.json()
    #     print(f"✅ Execution result: {result.get('result')}")
    # else:
    #     print(f"❌ Error: {response.text}")
    
    # Test 8: String Uppercase core tool
    # print("\n8. Testing String Uppercase core tool")
    # uppercase_flow = {
    #     "flow_id": "test_uppercase_flow",
    #     "name": "Uppercase Flow",
    #     "description": "Converts input to uppercase",
    #     "nodes": [
    #         {"id": "input_1", "type": "input", "function": "input_node", "position": {"x": 100, "y": 100}, "data": {"label": "Input", "properties": {}}},
    #         {"id": "uppercase_1", "type": "string_uppercase", "function": "string_uppercase_node", "position": {"x": 300, "y": 100}, "data": {"label": "Uppercase", "properties": {}}},
    #         {"id": "output_1", "type": "output", "function": "output_node", "position": {"x": 500, "y": 100}, "data": {"label": "Output", "properties": {}}}
    #     ],
    #     "edges": [
    #         {"id": "e1", "source": "input_1", "target": "uppercase_1"},
    #         {"id": "e2", "source": "uppercase_1", "target": "output_1"}
    #     ],
    #     "entry_point": "input_1",
    #     "finish_point": "output_1",
    #     "state_schema": {"user_input": {"type": "string", "required": True}, "uppercase": {"type": "string", "required": False}},
    #     "llm_config": {"provider": "GoogleGenerativeAI", "model": "gemini-2.0-flash", "api_key": "env:GOOGLE_API_KEY"}
    # }
    # response = requests.post(f"{BASE_URL}/api/flows", json=uppercase_flow)
    # print(f"Create flow status: {response.status_code}")
    # response = requests.post(f"{BASE_URL}/api/flows/test_uppercase_flow/execute", json={"flow_id": "test_uppercase_flow", "initial_state": {"user_input": "hello world"}})
    # print(f"Execute status: {response.status_code}")
    # print(f"Response: {response.json()}")
    # if response.status_code == 200:
    #     result = response.json()
    #     print(f"Uppercase result: {result.get('result')}")
    # else:
    #     print(f"❌ Error: {response.text}")
    
    # Test 9: Math Add core tool
    # print("\n9. Testing Math Add core tool")
    # math_add_flow = {
    #     "flow_id": "test_math_add_flow",
    #     "name": "Math Add Flow",
    #     "description": "Adds two numbers",
    #     "nodes": [
    #         {"id": "input_1", "type": "input", "function": "input_node", "position": {"x": 100, "y": 100}, "data": {"label": "Input", "properties": {}}},
    #         {"id": "add_1", "type": "math_add", "function": "math_add_node", "position": {"x": 300, "y": 100}, "data": {"label": "Add", "properties": {}}},
    #         {"id": "output_1", "type": "output", "function": "output_node", "position": {"x": 500, "y": 100}, "data": {"label": "Output", "properties": {}}}
    #     ],
    #     "edges": [
    #         {"id": "e1", "source": "input_1", "target": "add_1"},
    #         {"id": "e2", "source": "add_1", "target": "output_1"}
    #     ],
    #     "entry_point": "input_1",
    #     "finish_point": "output_1",
    #     "state_schema": {"a": {"type": "number", "required": True}, "b": {"type": "number", "required": True}, "sum": {"type": "number", "required": False}},
    #     "llm_config": {"provider": "GoogleGenerativeAI", "model": "gemini-2.0-flash", "api_key": "env:GOOGLE_API_KEY"}
    # }
    # response = requests.post(f"{BASE_URL}/api/flows", json=math_add_flow)
    # print(f"Create flow status: {response.status_code}")
    # response = requests.post(f"{BASE_URL}/api/flows/test_math_add_flow/execute", json={"flow_id": "test_math_add_flow", "initial_state": {"a": 5, "b": 7}})
    # print(f"Execute status: {response.status_code}")
    # print(f"Response: {response.json()}")
    # if response.status_code == 200:
    #     result = response.json()
    #     print(f"Math Add result: {result.get('result')}")
    # else:
    #     print(f"❌ Error: {response.text}")
    
    # Test 10: Agent node with string_uppercase tool
    # print("\n10. Testing Agent node with string_uppercase tool")
    # agent_uppercase_flow = {
    #     "flow_id": "test_agent_uppercase_flow",
    #     "name": "Agent Uppercase Flow",
    #     "description": "Agent uses uppercase tool",
    #     "nodes": [
    #         {"id": "input_1", "type": "input", "function": "input_node", "position": {"x": 100, "y": 100}, "data": {"label": "Input", "properties": {}}},
    #         {"id": "uppercase_1", "type": "string_uppercase", "function": "string_uppercase_node", "position": {"x": 300, "y": 100}, "data": {"label": "Uppercase", "properties": {}}},
    #         {"id": "agent_1", "type": "agent", "function": "agent_node", "position": {"x": 500, "y": 100}, "data": {"label": "Agent", "properties": {"tools": ["string_uppercase_node"]}}},
    #         {"id": "output_1", "type": "output", "function": "output_node", "position": {"x": 700, "y": 100}, "data": {"label": "Output", "properties": {}}}
    #     ],
    #     "edges": [
    #         {"id": "e1", "source": "input_1", "target": "uppercase_1"},
    #         {"id": "e2", "source": "uppercase_1", "target": "agent_1"},
    #         {"id": "e3", "source": "agent_1", "target": "output_1"}
    #     ],
    #     "entry_point": "input_1",
    #     "finish_point": "output_1",
    #     "state_schema": {"user_input": {"type": "string", "required": True}, "uppercase": {"type": "string", "required": False}, "response": {"type": "string", "required": False}},
    #     "llm_config": {"provider": "GoogleGenerativeAI", "model": "gemini-2.0-flash", "api_key": "env:GOOGLE_API_KEY"}
    # }
    # response = requests.post(f"{BASE_URL}/api/flows", json=agent_uppercase_flow)
    # print(f"Create flow status: {response.status_code}")
    # response = requests.post(f"{BASE_URL}/api/flows/test_agent_uppercase_flow/execute", json={"flow_id": "test_agent_uppercase_flow", "initial_state": {"user_input": "convert this to uppercase"}})
    # print(f"Execute status: {response.status_code}")
    # print(f"Response: {response.json()}")
    # if response.status_code == 200:
    #     result = response.json()
    #     print(f"Agent Uppercase result: {result.get('result')}")
    # else:
    #     print(f"❌ Error: {response.text}")
    
    # Test 11: Agent node with math_add tool
    # print("\n11. Testing Agent node with math_add tool")
    # agent_math_add_flow = {
    #     "flow_id": "test_agent_math_add_flow",
    #     "name": "Agent Math Add Flow",
    #     "description": "Agent uses math add tool",
    #     "nodes": [
    #         {"id": "input_1", "type": "input", "function": "input_node", "position": {"x": 100, "y": 100}, "data": {"label": "Input", "properties": {}}},
    #         {"id": "math_1", "type": "math_add", "function": "math_add_node", "position": {"x": 300, "y": 100}, "data": {"label": "MathAdd", "properties": {}}},
    #         {"id": "agent_1", "type": "agent", "function": "agent_node", "position": {"x": 500, "y": 100}, "data": {"label": "Agent", "properties": {"tools": ["math_add_node"]}}},
    #         {"id": "output_1", "type": "output", "function": "output_node", "position": {"x": 700, "y": 100}, "data": {"label": "Output", "properties": {}}}
    #     ],
    #     "edges": [
    #         {"id": "e1", "source": "input_1", "target": "math_1"},
    #         {"id": "e2", "source": "math_1", "target": "output_1"}
    #     ],
    #     "entry_point": "input_1",
    #     "finish_point": "output_1",
    #     "state_schema": {"a": {"type": "number", "required": True}, "b": {"type": "number", "required": True}, "sum": {"type": "number", "required": False}, "response": {"type": "string", "required": False}},
    #     "llm_config": {"provider": "GoogleGenerativeAI", "model": "gemini-2.0-flash", "api_key": "env:GOOGLE_API_KEY"}
    # }
    # response = requests.post(f"{BASE_URL}/api/flows", json=agent_math_add_flow)
    # print(f"Create flow status: {response.status_code}")
    # response = requests.post(f"{BASE_URL}/api/flows/test_agent_math_add_flow/execute", json={"flow_id": "test_agent_math_add_flow", "initial_state": {"a": 10, "b": 15}})
    # print(f"Execute status: {response.status_code}")
    # print(f"Response: {response.json()}")
    # if response.status_code == 200:
    #     result = response.json()
    #     print(f"Agent Math Add result: {result.get('result')}")
    # else:
    #     print(f"❌ Error: {response.text}")
    
    # Test: Multi-agent router flow
#     print("\nMULTI-AGENT ROUTER FLOW TEST")
#     router_flow = {
#         "flow_id": "test_router_flow",
#         "name": "Test Router Flow",
#         "description": "Flow with router and three agents (greeting, coding, conversation)",
#         "nodes": [
#             {
#                 "id": "input_1",
#                 "type": "input",
#                 "function": "input_node",
#                 "position": {"x": 100, "y": 100},
#                 "data": {"label": "User Input", "properties": {"placeholder": "Enter your message..."}}
#             },
#             {
#                 "id": "router_1",
#                 "type": "router",
#                 "function": "router_node",
#                 "position": {"x": 250, "y": 100},
#                 "data": {
#                     "label": "Router",
#                     "properties": {
#                         "routing_logic": """
# # Set state['route_label'] to 'greeting', 'coding', or 'conversation'\nif 'code' in state.get('user_input', '').lower():\n    state['route_label'] = 'coding'\nelif any(greet in state.get('user_input', '').lower() for greet in ['hi', 'hello', 'hey']):\n    state['route_label'] = 'greeting'\nelse:\n    state['route_label'] = 'conversation'\nreturn state
# """
#                 }
#             },
#             {
#                 "id": "greeting_agent",
#                 "type": "agent",
#                 "function": "agent_node",
#                 "position": {"x": 400, "y": 50},
#                 "data": {
#                     "label": "Greeting Agent",
#                     "properties": {
#                         "model": "gemini-2.0-flash",
#                         "system_prompt": "You are a well-trained, polite communicator. Always greet and respond to the user in a friendly and polite manner.",
#                         "api_key": "env:GOOGLE_API_KEY"
#                     }
#                 }
#             },
#             {
#                 "id": "coding_agent",
#                 "type": "agent",
#                 "function": "agent_node",
#                 "position": {"x": 400, "y": 100},
#                 "data": {
#                     "label": "Coding Agent",
#                     "properties": {
#                         "model": "gemini-2.0-flash",
#                         "system_prompt": "You are a Python expert. Only return Python code snippets relevant to the user's query. No explanations, just code.",
#                         "api_key": "env:GOOGLE_API_KEY"
#                     }
#                 }
#             },
#             {
#                 "id": "conversation_agent",
#                 "type": "agent",
#                 "function": "agent_node",
#                 "position": {"x": 400, "y": 150},
#                 "data": {
#                     "label": "Conversation Agent",
#                     "properties": {
#                         "model": "gemini-2.0-flash",
#                         "system_prompt": "You are a helpful assistant for general conversation.",
#                         "api_key": "env:GOOGLE_API_KEY"
#                     }
#                 }
#             },
#             {
#                 "id": "output_1",
#                 "type": "output",
#                 "function": "output_node",
#                 "position": {"x": 600, "y": 100},
#                 "data": {"label": "Output", "properties": {}}
#             }
#         ],
#         "edges": [
#             {"id": "e1", "source": "input_1", "target": "router_1"},
#             {
#                 "id": "e2",
#                 "source": "router_1",
#                 "target": "greeting_agent",  # <-- Add a valid target for Pydantic
#                 "type": "conditional",
#                 "condition": "lambda state: state['route_label']",
#                 "path_map": {
#                     "greeting": "greeting_agent",
#                     "coding": "coding_agent",
#                     "conversation": "conversation_agent"
#                 }
#             },
#             {"id": "e3", "source": "greeting_agent", "target": "output_1"},
#             {"id": "e4", "source": "coding_agent", "target": "output_1"},
#             {"id": "e5", "source": "conversation_agent", "target": "output_1"}
#         ],
#         "entry_point": "input_1",
#         "finish_point": "output_1",
#         "state_schema": {
#             "user_input": {"type": "string", "required": True},
#             "route_label": {"type": "string", "required": False},
#             "response": {"type": "string", "required": False}
#         },
#         "llm_config": {
#             "provider": "GoogleGenerativeAI",
#             "model": "gemini-2.0-flash",
#             "api_key": "env:GOOGLE_API_KEY"
#         }
#     }
#     # Create the flow
#     response = requests.post(f"{BASE_URL}/api/flows", json=router_flow)
#     print(f"Router flow create status: {response.status_code}")
#     if response.status_code == 200:
#         print("✅ Router flow created successfully!")
#     else:
#         print(f"❌ Error: {response.text}")
#     # Test greeting
#     payload = {"initial_state": {"user_input": "Hello!"}}
#     response = requests.post(f"{BASE_URL}/api/flows/test_router_flow/execute", json=payload)
#     print(f"Greeting test status: {response.status_code}")
#     if response.status_code == 200:
#         print(f"Greeting agent response: {response.json().get('result', {})}")
#     else:
#         print(f"❌ Error: {response.text}")
#     # Test coding
#     payload = {"initial_state": {"user_input": "Write code to sum a list in python."}}
#     response = requests.post(f"{BASE_URL}/api/flows/test_router_flow/execute", json=payload)
#     print(f"Coding test status: {response.status_code}")
#     if response.status_code == 200:
#         print(f"Coding agent response: {response.json().get('result', {})}")
#     else:
#         print(f"❌ Error: {response.text}")
#     # Test conversation
#     payload = {"initial_state": {"user_input": "What's the weather today?"}}
#     response = requests.post(f"{BASE_URL}/api/flows/test_router_flow/execute", json=payload)
#     print(f"Conversation test status: {response.status_code}")
#     if response.status_code == 200:
#         print(f"Conversation agent response: {response.json().get('result', {})}")
#     else:
#         print(f"❌ Error: {response.text}")

    # print("\n=== Test: Simple If-Else Router Flow ===")
    # # Define the flow with router, greeting agent, coding agent, and output
    # simple_router_flow = {
    #     "flow_id": "test_router_flow",
    #     "name": "Router If-Else Flow",
    #     "description": "Routes to greeting or coding agent based on input prefix.",
    #     "nodes": [
    #         {"id": "input_1", "type": "input", "function": "input_node", "position": {"x": 100, "y": 100}, "data": {"label": "User Input", "properties": {}}},
    #         {"id": "router_1", "type": "router", "function": "router_node", "position": {"x": 250, "y": 100}, "data": {"label": "Router", "properties": {"routing_logic": "if any(word in state.get('user_input', '').strip().lower() for word in ['code', 'python', 'function', 'script', 'program']):\n    state['route_label'] = 'coding'\nelif any(greet in state.get('user_input', '').strip().lower() for greet in ['hi', 'hello', 'hey', 'greetings']):\n    state['route_label'] = 'greeting'\nelse:\n    state['route_label'] = 'conversation'"}}},
    #         {"id": "greeting_agent", "type": "agent", "function": "agent_node", "position": {"x": 400, "y": 50}, "data": {"label": "Greeting Agent", "properties": {"system_prompt": "You are a greeting bot. Only respond to greetings. If the input is not a greeting, reply: 'I am only a greeting agent.'"}}},
    #         {"id": "coding_agent", "type": "agent", "function": "agent_node", "position": {"x": 400, "y": 150}, "data": {"label": "Coding Agent", "properties": {"system_prompt": "You are a coding assistant. Only return code snippets. If the input is not a code request, reply: 'Not a code request.'"}}},
    #         {"id": "output_1", "type": "output", "function": "output_node", "position": {"x": 600, "y": 100}, "data": {"label": "Output", "properties": {}}}
    #     ],
    #     "edges": [
    #         {"id": "e1", "source": "input_1", "target": "router_1"},
    #         {
    #             "id": "e2",
    #             "source": "router_1",
    #             "type": "conditional",
    #             "condition": "lambda state: state['route_label']",
    #             "path_map": {
    #                 "greeting": "greeting_agent",
    #                 "coding": "coding_agent",
    #                 "error": "output_1",
    #                 "conversation": "output_1"
    #             },
    #             "target": "greeting_agent"  # <-- Use a valid node id for validation
    #         },
    #         {"id": "e3", "source": "greeting_agent", "target": "output_1"},
    #         {"id": "e4", "source": "coding_agent", "target": "output_1"}
    #     ],
    #     "entry_point": "input_1",
    #     "finish_point": "output_1",
    #     "state_schema": {"user_input": {"type": "string", "required": True}, "response": {"type": "string", "required": False}},
    #     "llm_config": {"provider": "GoogleGenerativeAI", "model": "gemini-2.0-flash", "api_key": "env:GOOGLE_API_KEY"},
    #     "environment": {"variables": [{"key": "GOOGLE_API_KEY", "type": "secret", "required": True, "description": "Google API key"}]}
    # }
    # resp = requests.post(f"{BASE_URL}/api/flows", json=simple_router_flow)
    # print(f"Create flow status: {resp.status_code}")
    # assert resp.status_code == 200, resp.text

    # payload_greet = {"flow_id": "test_router_flow", "initial_state": {"user_input": "false hello"}}
    # resp = requests.post(f"{BASE_URL}/api/flows/test_router_flow/execute", json=payload_greet)
    # print(f"Greeting path status: {resp.status_code}")
    # print(f"Greeting path response: {resp.json()}")
    # if resp.status_code != 200:
    #     print(f"[ERROR] Unexpected status code: {resp.status_code}")
    # result = resp.json().get("result", "")
    # if isinstance(result, str):
    #     if not ("greeting" in result.lower() or "hello" in result.lower()):
    #         print(f"[WARN] Unexpected greeting result: {result}")
    # elif isinstance(result, dict):
    #     response_text = result.get("response", "")
    #     if not ("greeting" in response_text.lower() or "hello" in response_text.lower() or "not a greeting" in response_text.lower()):
    #         print(f"[WARN] Unexpected greeting response: {response_text}")
    # else:
    #     print(f"[DEBUG] Unexpected result type: {result}")

    # payload_code = {"flow_id": "test_router_flow", "initial_state": {"user_input": "true write a python function"}}
    # resp = requests.post(f"{BASE_URL}/api/flows/test_router_flow/execute", json=payload_code)
    # print(f"Coding path status: {resp.status_code}")
    # print(f"Coding path response: {resp.json()}")
    # if resp.status_code != 200:
    #     print(f"[ERROR] Unexpected status code: {resp.status_code}")
    # result = resp.json().get("result", "")
    # if isinstance(result, str):
    #     if not ("def " in result or "code" in result.lower()):
    #         print(f"[WARN] Unexpected coding result: {result}")
    # elif isinstance(result, dict):
    #     response_text = result.get("response", "")
    #     if not ("def " in response_text or "code" in response_text.lower() or "not a code request" in response_text.lower()):
    #         print(f"[WARN] Unexpected coding response: {response_text}")
    # else:
    #     print(f"[DEBUG] Unexpected result type: {result}")

    # print("\n=== Test: Manager Agent with Tech & Sales Tools ===")
    # manager_hrm_flow = {
    #     "flow_id": "manager_hrm_flow",
    #     "name": "Manager HRM Platform Flow",
    #     "description": "A manager agent orchestrates technical and marketing agents to answer HRM platform queries.",
    #     "nodes": [
    #         {"id": "input_1", "type": "input", "function": "input_node", "position": {"x": 100, "y": 100}, "data": {"label": "User Input", "properties": {"placeholder": "Describe your HRM platform needs or ask about marketing strategy..."}}},
    #         {"id": "tech_agent", "type": "agent", "function": "agent_node", "position": {"x": 350, "y": 60}, "data": {"label": "Technology Agent", "properties": {"system_prompt": "You are a senior technical architect. Recommend scalable, enterprise-level technology stacks for building HRM platforms. Be concise and specific.", "model": "gemini-2.0-flash", "temperature": 0.5}}},
    #         {"id": "sales_agent", "type": "agent", "function": "agent_node", "position": {"x": 350, "y": 140}, "data": {"label": "Sales Agent", "properties": {"system_prompt": "You are a SaaS marketing strategist. Suggest effective go-to-market and sales strategies for a new HRM platform. Be practical and actionable.", "model": "gemini-2.0-flash", "temperature": 0.7}}},
    #         {"id": "manager_agent", "type": "agent", "function": "agent_node", "position": {"x": 600, "y": 100}, "data": {"label": "Manager Agent", "properties": {"system_prompt": "You are a product manager for HRM platforms. You have two expert tools: (1) Technology Agent: recommends scalable, enterprise-level tech stacks; (2) Sales Agent: provides go-to-market and sales strategies. For technical questions, use the Technology Agent. For marketing/sales questions, use the Sales Agent. Only use a tool if the user query is relevant. Respond to the user with the tool's answer and a brief manager summary.", "model": "gemini-2.0-flash", "temperature": 0.6, "tools": ["tech_agent", "sales_agent"], "input_keys": ["user_input"]}}},
    #         {"id": "output_1", "type": "output", "function": "output_node", "position": {"x": 850, "y": 100}, "data": {"label": "Output", "properties": {}}}
    #     ],
    #     "edges": [
    #         {"id": "e1", "source": "input_1", "target": "manager_agent"},
    #         {"id": "e2", "source": "manager_agent", "target": "output_1"}
    #     ],
    #     "entry_point": "input_1",
    #     "finish_point": "output_1",
    #     "state_schema": {"user_input": {"type": "string", "required": True}, "response": {"type": "string", "required": False}},
    #     "llm_config": {"provider": "GoogleGenerativeAI", "model": "gemini-2.0-flash", "api_key": "env:GOOGLE_API_KEY"},
    #     "environment": {"variables": [{"key": "GOOGLE_API_KEY", "type": "secret", "required": True, "description": "Google API key"}]}
    # }
    # resp = requests.post(f"{BASE_URL}/api/flows", json=manager_hrm_flow)
    # print(f"Manager HRM flow create status: {resp.status_code}")
    # assert resp.status_code == 200, resp.text

    # # Test technical query
    # tech_query = {"flow_id": "manager_hrm_flow", "initial_state": {"user_input": "I want to build a HRM platform. What tech stack should I use for scalable enterprise level?"}}
    # resp = requests.post(f"{BASE_URL}/api/flows/manager_hrm_flow/execute", json=tech_query)
    # print(f"Tech query status: {resp.status_code}")
    # print(f"Tech query response: {resp.json()}")
    # assert resp.status_code == 200

    # # Test marketing query
    # marketing_query = {"flow_id": "manager_hrm_flow", "initial_state": {"user_input": "Suggest a go-to-market strategy for selling the HRM platform after development."}}
    # resp = requests.post(f"{BASE_URL}/api/flows/manager_hrm_flow/execute", json=marketing_query)
    # print(f"Marketing query status: {resp.status_code}")
    # print(f"Marketing query response: {resp.json()}")
    # assert resp.status_code == 200

    # # Test unrelated query (should not use tools)
    # unrelated_query = {"flow_id": "manager_hrm_flow", "initial_state": {"user_input": "Tell me a joke."}}
    # resp = requests.post(f"{BASE_URL}/api/flows/manager_hrm_flow/execute", json=unrelated_query)
    # print(f"Unrelated query status: {resp.status_code}")
    # print(f"Unrelated query response: {resp.json()}")
    # assert resp.status_code == 200

    print("\n=== Test: Agent with Current Year Tool ===")
    current_year_flow = {
        "flow_id": "test_current_year_agent_flow",
        "name": "Agent with Current Year Tool Flow",
        "description": "An agent that uses a tool to find the current year.",
        "nodes": [
            {"id": "input_1", "type": "input", "function": "input_node", "position": {"x": 100, "y": 100}, "data": {"label": "User Input", "properties": {}}},
            {
                "id": "agent_1", 
                "type": "agent", 
                "function": "agent_node", 
                "position": {"x": 350, "y": 100}, 
                "data": {
                    "label": "Year Agent", 
                    "properties": {
                        "system_prompt": "You are an assistant. When asked for the current year, you MUST use the 'current_year_node' tool. Do not answer from your own knowledge. Simply invoke the tool.",
                        "tool_descriptions": {
                            "current_year_node": "Gets the current calendar year."
                        },
                        "input_keys": ["user_input"]
                    }
                }
            },
            {"id": "current_year_node", "type": "current_year", "function": "current_year_node", "position": {"x": 600, "y": 200}, "data": {"label": "Current Year Tool", "properties": {}}},
            {"id": "output_1", "type": "output", "function": "output_node", "position": {"x": 850, "y": 100}, "data": {"label": "Output", "properties": {}}}
        ],
        "edges": [
            {"id": "e1", "source": "input_1", "target": "agent_1"},
            {"id": "e2", "source": "agent_1", "target": "output_1"}
        ],
        "entry_point": "input_1",
        "finish_point": "output_1",
        "state_schema": {
            "user_input": {"type": "string", "required": True},
            "response": {"type": "string", "required": False},
            "current_year": {"type": "number", "required": False}
        },
        "llm_config": {"provider": "GoogleGenerativeAI", "model": "gemini-2.0-flash", "api_key": "env:GOOGLE_API_KEY"}
    }
    
    resp = requests.post(f"{BASE_URL}/api/flows", json=current_year_flow)
    print(f"Create Agent with Current Year Tool Flow status: {resp.status_code}")
    if resp.status_code != 200:
        print(f"❌ Failed to create flow: {resp.text}")

    # Test query for the current year
    year_query = {"initial_state": {"user_input": "What is the current year?"}}
    resp = requests.post(f"{BASE_URL}/api/flows/test_current_year_agent_flow/execute", json=year_query)
    print(f"Current year query status: {resp.status_code}")
    print(f"Current year query response: {resp.json()}")
    if resp.status_code != 200:
        print(f"❌ Failed to execute query: {resp.text}")

    current_year = datetime.datetime.now().year
    response_data = resp.json()
    result_text = response_data.get("result", {}).get("response", "")
    if str(current_year) not in result_text:
        print(f"⚠️ Warning: Current year ({current_year}) not found in response: {result_text}")   

if __name__ == "__main__":
    try:
        test_api()
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to API server. Make sure it's running on port 8000")