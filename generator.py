from groq import Groq
from config import GROQ_API_KEY, LLM_MODEL

_client = Groq(api_key=GROQ_API_KEY)


def generate_response(query, retrieved_chunks):
    """
    Generate a grounded answer from retrieved rule chunks.

    TODO — Milestone 3:

    `retrieved_chunks` is the list returned by retrieve(). Each item is a dict:
      - "text"     : the chunk text
      - "game"     : the game name
      - "distance" : similarity score (you can use this to filter weak matches)

    Before writing code, talk through these with your group:
      - How will you format the chunks into a context block for the prompt?
      - What instructions will stop the model from answering beyond what the
        rules say? (Grounding is the whole point — a confident wrong answer
        is worse than an honest "I don't know.")
      - How will you surface which game each answer comes from?

    Your response should:
      1. Answer using only the retrieved context — not the model's general knowledge
      2. Make clear which game the answer comes from
      3. Say so clearly when the answer isn't in the loaded rules

    Return the response as a plain string.
    """
    if not retrieved_chunks:
        return (
            "I couldn't find anything relevant in the loaded rule books. "
            "Try rephrasing your question — or check that your ingestion pipeline is working."
        )

    # Build the context block: one labeled, delimited source per chunk,
    # tagged with its game name and distance score.
    context_blocks = []
    for i, chunk in enumerate(retrieved_chunks, start=1):
        context_blocks.append(
            f"[Source {i} - Game: {chunk['game']}]\n"
            f"[Distance score: {chunk['distance']:.3f}]\n"
            f"{chunk['text']}\n"
            f"---"
        )
    context = "\n".join(context_blocks)

    system_prompt = (
        "Using only the evidence given here:\n\n"
        "Provide an answer to answer the query. Do NOT use any information "
        "outside of the given evidence to support your answer. If you cannot "
        "provide an answer given the evidence, just say that you cannot answer "
        "the question. Clearly identify which game the answer comes from."
    )

    user_prompt = f"Question: {query}\n\nRetrieved rules:\n{context}"

    response = _client.chat.completions.create(
        model=LLM_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )

    return response.choices[0].message.content
