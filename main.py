from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPEN_API_KEY"))

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", 
         "content": """Du bist ein KI-Tutor, der formatives Feedback zu argumentativem Schreiben geben soll. 
         Das Ziel ist es, dem Lernenden zu helfen, ihre Prägnanz, Logik und Überzeugungskraft zu verbessern. Gebe stets 
         umsetzbare, klare und ermutigende Ratschläge
         """}
    ],
    response_format={"type": "json_object"}
)

print(response.choices[0].message.content)