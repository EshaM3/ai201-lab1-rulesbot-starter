# Spec: `retrieve()`

**File:** `retriever.py`
**Status:** Spec incomplete — fill in all blank fields before implementing

---

## Purpose

Given a user's natural language query, find the most relevant chunks from the vector store using semantic similarity search. Return them ranked by relevance so that `generate_response()` can use them as context.

---

## Input / Output Contract

**Inputs:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `query` | `str` | The user's natural language question |
| `n_results` | `int` | Maximum number of chunks to return (default: `N_RESULTS` from `config.py`) |

**Output:** `list[dict]`

Each dict in the returned list must contain exactly these keys:

| Key | Type | Description |
|-----|------|-------------|
| `"text"` | `str` | The chunk text |
| `"game"` | `str` | The game name this chunk came from |
| `"distance"` | `float` | Cosine distance score — lower means more similar to the query |

Results should be ordered from most to least relevant (lowest to highest distance). Returns an empty list `[]` if the collection contains no documents.

---

## Design Decisions

*Complete the fields below before writing any code. Use your AI tool in Plan or Ask mode to help you reason through what belongs here — but the decisions are yours.*

---

### Query approach

*Describe how you will use `_collection.query()` to find relevant chunks. What arguments will you pass, and why?*

```
I will use `_collection.query()` to take the user's query (in a list), 3 results to return, and a specification to return me the text (documents), where it came from (metadatas), and their similarity scores to the input query (distances). The top 3 chunks with the most relevant information (lowest distances) should be returned. I want 3 because it seems like a decent number of chunks to sift through and find a valuable answer.
```

---

### Return structure

*Sketch out what one item in your return list looks like as a concrete example. Where does each field come from in the query results?*

```
It will return a list of dicts, each with:
      - "documents"     : chunks of text (pulled from each embedding's document field)
      - "metadatas"     : the game names (pulled from each embedding's metadatas field)
      - "distances" : the similarity scores (lower = more similar for cosine; calculated)
```

---

### Handling the nested result structure

*`_collection.query()` returns nested lists. Describe what index you need to access to get the actual list of results for a single query, and why the nesting exists.*

```
Use [0]. The nesting exists because the function can be used for multiple query searches. But we are only using one per call.
```

---

### Relevance threshold

*Will you filter out results above a certain distance score, or return all `n_results` regardless of how relevant they are? What are the tradeoffs of each approach?*

```
It would be better to have a light threshold so something comepletely off does not make it into the retrieved list. If this is the case, it may be best to have n_results not just be 1-2. You want slightly more ranking leeway in case scores are too similar (ex: threshold of 0.5 where you had n_results set to 2 but 3 results had a distance of 0.5; all 3 might be helpful to consider). 
Not having a cutoff would leave more room for hallucination.
```

---

### Edge cases

*How does your implementation behave when: (a) the collection is empty, (b) the query matches no chunks well, (c) the query matches chunks from multiple games?*

```
[your answer here]
```

---

## Implementation Notes

*Fill this in after implementing, before moving to Milestone 3.*

**Test query and top result returned:**

```
Query: What happens if you roll a 7 in Catan?
Top result game: Catan
Distance score: 0.471
Does it make sense? Yes
```

**One thing about the query results that surprised you:**

```
[your answer here]
```
