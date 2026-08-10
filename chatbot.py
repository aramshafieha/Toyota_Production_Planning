import os
from dotenv import load_dotenv
from google import genai

# Load .env
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

# Create client
client = genai.Client(api_key=api_key)

print("🤖 Toyota Production Planning AI Assistant")
print("Type 'exit' to quit.\n")

while True:
    question = input("You: ")

    if question.lower() == "exit":
        print("Goodbye!")
        break

    prompt = f"""
You are an AI assistant for a Toyota Production Planning project.

Answer questions about:
- Linear Programming
- Genetic Algorithms
- Toyota Production System
- Production Planning
- Manufacturing Optimization

Question:
{question}
"""

    try:
        response = client.models.generate_content(
         model="gemini-3.5-flash",
         contents=prompt
         )

        print("\nAI:")
        print(response.text)
        print()

    except Exception as e:
        print("\nError:")
        print(e)