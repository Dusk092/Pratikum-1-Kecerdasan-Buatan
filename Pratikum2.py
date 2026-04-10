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
st.set_page_config(page_title="Hybrid Sistem Pakar", layout="wide")

# =========================
# HEADER
# =========================
st.markdown("""
<h1 style='text-align: center;'>🧠 Hybrid Sistem Pakar Diagnosa Penyakit</h1>
<p style='text-align: center; color: gray;'>Experta + Forward Chaining + Persentase</p>
""", unsafe_allow_html=True)

st.divider()

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
# RULE MANUAL (PERSEN)
# =========================
rules_manual = {
    "COVID-19": {0:2,1:2,2:3,5:3,6:3,8:2},
    "Flu": {0:2,1:2,3:2,4:2,11:1,12:1},
    "Bronkitis": {1:2,2:3,13:2,14:2}
}

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
    st.session_state.jawaban = [False]*len(gejala)

# =========================
# EXPERTA ENGINE
# =========================
class DiagnosaEngine(KnowledgeEngine):

    @DefFacts()
    def fakta(self):
        for i, val in enumerate(st.session_state.jawaban):
            yield Fact(**{f"g{i}": val})

    @Rule(Fact(g0=True), Fact(g1=True), Fact(g2=True), Fact(g5=True))
    def covid(self):
        self.declare(Fact(hasil="COVID-19"))

    @Rule(Fact(g0=True), Fact(g1=True), Fact(g3=True))
    def flu(self):
        self.declare(Fact(hasil="Flu"))

    @Rule(Fact(g1=True), Fact(g2=True))
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

    st.progress(total/len(gejala))
    st.caption(f"{total} dari {len(gejala)} gejala dipilih")

    col_btn1, col_btn2 = st.columns(2)

    with col_btn1:
        proses = st.button("🚀 Diagnosa")

    with col_btn2:
        if st.button("🔄 Reset"):
            st.session_state.clear()
            st.rerun()

# =========================
# OUTPUT
# =========================
with col2:
    st.subheader("📊 Hasil Diagnosa")

    if proses:
        if total < 2:
            st.warning("⚠️ Pilih minimal 2 gejala!")
        else:

            # =========================
            # EXPERTA
            # =========================
            engine = DiagnosaEngine()
            engine.reset()
            engine.run()

            hasil_experta = []
            for fact in engine.facts.values():
                if isinstance(fact, Fact) and "hasil" in fact:
                    hasil_experta.append(fact["hasil"])

            # =========================
            # MANUAL (PERSEN)
            # =========================
            skor = {}

            for penyakit, rule in rules_manual.items():
                total_bobot = sum(rule.values())
                skor_penyakit = 0

                for idx, bobot in rule.items():
                    if st.session_state.jawaban[idx]:
                        skor_penyakit += bobot

                skor[penyakit] = (skor_penyakit / total_bobot) * 100

            ranking = sorted(skor.items(), key=lambda x: x[1], reverse=True)

            # =========================
            # GRAFIK
            # =========================
            st.bar_chart(skor)

            # =========================
            # OUTPUT PERSEN
            # =========================
            for p, val in ranking:
                st.write(f"{p}: {val:.1f}%")

            st.divider()

            # =========================
            # HASIL EXPERTA
            # =========================
            if hasil_experta:
                utama = hasil_experta[0]
                st.error(f"🩺 Diagnosis (Experta): {utama}")
                st.success(f"💡 Saran: {saran[utama]}")
            else:
                st.info("❓ Tidak ditemukan rule pasti (Experta)")
