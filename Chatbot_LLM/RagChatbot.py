import pdfplumber
import streamlit as st
from click import prompt
from langchain_community.vectorstores import FAISS
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_text_splitters import RecursiveCharacterTextSplitter

st.header("My First Chatbot")

OPEN_AI_KEY = "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"

with st.sidebar:
    st.title("Your Documents")

    file = st.file_uploader("Upload PDF File & Start Asking Questions", type="pdf")

# Extract contents from pdf & chunk it

if file is not None:
    # extract text from it
    with pdfplumber.open(file) as pdf:
        text = ""

        for page in pdf.pages:
            text += page.extract_text() + "\n"


    # st.write(text)

    # Split text into chunks

    text_splitter = RecursiveCharacterTextSplitter(
        separators=["\n", "\n\n", ". ", " ", ""],
        chunk_size=1000, # Each chunk is 1000 characters
        chunk_overlap=200
    )
    # chunk_overlap --> First chunk some characters should be remembered
    # so that the Second chunk is meaningful

    chunks = text_splitter.split_text(text)

    # st.write(chunks)

    # Generating embeddings

    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small",
        openai_api_key=OPEN_AI_KEY
    )

    # Store Embeddings

    vector_store = FAISS.from_texts(chunks, embeddings)

    # Get user question

    user_question = st.text_input("Type your question")

    # Generate answer
    # sending question --> embeddings --> similarity search --> results to LLM --> response ( CHAIN )

    # Similarity Search occuring for the below line
    retriever = vector_store.as_retriever(
        search_type = "mmr",
        search_kwargs = {"k":4}
    )

    # search_type = "mmr" means its a technique for searching
    # search_kwargs = {"k":4} finds the closest four matches
    # So basically it returns the best 4 results from the vector_store database


    def format_docs(docs):
        return "\n\n".join([docs.page_content for docs in docs])

    # define the LLM & prompt

    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.3,
        max_tokens=1000,
        openai_api_key=OPEN_AI_KEY
    )

    # provide the prompts
    prompt = ChatPromptTemplate.from_messages([
        ("system",
         "You are a helpful assistant answering questions about a PDF document.\n\n"
         "Guidelines:\n"
         "1. Provide complete, well-explained answers using the context below.\n"
         "2. Include relevant details, numbers, and explanations to give a thorough response.\n"
         "3. If the context mentions related information, include it to give fuller picture.\n"
         "4. Only use information from the provided context - do not use outside knowledge.\n"
         "5. Summarize long information, ideally in bullets where needed.\n"
         "5. If the information is not in the context, say so politely.\n\n"
         "Context:\n{context}"),
        ("human", "{question}")
    ])

    chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    if user_question:
        response = chain.invoke(user_question)
        st.write(response)

