import streamlit as st
import qrcode
import qrcode.image.svg
from io import BytesIO
from PIL import Image
import cv2
import numpy as np
import tempfile

# Streamlit Page Configurations
st.set_page_config(page_title="QR Code Generator & Scanner", page_icon="🔗", layout="wide")

# Custom CSS for better UI
st.markdown(
    """
    <style>
        .stButton>button {background-color: #007BFF; color: white; border-radius: 10px; padding: 10px 20px;}
        .stTextInput>div>div>input {border-radius: 10px; padding: 10px; border: 1px solid #007BFF;}
        .stFileUploader>div>div>button {background-color: #28a745; color: white; border-radius: 10px;}
        .stDownloadButton>button {background-color: #dc3545; color: white; border-radius: 10px;}
    </style>
    """,
    unsafe_allow_html=True
)

# Function to generate QR code
def generate_qr(data):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill="black", back_color="white")
    return img

# Function to generate SVG QR Code
def generate_svg_qr(data):
    factory = qrcode.image.svg.SvgImage
    qr = qrcode.make(data, image_factory=factory)
    return qr

# Function to scan QR code from an image file
# def scan_qr_code(uploaded_file):
#     with tempfile.NamedTemporaryFile(delete=False) as temp:
#         temp.write(uploaded_file.getvalue())
#         temp_path = temp.name
    
#     image = cv2.imdecode(np.fromfile(temp_path, np.uint8), cv2.IMREAD_COLOR)
    
#     if image is None:
#         return "Error: Unable to read image. Please upload a valid QR Code image."

#     detector = cv2.QRCodeDetector()
#     data, _, _ = detector.detectAndDecode(image)
    
#     return data if data else "No valid QR Code found."

# Main UI Section
st.title("🔗 QR Code Generator & Scanner")
st.markdown("Generate & scan QR Codes easily with this modern tool!")

col1, col2 = st.columns([2, 1])

# QR Code Generator
with col1:
    st.subheader("🎨 Generate QR Code")
    link = st.text_input("🔗 Enter the URL or Text:")
    
    if st.button("Genrate Qr Code"):
        qr_img = generate_qr(link)
        buffer = BytesIO()
        qr_img.save(buffer, format="PNG")
        buffer.seek(0)
        st.image(buffer, caption="✅ Your QR Code", use_column_width=True)
        
        st.subheader("📥 Download Options")
        col_a, col_b, col_c, col_d = st.columns(4)
        with col_a:
            st.download_button("📸 PNG", buffer.getvalue(), file_name="qr_code.png", mime="image/png")
        with col_b:
            svg_qr = generate_svg_qr(link)
            buffer_svg = BytesIO()
            svg_qr.save(buffer_svg)
            buffer_svg.seek(0)
            st.download_button("🖼️ SVG", buffer_svg.getvalue(), file_name="qr_code.svg", mime="image/svg+xml")
        with col_c:
            buffer_jpeg = BytesIO()
            qr_img.save(buffer_jpeg, format="JPEG")
            buffer_jpeg.seek(0)
            st.download_button("📷 JPEG", buffer_jpeg.getvalue(), file_name="qr_code.jpeg", mime="image/jpeg")
        with col_d:
            buffer_pdf = BytesIO()
            qr_img.save(buffer_pdf, format="PNG")
            buffer_pdf.seek(0)
            st.download_button("📄 PDF", buffer_pdf.getvalue(), file_name="qr_code.pdf", mime="application/pdf")

# QR Code Scanner
# with col2:
#     st.subheader("📷 Scan QR Code")
#     uploaded_file = st.file_uploader("📂 Upload QR Code image:", type=["png", "jpg", "jpeg", "svg", "pdf"], help="Supported formats: PNG, JPEG, SVG, PDF")
#     if uploaded_file:
#         result = scan_qr_code(uploaded_file)
#         if result:
#             st.success(f"🔍 Scanned Data: {result}")
#         else:
#             st.error("⚠️ No valid QR Code found in the uploaded image.")

# Sidebar Feedback Section
st.sidebar.title("💬 Feedback & Rating")
if "feedback_list" not in st.session_state:
    st.session_state.feedback_list = []

username = st.sidebar.text_input("👤 Your Name:")
feedback = st.sidebar.text_area("✍️ Leave your feedback:")
rating = st.sidebar.slider("⭐ Rate this app:", 1, 5, 5)
if st.sidebar.button("✅ Submit Feedback"):
    if username and feedback:
        st.session_state.feedback_list.append({"name": username, "feedback": feedback, "rating": rating})
        st.sidebar.success("🎉 Thank you for your feedback!")
    else:
        st.sidebar.error("⚠️ Please enter your name and feedback before submitting.")

st.sidebar.subheader("📜 Feedback History")
if st.session_state.feedback_list:
    for fb in reversed(st.session_state.feedback_list):
        st.sidebar.write(f"**{fb['name']}** ⭐ {fb['rating']}/5")
        st.sidebar.write(f"_\"{fb['feedback']}\"_")
        st.sidebar.write("---")
    
    if st.sidebar.button("🗑️ Clear Feedback History"):
        st.session_state.feedback_list = []
        st.sidebar.success("✅ Feedback history cleared!")
else:
    st.sidebar.write("No feedback yet. Be the first to share your thoughts! 📝")

# Footer
st.markdown("---")
st.markdown("""
    <p style='text-align: center; color: gray;'>© 2025 QR Code Generator | Developed with ❤️ by Ayesha</p>
""", unsafe_allow_html=True)