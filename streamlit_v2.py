import streamlit as st
import requests
from funcs import bible_chapters, cleanText

st.title("Real Bread: A Bible App")

lang = st.selectbox("Pilih bahasa:", ["English", "Indonesia"])
if lang == 'English':
    version = st.selectbox("Pilih versi:", ["NIV", "ESV", "NLT", "AMP"])
else:
    version = st.selectbox("Pilih versi:", ["TB", "FAYH", "AMD", "TSI"])
book = st.selectbox("Pilih kitab:", [x for x in bible_chapters])
chapter = st.selectbox("Pilih pasal:", [x for x in range(1, bible_chapters[book]+1)])

bookREQ = requests.get(f'https://beeble.vercel.app/api/v1/passage/{book.lower()}/{chapter}?ver={version.lower()}')

try:
    if bookREQ.status_code != 200:
        st.error('Gagal ambil')
    else:
        data = bookREQ.json()
        hasil = cleanText(data)
        if len(hasil) == 0:
            st.error('Tidak ada di versi ini')
        else:
            st.write(f'## {book} {chapter}: 1-{len([x for x in hasil if x[1] != '0'])}')
            for i in hasil:
                if i[1] == '0':
                    st.write(f'###{i[3:]}')
                else: i

            col1, col2 = st.columns(2)
            with col1:
                with st.button('Sebelumnya'):
                    chapter -= 1
            with col2:
                with st.button('Setelahnya'):
                    chapter += 1
                

        data
except Exception as e:
    st.error(e)
