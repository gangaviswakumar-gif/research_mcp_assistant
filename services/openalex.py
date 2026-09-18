import os
import httpx
from dotenv import load_dotenv

load_dotenv()

API_URL = "https://api.openalex.org/works"
API_KEY = os.getenv("OPENALEX_API_KEY")


def reconstruct_abstract(abstract_inverted_index):
    if not abstract_inverted_index:
        return None

    words = []

    for word, positions in abstract_inverted_index.items():
        for position in positions:
            words.append((position, word))

    words.sort()

    return " ".join(word for position, word in words)

def extract_paper(paper):
    authors = []

    for authorship in paper.get("authorships", []):
        author = authorship.get("author")

        if author and author.get("display_name"):
            authors.append(author["display_name"])

    abstract = reconstruct_abstract(
        paper.get("abstract_inverted_index")
    )

    doi = paper.get("doi")

    paper_url = doi if doi else paper.get("id")

    pdf_url = None

    best_oa_location = paper.get("best_oa_location")

    if best_oa_location:
        pdf_url = best_oa_location.get("pdf_url")

    if not pdf_url:
        for location in paper.get("locations", []):
            pdf_url = location.get("pdf_url")

            if pdf_url:
                break

    return {
        "title": paper.get("title"),
        "authors": authors,
        "year": paper.get("publication_year"),
        "abstract": abstract,
        "citations": paper.get("cited_by_count", 0),
        "doi": doi,
        "source": "OpenAlex",
        "paper_url": paper_url,
        "pdf_url": pdf_url
    }


def search_papers(query: str, limit: int = 5):
    params = {
        "search": query,
        "per-page": limit
    }

    try:
        response = httpx.get(
    API_URL,
    params=params,
    headers={
        "Authorization": f"Bearer {API_KEY}"
    },
    timeout=30

        )

        response.raise_for_status()

        data = response.json()

        papers = []

        for paper in data.get("results", []):
            papers.append(extract_paper(paper))

        return papers

    except httpx.ReadTimeout:
        print("Error: OpenAlex API took too long to respond.")
        return None

    except httpx.HTTPStatusError as error:
        print(f"HTTP Error: {error.response.status_code}")
        print(error.response.text)
        return None

    except httpx.RequestError as error:
        print(f"Request Error: {error}")
        return None