from fastapi import FastAPI, HTTPException, Query
from dotenv import load_dotenv
import os
import json

# Assuming you have the correct import for Groq client
from groq import Groq

load_dotenv()
api_key = os.getenv("STORY_API")

if api_key is None:
    raise ValueError("API key not found in environment variables")

client = Groq(api_key=api_key)

message = [
    {
        "role": "system",
        "content": '''Imagine you are a children's storybook author. Create an interactive story where the main character faces several key decision points. At each of these points, offer a set of possible actions the main character can take. I will choose an action from the provided options to continue the story. Additionally, for each scenario, provide a text prompt to generate an AI image to visualize the scene for the child.

Use the following JSON format for your output:

{
    "narration": "story text here",
    "options": ["option 1", "option 2"],
    "image_prompt": "text to generate the image"
}

Here’s an example output:

{
    "narration": "Once upon a time in a magical forest, a young fox named Finn found a mysterious map. The map hinted at a hidden treasure. As Finn followed the map, he arrived at a fork in the road.",
    "options": ["Follow the left path towards the dark forest", "Take the right path towards the sunny meadow", "Climb the hill to get a better view"],
    "image_prompt": "A young fox holding a map, standing at a fork in the road with one path leading to a dark forest and the other to a sunny meadow."
}

Guidelines:

Story: Write a short, engaging, and age-appropriate narrative for children.
Key Points: Introduce key decision points where the main character must choose between different actions.
Options: Provide 3 different actions the main character can take at each key decision point.
Image Prompt: Create a descriptive text that captures the scene in the story, which can be used to generate an AI image.
Ending: The story should end between 10 to 15 responses from the user. The story should always end with a moral for children.
Strict JSON Output: Return only the JSON output without any additional text or explanations.''',
    },
    {
        "role": "user",
        "content": "start",
    },
]

app = FastAPI()

@app.get("/")
def root():
    try:
        completion = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=message,
            temperature=1,
            max_tokens=1220,
            top_p=1,
            stream=False,
            response_format={"type": "json_object"},
            stop=None,
        )
        role = completion.choices[0].message.role
        content = completion.choices[0].message.content
        message.append({"role": role, "content": content})

        data = json.loads(content)

        narration = data['narration']
        options = data['options']
        image_prompt = data['image_prompt']

        return {"narration": narration, "options": options, "image_prompt": image_prompt}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/options")
def set_option(option: str = Query(...)):
    message.append({"role": "user", "content": option})
    print("\n\n your option is ", option)
    
    try:
        completion = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=message,
            temperature=1,
            max_tokens=1220,
            top_p=1,
            stream=False,
            response_format={"type": "json_object"},
            stop=None,
        )
        role = completion.choices[0].message.role
        content = completion.choices[0].message.content
        message.append({"role": role, "content": content})

        data = json.loads(content)

        narration = data['narration']
        options = data['options']
        image_prompt = data['image_prompt']

        print("\n\n\nRole is ", role)
        print("\n\n\n content is ", content)
        print("\n\n\n message is ", message)

        return {"narration": narration, "options": options, "image_prompt": image_prompt}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
