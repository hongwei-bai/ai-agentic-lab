from langchain_openai import ChatOpenAI
from langchain.agents import Tool, initialize_agent, AgentType

from calculator_tool import calculator_tool
from mem import get_memory

from dotenv import load_dotenv
load_dotenv()

# Define the tool
tools = [
    Tool(
        name="Calculator",
        func=calculator_tool,
        description="Useful for doing math calculations."
    )
]

# Initialize the LLM and memory
llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
memory = get_memory()

# Create the agent
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    memory=memory,
    verbose=True
)

# Run the agent
if __name__ == "__main__":
    print("🤖 AI Agent Ready (type 'exit' to quit)")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break
        response = agent.run(user_input)
        print("Agent:", response)
