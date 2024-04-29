import streamlit as st
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

def user_input(user_question, context, chats):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=GOOGLE_API_KEY)
    
    new_db = FAISS.load_local("chatbot", embeddings, allow_dangerous_deserialization=True)
    docs = new_db.similarity_search(user_question)

    chain = get_conversational_chain()
    
    # Add previous context to user_question if not found in current question
    if context and context not in user_question:
        user_question = context + " " + user_question

    response = chain(
        {"input_documents": docs, "question": user_question},
        return_only_outputs=True
    )
    
    # Update context
    if "context" in response:
        context = response["context"]
    
    chats.insert(0, {"User": user_question, "Amy": response["output_text"]})
    
    return context, chats

def cool_header():
    st.title("🚀 Chat with Amy, my AI assistant💁")
    st.markdown("Amy is a chatbot designed to answer your queries about me")
    
def display_chat(chats):
    for chat in chats:
        st.write(f"You: {chat['User']}")
        st.write(f"Amy: {chat['Amy']}")


