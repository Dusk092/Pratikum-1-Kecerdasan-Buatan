import streamlit as st

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="Diagnosa Pernapasan", layout="wide")

# =========================
# CUSTOM CSS (MINIMAL CLEAN)
# =========================
st.markdown("""
<style>
.main {
    background-color: #f1f5f9;
}

.card {
    background: white;
    padding: 20px;
    border-radius: 12px;
    border: 1px solid #e2e8f0;
    margin-bottom: 15px;
}

h1 {
    text-align: center;
    color: #0f172a;
}

.subtitle {
    text-align: center;
    color: #64748b;
    margin-bottom: 20px;
}

.stButton>button {
    border-radius: 8px;
    background-color: #2563eb;
    color: white;
    font-weight: 500;
}

.stProgress > div > div {
    background-color: #2563eb;
}
</style>
""", unsafe_allow_html=True)

# =========================
# HEADER (LEBIH NATURAL)
# =========================
st.markdown("<h1>Sistem Diagnosa Penyakit Pernapasan</h1>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Analisis gejala untuk membantu diagnosis awal</div>", unsafe_allow_html=True)

# =========================
# DATA
# =========================
gejala = [
    "Demam",
    "Batuk",
    "Sesak napas",
    "Pilek",
    "Sakit tenggorokan",
    "Kehilangan penciuman",
    "Kehilangan rasa",
    "Sakit kepala",
    "Lemas",
    "Nyeri otot",
    "Menggigil",
    "Hidung tersumbat",
    "Bersin-bersin",
    "Batuk berdahak",
    "Dada terasa berat"
]

rules = {
    "COVID-19": {0:2,1:2,2:3,5:3,6:3,8:2},
    "Flu": {0:2,1:2,3:2,4:2,11:1,12:1},
    "Bronkitis": {1:2,2:3,13:2,14:2}
}

saran = {
    "COVID-19": "Disarankan melakukan pemeriksaan lanjutan dan membatasi kontak.",
    "Flu": "Istirahat cukup, konsumsi cairan hangat, dan vitamin.",
    "Bronkitis": "Hindari asap dan konsultasikan ke tenaga medis."
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
    st.markdown("<div class='card'>", unsafe_allow_html=True)

    st.subheader("Gejala")

    total = 0

    for i, g in enumerate(gejala):
        val = st.checkbox(g, key=f"g{i}")
        st.session_state.jawaban[i] = val
        if val:
            total += 1

    st.progress(total / len(gejala))
    st.caption(f"{total} gejala dipilih")

    proses = st.button("Proses")
    reset = st.button("Reset")

    if reset:
        st.session_state.clear()
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

# =========================
# OUTPUT
# =========================
with col2:
    st.markdown("<div class='card'>", unsafe_allow_html=True)

    st.subheader("Hasil")

    if proses:

        if total < 2:
            st.warning("Minimal pilih dua gejala.")
        else:

            with st.spinner("Memproses data..."):

                # Forward chaining sederhana
                hasil_rule = []

                if (
                    st.session_state.jawaban[0] and
                    st.session_state.jawaban[1] and
                    st.session_state.jawaban[2] and
                    st.session_state.jawaban[5]
                ):
                    hasil_rule.append("COVID-19")

                elif (
                    st.session_state.jawaban[0] and
                    st.session_state.jawaban[1] and
                    st.session_state.jawaban[3]
                ):
                    hasil_rule.append("Flu")

                elif (
                    st.session_state.jawaban[1] and
                    st.session_state.jawaban[2]
                ):
                    hasil_rule.append("Bronkitis")

                # Skor persentase
                skor = {}

                for penyakit, rule in rules.items():
                    total_bobot = sum(rule.values())
                    skor_penyakit = sum(
                        bobot for idx, bobot in rule.items()
                        if st.session_state.jawaban[idx]
                    )
                    skor[penyakit] = (skor_penyakit / total_bobot) * 100

                ranking = sorted(skor.items(), key=lambda x: x[1], reverse=True)

            # hasil utama
            if hasil_rule:
                utama = hasil_rule[0]
            else:
                utama = ranking[0][0]

            st.success(f"Kemungkinan terbesar: {utama}")
            st.write(saran[utama])

            st.divider()

            # progress instead of chart (lebih natural)
            for p, val in ranking:
                st.progress(val / 100)
                st.caption(f"{p} ({val:.1f}%)")

    st.markdown("</div>", unsafe_allow_html=True)
