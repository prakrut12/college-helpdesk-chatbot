import os
import google.generativeai as genai

# Configure your Google API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# List all available models
models = genai.list_models()

print("Available models for your API key:\n")
for m in models:
    # 'name' is the model ID; 'capabilities' lists supported features
    print("Model Name:", m.name)
    if hasattr(m, "capabilities"):
        print("Capabilities:", m.capabilities)
    print("-" * 40)
