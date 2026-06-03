import sys
from pathlib import Path
import asyncio
import os

os.environ["OPENAI_BASE_URL"] = "https://api.openai.com/v1"

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


from dotenv import load_dotenv
import braintrust
from braintrust import Eval
from autoevals import Factuality, AnswerRelevancy, ContextPrecision
from backend.rag_system.rag import run_rag
from backend.rag_system.eval_dataset import dataset

load_dotenv()
braintrust.login(api_key=os.getenv("BRAINTRUST_API_KEY"), org_name="Lab Maxers")
braintrust.auto_instrument()

#   define task function: takes input question and calls run_rag and returns response
def task(input):
    query = input if isinstance(input, str) else input["input"]
    response, value = asyncio.run(run_rag(query))

    result = {
        "output": response,
        "context": " ".join([doc.page_content for doc in value["documents"]])
    }

    # print("TASK RETURN VALUE:", result)
    # print("CONTEXT TYPE:", type(result["context"]))
    # print("CONTEXT LENGTH:", len(result["context"]))
    # print("CONTEXT SAMPLE:", result["context"][:1])

    return result

#   define list of scorers from autoevals 
#   - Fractuality to check ansewrs for correctness
#   - AnswerRelevancy checks if answer addersses question, 
#   - Context Precision checks if retrieved chunks were useful
fractuality_scorer = Factuality()

def answer_relevancy_scorer(input, output, expected=None, context=None, **kwargs):
    scorer = AnswerRelevancy(model="gpt-3.5-turbo")
    if isinstance(output, dict):
        return scorer(input=input, output=output.get("output"), context=output.get("context"))
    return scorer(input=input, output=output, context=context)

def context_precision_scorer(input, output, expected=None, context=None, **kwargs):
    scorer = ContextPrecision(model="gpt-3.5-turbo")
    if isinstance(output, dict):
        return scorer(input=input, output=output.get("output"), expected=expected, context=output.get("context"))
    return scorer(input=input, output=output, expected=expected, context=context)

#   Call Eval - pass eval_dataset, task fxn, and scorers
Eval(
    "RAG Stock Market Evaluation",
    experiment_name="RAG Evaluation Experiment",
    data=dataset,
    task=task,
    scores=[fractuality_scorer, answer_relevancy_scorer, context_precision_scorer],
)


