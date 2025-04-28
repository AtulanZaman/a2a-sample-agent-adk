# adk_a2a/client_agent.py

from google.adk.agents.llm_agent import LlmAgent
from google.adk.tools.tool_context import ToolContext
from google.adk.artifacts import InMemoryArtifactService
from google.adk.memory.in_memory_memory_service import InMemoryMemoryService
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
import requests
import os
from dotenv import load_dotenv

load_dotenv()

def call_reimbursement_agent(query: str, tool_context: ToolContext) -> str:
    """Tool to call the reimbursement agent via A2A protocol."""
    agent_url = os.getenv("REIMBURSEMENT_AGENT_URL", "http://localhost:10002/")
    payload = {
        "jsonrpc": "2.0",
        "method": "tasks/send",
        "id": "1",
        "params": {
            "id": "task-1",
            "message": {
                "role": "user",
                "parts": [{"type": "text", "text": query}]
            },
            "acceptedOutputModes": ["text"],
            "sessionId": "client-session"
        }
    }
    # print(f"Sending to reimbursement agent: {payload}")
    response = requests.post(agent_url, json=payload)
    # print(f"Raw response: {response.text}")
    try:
        result = response.json()
        # Try to extract the main message
        agent_reply = (
            result.get("result", {})
                  .get("status", {})
                  .get("message", {})
                  .get("parts", [{}])[0]
                  .get("text", "")
        )
        # If the main message is empty, look for a non-empty artifact
        if not agent_reply:
            artifacts = result.get("result", {}).get("artifacts", [])
            for artifact in artifacts:
                for part in artifact.get("parts", []):
                    text = part.get("text", "")
                    if text and text.strip():
                        agent_reply = text
                        break
                if agent_reply:
                    break
        return agent_reply or "No response from reimbursement agent."
    except Exception as e:
        return f"Error communicating with reimbursement agent: {e}"

class UserProxyAgent:
    SUPPORTED_CONTENT_TYPES = ["text", "text/plain"]

    def __init__(self):
        self._agent = self._build_agent()
        self._user_id = "user_proxy"
        self._runner = Runner(
            app_name=self._agent.name,
            agent=self._agent,
            artifact_service=InMemoryArtifactService(),
            session_service=InMemorySessionService(),
            memory_service=InMemoryMemoryService(),
        )

    def invoke(self, query, session_id) -> str:
        session = self._runner.session_service.get_session(
            app_name=self._agent.name, user_id=self._user_id, session_id=session_id
        )
        content = types.Content(
            role="user", parts=[types.Part.from_text(text=query)]
        )
        if session is None:
            session = self._runner.session_service.create_session(
                app_name=self._agent.name,
                user_id=self._user_id,
                state={},
                session_id=session_id,
            )
        events = list(self._runner.run(
            user_id=self._user_id, session_id=session.id, new_message=content
        ))
        if not events or not events[-1].content or not events[-1].content.parts:
            return ""
        return "\n".join([p.text for p in events[-1].content.parts if p.text])

    def _build_agent(self) -> LlmAgent:
        project = os.getenv("GOOGLE_CLOUD_PROJECT")
        location = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
        return LlmAgent(
            model="gemini-2.0-flash-001",
            name="user_proxy_agent",
            description="An agent that helps users interact with the reimbursement agent in a friendly way.",
            instruction="""
You are a helpful assistant. When the user asks about reimbursements, use the 'call_reimbursement_agent' tool to send their request to the reimbursement agent. Present the response in a friendly, conversational way. If the response is a form (JSON) or a prompt for more information, clearly ask the user for the required details. Always show the most relevant information from the reimbursement agent's response.
""",
            tools=[call_reimbursement_agent]
        )

if __name__ == "__main__":
    agent = UserProxyAgent()
    print("Welcome to the Reimbursement Assistant!")
    session_id = "user-session"
    while True:
        user_input = input("You: ")
        if user_input.lower() in ("exit", "quit"):
            break
        response = agent.invoke(user_input, session_id)
        print("Agent:", response)