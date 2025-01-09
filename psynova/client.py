import requests
from .exceptions import PsynovaAPIError


class PsynovaClient:
    def __init__(
        self,
        private_key,
        base_url: str = "https://api.psynova.ai",
        timeout: int = 30,
    ):
        """Initialize Psynova API client

        Args:
            private_key (str): Private key of the wallet for authentication.
            base_url (str, optional): Base URL for API. Defaults to "https://api.psynova.ai".
            timeout (int, optional): Request timeout in seconds. Defaults to 30.
        """
        self.base_url = base_url
        self.session = requests.Session()
        self.private_key = private_key
        self.timeout = timeout

    def get_agent(self, agent_id: int) -> dict:
        """Get details of a specific agent.

        Args:
            agent_id (int): ID of the agent to retrieve

        Returns:
            dict: Agent details including id, name, version_id, and status

        Raises:
            PsynovaAPIError: If agent retrieval fails or API request errors
        """
        access_token = self._login()
        response = self._make_request(
            method="GET",
            endpoint=f"/agent/get",
            params={"id": agent_id},
            data={},
            access_token=access_token,
        )
        return response["data"]

    def list_agents(self) -> list:
        """List all agents associated with the account.

        Returns:
            list: List of dictionaries containing agent details including id, name, version_id, and status

        Raises:
            PsynovaAPIError: If agent listing fails or API request errors
        """
        access_token = self._login()
        response = self._make_request(
            method="GET",
            endpoint="/agent/list",
            params={},
            data={},
            access_token=access_token,
        )
        return response["data"].get('data', [])

    def chat(self, agent_id: int, message: str) -> str:
        """Send a chat message to an agent.

        Args:
            agent_id (int): ID of the agent to chat with
            message (str): Message to send to the agent

        Returns:
            str: Response message from the agent

        Raises:
            PsynovaAPIError: If chat request fails or API request errors
        """
        access_token = self._login()
        response = self._make_request(
            method="POST",
            endpoint="/chat/completions/create",
            params={},
            data={"id": agent_id, "message": message},
            access_token=access_token,
        )
        return response["data"]["response_message"]

    def create_agent(
        self,
        name: str,
        version_id: int,
        using_https: bool = True,
        using_socket: bool = True,
    ) -> int:
        """Create a new agent.

        Args:
            name (str): Name of the agent
            version_id (int): ID of the provider version to use
            using_https (bool, optional): Flag indicating if agent should use HTTPS. Defaults to True.
            using_socket (bool, optional): Flag indicating if agent should use WebSocket. Defaults to True.

        Returns:
            int: ID of the newly created agent

        Raises:
            PsynovaAPIError: If agent creation fails or API request errors
        """
        access_token = self._login()
        response = self._make_request(
            method="POST",
            endpoint="/agent/create",
            params={},
            data={
                "name": name,
                "version_id": version_id,
                "using_https": using_https,
                "using_socket": using_socket,
            },
            access_token=access_token,
        )
        agent_id = response["data"]["id"]
        return agent_id

    def _login(self) -> str:
        """Authenticate with the Psynova API using private key.

        This method makes a POST request to /sdk/login endpoint with the private key
        to obtain an access token for subsequent API calls.

        Returns:
            str: The access token to be used for authentication

        Raises:
            PsynovaAPIError: If authentication fails or API request errors
        """
        if not self.private_key:
            raise PsynovaAPIError("Private key is required for authentication")

        try:
            response = self._make_request(
                method="POST",
                endpoint="/sdk/login",
                params={},
                data={"private_key": self.private_key},
            )
            return response["data"]["access_token"]
        except PsynovaAPIError:
            raise PsynovaAPIError("Invalid response format from login endpoint")

    def _make_request(
        self,
        method: str,
        endpoint: str,
        params: dict = {},
        data: dict = {},
        access_token: str = "",
    ) -> dict:
        """Make HTTP request to Psynova API endpoint.

        This method handles making HTTP requests to the Psynova API, including setting up
        headers, handling authentication tokens, and processing responses.

        Args:
            method (str): HTTP method to use (GET, POST, etc)
            endpoint (str): API endpoint path
            params (dict, optional): Query parameters to include in URL. Defaults to {}.
            data (dict, optional): JSON data to send in request body. Defaults to {}.
            access_token (str, optional): Bearer token for authentication. Defaults to empty string.

        Returns:
            dict: Parsed JSON response from the API

        Raises:
            PsynovaAPIError: If the request fails or returns an error response
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"

        headers = {
            "Content-Type": "application/json",
        }

        if access_token.strip():
            headers["Authorization"] = f"Bearer {access_token}"

        try:
            response = self.session.request(
                method=method,
                url=url,
                headers=headers,
                params=params,
                json=data,
                timeout=self.timeout,
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise PsynovaAPIError(f"API request failed: {str(e)}")
