from django.shortcuts import render
from dotenv import load_dotenv
import os
from groq import Groq
load_dotenv()
api_key = os.getenv("STORY_API")

def story(request): 
    message = [
            {
                "role": "system",
                "content": '"Imagine you are a children\'s storybook author. Create an interactive story where the main character faces several key decision points. At each of these points, offer a set of possible actions the main character can take. I will choose an action from the provided options to continue the story. Additionally, for each scenario, provide a text prompt to generate an AI image to visualize the scene for the child.\n\nUse the following JSON format for your output:\n\njson\n\n{\n    "narration": "story text here",\n    "options": ["option 1", "option 2", "option 3"],\n    "image_prompt": "text to generate the image"\n}\n\nHere’s an example output:\n\njson\n\n{\n    "narration": "Once upon a time in a magical forest, a young fox named Finn found a mysterious map. The map hinted at a hidden treasure. As Finn followed the map, he arrived at a fork in the road.",\n    "options": ["Follow the left path towards the dark forest", "Take the right path towards the sunny meadow", "Climb the hill to get a better view"],\n    "image_prompt": "A young fox holding a map, standing at a fork in the road with one path leading to a dark forest and the other to a sunny meadow."\n}\n\nGuidelines:\n\n    Story: Write a short, engaging, and age-appropriate narrative for children.\n    Key Points: Introduce key decision points where the main character must choose between different actions.\n    Options: Provide 3 different actions the main character can take at each key decision point.\n    Image Prompt: Create a descriptive text that captures the scene in the story, which can be used to generate an AI image.\nStrict JSON Output: Return only the JSON output without any additional text or explanations.',
            },
            {"role": "user", "content": "start"},
        ]

    client = Groq(api_key=api_key)
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
    print("\n\n\nRole is ", role)
    print("\n\n\n content is ", content)
    message.append({"role": role, "content": content})
    reply = input("enter ur reply:")
    print("\n\n your reply is ", reply)
    message.append({"role": "user", "content": reply})
    print("\n\n\n message is ", message)

