from fastapi import FastAPI, HTTPException, Query
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
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

json

{
  "question": "Question text here",
  "options": [
    { "choice": "Option 1 text", "nextStory": "Continuation of the story based on option 1" },
    { "choice": "Option 2 text", "nextStory": "Continuation of the story based on option 2" },
    { "choice": "Option 3 text", "nextStory": "Continuation of the story based on option 3" },
    { "choice": "Option 4 text", "nextStory": "Continuation of the story based on option 4" }
  ],
  "image_prompt": "Text to generate the image"
}

Here’s an example output:

json

{
  "question": "What was the knight seeking?",
  "options": [
    { "choice": "A magical sword", "nextStory": "The knight discovered the ancient sword hidden deep within the enchanted forest." },
    { "choice": "A legendary treasure", "nextStory": "The knight embarked on a perilous journey to uncover the mythical treasure of the ancient kings." },
    { "choice": "A dragon to slay", "nextStory": "The knight faced the mighty dragon in a fierce battle to protect the kingdom from its wrath." },
    { "choice": "A lost kingdom", "nextStory": "The knight ventured into the unknown, seeking the lost kingdom of his ancestors." }
  ],
  "image_prompt": "A brave knight in shining armor, standing at the edge of an enchanted forest, holding a map with various paths leading to different adventures."
}

Guidelines:

    Question: Frame a question based on the current scenario in the story.
    Options: Provide 4 different main points with minimal words as choices the main character can take at each key decision point, with each choice leading to a different continuation of the story.
    Next Story: Write a continuation of the story for each option.
    Image Prompt: Create a descriptive text that captures the scene in the story, which can be used to generate an AI image.
    Ending: The story should always end meaningfully between 19 to 25 responses from the userwith a moral for children.  
    Strict JSON Output: Return only the JSON output without any additional text or explanations.''',
    },
    {
        "role": "user",
        "content": "start",
    },
]

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",  # Add the URL where your React app is hosted
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)


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

        narration = data['question']
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

        narration = data['question']
        options = data['options']
        image_prompt = data['image_prompt']

        print("\n\n\nRole is ", role)
        print("\n\n\n content is ", content)
        print("\n\n\n message is ", message)

        return {"narration": narration, "options": options, "image_prompt": image_prompt}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
