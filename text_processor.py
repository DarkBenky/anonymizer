import streamlit as st
import PyPDF2
import PIL.Image
import numpy as np
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
			pdf = PyPDF2.PdfFileReader(io.BytesIO(file_data))
			pages = pdf.getNumPages()
			text = ""
			for page in range(pages):
				text += pdf.getPage(page).extractText()
			if text != "":
				return text
		if file.name.endswith(".pdf"):
			images = pdf2image.convert_from_bytes(file_data,dpi=300)
			reader = easyocr.Reader(['en','sk'],gpu=True)
			for page in images:
				text = reader.readtext(np.array(page),detail=0)
				st.image(page, use_column_width=True)
				st.write(text)
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

	



	