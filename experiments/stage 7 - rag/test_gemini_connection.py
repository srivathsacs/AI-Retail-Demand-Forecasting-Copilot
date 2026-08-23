from dotenv import load_dotenv
from google import genai
import os

# Load environment variables
load_dotenv()

# Read API key
api_key = os.getenv("GOOGLE_API_KEY")

# Create Gemini client
client = genai.Client(api_key=api_key)

# Send prompt
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Hello Gemini"
)

# Print response
print(response.text)