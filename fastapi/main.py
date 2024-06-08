from fastapi import FastAPI, HTTPException, Query
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
import os
import json
from components import *
from groq import Groq
#import replicate




def generate_image(text):
    input = {
        "width": 1920,
        "height": 1080,
        "prompt": text,
        "refine": "expert_ensemble_refiner",
        "apply_watermark": False,
        "num_inference_steps": 25
    }

    output = replicate.run(
        "stability-ai/sdxl:7762fd07cf82c948538e41f63f77d685e02b063e37e496e96eefd46c929f9bdc",
        input=input
    )
    print(output)
    return output[-1]






app = FastAPI()

load_dotenv()
api_key = os.getenv("STORY_API")

if api_key is None:
    raise ValueError("API key not found in environment variables")

client = Groq(api_key=api_key)

origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)










interaction = 0
message = []
options = []





@app.post("/themes")
def root(theme : str = Query(...)):
    global message, options, interaction
    interaction = 0
    message = []
    message.append({"role" : "user", "content" : f"generate me with{theme} of the story"})
    try:
        completion = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=start,
            temperature=1,
            max_tokens=1024,
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
        print(options)
        image_prompt = data['image_prompt']
        print("Image is being generated")
        # url = generate_image(image_prompt)

        return {"narration": narration, "question": question, "options": options, "image_prompt": image_prompt}
        # return {"narration": narration, "question": question, "options": options, "image_url": url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))




"""def try_again():
    global message, options
    message.pop()
    try:
        completion = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=message[-4:],
            temperature=1,
            max_tokens=1024,
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
    """




def end_story(option):
    global message, interaction
    print(interaction+1)
    interaction=0
    message.append({"role": "user", "content": option })
    try:
        completion = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=end+message[-4:],
            temperature=1,
            max_tokens=1024,
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
    global interaction, message
    interaction += 1
    if interaction >= 12:
        return end_story(option)
    
    message.append({"role" : "user", "content":option})
    print(interaction)
    try:
        completion = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=start+message[-4:],  # Use the last 4 messages to maintain context
            temperature=1,
            max_tokens=1024,
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
