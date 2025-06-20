import streamlit as st
import json
from google.oauth2 import service_account
import vertexai
from vertexai.vision_models import ImageGenerationModel
from PIL import Image as PILImage
from io import BytesIO

# Secure credentials loading
gcp_secrets = st.secrets["gcp"]
credentials_dict = json.loads(gcp_secrets["credentials"])
credentials = service_account.Credentials.from_service_account_info(credentials_dict)

vertexai.init(
    project=gcp_secrets["project_id"],
    location="us-central1",
    credentials=credentials
)

model = ImageGenerationModel.from_pretrained("imagegeneration@006")

def generate_image(prompt: str, style: str = "photorealistic", number_of_images: int = 1) -> list[PILImage.Image]:
    try:
        response = model.generate_images(
            prompt=f"{prompt}, in {style} style",
            number_of_images=number_of_images
        )
        return [PILImage.open(BytesIO(img._image_bytes)) for img in response]
    except Exception as e:
        st.error(f"Image generation failed: {e}")
        return []
