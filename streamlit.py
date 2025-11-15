import streamlit as st
import requests
from collections import deque
from funcs import chapters, kitab, cleanText


# =============================
# === CACHE DENGAN PREFETCH ===
# =============================
class BibleCache:
    def __init__(self, max_cache=5):
        self.cache = deque(maxlen=max_cache)  # simpan tuple (book, chapter, content)
        self.current_index = 0  # posisi user dalam cache

    def get_cached(self, book, chapter):
        for b, c, content in self.cache:
            if b == book and c == chapter:
                return content
        return None

    def add_to_cache(self, book, chapter, content):
        # tambahkan ke cache kalau belum ada
        if not any(b == book and c == chapter for b, c, _ in self.cache):
            self.cache.append((book, chapter, content))

    def chapters_in_cache(self):
        return [c for _, c, _ in self.cache]


# ======================
# === FETCH DARI API ===
# ======================
def fetch_chapter(book, chapter, version):
    url = f"https://beeble.vercel.app/api/v1/passage/{book.lower()}/{chapter}?ver={version.lower()}"
    res = requests.get(url)
    if res.status_code == 200:
        data = res.json()
        return cleanText(data)
    else:
        return [f"⚠️ Gagal ambil pasal {chapter}."]


# =============================
# === SETUP STREAMLIT APP  ====
# =============================
st.title("📖 Real Bread: A Bible App (Smart Prefetch Cache)")

# session_state cache
if "bible_cache" not in st.session_state:
    st.session_state.bible_cache = BibleCache(max_cache=5)
if "current_chapter" not in st.session_state:
    st.session_state.current_chapter = 1

# Pilihan UI
col1, col2, col3, col4 = st.columns(4)
with col1:
    lang = st.selectbox("Bahasa:", ["English", "Indonesia"])
if lang == "English":
    with col2:
        version = st.selectbox("Versi:", ["NIV", "ESV", "NLT", "AMP"])
    with col3:
        book = st.selectbox("Kitab:", list(chapters.keys()))
    max_chapter = chapters[book]
else:
    with col2:
        version = st.selectbox("Versi:", ["TB", "FAYH", "AMD", "TSI"])
    with col3:
        book = st.selectbox("Kitab:", list(kitab.keys()))
    max_chapter = kitab[book]

with col4:
    st.session_state.current_chapter = st.number_input(
        "Pasal:", min_value=1, max_value=max_chapter, step=1, value=st.session_state.current_chapter
    )

chapter = st.session_state.current_chapter
cache = st.session_state.bible_cache


# =============================
# === PREFETCH STRATEGY =======
# =============================
def prefetch_window(book, center, version):
    """Ambil 3 pasal (center-1, center, center+1)"""
    for ch in [center - 1, center, center + 1]:
        if 1 <= ch <= max_chapter and cache.get_cached(book, ch) is None:
            content = fetch_chapter(book, ch, version)
            cache.add_to_cache(book, ch, content)


# Prefetch saat pertama load
prefetch_window(book, chapter, version)

# Tampilkan isi
content = cache.get_cached(book, chapter)
if content:
    st.markdown(f"## {book} {chapter}")
    for line in content:
        st.markdown(line.replace("\n", "<br/>"), unsafe_allow_html=True)
else:
    st.warning("Pasal belum tersedia di cache, ambil dari API...")
    content = fetch_chapter(book, chapter, version)
    cache.add_to_cache(book, chapter, content)

# Navigasi
col1, col2, col3 = st.columns(3)
with col1:
    if chapter > 1 and st.button("⬅ Sebelumnya"):
        st.session_state.current_chapter -= 1
        st.rerun()

with col3:
    if chapter < max_chapter and st.button("➡ Setelahnya"):
        st.session_state.current_chapter += 1
        st.rerun()

# Cache management: jika posisi sudah di ujung window
cache_chaps = cache.chapters_in_cache()
if len(cache_chaps) >= 5:
    if chapter == max(cache_chaps):  # di ujung kanan
        next_two = [chapter + 1, chapter + 2]
        for ch in next_two:
            if ch <= max_chapter and ch not in cache_chaps:
                content = fetch_chapter(book, ch, version)
                cache.add_to_cache(book, ch, content)
    elif chapter == min(cache_chaps):  # di ujung kiri
        prev_two = [chapter - 1, chapter - 2]
        for ch in reversed(prev_two):
            if ch >= 1 and ch not in cache_chaps:
                content = fetch_chapter(book, ch, version)
                cache.add_to_cache(book, ch, content)
