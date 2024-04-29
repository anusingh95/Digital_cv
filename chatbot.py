import streamlit as st
import os

from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains.question_answering import load_qa_chain
from langchain_community.vectorstores import FAISS


GOOGLE_API_KEY = st.secrets['api']['API_KEY']

if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY not found. Please set it in your .env file.")



def get_conversational_chain():
    prompt_template = """
    Answer the question and don't provide the wrong answer\n\n
    Context:\n {context}?\n
    Question: \n{question}\n

    Answer:
    """

    model = ChatGoogleGenerativeAI(model="gemini-pro",
                                   temperature=0.3, google_api_key=GOOGLE_API_KEY)

    prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)

    return chain
def user_input(user_question, chats):
    # Store only unique contexts
    unique_contexts = set(chat['User'] for chat in chats)
    unique_contexts.add(user_question)
    # Limit the number of contexts to 9
    if len(unique_contexts) > 10:
        unique_contexts = sorted(unique_contexts, key=lambda x: -chats[-1]['User'].similarity(x))[:9]

    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=GOOGLE_API_KEY)
    
    new_db = FAISS.load_local("chatbot", embeddings, allow_dangerous_deserialization=True)
    docs = new_db.similarity_search(user_question)

    chain = get_conversational_chain()

    response = chain(
        {"input_documents": [doc for context in unique_contexts for doc in new_db.similarity_search(context)], "question": user_question},
        return_only_outputs=True
    )
    
    chats.insert(0, {"User": user_question, "Amy": response["output_text"]})
    
    return chats


def cool_header():
    st.title("🚀 Chat with Amy, my AI assistant💁")
    st.markdown("Amy is a chatbot designed to answer your queries about me")
    
def display_chat(chats):
    for chat in chats:
        st.write(f"You: {chat['User']}")
        st.write(f"Amy: {chat['Amy']}")

