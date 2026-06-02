import sys
from pathlib import Path
import asyncio

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import braintrust
from braintrust import Eval
from autoevals import Factuality, AnswerRelevancy, ContextPrecision
from backend.rag_system.rag import run_rag
from backend.rag_system.eval_dataset import dataset

braintrust.auto_instrument()

#   define task function: takes input question and calls run_rag and returns response
def task(query):
    response, chunk_records = asyncio.run(run_rag(query))

    return response


#   define list of scorers from autoevals 
#   - Fractuality to check ansewrs for correctness
#   - AnswerRelevancy checks if answer addersses question, 
#   - Context Precision checks if retrieved chunks were useful
fract_evaluator = Factuality()
answer_relevancy_evaluator = AnswerRelevancy()
context_precision_evaluator = ContextPrecision()



#   Call Eval - pass eval_dataset, task fxn, and scorers
Eval(
    "RAG Stock Market Evaluation",
    experiment_name = "RAG Evaluation Experiment",

    data = dataset,
    task=task,
    scores=[fract_evaluator, answer_relevancy_evaluator, context_precision_evaluator],
)


