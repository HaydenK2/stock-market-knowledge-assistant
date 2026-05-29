from langgraph.graph import END, StateGraph, START
from typing import List
from typing_extensions import TypedDict
import rag_nodes as nodes
import rag_components.llm_doc_grader as doc_grader_agent
import rag_components.llm_question_rewriter as llm_question_rewriter
import web_search_tool as web_search
from langchain_core.documents import Document

retriever = nodes.create_index()
retrieval_grader = doc_grader_agent.create_structured_llm_grader()
question_rewriter = llm_question_rewriter.create_question_rewriter()
web_search_tool = web_search.create_web_search_tool()
rag_chain = nodes.create_rag_chain()

class GraphState(TypedDict):
    """
    Represents the state of our graph.

    Attributes:
        question: question
        generation: LLM generation
        web_search: whether to add search
        documents: list of documents
    """

    question: str
    generation: str
    web_search: str
    documents: List[str]

def build_graph():
    def retrieve(state):
        """
            retrieve the documents

            Args:
                state (dict): cur graph state
            
            Returns:
                state (dict): New key added to state, docs, that contain retrieved docs
        """

        print("---RETRIEVE---")
        question = state["question"]

        # Retrieval
        documents = retriever.invoke(question)
        return {"documents": documents, "question": question}


    def generate(state):
        """
            generates prompt based on question

            Args:
                state (dict): Current state of graph

            Returns:
                state (dict): New key added to state, generation, that contains LLM generation
        """

        print("---GENERATE---")
        question = state["question"]
        documents = state["documents"]

        #   RAG generation
        generation = rag_chain.invoke({"context": documents, "question": question})
        return {"documents": documents, "question": question, "generation": generation}



    def grade_documents(state):

        """
            Determine if retrived documents are relevant to question

            Args:
                state (dict): Current state of graph

            Returns:
                state (dict): Updates documents key with filtered relevant documents
        """

        print("---CHECK DOCUMENT RELEVANCE TO QUESTION---")
        question = state["question"]
        documents = state["documents"]

        filtered_docs = []
        web_search = "No"

        #   score each doc
        for d in documents:
            score = retrieval_grader.invoke(
                {"question": question, "document": d.page_content}
            )

            grade = score.binary_score
            if grade == "yes":
                print("---GRADE: DOCUMENT RELEVANT---")
                filtered_docs.append(d)
            else:
                print("---GRADE: DOCUMENT NOT RELEVANT---")
                web_search = "Yes"
                continue
        
        return {"documents": filtered_docs, "question": question, "web_search": web_search}


    def transform_query(state):
        """
        Transform the query to produce a better question.

        Args:
            state (dict): The current graph state

        Returns:
            state (dict): Updates question key with a re-phrased question
        """

        print("---TRANSFORM QUERY---")
        question = state["question"]
        documents = state["documents"]

        # Re-write question
        better_question = question_rewriter.invoke({"question": question})
        return {"documents": documents, "question": better_question}

    def web_search(state):
        """
        Web search based on the re-phrased question.

        Args:
            state (dict): The current graph state

        Returns:
            state (dict): Updates documents key with appended web results
        """

        print("---WEB SEARCH---")
        question = state["question"]
        documents = state["documents"]

        # Web search
        docs = web_search_tool.invoke({"query": question})
        web_results = "\n".join([d["content"] for d in docs])
        web_results = Document(page_content=web_results)
        documents.append(web_results)

        return {"documents": documents, "question": question}

    ### Edges
    def decide_to_generate(state):
        """
        Determines whether to generate an answer, or re-generate a question.

        Args:
            state (dict): The current graph state

        Returns:
            str: Binary decision for next node to call
        """

        print("---ASSESS GRADED DOCUMENTS---")
        state["question"]
        web_search = state["web_search"]
        state["documents"]

        if web_search == "Yes":
            # All documents have been filtered check_relevance
            # We will re-generate a new query
            print(
                "---DECISION: ALL DOCUMENTS ARE NOT RELEVANT TO QUESTION, TRANSFORM QUERY---"
            )
            return "transform_query"
        else:
            # We have relevant documents, so generate answer
            print("---DECISION: GENERATE---")
            return "generate"
        


    workflow = StateGraph(GraphState)

    #   define nodes
    workflow.add_node("retrieve", retrieve)
    workflow.add_node("grade_documents", grade_documents)
    workflow.add_node("generate", generate)
    workflow.add_node("transform_query", transform_query)
    workflow.add_node("web_search_node", web_search)


    #   build graph
    workflow.add_edge(START, "retrieve")
    workflow.add_edge("retrieve", "grade_documents")
    workflow.add_conditional_edges(
        "grade_documents",
        decide_to_generate,
        {
            "transform_query": "transform_query",
            "generate": "generate",
        }
    )
    workflow.add_edge("transform_query", "web_search_node")
    workflow.add_edge("web_search_node", "generate")
    workflow.add_edge("generate", END)

    #   compile
    return workflow.compile()