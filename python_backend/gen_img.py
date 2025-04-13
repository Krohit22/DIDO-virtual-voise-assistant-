import datetime
import os
from dotenv import load_dotenv
from gradio_client import Client
from PIL import Image

def main():
    load_dotenv()
    os.environ['FLUX'] = os.getenv('FLUX', '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')

    output_dir = "generated_images"
    os.makedirs(output_dir, exist_ok=True)

    client = Client("black-forest-labs/FLUX.1-schnell")

    result = client.predict(
        prompt="babies swimming in the lake at sunset, realistic style",
        seed=42,
        randomize_seed=False,
        width=1024,
        height=1024,
        num_inference_steps=20,
        api_name="/infer"
    )

    temp_image_path, used_seed = result

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"image_{timestamp}_seed{used_seed}.png"
    save_path = os.path.join(output_dir, filename)

    with Image.open(temp_image_path) as img:
        img.save(save_path)

    print(f"Image successfully saved to: {save_path}")
    print(f"Used seed: {used_seed}")

if __name__ == "__main__":
    main()