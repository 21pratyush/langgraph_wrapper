import requests
import json

BASE_URL = "http://localhost:8000"

def test_api():
    print("🧪 Testing Flow Builder API")
    
    # Test 1: Get components
    print("\n1. Testing GET /api/components")
    response = requests.get(f"{BASE_URL}/api/components")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Found {len(data.get('component_definitions', {}))} components")
    
    # Test 2: Get categories
    print("\n2. Testing GET /api/categories")
    response = requests.get(f"{BASE_URL}/api/categories")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        categories = response.json()
        print(f"Found {len(categories)} categories")
    
    # Test 3: Create a flow
    print("\n3. Testing POST /api/flows")
    test_flow = {
        "flow_id": "test_chatbot_flow",
        "name": "Test Chatbot Flow",
        "description": "A simple test flow",
        "version": "1.0.0",
        "created_at": "2024-01-20T10:00:00Z",
        "updated_at": "2024-01-20T10:00:00Z",
        "metadata": {
            "author": "Test User",
            "tags": ["test", "chatbot"],
            "complexity": "simple"
        },
        "nodes": [
            {
                "id": "input_1",
                "type": "input",
                "position": {"x": 100, "y": 200},
                "data": {
                    "label": "User Input",
                    "properties": {
                        "placeholder": "Enter your message..."
                    }
                }
            },
            {
                "id": "agent_1",
                "type": "agent",
                "position": {"x": 400, "y": 200},
                "data": {
                    "label": "AI Agent",
                    "properties": {
                        "model": "gemini-2.0-flash",
                        "temperature": 0.7
                    }
                }
            },
            {
                "id": "output_1",
                "type": "output",
                "position": {"x": 700, "y": 200},
                "data": {
                    "label": "Response Output",
                    "properties": {}
                }
            }
        ],
        "edges": [
            {
                "id": "edge_1",
                "source": "input_1",
                "target": "agent_1"
            },
            {
                "id": "edge_2",
                "source": "agent_1",
                "target": "output_1"
            }
        ],
        "entry_point": "input_1",
        "finish_point": "output_1",
        "state_schema": {
            "user_input": {
                "type": "string",
                "required": True
            },
            "response": {
                "type": "string",
                "required": False
            }
        },
        "llm_config": {
            "provider": "GoogleGenerativeAI",
            "model": "gemini-2.0-flash",
            "api_key": "env:GOOGLE_API_KEY"
        },
        "environment": {
            "variables": [
                {
                    "key": "GOOGLE_API_KEY",
                    "type": "secret",
                    "required": True,
                    "description": "Google API key"
                }
            ]
        },
        "validation": {
            "required_nodes": ["input", "output"],
            "max_nodes": 50,
            "max_edges": 100,
            "allowed_cycles": False
        }
    }
    
    response = requests.post(f"{BASE_URL}/api/flows", json=test_flow)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print("✅ Flow created successfully!")
    else:
        print(f"❌ Error: {response.text}")
    
    # Test 4: Get all flows
    print("\n4. Testing GET /api/flows")
    response = requests.get(f"{BASE_URL}/api/flows")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        flows = response.json()
        print(f"Found {len(flows)} flows")
    
    # Test 5: Validate flow
    print("\n5. Testing POST /api/flows/{flow_id}/validate")
    response = requests.post(f"{BASE_URL}/api/flows/test_chatbot_flow/validate")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"Validation result: {'✅ Valid' if result['valid'] else '❌ Invalid'}")
        if not result['valid']:
            print(f"Errors: {result['errors']}")
    
    # Test 6: Export flow
    print("\n6. Testing GET /api/flows/{flow_id}/export")
    response = requests.get(f"{BASE_URL}/api/flows/test_chatbot_flow/export?format=langgraph")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        exported = response.json()
        print("✅ Flow exported to LangGraph format")
        print(f"Nodes: {list(exported.get('nodes', {}).keys())}")
    
    # Test 7: Execute flow
    print("\n7. Testing POST /api/flows/{flow_id}/execute")
    execution_payload = {
        "flow_id": "test_chatbot_flow",
        "initial_state": {
            "user_input": "Hello, how are you?",
            "response": None
        }
    }
    response = requests.post(f"{BASE_URL}/api/flows/test_chatbot_flow/execute", json=execution_payload)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Execution result: {result.get('result')}")
    else:
        print(f"❌ Error: {response.text}")
    
    # Test 8: String Uppercase core tool
    print("\n8. Testing String Uppercase core tool")
    uppercase_flow = {
        "flow_id": "test_uppercase_flow",
        "name": "Uppercase Flow",
        "description": "Converts input to uppercase",
        "nodes": [
            {"id": "input_1", "type": "input", "position": {"x": 100, "y": 100}, "data": {"label": "Input", "properties": {}}},
            {"id": "uppercase_1", "type": "string_uppercase", "position": {"x": 300, "y": 100}, "data": {"label": "Uppercase", "properties": {}}},
            {"id": "output_1", "type": "output", "position": {"x": 500, "y": 100}, "data": {"label": "Output", "properties": {}}}
        ],
        "edges": [
            {"id": "e1", "source": "input_1", "target": "uppercase_1"},
            {"id": "e2", "source": "uppercase_1", "target": "output_1"}
        ],
        "entry_point": "input_1",
        "finish_point": "output_1",
        "state_schema": {"user_input": {"type": "string", "required": True}, "uppercase": {"type": "string", "required": False}},
        "llm_config": {"provider": "GoogleGenerativeAI", "model": "gemini-2.0-flash", "api_key": "env:GOOGLE_API_KEY"}
    }
    response = requests.post(f"{BASE_URL}/api/flows", json=uppercase_flow)
    print(f"Create flow status: {response.status_code}")
    response = requests.post(f"{BASE_URL}/api/flows/test_uppercase_flow/execute", json={"flow_id": "test_uppercase_flow", "initial_state": {"user_input": "hello world"}})
    print(f"Execute status: {response.status_code}")
    print(f"Response: {response.json()}")
    if response.status_code == 200:
        result = response.json()
        print(f"Uppercase result: {result.get('result')}")
    else:
        print(f"❌ Error: {response.text}")
    
    # Test 9: Math Add core tool
    print("\n9. Testing Math Add core tool")
    math_add_flow = {
        "flow_id": "test_math_add_flow",
        "name": "Math Add Flow",
        "description": "Adds two numbers",
        "nodes": [
            {"id": "input_1", "type": "input", "position": {"x": 100, "y": 100}, "data": {"label": "Input", "properties": {}}},
            {"id": "add_1", "type": "math_add", "position": {"x": 300, "y": 100}, "data": {"label": "Add", "properties": {}}},
            {"id": "output_1", "type": "output", "position": {"x": 500, "y": 100}, "data": {"label": "Output", "properties": {}}}
        ],
        "edges": [
            {"id": "e1", "source": "input_1", "target": "add_1"},
            {"id": "e2", "source": "add_1", "target": "output_1"}
        ],
        "entry_point": "input_1",
        "finish_point": "output_1",
        "state_schema": {"a": {"type": "number", "required": True}, "b": {"type": "number", "required": True}, "sum": {"type": "number", "required": False}},
        "llm_config": {"provider": "GoogleGenerativeAI", "model": "gemini-2.0-flash", "api_key": "env:GOOGLE_API_KEY"}
    }
    response = requests.post(f"{BASE_URL}/api/flows", json=math_add_flow)
    print(f"Create flow status: {response.status_code}")
    response = requests.post(f"{BASE_URL}/api/flows/test_math_add_flow/execute", json={"flow_id": "test_math_add_flow", "initial_state": {"a": 5, "b": 7}})
    print(f"Execute status: {response.status_code}")
    print(f"Response: {response.json()}")
    if response.status_code == 200:
        result = response.json()
        print(f"Math Add result: {result.get('result')}")
    else:
        print(f"❌ Error: {response.text}")
    
    # Test 10: Agent node with string_uppercase tool
    print("\n10. Testing Agent node with string_uppercase tool")
    agent_uppercase_flow = {
        "flow_id": "test_agent_uppercase_flow",
        "name": "Agent Uppercase Flow",
        "description": "Agent uses uppercase tool",
        "nodes": [
            {"id": "input_1", "type": "input", "position": {"x": 100, "y": 100}, "data": {"label": "Input", "properties": {}}},
            {"id": "uppercase_1", "type": "string_uppercase", "position": {"x": 300, "y": 100}, "data": {"label": "Uppercase", "properties": {}}},
            {"id": "agent_1", "type": "agent", "position": {"x": 500, "y": 100}, "data": {"label": "Agent", "properties": {}}},
            {"id": "output_1", "type": "output", "position": {"x": 700, "y": 100}, "data": {"label": "Output", "properties": {}}}
        ],
        "edges": [
            {"id": "e1", "source": "input_1", "target": "uppercase_1"},
            {"id": "e2", "source": "uppercase_1", "target": "agent_1"},
            {"id": "e3", "source": "agent_1", "target": "output_1"}
        ],
        "entry_point": "input_1",
        "finish_point": "output_1",
        "state_schema": {"user_input": {"type": "string", "required": True}, "uppercase": {"type": "string", "required": False}, "response": {"type": "string", "required": False}},
        "llm_config": {"provider": "GoogleGenerativeAI", "model": "gemini-2.0-flash", "api_key": "env:GOOGLE_API_KEY"}
    }
    response = requests.post(f"{BASE_URL}/api/flows", json=agent_uppercase_flow)
    print(f"Create flow status: {response.status_code}")
    response = requests.post(f"{BASE_URL}/api/flows/test_agent_uppercase_flow/execute", json={"flow_id": "test_agent_uppercase_flow", "initial_state": {"user_input": "convert this to uppercase"}})
    print(f"Execute status: {response.status_code}")
    print(f"Response: {response.json()}")
    if response.status_code == 200:
        result = response.json()
        print(f"Agent Uppercase result: {result.get('result')}")
    else:
        print(f"❌ Error: {response.text}")
    
    # Test 11: Agent node with math_add tool
    print("\n11. Testing Agent node with math_add tool")
    agent_math_add_flow = {
        "flow_id": "test_agent_math_add_flow",
        "name": "Agent Math Add Flow",
        "description": "Agent uses math add tool",
        "nodes": [
            {"id": "input_1", "type": "input", "position": {"x": 100, "y": 100}, "data": {"label": "Input", "properties": {}}},
            {"id": "math_1", "type": "math_add", "position": {"x": 300, "y": 100}, "data": {"label": "MathAdd", "properties": {}}},
            {"id": "agent_1", "type": "agent", "position": {"x": 500, "y": 100}, "data": {"label": "Agent", "properties": {}}},
            {"id": "output_1", "type": "output", "position": {"x": 700, "y": 100}, "data": {"label": "Output", "properties": {}}}
        ],
        "edges": [
            {"id": "e1", "source": "input_1", "target": "math_1"},
            {"id": "e2", "source": "math_1", "target": "agent_1"},
            {"id": "e3", "source": "agent_1", "target": "output_1"}
        ],
        "entry_point": "input_1",
        "finish_point": "output_1",
        "state_schema": {"a": {"type": "number", "required": True}, "b": {"type": "number", "required": True}, "sum": {"type": "number", "required": False}, "response": {"type": "string", "required": False}},
        "llm_config": {"provider": "GoogleGenerativeAI", "model": "gemini-2.0-flash", "api_key": "env:GOOGLE_API_KEY"}
    }
    response = requests.post(f"{BASE_URL}/api/flows", json=agent_math_add_flow)
    print(f"Create flow status: {response.status_code}")
    response = requests.post(f"{BASE_URL}/api/flows/test_agent_math_add_flow/execute", json={"flow_id": "test_agent_math_add_flow", "initial_state": {"a": 10, "b": 15}})
    print(f"Execute status: {response.status_code}")
    print(f"Response: {response.json()}")
    if response.status_code == 200:
        result = response.json()
        print(f"Agent Math Add result: {result.get('result')}")
    else:
        print(f"❌ Error: {response.text}")

if __name__ == "__main__":
    try:
        test_api()
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to API server. Make sure it's running on port 8000")