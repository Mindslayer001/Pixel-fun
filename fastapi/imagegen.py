from fastapi import FastAPI, HTTPException, Query
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
import os
import replicate
import json

# Load environment variables from .env file
load_dotenv()

# Initialize FastAPI app
app = FastAPI()

# Set allowed origins for CORS
origins = [
    "http://localhost",
    "http://localhost:3000",
]

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

@app.post('/texts')
def imgGen(text: str = Query(...)):
    input = {
        "width": 768,
        "height": 768,
        "prompt": text,
        "refine": "expert_ensemble_refiner",
        "apply_watermark": False,
        "num_inference_steps": 25
    }
    
    try:
        # Call the replicate API
        output = replicate.run(
            "stability-ai/sdxl:7762fd07cf82c948538e41f63f77d685e02b063e37e496e96eefd46c929f9bdc",
            input=input
        )
        return {"image_url": output[0]}
    except Exception as e:
        # Handle exceptions
        raise HTTPException(status_code=500, detail=str(e))

# Make sure to set REPLICATE_API_TOKEN in your .env file
os.environ["REPLICATE_API_TOKEN"] = os.getenv("REPLICATE_API_TOKEN")