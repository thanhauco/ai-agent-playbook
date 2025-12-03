from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain.llms import OpenAI

# Note: You need to set OPENAI_API_KEY in your environment variables.

llm = OpenAI(temperature=0)
memory = ConversationBufferMemory()
conversation = ConversationChain(
    llm=llm,
    memory=memory,
    verbose=True
)

print(conversation.predict(input="Hi, I'm Alice"))
# Agent should remember: "Hello Alice!"

print(conversation.predict(input="What's my name?"))
# Agent should recall: "Your name is Alice."
