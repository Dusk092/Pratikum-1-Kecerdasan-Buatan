import streamlit as st

# =========================
# CONFIG
# =========================
st.set_page_config(
    page_title="Sistem Pakar Gastro Usus",
    layout="wide"
)

# =========================
# HEADER
# =========================
st.markdown("""
<h1 style='text-align: center;'>🧠 Sistem Pakar Diagnosa Gastro Usus</h1>
<p style='text-align: center; color: gray;'>Forward Chaining - Rule Based Expert System</p>
""", unsafe_allow_html=True)

st.divider()

# =========================
# DATA
# =========================
gejala = [
    "Buang air besar lebih dari 2 kali",
    "Berak encer",
    "Berak berdarah",
    "Lesu dan tidak bergairah",
    "Tidak selera makan",
    "Mual dan muntah",
    "Sakit perut",
    "Tekanan darah rendah",
    "Pusing",
    "Pingsan",
    "Demam",
    "Memakan daging",
    "Memakan jamur",
    "Memakan makanan kaleng",
    "Meminum susu"
]

rules = {
    "Staphylococcus aureus": [1, 5, 14],
    "Keracunan jamur beracun": [5, 6, 12],
    "Salmonella": [1, 5, 10, 11],
    "Clostridium botulinum": [5, 6, 13],
    "Campylobacter": [1, 10, 6]
}

saran = {
    "Staphylococcus aureus": "Hindari susu dan minum banyak air.",
    "Keracunan jamur beracun": "Segera ke rumah sakit.",
    "Salmonella": "Minum oralit dan istirahat.",
    "Clostridium botulinum": "DARURAT! Segera ke dokter.",
    "Campylobacter": "Jaga kebersihan makanan."
}

# =========================
# INIT STATE (AMAN)
# =========================
if "jawaban" not in st.session_state:
    st.session_state.jawaban = [False] * len(gejala)

# =========================
# LAYOUT
# =========================
col1, col2 = st.columns([1, 1])

# =========================
# INPUT
# =========================
with col1:
    st.subheader("📝 Jawab Pertanyaan")

    total_terisi = 0

    # gunakan key + sync ke jawaban
    for i, g in enumerate(gejala):
        val = st.toggle(f"Apakah Anda {g}?", key=f"g{i}")
        st.session_state.jawaban[i] = val
        if val:
            total_terisi += 1

    st.progress(total_terisi / len(gejala))
    st.caption(f"{total_terisi} dari {len(gejala)} gejala dipilih")

    col_btn1, col_btn2 = st.columns(2)

    with col_btn1:
        proses = st.button("🚀 Diagnosa", use_container_width=True)

    with col_btn2:
        if st.button("🔄 Reset", use_container_width=True):
            # RESET AMAN 100%
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

# =========================
# OUTPUT
# =========================
with col2:
    st.subheader("📊 Hasil Diagnosa")

    if proses:

        if total_terisi < 2:
            st.warning("⚠️ Pilih minimal 2 gejala terlebih dahulu!")
        else:
            skor = {}

            for p, r in rules.items():
                cocok = sum([1 for i in r if st.session_state.jawaban[i]])
                skor[p] = (cocok / len(r)) * 100 if len(r) > 0 else 0

            ranking = sorted(skor.items(), key=lambda x: x[1], reverse=True)

            # =========================
            # GRAFIK BATANG (SUPER STABIL)
            # =========================
            st.bar_chart(skor)

            # =========================
            # TEXT OUTPUT
            # =========================
            for p, val in ranking:
                st.write(f"{p}: {val:.1f}%")

            terbaik = ranking[0][0]

            st.divider()

            st.error(f"🩺 Diagnosis Utama: {terbaik}")
            st.success(f"💡 Saran: {saran[terbaik]}")
