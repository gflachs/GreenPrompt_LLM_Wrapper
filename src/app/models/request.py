from pydantic import BaseModel, ConfigDict, Field

class PromptingArgs(BaseModel):
    model_config = ConfigDict(extra='allow')

class DeploymentArgs(BaseModel):
    model_config = ConfigDict(extra='allow')

class ModelArgs(BaseModel):
    prompting: PromptingArgs
    deployment: DeploymentArgs

class ModelConfig(BaseModel):
    modeltyp: str = Field(..., description="The typ or categorie of a llm for example 'text-generation'.")
    model: str = Field(..., description="The name of the llm model you want to use for example 'TinyLlama/TinyLlama-1.1B-Chat-v1.0'.")
    uses_chat_template: bool = Field(..., description="True if the model from hugging face is usable with the function apply_chat_template, otherwise false")
    args: ModelArgs

class PromptResponse(BaseModel):
    answer: str = Field(..., description="The llm's answer to a previously asked question.")
    sci_score: int = Field(..., description="A numerical value as a representation of the sci score as a representation of the energy consumption and the associated CO2 emissions generated during the processing of the prompt and the creation of the answer.")

class Prompt(BaseModel):
    question: str = Field(..., description="A string formatted question which is to be answered by the llm while measuring the energy consumption needed to generate the answer")