import httpx


API_URL = "https://api.semanticscholar.org/graph/v1/paper/search"


def search_papers(query: str, limit: int = 5):

    params = {
        "query": query,
        "limit": limit
    }

    try:
        response = httpx.get(
            API_URL,
            params=params,
            timeout=30
        )

        response.raise_for_status()

        return response.json()

    except httpx.ReadTimeout:
        print("Error: Semantic Scholar API took too long to respond.")
        return None

    except httpx.HTTPStatusError as error:
        print(f"HTTP Error: {error.response.status_code}")
        print(error.response.text)
        return None

    except httpx.RequestError as error:
        print(f"Request Error: {error}")
        return None