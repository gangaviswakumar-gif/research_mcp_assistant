from services.semantic_scholar import search_papers


result = search_papers(
    query="EEG emotion recognition",
    limit=3
)

print(result)