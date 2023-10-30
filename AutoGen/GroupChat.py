from autogen import AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager, config_list_from_json

config_list = config_list_from_json(env_or_file="OAI_CONFIG_LIST")
llm_config = {
    "config_list": config_list,
    "seed": 42,
    "request_timeout": 120
}

user_proxy = UserProxyAgent(
    name = "user_proxy",
    system_message = "A human user.",
    code_execution_config = {
        "last_n_messages": 2,
        "work_dir": "code"
        },
    human_input_mode = "ALWAYS"    
)

coder = AssistantAgent(
    name = "coder",
    llm_config = llm_config
)

pm = AssistantAgent(
    name = "product_manager",
    system_message = "Break down the idea into a well scoped requirements for the coder",
    llm_config = llm_config
)

groupchat = GroupChat(
    agents = [user_proxy, coder, pm],
    messages = []
)

manager = GroupChatManager(
    groupchat = groupchat,
    llm_config = llm_config
)

user_proxy.initiate_chat(manager, message="Build a classic, basic pong game. Save the code on disc in python file that runs in Windows.")