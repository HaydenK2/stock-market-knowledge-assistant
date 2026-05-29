from .rag_stock_market_graph import build_graph
from pprint import pprint

app = build_graph()

# Run
async def run_rag(question):
    inputs = {"question": question}
    for output in app.stream(inputs):
        
        for key, value in output.items():
            # Node
            pprint(f"Node '{key}':")
            # Optional: print full state at each node
            # pprint.pprint(value["keys"], indent=2, width=80, depth=None)
        pprint("\n---\n")

    # Final generation
    output = value["generation"]
    # pprint(output)
    return output


# run_rag("What is the current state of the stock market?") 
if __name__ == "__main__":
    import asyncio
    asyncio.run(run_rag("What are some basic terms I should know about the stock market? Give a brief definition of each term and explain why it's important"))