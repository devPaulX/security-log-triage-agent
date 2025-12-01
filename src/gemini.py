# Configure Gemini with your API key
import os
import google.generativeai as genai


api_key = os.getenv("GOOGLE_API_KEY")  # or GEMINI_API_KEY if you prefer
genai.configure(api_key=api_key) # type: ignore


# Create a model instance
model = genai.GenerativeModel("models/gemini-2.5-flash")  # type: ignore

def explain_incident(incident) -> str:
    """
    Use Gemini to generate a natural-language explanation for an incident.
    """
    prompt = (
        f"Explain why this incident is risky:\n"
        f"Action={incident.action}, User={incident.user}, "
        f"IP={incident.ip}, Count={incident.count}, Severity={incident.severity}"
    )
    response = model.generate_content(prompt)
    return response.text.strip()
