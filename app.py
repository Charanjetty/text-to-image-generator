import streamlit as st
from utils.imagen import generate_image
from utils.gemini import enhance_prompt
from utils.style_presets import STYLE_PRESETS
from io import BytesIO
from PIL import Image

# Page setup
st.set_page_config("Charan's AI Art Generator 🎨", page_icon="🎨")
st.title("🎨 Charan Jetty's AI Art Generator")
st.caption("Powered by Gemini + Imagen · Built with ❤️ by Charan")

# Prompt input
prompt = st.text_input("🖋 Describe your vision:", placeholder="e.g., A futuristic city in Studio Ghibli style")
use_enhancer = st.checkbox("✨ Enhance prompt using Gemini 2.5 Pro", value=True)
num_images = st.slider("🖼️ Number of images to generate", 1, 4, 1)

# Style picker
st.markdown("🎨 **Choose an art style:**")
style_key = st.radio("", list(STYLE_PRESETS.keys()), label_visibility="collapsed", horizontal=True)
cols = st.columns(len(STYLE_PRESETS))

for i, key in enumerate(STYLE_PRESETS):
    with cols[i]:
        st.image(STYLE_PRESETS[key]["preview"], width=80)
        st.caption(STYLE_PRESETS[key]["label"])

st.divider()

# Generate button
if st.button("🎨 Generate Art"):
    if not prompt:
        st.warning("Please enter a prompt to generate art.")
    else:
        with st.spinner("Generating your masterpiece..."):
            style = STYLE_PRESETS[style_key]["preset"]
            final_prompt = enhance_prompt(prompt, style) if use_enhancer else f"{prompt}, {style}"
            images = generate_image(final_prompt, style, num_images)

        if images:
            st.success("✅ Here are your creations!")
            for i, img in enumerate(images):
                st.image(img, use_container_width=True)
                st.download_button(
                    label=f"💾 Download Image {i+1}",
                    data=BytesIO(img.tobytes()),
                    file_name=f"charan_art_{i+1}.png",
                    mime="image/png"
                )
        else:
            st.error("❌ Image generation failed. Please try again.")
