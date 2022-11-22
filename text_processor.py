import streamlit as st
import fitz
import PIL.Image
import pytesseract
import io 
import pdf2image
import easyocr

def scannedPdfConverter(file_path, save_path):
    ocrmypdf.ocr(file_path, save_path, skip_text=True)
    print('File converted successfully!')

file = st.file_uploader("Upload a file")
def text_processor(file):
	if file is not None:
		file_data = file.read()
		if file.name.endswith(".txt"):
			text = file.read().decode("utf-8")
			return text
		if file.name.endswith(".pdf"):
			doc = fitz.open(stream=file_data, filetype="pdf")
			text = ""
			for page in doc:
				text += page.get_text()
			if text != "":
				return text
		if file.name.endswith(".pdf"):
			images = pdf2image.convert_from_bytes(file_data,dpi=300)
			reader = easyocr.Reader(['en','sk'],gpu=True)
			for page in images:
				text = reader.readtext(np.array(page))
				st.image(page, use_column_width=True)
				st.write(text)
			images = scannedPdfConverter(file.read(), "converted.pdf")
			return images
		if file.name.endswith(".jpg"):
			image = PIL.Image.open(io.BytesIO(file_data))
			return image
		if file.name.endswith(".png"):
			image = PIL.Image.open(io.BytesIO(file_data))
			return image
		if file.name.endswith(".jpeg"):
			image = PIL.Image.open(io.BytesIO(file_data))
			return image
		if file.name.endswith(".jpg"):
			image = PIL.Image.open(io.BytesIO(file_data))
			return image

st.write(text_processor(file))

	



	