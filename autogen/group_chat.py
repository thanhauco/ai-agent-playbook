from autogen import AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager

# Note: You need to set OPENAI_API_KEY in your environment variables.

llm_config = {"model": "gpt-4", "temperature": 0}

user_proxy = UserProxyAgent(
    name="user_proxy",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=10,
    code_execution_config={"work_dir": "coding", "use_docker": False}
)

coder = AssistantAgent(
    name="Coder",
    system_message="You write Python code to solve problems",
    llm_config=llm_config
)

reviewer = AssistantAgent(
    name="Reviewer",
    system_message="You review code for bugs and improvements",
    llm_config=llm_config
)

tester = AssistantAgent(
    name="Tester",
    system_message="You write and run tests",
    llm_config=llm_config
)

groupchat = GroupChat(
    agents=[coder, reviewer, tester, user_proxy],
    messages=[],
    max_round=12
)

manager = GroupChatManager(groupchat=groupchat, llm_config=llm_config)

user_proxy.initiate_chat(
    manager,
    message="Build a function to calculate Fibonacci numbers"
)
