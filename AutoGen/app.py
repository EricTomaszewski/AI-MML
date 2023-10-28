import autogen

config_list = [
    {
        'model': 'gpt-3.5-turbo-16k',
        'api_key': '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'
    }
]

llm_config = {
    "request_timeout": 600,
    "seed": 42,         # with same prompt & seed => using cached version
    "config_list": config_list,
    "temperature": 0
}

assistant = autogen.AssistantAgent(
    name = "assistant",
    llm_config = llm_config
)

'''assistant = autogen.AssistantAgent(
    name = "CTO",
    llm_config = llm_config,
    system_message = "Chief technical officer of a tech company"
)
'''
# user_proxy => agent acting on behalf of the human
user_proxy = autogen.UserProxyAgent(
    name = "user_proxy",
    human_input_mode = "TERMINATE",
    max_consecutive_auto_reply = 10,
    is_termination_msg = lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
    code_execution_config = {"work_dir": "web"},     # any files it creates will be saved here
    llm_config = llm_config,
    system_message = """Reply TERMINATE if the task has been solved at full satisfaction.
    Otherwise, reply CONTINUE, or the reason why the task is not solved yet."""
)

task = """
Give me a summary of this article: https://www.bbc.co.uk/news/live/world-middle-east-67165505
"""

user_proxy.initiate_chat(
    assistant,
    message = task
)