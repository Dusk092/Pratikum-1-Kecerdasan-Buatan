import streamlit as st

# =========================
# CONFIG
# =========================
st.set_page_config(
    page_title="Sistem Pakar Gastro Usus",
    layout="wide"
)

# =========================
# JUDUL
# =========================
st.title("🧠 Sistem Pakar Diagnosa Penyakit Gastro Usus")
st.caption("Metode: Rule-Based Expert System (Forward Chaining)")

# =========================
# DATA GEJALA
# =========================
gejala = [
    "Apakah Anda sering buang air besar (>2x)?",
    "Apakah Anda mengalami berak encer?",
    "Apakah Anda mengalami berak berdarah?",
    "Apakah Anda merasa lesu dan tidak bergairah?",
    "Apakah Anda tidak selera makan?",
    "Apakah Anda merasa mual dan sering muntah?",
    "Apakah Anda merasa sakit di bagian perut?",
    "Apakah tekanan darah Anda rendah?",
    "Apakah Anda merasa pusing?",
    "Apakah Anda pernah pingsan?",
    "Apakah suhu badan Anda tinggi?",
    "Apakah Anda memiliki luka di bagian tertentu?",
    "Apakah Anda tidak dapat menggerakkan anggota tubuh tertentu?",
    "Apakah Anda memakan sesuatu sebelumnya?",
    "Apakah Anda memakan daging?",
    "Apakah Anda memakan jamur?",
    "Apakah Anda memakan makanan kaleng?",
    "Apakah Anda membeli susu?",
    "Apakah Anda meminum susu?"
]

# =========================
# RULE
# =========================
rules = {
    "Staphylococcus aureus": [0, 5, 18],
    "Keracunan jamur beracun": [5, 6, 15],
    "Salmonella": [1, 5, 10, 14],
    "Clostridium botulinum": [5, 6, 16],
    "Campylobacter": [1, 10, 6]
}

# =========================
# SARAN
# =========================
saran = {
    "Staphylococcus aureus": "Hindari susu sementara, minum air banyak, dan istirahat.",
    "Keracunan jamur beracun": "Segera ke rumah sakit, jangan konsumsi jamur liar.",
    "Salmonella": "Minum oralit, istirahat, dan makan makanan matang.",
    "Clostridium botulinum": "DARURAT! Segera ke dokter atau rumah sakit.",
    "Campylobacter": "Jaga kebersihan makanan dan minum air yang cukup."
}

# =========================
# STATE
# =========================
if "jawaban" not in st.session_state:
    st.session_state.jawaban = [False] * len(gejala)

# =========================
# FUNGSI HITUNG
# =========================
def hitung():
    skor = {}
    for p, r in rules.items():
        cocok = sum([1 for i in r if st.session_state.jawaban[i]])
        skor[p] = (cocok / len(r)) * 100
    return skor

# =========================
# LAYOUT
# =========================
col1, col2 = st.columns(2)

# =========================
# INPUT (KIRI)
# =========================
with col1:
    st.subheader("📝 Input Gejala")

    for i, g in enumerate(gejala):
        st.session_state.jawaban[i] = st.toggle(
            g,
            value=st.session_state.jawaban[i]
        )

    progress = sum(st.session_state.jawaban) / len(gejala)
    st.progress(progress)

# =========================
# OUTPUT (KANAN)
# =========================
with col2:
    st.subheader("📊 Hasil Diagnosa")

    if st.button("🔍 Proses Diagnosa"):
        skor = hitung()

        # tampil semua hasil
        for p, val in skor.items():
            st.write(f"{p}: {val:.1f}%")

        terbaik = max(skor, key=skor.get)

        st.markdown("---")
        st.error(f"🩺 Diagnosis: {terbaik}")
        st.info(f"💡 Saran: {saran[terbaik]}")
    