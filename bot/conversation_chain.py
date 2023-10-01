import dotenv
import os
from langchain.chat_models import ChatOpenAI
from langchain.chains import (
    ConversationChain,
    RetrievalQAWithSourcesChain,
    ConversationalRetrievalChain,
    LLMChain)
from langchain.memory import ConversationBufferMemory
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.prompts import (
    ChatPromptTemplate,
    PromptTemplate,
    MessagesPlaceholder,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate
)
from langchain.chains import ConversationalRetrievalChain, LLMChain
from langchain.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter, CharacterTextSplitter
from email_fatcher import access_outlook_email
from langchain.embeddings.openai import OpenAIEmbeddings

dotenv.load_dotenv()
system_template = SystemMessagePromptTemplate.from_template("""do nothing""")
human_template = HumanMessagePromptTemplate.from_template("{question}")
ai_template = AIMessagePromptTemplate.from_template("")
prompt_template = ChatPromptTemplate.from_messages(
    messages=[
        #system_template,
        MessagesPlaceholder(variable_name='chat_history'),
        human_template,
        ai_template,   
    ],
    #input_variables=["context", "question","chat_history"]
)
generic_template = """        
Context: You are a smart, helpful and intelligent coorperate business assistant for staff members
of the business team at CypherCrescent Limited a fast growing Technology company in the oil and gas
servicing and consultancy space. You will assist staff members of the business team whenever called upon,
your primary duties and responsibility are limited to the following,
1. Supporting the business team with helpful informations about client engagement from previous conversations.
2. Generating helpful responds suggestions to new messages from which a staff member can edit or modify before replying.
3. Use the context provided to access or provide information about specific emails or their content when asked.

Use the following guide when given a helpful user responds.
- Respond politely to short greetings
- Use context to share short information about yourself when asked.
- Only respond with short, meaningful replies. 
- If the user attemps to have an off-topic conversation that is related to sports, politics, social life,
etc you will simply repsonds in a very polite manner that suggest that as Business assistant you will
restrain from having unofficial and unproductive converations,
while also responding if there is any other way you can help the staff member.
- When the user says tries to end the conversation by saying "thankyou for helpfing" or "goodbye" or "talk to you later" you have to end the conversation nicely and say goodbye.
To answer Business related questions regarding emails from client you will utilise information from the context provided here:
{context}
    
chat history:
{chat_history}

Question:
{question}
            """
PROMPT = PromptTemplate(
    input_variables=["chat_history", "question", "context"],
    template=generic_template
)
llm = ChatOpenAI(
    #streaming=True, callbacks=[StreamingStdOutCallbackHandler()]
    )

embedding = OpenAIEmbeddings()
chunk_size = 500
chunk_overlap = 100
r_splitter = RecursiveCharacterTextSplitter(
    #separator = "\n",
    chunk_size=chunk_size,
    chunk_overlap=chunk_overlap,
    #length_function = len
)
target_sender_email = 'hellonigeria@getreliancehealth.com'
email_doc = access_outlook_email(target_sender_email)
#print(email_doc)
persist_directory = r'C:\Users\egbet\Desktop\2023\dev projects 2023\llm-chatbot\bot\chromadb'
splits = r_splitter.split_text(email_doc)
#print(len(splits))
vectordb = Chroma.from_texts(
    texts=splits,
    embedding=embedding,
    persist_directory=persist_directory
)
#print(vectordb._collection.count())

memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True,
    output_key="answer",
    )

conversation_qa = ConversationalRetrievalChain.from_llm(
    llm=llm,
    memory=memory,
    retriever=vectordb.as_retriever(search_kwargs={'k': 2, 'lambda_mult': 0.25}),
    verbose=True,
    return_source_documents=True,
    combine_docs_chain_kwargs={
         "prompt": PROMPT
         }
)

import sys
if __name__ == "__main__":
    # user_prompt = "What was this email about?" #Tell me about Football
    # result = conversation_qa({"question": user_prompt})
    #print(memory.buffer)
    # print(conversation.memory.buffer)
    #print(conversation_qa.prompt)
    query = None
    if len(sys.argv) > 1:
        query = sys.argv[1]
        
    chat_history = []
    while True:
        if not query:
            query = input("Prompt: ")
        if query in ['quit', 'q', 'exit']:
            sys.exit()
        result = conversation_qa({"question": query, "chat_history": chat_history})
        print(result['answer'])
        chat_history.append((query, result['answer']))
        query = None