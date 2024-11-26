from llm_model import LLMModel

# This script is used for terminal-based interaction with the llm_model class 
# just run it within the terminal with "python model_handler.py"

llm = LLMModel(modeltyp="text-generation", model = "TinyLlama/TinyLlama-1.1B-Chat-v1.0")
llm.download_model()

print("\nHello im a chatbot\n")

while True:
    question = input("Ask the LLM a question:\n")
    answer = llm.answer_question(question)
    print("\nAnswer:")
    print(answer)
    
    ask_again = input("\nIf you want to ask another question say y:")

    if not (ask_again == "y"):
        break

print("Goodbye")    
