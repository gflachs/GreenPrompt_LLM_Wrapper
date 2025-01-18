import torch
from src.app.llm_model import LLMModel

# This script is used for terminal-based interaction with the llm_model class 
# just run it within the terminal with "python model_handler.py"

modeltyp =  "text-generation"
model = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
uses_chat_template =  {"uses_chat_template":True}

prompting =  {
    "max_new_tokens": 256, 
    "do_sample": True,
    "temperature": 0.7,
    "top_k": 50, 
    "top_p": 0.95}
deployment = {
    "torch_dtype": torch.bfloat16,
    "device_map": "auto"}

llm = LLMModel(modeltyp=modeltyp, model = model, prompting_config=prompting, deployment_config=deployment, **uses_chat_template)
llm.download_model()

print("\nHello im a chatbot\n")

while True:
    question = input("Ask the LLM a question:\n")
    answer = llm.answer_question(question)
    print("\nAnswer:")
    print(answer)
    
    ask_again = input("\nIf you want to ask another question say y:")

    if (ask_again != "y"):
        break

print("Goodbye")    
