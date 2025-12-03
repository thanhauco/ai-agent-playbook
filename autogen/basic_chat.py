from autogen import AssistantAgent, UserProxyAgent

# Note: You need to set OPENAI_API_KEY in your environment variables.
# You also need to have 'pyautogen' installed.

llm_config = {"model": "gpt-4", "temperature": 0}

assistant = AssistantAgent(
    name="assistant",
    llm_config=llm_config
)

user_proxy = UserProxyAgent(
    name="user_proxy",
    human_input_mode="NEVER",  # or "ALWAYS" or "TERMINATE"
    max_consecutive_auto_reply=10,
    code_execution_config={"work_dir": "coding", "use_docker": False}
)

# Initiate chat
user_proxy.initiate_chat(
    assistant,
    message="Plot a chart of NVDA and TESLA stock price change YTD."
)
