from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# Initialize Ollama LLM (local)
llm = Ollama(model="llama2")  # replace "llama2" with your local model name

# Prompt template for English sentence generation
sentence_template = PromptTemplate(
    input_variables=["occupation"],
    template=(
        "Generate a simple English sentence suitable for a learner whose occupation is {occupation}."
    ),
)

sentence_chain = LLMChain(llm=llm, prompt=sentence_template)

# Run the chain
result = sentence_chain.run({"occupation": "teacher"})
print("Generated sentence:", result)