import streamlit as st

# =========================
# CONFIG
# =========================
st.set_page_config(
    page_title="Diagnosa Sistem Pencernaan",
    layout="wide"
)

# =========================
# CUSTOM CSS (LIGHT MEDICAL)
# =========================
st.markdown("""
<style>
.main {
    background-color: #f8fafc;
}

.card {
    background-color: white;
    padding: 20px;
    border-radius: 14px;
    margin-bottom: 15px;
    border: 1px solid #e2e8f0;
}

h1 {
    color: #065f46;
}

h2, h3 {
    color: #0f172a;
}

.stButton>button {
    border-radius: 10px;
    background-color: #10b981;
    color: white;
    font-weight: 600;
}

.stProgress > div > div {
    background-color: #10b981;
}
</style>
""", unsafe_allow_html=True)

# =========================
# HEADER (ICON DIGANTI)
# =========================
st.markdown("""
<div style='text-align:center; margin-bottom:25px'>
    <h1>🩺 Sistem Pakar Gangguan Pencernaan</h1>
    <p style='color:#64748b;'>Analisis gejala untuk diagnosis awal gangguan gastro-usus</p>
</div>
""", unsafe_allow_html=True)

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
    "Staphylococcus aureus": "Hindari susu dan perbanyak cairan.",
    "Keracunan jamur beracun": "Segera ke rumah sakit.",
    "Salmonella": "Istirahat dan minum oralit.",
    "Clostridium botulinum": "Segera ke dokter (darurat).",
    "Campylobacter": "Jaga kebersihan makanan."
}

# =========================
# SESSION
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
    st.markdown("<div class='card'>", unsafe_allow_html=True)

    st.subheader("Form Gejala")

    total = 0

    for i, g in enumerate(gejala):
        val = st.checkbox(g, key=f"g{i}")
        st.session_state.jawaban[i] = val
        if val:
            total += 1

    st.progress(total / len(gejala))
    st.caption(f"{total} gejala dipilih")

    proses = st.button("Proses Diagnosa")
    reset = st.button("Reset")

    if reset:
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

# =========================
# OUTPUT
# =========================
with col2:
    st.markdown("<div class='card'>", unsafe_allow_html=True)

    st.subheader("Hasil Diagnosis")

    if proses:

        if total < 2:
            st.warning("Minimal pilih 2 gejala.")
        else:
            with st.spinner("Sedang menganalisis..."):
                skor = {}

                for p, r in rules.items():
                    cocok = sum([1 for i in r if st.session_state.jawaban[i]])
                    skor[p] = (cocok / len(r)) * 100

                ranking = sorted(skor.items(), key=lambda x: x[1], reverse=True)
                utama = ranking[0][0]

            st.success(f"Hasil utama: {utama}")
            st.info(saran[utama])

            st.divider()

            for p, val in ranking:
                st.progress(val / 100)
                st.caption(f"{p} ({val:.1f}%)")

    st.markdown("</div>", unsafe_allow_html=True)
