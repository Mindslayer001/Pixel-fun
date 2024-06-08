from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
import json
from groq import Groq

app = FastAPI()

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
  "theme" : [
  {"choice":"Option 1 text"}
  {"choice":"Option 2 text"}
  {"choice":"Option 3 text"}
  {"choice":"Option 4 text"}
  ]
  "narration": "Story text here",
  "question": "Question text here",
  "options": [
    { "choice": "Option 1 text", "nextStory": "Continuation of the story based on option 1" },
    { "choice": "Option 2 text", "nextStory": "Continuation of the story based on option 2" },
    { "choice": "Option 3 text", "nextStory": "Continuation of the story based on option 3" },
    { "choice": "Option 4 text", "nextStory": "Continuation of the story based on option 4" }
  ],
  "image_prompt": "Text to generate the image"
}

Guidelines:

    Question: Frame a question based on the current scenario in the story.
    Options: Provide 4 different main points with minimal words as choices the main character can take at each key decision point, with each choice leading to a different continuation of the story.
    Next Story: Write a continuation of the story for each option.
    Image Prompt: Create a descriptive text that captures the scene in the story, which can be used to generate an AI image.
    Ending: The story should always end meaningfully between 19 to 25 responses from the user with a moral for children.
    Strict JSON Output: Return only the JSON output without any additional text or explanations.''',
    },
    {
        "role": "user",
        "content": "start",
    },
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
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

        narration = data['narration']
        question = data['question']
        options = data['options']
        image_prompt = data['image_prompt']

        return {"narration": narration, "question": question, "options": options, "image_prompt": image_prompt}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/options")
def set_option(option: str = Query(...)):
    message.append({"role": "user", "content": option})
    
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
        question = data['question']
        options = data['options']
        image_prompt = data['image_prompt']

        return {"narration": narration, "question": question, "options": options, "image_prompt": image_prompt}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
