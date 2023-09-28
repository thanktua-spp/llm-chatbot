import dotenv
import os
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate
)

dotenv.load_dotenv()
system_template = SystemMessagePromptTemplate.from_template(
            """
            Instruction: Answer the question based on the context given below.
                    
            Context: You are a smart, helpful and intelligent coorperate business assistant for staff members
            of the business team at CypherCrescent Limited a fast growing Technology company in the oil and gas
            servicing and consultancy space. You will assist staff members of the business team whenever called upon,
            your primary duties and responsibility are limited to the following,
            1. Supporting the business team with helpful informations about client engagement from previous conversations.
            2. Generating helpful responds suggestions to new messages from which a staff member can edit or modify before replying.
            
            Use the following guide when given a helpful user responds.
            - Respond politely to short greetings
            - Use context to share short information about yourself when asked.
            - Only respond with short, meaningful replies. 
            - If the user attemps to have an off-topic conversation that is related to sports, politics, social life,
                etc you will simply repsonds in a very polite manner that suggest that as Business assistant you will
                restrain from having unofficial and unproductive converations,
                while also responding if there is any other way you can help the staff member. 
            """
        )
human_template = HumanMessagePromptTemplate.from_template("{question}")
ai_template = AIMessagePromptTemplate.from_template("")
prompt_template = ChatPromptTemplate(
    messages=[
        system_template,
        MessagesPlaceholder(variable_name='chat_history'),
        human_template,
        ai_template,   
    ]
)

llm_chat = ChatOpenAI(
    #streaming=True, callbacks=[StreamingStdOutCallbackHandler()]
    )
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
conversation = ConversationChain(
    prompt=prompt_template,
    llm=llm_chat,
    memory=memory,
    input_key = "question",
    verbose=False)

if __name__ == "__main__":
    user_prompt = "Tell me about Football"
    info = conversation({"question":user_prompt })
    print(info['response'])
    
    #print(memory.buffer)
    # print(conversation.memory.buffer)
    # print(conversation.prompt)