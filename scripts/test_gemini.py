import os
import google.generativeai as genai

API_KEY = os.getenv("GEMINI_API_KEY") or # or GEMINI_API_KEY if you prefer
genai.configure(api_key=API_KEY)  # type: ignore

# Use a supported model from list_models output
model = genai.GenerativeModel("models/gemini-2.5-pro")  # or "models/gemini-flash-latest" # type: ignore

response = model.generate_content("Explain why multiple failed admin logins are suspicious.")
print(response.text.strip())
