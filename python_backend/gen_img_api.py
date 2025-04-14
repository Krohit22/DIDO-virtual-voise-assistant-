import datetime
import os
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from gradio_client import Client
from PIL import Image
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Load environment variables
load_dotenv()
os.environ['FLUX'] = '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'

# Serve static files
app.mount("/generated_images", StaticFiles(directory="generated_images"), name="generated_images")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic model for request
class ImageRequest(BaseModel):
    prompt: str = ""
    width: int = 1024
    height: int = 720
    steps: int = 20

@app.post("/generate-poster")
async def generate_poster(request: ImageRequest):
    try:
        output_dir = "generated_images"
        os.makedirs(output_dir, exist_ok=True)

        client = Client("black-forest-labs/FLUX.1-schnell")

        # Using fixed seed (42) with randomize_seed=False
        result = client.predict(
            prompt=request.prompt,
            seed=42,  # Fixed seed value
            randomize_seed=False,  # Always disable randomization
            width=request.width,
            height=request.height,
            num_inference_steps=request.steps,
            api_name="/infer"
        )

        temp_image_path, _ = result  # Ignoring the returned seed since we're using fixed seed

        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"ben10_poster_{timestamp}.png"
        save_path = os.path.join(output_dir, filename)

        with Image.open(temp_image_path) as img:
            img.save(save_path)

        return {
            "image_url": f"/generated_images/{filename}",
            "prompt": request.prompt
        }

    except Exception as e:
        error_msg = str(e)
        if 'exceeded your GPU quota' in error_msg:
            raise HTTPException(
                status_code=402, 
                detail={
                    "error": "quota_exceeded",
                    "message": "You need to purchase Dido Premium for further use", 
                }
            )
        else:
            logger.error(f"Generation failed: {error_msg}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={
                    "error": "generation_failed",
                    "message": error_msg
                }
            )

@app.get("/")
async def health_check():
    return {"status": "ready", "service": "Ben 10 Poster Generator"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)