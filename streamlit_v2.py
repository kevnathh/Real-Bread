import streamlit as st
import requests
from funcs import chapters, kitab, cleanText

st.title("Real Bread: A Bible App")

if 'lang' not in st.session_state:
    st.session_state.lang = 'Indonesia'
if 'version' not in st.session_state:
    st.session_state.version = 'TB'
if 'book' not in st.session_state:
    st.session_state.book = 'Kejadian'
if 'chapter' not in st.session_state:
    st.session_state.chapter = 1

col1, col2, col3, col4 = st.columns(4)
with col1:
    lang = st.selectbox("Bahasa:", ["English", "Indonesia"], index=["English", "Indonesia"].index(st.session_state.lang))
if lang == 'English':
    with col2: version = st.selectbox("Versi:", ["NIV", "ESV", "NLT", "AMP"])
    with col3: book = st.selectbox("Kitab:", [x for x in chapters], index=list(chapters.keys()).index(st.session_state.book))
    with col4: chapter = st.selectbox("Pasal:", [x for x in range(1, chapters[book] + 1)], index=st.session_state.chapter - 1)
else:
    with col2: version = st.selectbox("Versi:", ["TB", "FAYH", "AMD", "TSI"])
    with col3: book = st.selectbox("Kitab:", [x for x in kitab], index=list(kitab.keys()).index(st.session_state.book))
    with col4: chapter = st.selectbox("Pasal:", [x for x in range(1, kitab[book] + 1)], index=st.session_state.chapter - 1)

if lang != st.session_state.lang:
    st.session_state.lang = lang
if version != st.session_state.version:
    st.session_state.version = version
if book != st.session_state.book:
    st.session_state.book = book
    st.session_state.chapter = 1
if chapter != st.session_state.chapter:
    st.session_state.chapter = chapter

try:
    def getChapter(book, chapter, version):
        bookREQ = requests.get(f'https://beeble.vercel.app/api/v1/passage/{book.lower()}/{chapter}?ver={version.lower()}')
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
                    else: st.write(i)

except Exception as e:
    st.error(e)

getChapter(st.session_state.book, st.session_state.chapter, st.session_state.version)

col1, col2, col3 = st.columns(3)
with col1:
    if chapter > 1 and st.button("⬅ Sebelumnya"):
        st.session_state.chapter -= 1
        st.rerun()
with col2:
    st.write(st.session_state)
with col3:
    max_chapter = chapters[book] if lang == "English" else kitab[book]
    if chapter < max_chapter and st.button("➡ Setelahnya"):
        st.session_state.chapter += 1
        st.rerun()