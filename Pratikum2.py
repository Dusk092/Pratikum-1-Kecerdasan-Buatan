import streamlit as st

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="Hybrid Sistem Pakar", layout="wide")

# =========================
# HEADER
# =========================
st.markdown("""
<h1 style='text-align: center;'>🧠 Sistem Pakar Diagnosa Penyakit Pernapasan</h1>
<p style='text-align: center; color: gray;'>Forward Chaining + Persentase (Hybrid)</p>
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
# RULE PERSENTASE
# =========================
rules = {
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
    st.session_state.jawaban = [False] * len(gejala)

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
            st.warning("⚠️ Pilih minimal 2 gejala!")
        else:

            # =========================
            # FORWARD CHAINING (SIMULASI EXPERTA)
            # =========================
            hasil_experta = []

            if (
                st.session_state.jawaban[0] and
                st.session_state.jawaban[1] and
                st.session_state.jawaban[2] and
                st.session_state.jawaban[5]
            ):
                hasil_experta.append("COVID-19")

            elif (
                st.session_state.jawaban[0] and
                st.session_state.jawaban[1] and
                st.session_state.jawaban[3]
            ):
                hasil_experta.append("Flu")

            elif (
                st.session_state.jawaban[1] and
                st.session_state.jawaban[2]
            ):
                hasil_experta.append("Bronkitis")

            # =========================
            # PERHITUNGAN PERSENTASE
            # =========================
            skor = {}

            for penyakit, rule in rules.items():
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
            # HASIL PERSEN
            # =========================
            for p, val in ranking:
                st.write(f"{p}: {val:.1f}%")

            st.divider()

            # =========================
            # HASIL DIAGNOSA (SIMULASI EXPERTA)
            # =========================
            if hasil_experta:
                utama = hasil_experta[0]
            else:
                utama = ranking[0][0]

            st.error(f"🩺 Diagnosis: {utama}")
            st.success(f"💡 Saran: {saran[utama]}")
