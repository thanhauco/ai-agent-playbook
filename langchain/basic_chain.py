from langchain import OpenAI, PromptTemplate, LLMChain

# Note: You need to set OPENAI_API_KEY in your environment variables.

prompt = PromptTemplate(
    input_variables=["product"],
    template="Write a tagline for a company that makes {product}"
)

llm = OpenAI(temperature=0.9)
chain = LLMChain(llm=llm, prompt=prompt)

result = chain.run("AI agents")
print(result)
