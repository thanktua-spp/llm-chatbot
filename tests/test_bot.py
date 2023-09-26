from bot.bot import initiate_index
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI


def test_prompt():
    index = initiate_index()
    chain = ConversationalRetrievalChain.from_llm(
        llm=ChatOpenAI(model="gpt-3.5-turbo"),
        retriever=index.vectorstore.as_retriever(search_kwargs={"k": 1}),
    )
    query = "Are you working fine?"

    result = chain({"question": query, "chat_history": []})

    assert "answer" in result
    assert isinstance(result["answer"], str)
