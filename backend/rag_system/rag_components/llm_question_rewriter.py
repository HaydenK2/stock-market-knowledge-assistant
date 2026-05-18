from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser


def create_question_rewriter():
    """
        creates agent that rewrites user's question into something easier for llm to understand
    """
    llm = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0)

    #   prompt
    system = """
    You are a question/prompt rewriter whose job is to convert the user's input into a clean, concise, search-friendly query. \n

    Rules:
    - Keep the original meaning and intent exactly the same.
    - Remove filler words, unnecessary context, and conversational phrasing.
    - Add relevant keywords and structure the query for search engines.
    - Prefer short, direct phrasing that a user would type into a search bar.
    - Preserve any specific entities, technologies, dates, or domain details.
    - Look at the input and try to reason about the underlying semantic intent / meaning
    - If the input is already a good search query, simply refine it without changing meaning.
    - Output only the rewritten search query, nothing else.
    """

    re_write_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system),
            (
                "human",
                "Here is the initial question: \n\n {question} \n formulate an improved question.",
            ),
        ]
    )
    

    question_rewriter = re_write_prompt | llm | StrOutputParser()

    return question_rewriter




