import streamlit as st
from PIL import Image
import numpy as np
from io import BytesIO

st.set_page_config(page_title="Image Steganography", layout="centered")

# ------------------ Helper Functions ------------------

def text_to_binary(text):
    return ''.join(format(ord(i), '08b') for i in text)

def binary_to_text(binary):
    chars = [binary[i:i+8] for i in range(0, len(binary), 8)]
    text = ""
    for c in chars:
        if int(c, 2) == 0:
            break
        text += chr(int(c, 2))
    return text

def encode_image(image, secret_text):
    img = np.array(image)
    binary_text = text_to_binary(secret_text) + '00000000'
    idx = 0

    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            for k in range(3):
                if idx < len(binary_text):
                    img[i][j][k] = (img[i][j][k] & ~1) | int(binary_text[idx])
                    idx += 1
                else:
                    return Image.fromarray(img)
    return Image.fromarray(img)

def decode_image(image):
    img = np.array(image)
    binary_data = ""

    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            for k in range(3):
                binary_data += str(img[i][j][k] & 1)

    return binary_to_text(binary_data)

# ------------------ UI ------------------

st.title("🖼️ Image Steganography")
st.subheader("Data Hiding in Image")

option = st.radio("Choose Action", ["Encode", "Decode"])

uploaded_image = st.file_uploader(
    "Upload Image",
    type=["png", "jpg", "jpeg"]
)

if uploaded_image:
    image = Image.open(uploaded_image).convert("RGB")
    st.image(image, caption="Uploaded Image", width=450)

    if option == "Encode":
        secret = st.text_area("Enter secret message")

        if st.button("Encode Image"):
            if secret.strip() == "":
                st.error("Please enter a message to hide.")
            else:
                encoded_img = encode_image(image, secret)
                st.success("Message encoded successfully!")

                buf = BytesIO()
                encoded_img.save(buf, format="PNG")

                st.download_button(
                    label="Download Encoded Image",
                    data=buf.getvalue(),
                    file_name="encoded_image.png",
                    mime="image/png"
                )

    elif option == "Decode":
        if st.button("Decode Image"):
            message = decode_image(image)
            if message.strip() == "":
                st.warning("No hidden message found.")
            else:
                st.success("Hidden Message:")
                st.code(message)
