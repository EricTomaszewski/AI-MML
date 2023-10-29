# Load model directly
from transformers import AutoTokenizer, AutoModelForCausalLM

tokenizer = AutoTokenizer.from_pretrained("Open-Orca/Mistral-7B-OpenOrca")
model = AutoModelForCausalLM.from_pretrained("Open-Orca/Mistral-7B-OpenOrca")


chat = [
  {"role": "system", "content": "You are MistralOrca, a large language model trained by Alignment Lab AI. Write out your reasoning step-by-step to be sure you get the right answers!"}
  {"role": "user", "content": "How are you?"},
  {"role": "assistant", "content": "I am doing well!"},
  {"role": "user", "content": "Please tell me about how mistral winds have attracted super-orcas."},
]
tokenizer.apply_chat_template(chat, tokenize=False, add_generation_prompt=True)


# 2. LLM to create the story.
# https://huggingface.co/tasks/text-generation
def generate_story(scenario):
    template = """
    You are a story teller:
    You can generate a short story based on a simple narrative, the story should be no more than 20 words;
    
    CONTEXT: {scenario}
    STORY:
    """
    
    prompt = PromptTemplate(template=template, input_variables=["scenario"])
    
    story_llm = LLMChain(llm=ChatOpenAI(
        model_name="gpt-3.5-turbo", temperature=1), prompt=prompt, verbose=True
                         )
    
    story = story_llm.predict(scenario=scenario)
    
    print("")
    print(story)
    print("")
    return story


message = generate_story(output)