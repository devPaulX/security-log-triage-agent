import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("GEMINI_API_KEY") )  # type: ignore

for model in genai.list_models(): # type: ignore
    print(model.name, "→", model.supported_generation_methods)