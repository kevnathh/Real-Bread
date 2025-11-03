import streamlit as st
import requests
from funcs import bible_chapters, cleanText

st.title("Real Bread: A Bible App")

lang = st.selectbox("Pilih bahasa:", ["English", "Indonesia"])
version = st.selectbox("Pilih versi:", ["ASV", "KJV"])
book = st.selectbox("Pilih kitab:", [x for x in bible_chapters])
chapter = st.selectbox("Pilih pasal:", [x for x in range(1, bible_chapters[book]+1)])

bookREQ = requests.get(f'https://cdn.jsdelivr.net/gh/wldeh/bible-api/bibles/en-{version.lower()}/books/{book.lower()}/chapters/{chapter}.json')

try:
    if bookREQ.status_code != 200:
        st.error('Gagal ambil')
    else:
        data = bookREQ.json()
        hasil = cleanText(data)
        for i in hasil: i

        data
except Exception as e:
    st.error(e)
