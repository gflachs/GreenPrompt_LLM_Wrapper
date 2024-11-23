
#below is just an exemple to test my code, it will be replaced by the code of niklas's api
from sci_score import calculate_sci_score
from transformers import pipeline

model = pipeline("text-generation", model="gpt2")
prompt = "What is the capital of France?"
response = model(prompt, max_length=50)[0]["generated_text"]
#When niklas has finished the api model he will have some thing like that i think in the end so i will colect him prompt


# I will add my  function below in him code to calculate the SCI-Score
sci_score = calculate_sci_score(prompt, response)

# Some Logs
print(f"Prompt: {prompt}")
print(f"Response: {response}")
print(f"SCI-Score: {sci_score}")
