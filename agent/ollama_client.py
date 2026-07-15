from ollama import Client


class OllamaClient:

    def __init__(
        self,
        model: str = "qwen3:4b",
        host: str = "http://localhost:11434",
    ):
        self.client = Client(host=host)
        self.model = model

    def chat(
        self,
        system_prompt: str,
        user_prompt: str,
        format: str = None,
        think: bool = False,
    ) -> str:

        try:

            response = self.client.chat(

                model=self.model,

                messages=[
                    {
                        "role": "system",
                        "content": system_prompt,
                    },
                    {
                        "role": "user",
                        "content": user_prompt,
                    },
                ],

                format=format,

                think=think,

                options={
                    "temperature": 0,
                },

            )

            if "message" not in response:
                raise RuntimeError(
                    "Invalid response received from Ollama."
                )

            content = response["message"].get("content", "").strip()

            if not content:
                raise RuntimeError(
                    "Ollama returned an empty response."
                )

            return content

        except Exception as e:

            raise RuntimeError(
                "Failed to communicate with Ollama.\n\n"
                "Please ensure:\n"
                "1. Ollama is running.\n"
                "2. The model is installed.\n"
                "3. The model name is correct.\n\n"
                f"Original Error: {e}"
            ) from e