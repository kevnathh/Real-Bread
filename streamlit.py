import streamlit as st
import requests
from funcs import bible_chapters, cleanText

st.title("📖 Bible App by Kelompok StrukDat")

# --- Select Bible version and book ---
version = st.selectbox("Pilih versi:", ["ASV", "KJV"])
book = st.selectbox("Pilih kitab:", ["Matthew", "Mark", "Luke", "John"])
chapter = st.selectbox("Pilih pasal:", [x for x in range(1, bible_chapters[book]+1)])

bookREQ = requests.get(f'https://cdn.jsdelivr.net/gh/wldeh/bible-api/bibles/en-{version.lower()}/books/{book.lower()}/chapters/{chapter}.json')

try:
    if bookREQ.status_code != 200:
        st.error('Gagal ambil')
    else:
        data = bookREQ.json()
        hasil = cleanText(data)
        for i in hasil: i
except requests.exceptions.RequestException as e:
    st.error(f"Gagal ambil: {e}")
