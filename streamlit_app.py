import streamlit as st
import fitz  # PyMuPDF
from PIL import Image
from io import BytesIO

# PDF 페이지를 JPG로 변환하는 함수
def pdf_to_images(pdf_file):
    # PyMuPDF를 사용하여 PDF 문서 열기
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    images = []
    
    # 각 페이지를 이미지로 변환
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        pix = page.get_pixmap()  # 페이지를 이미지로 렌더링
        img = Image.open(BytesIO(pix.tobytes("png")))  # PIL 이미지로 변환
        images.append(img)
    
    return images

# Streamlit 앱 인터페이스
st.title("PDF to JPG Converter")

# 파일 업로드 위젯
uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")

if uploaded_file is not None:
    # PDF 파일을 이미지로 변환
    images = pdf_to_images(uploaded_file)

    st.write(f"Found {len(images)} pages in the PDF.")

    # 각 페이지를 화면에 표시
    for i, img in enumerate(images):
        st.write(f"Page {i+1}")
        st.image(img)

    # 다운로드 가능한 Zip 파일 생성
    if st.button("Download all as JPG"):
        # 이미지들을 BytesIO에 저장하여 다운로드 링크 제공
        zip_buffer = BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w') as zf:
            for i, img in enumerate(images):
                img_buffer = BytesIO()
                img.save(img_buffer, format="JPEG")
                zf.writestr(f"page_{i+1}.jpg", img_buffer.getvalue())
        
        zip_buffer.seek(0)
        st.download_button(
            label="Download Zip",
            data=zip_buffer,
            file_name="images.zip",
            mime="application/zip"
        )
