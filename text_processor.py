import streamlit as st
import fitz
import PIL.Image
import pytesseract
import io 
import pdf2image
import easyocr

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
			for page in images:
				st.image(page, use_column_width=True)
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

def ocr_img(img):
	ocr = easyocr.Reader(['sk'])
	result = ocr.readtext(img)
	return result
	


res = text_processor(file)
if res is not None:
	text = ocr_img(res)
	st.write(text)


	