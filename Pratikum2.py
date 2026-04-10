import streamlit as st
from experta import *

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="Sistem Pakar COVID", layout="wide")

# =========================
# HEADER
# =========================
st.title("🦠 Sistem Pakar Diagnosa Penyakit Pernapasan")
st.caption("Forward Chaining menggunakan Experta")

# =========================
# GEJALA
# =========================
gejala = [
    "Apakah Anda mengalami demam?",
    "Apakah Anda mengalami batuk?",
    "Apakah Anda mengalami sesak napas?",
    "Apakah Anda mengalami pilek?",
    "Apakah Anda mengalami sakit tenggorokan?",
    "Apakah Anda kehilangan penciuman?",
]

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
    def _initial_action(self):
        for i, val in enumerate(st.session_state.jawaban):
            yield Fact(**{f"g{i}": val})

    # COVID
    @Rule(Fact(g0=True), Fact(g1=True), Fact(g2=True), Fact(g5=True))
    def covid(self):
        self.declare(Fact(hasil="COVID-19"))

    # Flu
    @Rule(Fact(g0=True), Fact(g1=True), Fact(g3=True))
    def flu(self):
        self.declare(Fact(hasil="Flu"))

    # Bronkitis
    @Rule(Fact(g1=True), Fact(g2=True))
    def bronkitis(self):
        self.declare(Fact(hasil="Bronkitis"))

# =========================
# UI
# =========================
col1, col2 = st.columns(2)

# INPUT
with col1:
    st.subheader("📝 Jawab Pertanyaan")

    for i, g in enumerate(gejala):
        val = st.toggle(g, key=f"g{i}")
        st.session_state.jawaban[i] = val

    proses = st.button("🚀 Diagnosa")
    
    if st.button("🔄 Reset"):
        st.session_state.clear()
        st.rerun()

# OUTPUT
with col2:
    st.subheader("📊 Hasil Diagnosa")

    if proses:
        if sum(st.session_state.jawaban) < 2:
            st.warning("⚠️ Pilih minimal 2 gejala!")
        else:
            engine = DiagnosaEngine()
            engine.reset()
            engine.run()

            hasil = []

            for fact in engine.facts.values():
                if isinstance(fact, Fact) and "hasil" in fact:
                    hasil.append(fact["hasil"])

            if hasil:
                for h in hasil:
                    st.error(f"🩺 Diagnosis: {h}")
            else:
                st.info("❓ Diagnosis tidak ditemukan")
