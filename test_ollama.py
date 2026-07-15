from agent.ollama_client import OllamaClient

client = OllamaClient()

response = client.chat(

    system_prompt="You are a helpful assistant.",

    user_prompt="Reply with exactly this text: Hello PwC"

)

print(response)