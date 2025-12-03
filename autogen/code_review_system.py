from autogen import AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager

# Note: You need to set OPENAI_API_KEY in your environment variables.

llm_config = {"model": "gpt-4", "temperature": 0}

# Developer writes code
developer = AssistantAgent(
    name="Developer",
    system_message="""You're a senior developer. Write clean,
    efficient Python code with proper documentation.""",
    llm_config=llm_config
)

# Reviewer checks code
reviewer = AssistantAgent(
    name="Reviewer",
    system_message="""You're a code reviewer. Check for bugs,
    performance issues, and best practices violations.""",
    llm_config=llm_config
)

# Tester writes tests
tester = AssistantAgent(
    name="Tester",
    system_message="""You write comprehensive unit tests
    using pytest.""",
    llm_config=llm_config
)

# User proxy executes code
executor = UserProxyAgent(
    name="Executor",
    human_input_mode="NEVER",
    code_execution_config={"work_dir": "workspace", "use_docker": False}
)

# Group chat
groupchat = GroupChat(
    agents=[developer, reviewer, tester, executor],
    messages=[],
    max_round=20
)

manager = GroupChatManager(groupchat=groupchat, llm_config=llm_config)

# Start conversation
executor.initiate_chat(
    manager,
    message="""Create a function to validate email addresses.
    Include error handling and write tests."""
)
