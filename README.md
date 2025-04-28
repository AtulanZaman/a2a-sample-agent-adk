# A2A Sample Agent (Google ADK) – Expense Reimbursement

A sample project demonstrating how to build agent-to-agent (A2A) systems using the [Google Agent Development Kit (ADK)](https://github.com/google/A2A).  
This repo includes:
- A **Reimbursement Agent** (A2A server) that processes expense reimbursement requests.
- A **User Proxy Agent** (A2A client, also LLM-powered) that interacts with users and communicates with the reimbursement agent.

---

## Features

- **Agent-to-Agent (A2A) communication** using JSON-RPC over HTTP.
- **LLM-powered user proxy agent** for natural, conversational interaction.
- **Form-based information gathering** for missing details.
- **Vertex AI** (Google Cloud) integration for LLMs.

---

## Prerequisites

- Python 3.12+
- Google Cloud project with Vertex AI enabled
- Service account with Vertex AI permissions, or `gcloud auth application-default login`
- [google-adk](https://pypi.org/project/google-adk/), [google-genai](https://pypi.org/project/google-genai/), [python-dotenv](https://pypi.org/project/python-dotenv/)

---

## Setup

1. **Clone this repository:**
    ```bash
    git clone <your-repo-url>
    cd <your-repo-name>
    ```

2. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    # or, if using pyproject.toml:
    pip install .
    ```

3. **Set up environment variables:**
    - Create a `.env` file in the project root:
      ```
      GOOGLE_CLOUD_PROJECT=your-gcp-project-id
      GOOGLE_CLOUD_LOCATION=us-central1
      ```
    - Authenticate with Google Cloud:
      ```bash
      gcloud auth application-default login
      ```
    - Or set `GOOGLE_APPLICATION_CREDENTIALS` to your service account JSON.

---

## Running the Agents

### 1. **Start the Reimbursement Agent (A2A Server)**

```bash
python -m adk_a2a
```
- The agent will start on `http://localhost:10002/` by default.

### 2. **Start the User Proxy Agent (Client Agent)**

In a new terminal:
```bash
python adk_a2a/client_agent.py
```
- This agent will prompt you for input and handle the full conversation, including form-filling.

---

## Usage Example

```
Welcome to the Reimbursement Assistant!
You: Reimburse me $20 for lunch
Agent: What is the date, amount, and purpose of the transaction?
You: April 25, 2025, $20, Lunch with client
Agent: Your reimbursement request has been submitted!
```

---

## Project Structure

```
adk_a2a/
  agent.py           # Reimbursement agent (A2A server)
  client_agent.py    # User proxy agent (A2A client)
  task_manager.py    # Task management logic
  common/            # Shared types and server code
  __main__.py        # Entry point for the server agent
  README.md
  pyproject.toml
  ...
```

---

## Contributing

Contributions are welcome! Please open issues or pull requests.

---

## License

[Specify your license here, e.g., MIT, Apache 2.0, etc.]

---

## Acknowledgements

- Based on the [Google A2A sample agents](https://github.com/google/A2A).
- Uses [Google ADK](https://pypi.org/project/google-adk/) and [Vertex AI](https://cloud.google.com/vertex-ai).
