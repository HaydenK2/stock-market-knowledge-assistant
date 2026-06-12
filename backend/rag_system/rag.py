from .rag_stock_market_graph import build_graph
from sentence_transformers import CrossEncoder
from pprint import pprint
import asyncio
from functools import partial


def get_app():
    global _app
    if _app is None:
        _app = build_graph()
    return _app

_app = None

async def retrieve_with_eval_data(query, docs_and_scores):
    cross_encoder = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')

    chunk_records = []
    for rank, (doc, vector_score) in enumerate(docs_and_scores):
        chunk_records.append({
            "chunk_id": doc.metadata.get("chunk_id", f"chunk_{rank}"),
            "content_snippet": doc.page_content[:200],
            "vector_score": float(vector_score),
            "retrieval_source": "vector",
            "final_rank": rank + 1
        })

    #   call cross_encoder
    pairs = [[query, r["content_snippet"]] for r in chunk_records]
    loop = asyncio.get_event_loop()
    ce_scores = await loop.run_in_executor(None, cross_encoder.predict(pairs))

    for i, ce_score in enumerate(ce_scores):
        chunk_records[i]["cross_encoder_score"] = float(ce_score)

    chunk_records.sort(key=lambda x: x["cross_encoder_score"], reverse=True)
    for i, chunk in enumerate(chunk_records):
        chunk["final_rank"] = i + 1
    
    return chunk_records

# Run
async def run_rag(question):
    inputs = {"question": question}
    value = None

    def run_stream():
        result = None
        for output in get_app().stream(inputs):
            for key, value in output.items():
                # Node
                pprint(f"Node '{key}':")
                # Optional: print full state at each node
                # pprint.pprint(value["keys"], indent=2, width=80, depth=None)
            pprint("\n---\n")
        return result
    
    
    
    loop = asyncio.get_event_loop()
    value = await loop.run_in_executor(None, run_stream)

    if value is None:
        raise RuntimeError("run_rag did not receive any output from app.stream()")

    
    # print("final gen completed")
    # print(f"DEBUG - State keys: {value.keys()}")  # See what keys are available
    # print(f"DEBUG - docs_and_scores exists: {'docs_and_scores' in value}")

    # print("final gen completed")
    output = value["generation"]
    # chunk_records = await retrieve_with_eval_data(value["question"], value["docs_and_scores"])

    return output, value


# run_rag("What is the current state of the stock market?") 
# if __name__ == "__main__":
#     import asyncio
#     asyncio.run(run_rag("What are some basic terms I should know about the stock market? Give a brief definition of each term and explain why it's important"))