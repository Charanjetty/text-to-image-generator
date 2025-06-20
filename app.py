import streamlit as st
from utils.imagen import generate_image
from utils.gemini import enhance_prompt
from utils.style_presets import STYLE_PRESETS
from io import BytesIO

# Setup
st.set_page_config("Charan's AI Art Generator 🎨", page_icon="🎨")
st.title("🎨 Charan Jetty's AI Art Generator")
st.caption("Powered by Gemini + Imagen · Built with ❤️ by Charan")

# Prompt input
prompt = st.text_input("🖋 Describe your vision:", placeholder="e.g., A city in the sky with floating whales")
use_enhancer = st.checkbox("✨ Enhance prompt using Gemini 2.5 Pro", value=True)
num_images = st.slider("🖼️ Number of images to generate", 1, 4, 1)

# Art style selection (label-only)
style_key = st.selectbox(
    "🎨 Choose an art style:",
    options=list(STYLE_PRESETS.keys()),
    format_func=lambda x: STYLE_PRESETS[x]["label"]
)
st.divider()

# Generate button
if st.button("🎨 Generate Art"):
    if not prompt:
        st.warning("Please enter a prompt to generate art.")
    else:
        with st.spinner("Generating your masterpiece..."):
            final_prompt = enhance_prompt(prompt, STYLE_PRESETS[style_key]["preset"]) if use_enhancer else prompt
            images = generate_image(final_prompt, STYLE_PRESETS[style_key]["preset"], num_images)

        if images:
            st.success("✅ Here are your creations!")
            for idx, img in enumerate(images):
                st.image(img, use_container_width=True)
                st.download_button(
                    label=f"💾 Download Image {idx+1}",
                    data=BytesIO(img.tobytes()),
                    file_name=f"charan_art_{idx+1}.png",
                    mime="image/png"
                )
        else:
            st.error("❌ Image generation failed. Please try a different prompt or style.")
