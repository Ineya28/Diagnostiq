from openai import OpenAI

# 1️⃣ Connect to Featherless
client = OpenAI(
    base_url="https://api.featherless.ai/v1",
    api_key="rc_75e9782ce9570cbed0c28488b94f595dacbabdf94b9647cb3aaabe566bcbb8a0"  # 
)

print("Welcome to Featherless Playground! Type 'quit' to exit.\n")

# 2️⃣ Interactive loop
while True:
    user_input = input("You: ")
    if user_input.lower() in ["quit", "exit"]:
        print("Goodbye!")
        break

    # 3️⃣ Send the prompt to the AI
    response = client.chat.completions.create(
        model="mistralai/Mistral-7B-Instruct-v0.2",  # you can switch to any model
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_input}
        ],
    )

    # 4️⃣ Print the AI's reply
    print("AI:", response.choices[0].message.content, "\n")