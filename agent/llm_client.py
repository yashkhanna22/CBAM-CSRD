import os
import requests
from dotenv import load_dotenv
from ollama import Client as OllamaClientLib

# Load environment variables
load_dotenv()

class LLMClient:
    def __init__(self):
        # Read settings from environment
        self.use_llm = os.getenv("USE_LLM", "ollama").lower().strip()
        self.model = os.getenv("LLM_MODEL", "qwen3:4b").strip()
        
        # Groq specific config
        self.groq_api_key = os.getenv("GROQ_API_KEY", "").strip()
        
        # Ollama specific config
        self.ollama_host = os.getenv("OLLAMA_HOST", "http://localhost:11434").strip()
        
        # Initialize Ollama client library if using Ollama
        if self.use_llm == "ollama":
            self.ollama_client = OllamaClientLib(host=self.ollama_host)

    def describe(self) -> str:
        """
        Return a one-line description of the active LLM config for display at startup.
        """
        if self.use_llm == "groq":
            key_status = f"key={'***' + self.groq_api_key[-4:] if self.groq_api_key else 'NOT SET'}"
            return f"Groq  | model={self.model} | {key_status}"
        else:
            return f"Ollama | model={self.model} | host={self.ollama_host}"

    def chat(
        self,
        system_prompt: str,
        user_prompt: str,
        format: str = None,
        think: bool = False,
    ) -> str:
        if self.use_llm == "groq":
            return self._chat_groq(system_prompt, user_prompt, format)
        else:
            return self._chat_ollama(system_prompt, user_prompt, format, think)

    def _chat_groq(self, system_prompt: str, user_prompt: str, format: str = None) -> str:
        if not self.groq_api_key:
            raise ValueError("GROQ_API_KEY environment variable is not set or is empty.")

        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.groq_api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "temperature": 0.0
        }
        
        if format == "json":
            payload["response_format"] = {"type": "json_object"}

        try:
            response = requests.post(url, headers=headers, json=payload, timeout=30)

            if response.status_code == 401:
                raise RuntimeError(
                    "Groq API returned 401 Unauthorized.\n"
                    "Your GROQ_API_KEY is invalid or expired.\n"
                    "Get a fresh key at: https://console.groq.com/keys\n"
                    "Then update GROQ_API_KEY in your .env file."
                )

            response.raise_for_status()
            res_data = response.json()

            choices = res_data.get("choices", [])
            if not choices:
                raise RuntimeError("Empty choices returned from Groq API.")

            content = choices[0].get("message", {}).get("content", "").strip()
            if not content:
                raise RuntimeError("Groq API returned an empty message content.")

            return content
        except RuntimeError:
            raise
        except Exception as e:
            raise RuntimeError(
                f"Failed to communicate with Groq API (Model: {self.model}).\n"
                f"Error: {e}"
            ) from e

    def _chat_ollama(
        self,
        system_prompt: str,
        user_prompt: str,
        format: str = None,
        think: bool = False,
    ) -> str:
        try:
            response = self.ollama_client.chat(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                format=format,
                think=think,
                options={
                    "temperature": 0,
                },
            )

            if "message" not in response:
                raise RuntimeError("Invalid response received from Ollama.")

            content = response["message"].get("content", "").strip()
            if not content:
                raise RuntimeError("Ollama returned an empty response.")

            return content
        except Exception as e:
            raise RuntimeError(
                f"Failed to communicate with Ollama (Model: {self.model}).\n\n"
                "Please ensure:\n"
                "1. Ollama is running.\n"
                "2. The model is installed.\n"
                "3. The model name is correct.\n\n"
                f"Original Error: {e}"
            ) from e
