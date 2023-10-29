"""import transformers 
from transformers import pipeline

pipe = pipeline("text-generation", model="Open-Orca/Mistral-7B-OpenOrca")

# Ask a question about life
question = "What is the meaning of life?"

# Generate a response from the model
response = pipe(question)

# Print the response
print(response)"""




import transformers

# Load the model
model = transformers.TFAutoModelForCausalLM.from_pretrained("Open-Orca/Mistral-7B-OpenOrca", framework="tf")

# Create the pipeline
pipe = transformers.Pipeline(
    task="text-generation",
    model=model,
)

# Generate a response from the model
response = pipe(question="What is the meaning of life?")

# Print the response
print(response)