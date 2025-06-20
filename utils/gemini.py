
from vertexai.generative_models import GenerativeModel

gemini = GenerativeModel("gemini-2.5-pro")

def enhance_prompt(prompt: str, style: str) -> str:
    return f"{prompt}, in {style} style"