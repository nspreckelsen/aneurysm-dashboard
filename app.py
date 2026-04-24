import streamlit as st
from fpdf import FPDF
from datetime import datetime

# Seiteneinstellungen
st.set_page_config(page_title="UIATS & PHASES Klinisches Dashboard", layout="wide")

# Helfer-Funktion zum Extrahieren der Punkte aus dem Auswahltext
def get_pts(s):
    if not s or "(" not in s: return 0
    try:
        return int(s.split('(')[-1].split(')')[0])
    except:
        return 0

# --- Header ---
st.title("🧠 Klinische Aneurysma-Entscheidungshilfe")
st.caption("Strukturierte Auswertung nach UIATS (Neurology 2015) & PHASES (Lancet Neurol 2014)")

# --- Patienten- & Arzt-Info in der Sidebar ---
with st.sidebar:
    st.header("📋 Stammdaten")
    patient_id = st.text_input("Patienten ID / Name", placeholder="z.B. ID12345")
    clinician = st.text_input("Behandelnder Arzt", placeholder="Dr. Med. Muster")
    st.divider()
    st.markdown("### 📏 Referenz-Formeln")
    st.info("**Aspect Ratio (AR):** Höhe / Halsbreite\n\n**Size Ratio (SR):** Höhe / Durchmesser Ursprungsgefäß")

# --- Tabs ---
tab1, tab2 = st.tabs(["📊 UIATS Dashboard", "📈 PHASES Score"])

# --- UIATS LOGIK ---
with tab1:
    st.subheader("UIATS: Unruptured Intracranial Aneurysm Treatment Score")
    col_treat, col_cons = st.columns(2)

    # --- SPALTE 1: BEHANDLUNG BEGÜNSTIGEND (GRÜN) ---
    with col_treat:
        st.success("#### 1. BEHANDLUNG BEGÜNSTIGEND")
        
        # PATIENT
        st.markdown("##### **PATIENT**")
        with st.expander("Risikofaktoren", expanded=True):
            t_age = st.radio("Alter (Behandlung)", ["<40 (4)", "41-60 (3)", "61-70 (2)", "71-80 (1)", ">80 (0)", "N/A (0)"], index=5, horizontal=True)
            t_sah = st.radio("Frühere SAB (anderes Aneurysma)", ["Ja (4)", "N/A (0)"], index=1, horizontal=True)
            t_fam = st.radio("Familienanamnese für SAB", ["Ja (3)", "N/A (0)"], index=1, horizontal=True)
            t_eth = st.radio("Ethnie (Japanisch/Finnisch/Inuit)", ["Ja (2)", "N/A (0)"], index=1, horizontal=True)
            t_smk = st.radio("Aktuelles Rauchen", ["Ja (3)", "N/A (0)"], index=1, horizontal=True)
            t_htn = st.radio("Hypertonie (>140 mmHg)", ["Ja (2)", "N/A (0)"], index=1, horizontal=True)
            t_adpkd = st.radio("ADPKD (Zystennieren)", ["Ja (2)", "N/A (0)"], index=1, horizontal=True)
            t_drug = st.radio("Drogenabusus (Stimulantien)", ["Ja (2)", "N/A (0)"], index=1, horizontal=True)
            t_alc = st.radio("Alkoholabusus", ["Ja (1)", "N/A (0)"], index=1, horizontal=True)

        with st.expander("Klinische Symptome im Zusammenhang mit UIA", expanded=True):
            t_cnp = st.radio("Hirnnervenausfall", ["Ja (4)", "N/A (0)"], index=1, horizontal=True)
            t_mfx = st.radio("Masseneffekt (klinisch oder radiologisch)", ["Ja (4)", "N/A (0)"], index=1, horizontal=True)
            t_thr = st.radio("Thromboembolische Ereignisse (aus Aneurysma)", ["Ja (3)", "N/A (0)"], index=1, horizontal=True)
            t_epi = st.radio("Epilepsie", ["Ja (1)", "N/A (0)"], index=1, horizontal=True)

        # ANEURYSMA
        st.markdown("##### **ANEURYSMA**")
        with st.expander("Aneurysma-Morphologie", expanded=True):
            t_size = st.radio("Größe (Behandlung)", ["<3.9mm (0)", "4.0-6.9mm (1)", "7.0-12.9mm (2)", "13.0-24.9mm (3)", ">25mm (4)"], index=0, horizontal=True)
            t_morph = st.radio("Irregularität / Lobulierung", ["Ja (3)", "N/A (0)"], index=1, horizontal=True)
            t_ratio = st.radio("Aspect Ratio >1.6 oder Size Ratio >3", ["Ja (1)", "N/A (0)"], index=1, horizontal=True)

        with st.expander("Aneurysma-Lokalisation", expanded=True):
            t_loc = st.radio("Lokalisation (UIATS)", ["Basilariskopf (5)", "A. vertebralis / Basilaris (4)", "AcomA / PcomA (2)", "N/A (0)"], index=3, horizontal=True)

        with st.expander("Sonstiges (Aneurysma)", expanded=True):
            t_growth = st.radio("Wachstum (serielle Bildgebung)", ["Ja (4)", "N/A (0)"], index=1, horizontal=True)
            t_denovo = st.radio("De-novo Entwicklung", ["Ja (3)", "N/A (0)"], index=1, horizontal=True)
            t_steno = st.radio("Kontralaterale steno-okklusive Gefäßerkrankung", ["Ja (1)", "N/A (0)"], index=1, horizontal=True)

        # SONSTIGES
        st.markdown("##### **SONSTIGES**")
        with st.expander("Multiplizität / Lebensqualität", expanded=True):
            t_mult = st.radio("Aneurysma-Multiplizität", ["Ja (1)", "N/A (0)"], index=1, horizontal=True)
            t_qol = st.radio("Angst / Reduzierte Lebensqualität", ["Ja (2)", "N/A (0)"], index=1, horizontal=True)

    # --- SPALTE 2: KONSERVATIV BEGÜNSTIGEND (ROT) ---
    with col_cons:
        st.error("#### 2. KONSERVATIV BEGÜNSTIGEND")
        st.info("Basis-Interventionsrisiko: **5 Punkte**")
        
        # PATIENT
        st.markdown("##### **PATIENT**")
        with st.expander("Lebenserwartung", expanded=True):
            c_life = st.radio("Eingeschränkte Lebenserwartung", ["<5 Jahre (4)", "5-10 Jahre (3)", ">10 Jahre (1)", "N/A (0)"], index=3, horizontal=True)

        with st.expander("Begleiterkrankungen", expanded=True):
            c_neuro = st.radio("Neurokognitive Störung / Demenz", ["Ja (3)", "N/A (0)"], index=1, horizontal=True)
            c_coag = st.radio("Koagulopathie / Thrombophilie", ["Ja (2)", "N/A (0)"], index=1, horizontal=True)
            c_psych = st.radio("Psychiatrische Erkrankung", ["Ja (2)", "N/A (0)"], index=1, horizontal=True)

        # BEHANDLUNG & RISIKO
        st.markdown("##### **BEHANDLUNG & RISIKO**")
        with st.expander("Behandlungsschwierigkeit", expanded=True):
            c_complex = st.radio("Komplexität / Riesenaneurysma", ["Ja (3)", "Einfach (0)"], index=1, horizontal=True)

        with st.expander("Risiko bezogen auf Patient / Aneurysma", expanded=True):
            c_age = st.radio("Alter (Konservativ-Risiko)", ["<40 (0)", "41-60 (1)", "61-70 (3)", "71-80 (4)", ">80 (5)"], index=0, horizontal=True)
            c_size_risk = st.radio("Größe (Konservativ-Risiko)", ["<6mm (0)", "6-10mm (1)", "10.1-20mm (3)", ">20mm (5)"], index=0, horizontal=True)

    # --- BERECHNUNG UIATS ---
    t_list = [t_age, t_sah, t_fam, t_eth, t_smk, t_htn, t_adpkd, t_drug, t_alc, t_cnp, t_mfx, t_thr, t_epi, 
              t_size, t_morph, t_ratio, t_loc, t_growth, t_denovo, t_steno, t_mult, t_qol]
    c_list = [c_life, c_neuro, c_coag, c_psych, c_complex, c_age, c_size_risk]
    
    t_sum = sum(get_pts(p) for p in t_list)
    c_sum = 5 + sum(get_pts(p) for p in c_list)
    uiats_final = t_sum - c_sum

    if uiats_final >= 3: rec = "BEHANDLUNG EMPFOHLEN"
    elif uiats_final <= -3: rec = "BEOBACHTUNG EMPFOHLEN"
    else: rec = "ÄQUIVOKAL / INDIVIDUALISIEREN"

    st.divider()
    res_col1, res_col2, res_col3 = st.columns(3)
    res_col1.metric("Summe Behandlung", f"{t_sum} Pkt")
    res_col2.metric("Summe Konservativ", f"{c_sum} Pkt")
    res_col3.metric("UIATS Score (Netto)", f"{uiats_final}", f"Empfehlung: {rec}")

# --- PHASES LOGIK ---
with tab2:
    st.subheader("PHASES: 5-Jahres Rupturrisiko")
    p_col1, p_col2 = st.columns(2)
    
    with p_col1:
        p_pop = st.radio("Population", ["Andere (0)", "Japanisch (3)", "Finnisch (5)"], horizontal=True)
        p_htn = st.radio("Hypertonie Anamnese", ["Nein (0)", "Ja (1)"], horizontal=True)
        p_age_70 = st.radio("Alter >= 70 Jahre", ["Nein (0)", "Ja (1)"], horizontal=True)
        
    with p_col2:
        p_size = st.radio("Größe (PHASES)", ["<7mm (0)", "7-9.9mm (3)", "10-19.9mm (6)", ">=20mm (10)"], horizontal=True)
        p_sah_prev = st.radio("Frühere SAB (anderes Aneurysma)", ["Nein (0)", "Ja (1)"], horizontal=True)
        p_site = st.radio("Lokalisation (PHASES)", ["ICA (0)", "MCA (2)", "ACA/Pcom/Posteriore Zirkulation (4)"], horizontal=True)

    p_sum = sum(get_pts(x) for x in [p_pop, p_htn, p_age_70, p_size, p_sah_prev, p_site])
    
    risks = {0: "0.7%", 3: "0.9%", 5: "1.3%", 6: "1.7%", 7: "3.2%", 10: "5.1%", 12: "8.4%", 14: "12.2%", 17: "18.5%", 20: ">25%"}
    p_risk = next((v for k, v in sorted(risks.items(), reverse=True) if p_sum >= k), "0.7%")
    
    st.divider()
    st.metric("PHASES Score", f"{p_sum} Punkte", f"Risiko: {p_risk}")

# --- PDF EXPORT ---
if st.button("Bericht generieren"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, "Klinischer Aneurysma-Bericht", 0, 1, 'C')
    pdf.set_font("Arial", '', 10)
    pdf.cell(200, 10, f"Patient: {patient_id} | Arzt: {clinician} | Datum: {datetime.now().strftime('%d.%m.%Y')}", 0, 1, 'C')
    pdf.line(10, 30, 200, 30)
    
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, f"I. UIATS Resultat: {uiats_final} Punkte", 0, 1)
    pdf.set_font("Arial", '', 11)
    pdf.cell(0, 7, f"Empfehlung: {rec}", 0, 1)
    
    pdf.ln(5)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, f"II. PHASES Resultat: {p_sum} Punkte", 0, 1)
    pdf.set_font("Arial", '', 11)
    pdf.cell(0, 7, f"Rupturrisiko: {p_risk}", 0, 1)

    pdf_output = pdf.output(dest='S').encode('latin-1', 'ignore')
    st.download_button("Bericht herunterladen", data=pdf_output, file_name=f"Bericht_{patient_id}.pdf", mime="application/pdf")
