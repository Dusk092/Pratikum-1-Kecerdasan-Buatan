# =========================
# FIX EXPERTA
# =========================
import collections
import collections.abc
collections.Mapping = collections.abc.Mapping

from experta import *
import streamlit as st

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="Sistem Pakar COVID", layout="wide")

# =========================
# HEADER
# =========================
st.markdown("""
<h1 style='text-align: center;'>🦠 Sistem Pakar Diagnosa Penyakit Pernapasan</h1>
<p style='text-align: center; color: gray;'>Forward Chaining menggunakan Experta</p>
""", unsafe_allow_html=True)

st.divider()

# =========================
# GEJALA LENGKAP
# =========================
gejala = [
    "Apakah Anda mengalami demam?",
    "Apakah Anda mengalami batuk?",
    "Apakah Anda mengalami sesak napas?",
    "Apakah Anda mengalami pilek?",
    "Apakah Anda mengalami sakit tenggorokan?",
    "Apakah Anda kehilangan penciuman?",
    "Apakah Anda kehilangan rasa?",
    "Apakah Anda mengalami sakit kepala?",
    "Apakah Anda merasa lemas?",
    "Apakah Anda mengalami nyeri otot?",
    "Apakah Anda menggigil?",
    "Apakah Anda mengalami hidung tersumbat?",
    "Apakah Anda bersin-bersin?",
    "Apakah Anda mengalami batuk berdahak?",
    "Apakah Anda merasa dada terasa berat?"
]

# =========================
# SARAN
# =========================
saran = {
    "COVID-19": "Isolasi mandiri dan periksa ke fasilitas kesehatan.",
    "Flu": "Istirahat, minum air hangat, dan konsumsi vitamin.",
    "Bronkitis": "Hindari asap dan konsultasi ke dokter."
}

# =========================
# STATE
# =========================
if "jawaban" not in st.session_state:
    st.session_state.jawaban = [False] * len(gejala)

# =========================
# EXPERTA ENGINE
# =========================
class DiagnosaEngine(KnowledgeEngine):

    @DefFacts()
    def fakta_awal(self):
        for i, val in enumerate(st.session_state.jawaban):
            yield Fact(**{f"g{i}": val})

    # =========================
    # RULE COVID (GEJALA KUAT)
    # =========================
    @Rule(Fact(g0=True), Fact(g1=True), Fact(g2=True),
          Fact(g5=True), Fact(g6=True))
    def covid(self):
        self.declare(Fact(hasil="COVID-19"))

    # =========================
    # RULE FLU
    # =========================
    @Rule(Fact(g0=True), Fact(g1=True), Fact(g3=True),
          Fact(g4=True), Fact(g11=True))
    def flu(self):
        self.declare(Fact(hasil="Flu"))

    # =========================
    # RULE BRONKITIS
    # =========================
    @Rule(Fact(g1=True), Fact(g2=True),
          Fact(g13=True), Fact(g14=True))
    def bronkitis(self):
        self.declare(Fact(hasil="Bronkitis"))

# =========================
# LAYOUT
# =========================
col1, col2 = st.columns(2)

# =========================
# INPUT
# =========================
with col1:
    st.subheader("📝 Jawab Pertanyaan")

    total = 0

    for i, g in enumerate(gejala):
        val = st.toggle(g, key=f"g{i}")
        st.session_state.jawaban[i] = val
        if val:
            total += 1

    st.progress(total / len(gejala))
    st.caption(f"{total} dari {len(gejala)} gejala dipilih")

    col_btn1, col_btn2 = st.columns(2)

    with col_btn1:
        proses = st.button("🚀 Diagnosa", use_container_width=True)

    with col_btn2:
        if st.button("🔄 Reset", use_container_width=True):
            st.session_state.clear()
            st.rerun()

# =========================
# OUTPUT
# =========================
with col2:
    st.subheader("📊 Hasil Diagnosa")

    if proses:

        if total < 2:
            st.warning("⚠️ Pilih minimal 2 gejala terlebih dahulu!")
        else:
            engine = DiagnosaEngine()
            engine.reset()
            engine.run()

            hasil = []

            for fact in engine.facts.values():
                if isinstance(fact, Fact) and "hasil" in fact:
                    hasil.append(fact["hasil"])

            if hasil:
                for h in set(hasil):
                    st.error(f"🩺 Diagnosis: {h}")
                    st.success(f"💡 Saran: {saran[h]}")
            else:
                st.info("❓ Diagnosis tidak ditemukan")
