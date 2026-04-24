import streamlit as st
from fpdf import FPDF
from datetime import datetime

# Seiteneinstellungen
st.set_page_config(page_title="Aneurysm Risk Dashboard", layout="wide")

# --- CSS für medizinisches Design ---
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stRadio > div { flex-direction: row !important; }
    </style>
    """, unsafe_allow_html=True)

# --- Header ---
st.title("🧠 Aneurysm Management Suite (UIATS & PHASES)")
st.subheader("Klinisches Entscheidungs-Dashboard v3.1")

# --- Patientendaten ---
with st.sidebar:
    st.header("Patienten-Info")
    patient_id = st.text_input("Patienten ID / Name", placeholder="z.B. 123456")
    clinician = st.text_input("Untersuchender Arzt", placeholder="Dr. Med. Muster")
    st.divider()
    st.info("**Morphologie-Ref:**\n\n**AR (Aspect Ratio):** Höhe / Halsbreite (Risiko >1.6)\n\n**SR (Size Ratio):** Höhe / Gefäßdurchmesser (Risiko >3.0)")

# --- Tabs ---
tab1, tab2 = st.tabs(["📊 UIATS Dashboard", "📈 PHASES Rupture Risk"])

# --- UIATS LOGIK ---
with tab1:
    st.markdown("### UIATS Scoring (Behandlung vs. Beobachtung)")
    col_treat, col_cons = st.columns(2)

    with col_treat:
        st.error("#### 1. Favoring Treatment")
        t_age = st.radio("Alter (Behandlung)", ["<40 (4)", "41-60 (3)", "61-70 (2)", "71-80 (1)", ">80 (0)", "N/A (0)"], index=5)
        t_sah = st.radio("Frühere SAB (anderes Aneurysma)", ["Ja (4)", "N/A (0)"], index=1)
        t_fam = st.radio("Familienanamnese SAB", ["Ja (3)", "N/A (0)"], index=1)
        t_eth = st.radio("Ethnie (JP/FI/Inuit)", ["Ja (2)", "N/A (0)"], index=1)
        t_smk = st.radio("Aktuelles Rauchen", ["Ja (3)", "N/A (0)"], index=1)
        t_htn = st.radio("Hypertonie (>140 mmHg)", ["Ja (2)", "N/A (0)"], index=1)
        t_adpkd = st.radio("ADPKD", ["Ja (2)", "N/A (0)"], index=1)
        t_drug = st.radio("Drogenabusus (Stimulantien)", ["Ja (2)", "N/A (0)"], index=1)
        t_alc = st.radio("Alkoholabusus", ["Ja (1)", "N/A (0)"], index=1)
        t_symp = st.radio("Symptome (Hirnnerven/Masse)", ["Ja (4)", "N/A (0)"], index=1)
        t_fear = st.radio("Angst vor Ruptur (Lebensqualität)", ["Ja (2)", "N/A (0)"], index=1)
        t_size = st.radio("Größe (Behandlung)", ["<3.9 (0)", "4-6.9 (1)", "7-12.9 (2)", "13-24.9 (3)", ">25 (4)"], index=0)
        t_morph = st.radio("Morphologie (Irregulär)", ["Ja (3)", "N/A (0)"], index=1)
        t_ratio = st.radio("AR >1.6 oder SR >3.0", ["Ja (1)", "N/A (0)"], index=1)
        t_loc = st.radio("Lage (Basilaris/Acom/Pcom)", ["Basilaris (5)", "Acom/Pcom (2)", "Vert/Bas (4)", "N/A (0)"], index=3)
        t_growth = st.radio("Wachstum / De Novo", ["Ja (4)", "N/A (0)"], index=1)

    with col_cons:
        st.success("#### 2. Favoring Conservative")
        st.warning("Basis-Interventionsrisiko: **5 Punkte** (Konstante)")
        c_life = st.radio("Lebenserwartung", ["<5j (4)", "5-10j (3)", ">10j (1)", "N/A (0)"], index=3)
        c_neuro = st.radio("Neurokognitive Störung / Demenz", ["Ja (3)", "N/A (0)"], index=1)
        c_coag = st.radio("Koagulopathie / Thrombophilie", ["Ja (2)", "N/A (0)"], index=1)
        c_psych = st.radio("Psychiatrische Erkrankung", ["Ja (2)", "N/A (0)"], index=1)
        c_age = st.radio("Alter (Risiko Beobachtung)", ["<40 (0)", "41-60 (1)", "61-70 (3)", "71-80 (4)", ">80 (5)"], index=0)
        c_size = st.radio("Größe (Risiko Beobachtung)", ["<6 (0)", "6-10 (1)", "10.1-20 (3)", ">20 (5)"], index=0)
        c_complex = st.radio("Komplexität des Aneurysmas", ["Komplex (3)", "Einfach (0)"], index=1)

    # Punkte-Extraktion
    def get_pts(s): return int(s.split('(')[-1].replace(')', '')) if '(' in s else 0
    t_sum = sum([get_pts(t_age), get_pts(t_sah), get_pts(t_fam), get_pts(t_eth), get_pts(t_smk), get_pts(t_htn), 
                 get_pts(t_adpkd), get_pts(t_drug), get_pts(t_alc), get_pts(t_symp), get_pts(t_fear), 
                 get_pts(t_size), get_pts(t_morph), get_pts(t_ratio), get_pts(t_loc), get_pts(t_growth)])
    c_sum = 5 + sum([get_pts(c_life), get_pts(c_neuro), get_pts(c_coag), get_pts(c_psych), get_pts(c_age), get_pts(c_size), get_pts(c_complex)])
    
    uiats_score = t_sum - c_sum
    if uiats_score >= 3: rec = "FAVORS TREATMENT"
    elif uiats_score <= -3: rec = "FAVORS CONSERVATIVE"
    else: rec = "EQUIVOCAL"

    st.divider()
    st.metric("Finaler UIATS Score", f"{uiats_score}", f"Empfehlung: {rec}")

# --- PHASES LOGIK ---
with tab2:
    st.markdown("### PHASES (5-Jahres Rupturrisiko)")
    p_pop = st.radio("Population", ["Andere (0)", "Japanisch (3)", "Finnisch (5)"])
    p_htn = st.radio("Hypertonie", ["Nein (0)", "Ja (1)"])
    p_age = st.radio("Alter >= 70", ["Nein (0)", "Ja (1)"])
    p_size = st.radio("Größe (PHASES)", ["<7 (0)", "7-9.9 (3)", "10-19.9 (6)", ">20 (10)"])
    p_sah = st.radio("Frühere SAB", ["Nein (0)", "Ja (1)"])
    p_loc = st.radio("Lage (PHASES)", ["ICA (0)", "MCA (2)", "Post/Acom (4)"])
    
    p_sum = sum([get_pts(p_pop), get_pts(p_htn), get_pts(p_age), get_pts(p_size), get_pts(p_sah), get_pts(p_loc)])
    risks = {0: "0.7%", 3: "0.9%", 10: "5.1%", 12: "8.4%", 20: ">25%"}
    p_risk = next((v for k, v in sorted(risks.items(), reverse=True) if p_sum >= k), "0.7%")
    
    st.metric("PHASES Score", f"{p_sum}", f"5-Jahres Risiko: {p_risk}")

# --- PDF GENERIERUNG ---
if st.button("Klinischen Bericht (PDF) generieren"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, "Aneurysm Assessment Report", 0, 1, 'C')
    pdf.set_font("Arial", '', 10)
    pdf.cell(200, 10, f"Patient: {patient_id} | Arzt: {clinician} | Datum: {datetime.now().strftime('%d.%m.%Y')}", 0, 1, 'C')
    pdf.line(10, 30, 200, 30)
    
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, f"I. UIATS Resultat: {uiats_score} ({rec})", 0, 1)
    pdf.set_font("Arial", '', 10)
    pdf.cell(0, 5, f"- Favoring Treatment: {t_sum} Pkt", 0, 1)
    pdf.cell(0, 5, f"- Favoring Conservative: {c_sum} Pkt", 0, 1)
    
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 15, f"II. PHASES Resultat: {p_sum} (Risiko: {p_risk})", 0, 1)
    
    pdf_output = pdf.output(dest='S').encode('latin-1')
    st.download_button("Bericht herunterladen", data=pdf_output, file_name=f"Bericht_{patient_id}.pdf", mime="application/pdf")