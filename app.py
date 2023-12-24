from langchain_google_genai import ChatGoogleGenerativeAI
import streamlit as st
from langchain.callbacks.base import BaseCallbackHandler
# from dotenv import load_dotenv
# import os
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory

# load_dotenv()

# # File uploader in the sidebar on the left
# with st.sidebar:
#     openai_api_key = st.text_input("OpenAI API Key", type="password")
# if not openai_api_key:
#     st.info("Please add your OpenAI API key to continue.")
#     st.stop()


# # Set OPENAI_API_KEY as an environment variable
# os.environ["OPENAI_API_KEY"] = openai_api_key

st.set_page_config(page_title="LangChain Gemini Chatbot", page_icon="🦜")

st.title("Google Gemini Pro Max Model!!")

def take_api_key(model):
    # File uploader in the sidebar on the left
    with st.sidebar:
        api_key = st.text_input(f"Enter the {model} API Key", type="password")
    if not api_key:
        st.info(f"Please add your {model} API key to continue.")
        st.stop()
    
    return api_key

# Create a dropdown to select the model, on which we have to work
model = st.selectbox(
    'Select the model?',
    ('Falcon', 'Gemini-Pro', 'Mpt-30', 'Orca', 'Google PaLM', 'Open AI', 'Gemini-Pro-Vision', 'Mistral')
)

if model == "Gemini-Pro":
    api_key = take_api_key(model)

    # Create a llm model
    llm = ChatGoogleGenerativeAI(
        # google_api_key=os.environ.get("PALM_API_KEY"),
        google_api_key=api_key,
        model="gemini-pro"
    )
else:
    st.info("The model will come soon.")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Welcome to Enqurious Gemini Model!! 🙋‍♂️. How can I help you?"
        }
    ]

# Create the memory only the first time
if "memory" not in st.session_state:
    st.session_state.memory = ConversationBufferMemory()
    
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if prompt := st.chat_input("Input", key="input"):
    with st.chat_message("human"):
        st.session_state.messages.append({"role": "human", "content": prompt})
        st.write(prompt)

    chain = ConversationChain(
        llm=llm,
        memory=st.session_state.memory,
        verbose=True
    )

    with st.chat_message("assistant"):
        response = chain.run(prompt)
        # st_response = response.content
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.markdown(response)


### We can use the agent here  (Try the gemini-pro-vision once)