import os

# Single place to change the model for every agent. gemini-1.5-flash is retired.
GEMINI_MODEL = os.environ.get("GEMINI_MODEL", "gemini-3.6-flash")
