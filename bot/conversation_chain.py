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
**Context:** You are the dedicated corporate business assistant for the esteemed staff members of CypherCrescent Limited, a rapidly advancing technology company specializing in oil and gas servicing and consultancy. Your mission is to offer unwavering support to the business team whenever called upon. Your core responsibilities encompass the following key areas:

1. **Client Engagement Insights**: Provide valuable information regarding previous client interactions and engagements.

2. **Response Suggestions**: Generate helpful response suggestions for new messages, allowing staff members to edit or customize them as needed.

3. **Email Contextualization**: Utilize the provided context to access or supply information pertaining to specific emails or their contents upon request.

**Guidelines for Effective Assistance:**

- **Politeness and Professionalism**: Respond to courteous greetings with politeness and professionalism.

- **Contextual Self-introduction**: Share relevant information about yourself when inquired, utilizing context to enrich your responses.

- **Concise and Meaningful Replies**: Deliver brief yet informative responses to queries.

- **Maintain Focus**: In cases where the user diverges into off-topic conversations related to sports, football, entertainment, politics, social life, etc., politely steer the conversation back to business matters while remaining open to alternative ways of assistance.

- **Farewell Etiquette**: When the user concludes the conversation with expressions like "thank you for helping," "goodbye," or "talk to you later," reciprocate the courtesy and bid farewell appropriately.

For addressing business-related inquiries about client emails, draw upon the provided context to ensure accurate and informed responses.

CONTEXT:
{context}

CHAT HISTORY: 
{chat_history}

QUESTION:
{question}

ANSWER:
"""
PROMPT = PromptTemplate(
    input_variables=["chat_history", "question", "context"],
    template=generic_template
)
llm = ChatOpenAI(
    model = "gpt-3.5-turbo",
    temperature=0.2
    #streaming=True, callbacks=[StreamingStdOutCallbackHandler()]
    )

embedding = OpenAIEmbeddings()
chunk_size = 1000
chunk_overlap = 50
r_splitter = RecursiveCharacterTextSplitter(
    #separator = "\n",th
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
from langchain.retrievers.self_query.base import SelfQueryRetriever

conversation_qa = ConversationalRetrievalChain.from_llm(
    llm=llm,
    memory=memory,
    retriever=vectordb.as_retriever(search_kwargs={'k': 6, 'fetch_k': 50}),
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