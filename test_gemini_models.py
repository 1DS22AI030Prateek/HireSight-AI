import google.generativeai as genai

# Replace with your actual Gemini API key
genai.configure(api_key="AIzaSyCLpNVsM1mFcYbHciagz5xtkWAS4XqBSs0")

try:
    models = genai.list_models()
    print("✅ Available Gemini Models:\n")
    for m in models:
        print(m.name)
except Exception as e:
    print("❌ Error fetching models:")
    print(e)
