import os
from dotenv import load_dotenv

from services.openalex import search_papers

load_dotenv()

if os.getenv("OPENALEX_API_KEY"):
    print("OpenAlex API key loaded successfully.")
else:
    print("OpenAlex API key NOT found.")

result = search_papers(
    query="EEG emotion recognition",
    limit=3
)

if result:
    print(f"\nNumber of papers returned: {len(result)}")

    for i, paper in enumerate(result, start=1):
        print("\n" + "=" * 60)
        print(f"PAPER {i}")
        print("=" * 60)

        print("Title:", paper["title"])
        print("Authors:", paper["authors"])
        print("Year:", paper["year"])
        print("Citations:", paper["citations"])
        print("DOI:", paper["doi"])
        print("Source:", paper["source"])
        print("Paper URL:", paper["paper_url"])
        print("PDF URL:", paper["pdf_url"])

else:
    print("No data received.")