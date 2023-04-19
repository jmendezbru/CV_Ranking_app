import streamlit as st
import pdfplumber
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

st.title("Ranking de candidatos para un trabajo")
st.subheader("Aplicación NLP")
st.caption("La idea es matchear un curriculum con una descripción de trabajo y calcular una distancia entre ambos")

uploadedJD = st.file_uploader("Descripción de trabajo", type="pdf")

uploadedResumes = st.file_uploader("CVs", type="pdf", accept_multiple_files=True)

click = st.button("Procesar")

def getResult(JD_txt, resume_txt):
    content = [JD_txt, resume_txt]
    cv = CountVectorizer()
    matrix = cv.fit_transform(content)
    similarity_matrix = cosine_similarity(matrix)
    match = similarity_matrix[0][1] * 100
    return match

try:
    global job_description
    with pdfplumber.open(uploadedJD) as pdf:
        pages = pdf.pages[0]
        job_description = pages.extract_text()
except:
    st.write("")

results = []

if click:
    if uploadedResumes:
        for i, uploadedResume in enumerate(uploadedResumes):
            try:
                with pdfplumber.open(uploadedResume) as pdf:
                    pages = pdf.pages[0]
                    resume = pages.extract_text()
                match = getResult(job_description, resume)
                match = round(match, 2)
                file_name = uploadedResume.name
                results.append(f"{file_name} - Match Percentage: {match}%")
            except:
                file_name = uploadedResume.name
                results.append(f"{file_name} - Error occurred during processing")
    else:
        st.write("No se han subido archivos de CV")

    # Display results
    st.write("Resultados:")
    for result in results:
        st.write(result)
