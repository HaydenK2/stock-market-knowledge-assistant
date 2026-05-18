from backend.rag_system.rag_env import set_env_variables


set_env_variables()



import bs4
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from operator import itemgetter

#   Start vm
# .\.venv\Scripts\Activate.ps1 

# Node 1: create_index
def load_docs():
    """
        returns all docs in raw_docs directory as a list
    """
    loader = DirectoryLoader(
        "./data/raw_docs/",
        glob="**/*.md",
        loader_cls=TextLoader,
        loader_kwargs={'encoding': 'utf-8'}
    )

    docs = loader.load()

    return docs

def create_index():
    """
        indexing
    """
    docs = load_docs()

    print(f"Loaded {len(docs)} documents")

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=75)

    chunks = splitter.split_documents(docs)

    # embed
    vectorstore = Chroma.from_documents(documents=chunks,
                                        embedding=OpenAIEmbeddings(),
                                        collection_name="stock_market_rag",
                                        persist_directory="./data/vectorstore/")
    
    retriever = vectorstore.as_retriever()

    print("retriever:", type(retriever))

    return retriever




#
def format_docs(docs):
    formatted_docs = []
    for doc in docs:
        formatted_docs.append(f"Source: {doc.metadata.get('source', 'Unknown')}\nContent: {doc.page_content}")
    return "\n\n".join(formatted_docs)  


def create_rag_chain():
    #   Time to prompt
    prompt = ChatPromptTemplate.from_template(
        "Answer this question based on the context provided.\n\nContext: {context}\n\nQuestion: {question}"
    )

    #   LLM
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)

    #  Chain
    rag_chain = prompt | llm | StrOutputParser()

    #   Query
    return rag_chain





