# Psynova - A Powerful and Flexible AI Agent Framework


Psynova is a Python-based AI agent framework that enables developers to create, manage, and interact with AI agents through a simple yet powerful API interface.


## Key Features


1. **Easy Agent Management**

   - Create custom AI agents with unique configurations

   - Support for both HTTPS and WebSocket communications

   - Flexible version control for agent deployments

2. **Simple Authentication**

   - Secure private key-based authentication

   - Token-based API access

3. **Streamlined Communication**

   - Direct chat interface with agents

   - RESTful API integration

   - Configurable timeout settings

## Technical Requirements

- Python 3.10 or higher

- Dependencies:

  - requests 2.31.0


## Quick Start

### Installation

![Psynova Intro](images/intro.png)

```bash
pip install psynova==1.4

```


### Basic Usage

```python
from psynova import PsynovaClient

# Initialize the client
client = PsynovaClient(
    private_key="your_private_key",
    base_url="https://api.psynova.ai"  # Optional: defaults to dev environment
)

# Create a new agent
agent_id = client.create_agent(
    name="My AI Agent",
    version_id=1,
    using_https=True,
    using_socket=True
)

# Chat with the agent
response = client.chat(
    agent_id=agent_id,
    message="Hello, AI agent!"
)
print(response)
```


## Error Handling

The framework includes robust error handling through the `PsynovaAPIError` class, which provides detailed error messages and optional additional error context when API requests fail.

```python
try:
    response = client.chat(agent_id=1, message="Hello")
except PsynovaAPIError as e:
    print(f"Error: {str(e)}")
    if e.errors:
        print(f"Additional details: {e.errors}")
```

## API Reference

### PsynovaClient

#### Constructor

```python
client = PsynovaClient(private_key, base_url="https://api.psynova.ai", timeout=30)
```

- `private_key` (str): Private key for authentication
- `base_url` (str, optional): Base URL for API. Defaults to development environment
- `timeout` (int, optional): Request timeout in seconds. Defaults to 30

#### Methods

##### get_agent(agent_id)
Retrieves details of a specific agent.

```python
agent = client.get_agent(agent_id=1)
```

Returns: Dictionary containing agent details (id, name, version_id, status)

##### list_agents()
Lists all agents associated with the account.

```python
agents = client.list_agents()
```

Returns: List of dictionaries containing agent details

##### chat(agent_id, message)
Sends a chat message to an agent.

```python
response = client.chat(agent_id=1, message="Hello!")
```

Returns: String containing the agent's response

##### create_agent(name, version_id, using_https=True, using_socket=True)
Creates a new agent with specified configuration.

```python
agent_id = client.create_agent(
    name="My Agent",
    version_id=1,
    using_https=True,
    using_socket=True
)
```

Returns: Integer ID of the newly created agent

## Current Version

The current version of Psynova is v1.0, indicating a stable release ready for production use.

This framework appears to be designed for developers who need to integrate AI agents into their applications with minimal setup while maintaining flexibility for various use cases. The API design follows RESTful principles and provides a clean, intuitive interface for agent interactions.