import streamlit as st

st.set_page_config(page_title="Simulador de Fertirriego Colombia Pro", page_icon="🌱", layout="wide")

st.title("🌱 Software de Fertirriego Profesional")
st.write("Ajusta tus metas de PPM, los Kilogramos/Gramos a la izquierda, o añade fertilizantes nuevos a tu bodega en tiempo real.")

# Porcentajes de Menores Sólidos Daymsa
PCT_FE = 6.0
PCT_B = 20.5
PCT_CU = 13.5
PCT_ZN = 13.0
PCT_MN = 12.0
PCT_MO = 10.0

# ==========================================
# REGLA DE MEMORIA SEGURA: INVENTARIO EDITABLE DE NUEVAS FUENTES
# ==========================================
if "nuevos_fertilizantes" not in st.session_state:
    st.session_state.nuevos_fertilizantes = {}

# ==========================================
# FORMULARIO CENTRAL: REGISTRO MANUAL DE NUEVAS MARCAS
# ==========================================
st.header("📦 Creación y Registro de Nuevos Fertilizantes")
with st.expander("➕ Haz clic aquí para registrar una marca o mezcla nueva en tu inventario"):
    nombre_nuevo = st.text_input("Nombre Comercial del Fertilizante:", placeholder="Ej: Kelatex, Mix Menores, Fertisolo, etc.")
    
    st.markdown("#### 🥦 Macronutrientes (%)")
    col_n1, col_n2, col_n3, col_n4 = st.columns(4)
    with col_n1:
        n_no3 = st.number_input("% Nitrato (NO₃⁻) del saco nuevo:", min_value=0.0, max_value=100.0, value=0.0, step=0.1)
        n_nh4 = st.number_input("% Amonio (NH₄⁺) del saco nuevo:", min_value=0.0, max_value=100.0, value=0.0, step=0.1)
    with col_n2:
        n_p2o5 = st.number_input("% Fósforo (P₂O₅) del saco nuevo:", min_value=0.0, max_value=100.0, value=0.0, step=0.1)
        n_k2o = st.number_input("% Potasio (K₂O) del saco nuevo:", min_value=0.0, max_value=100.0, value=0.0, step=0.1)
    with col_n3:
        n_cao = st.number_input("% Calcio (CaO) del saco nuevo:", min_value=0.0, max_value=100.0, value=0.0, step=0.1)
        n_mgo = st.number_input("% Magnesio (MgO) del saco nuevo:", min_value=0.0, max_value=100.0, value=0.0, step=0.1)
    with col_n4:
        n_so3 = st.number_input("% Azufre (SO₃) del saco nuevo:", min_value=0.0, max_value=100.0, value=0.0, step=0.1)
        
    st.markdown("#### 🧪 Micronutrientes (%)")
    col_m1, col_m2, col_m3 = st.columns(3)
    with col_m1:
        n_fe = st.number_input("% Hierro (Fe) del saco nuevo:", min_value=0.0, max_value=100.0, value=0.0, step=0.01)
        n_mn = st.number_input("% Manganeso (Mn) del saco nuevo:", min_value=0.0, max_value=100.0, value=0.0, step=0.01)
    with col_m2:
        n_zn = st.number_input("% Zinc (Zn) del saco nuevo:", min_value=0.0, max_value=100.0, value=0.0, step=0.01)
        n_cu = st.number_input("% Cobre (Cu) del saco nuevo:", min_value=0.0, max_value=100.0, value=0.0, step=0.01)
    with col_m3:
        n_b = st.number_input("% Boro (B) del saco nuevo:", min_value=0.0, max_value=100.0, value=0.0, step=0.01)
        n_mo = st.number_input("% Molibdeno (Mo) del saco nuevo:", min_value=0.0, max_value=100.0, value=0.0, step=0.001, format="%.4f")
        
    if st.button("💾 Guardar e Incorporar a la Barra Lateral"):
        if nombre_nuevo:
            st.session_state.nuevos_fertilizantes[nombre_nuevo] = {
                "CaO": n_cao, "NO3": n_no3, "NH4": n_nh4, "P2O5": n_p2o5, "K2O": n_k2o, "MgO": n_mgo, "SO3": n_so3,
                "Fe": n_fe, "Mn": n_mn, "Zn": n_zn, "Cu": n_cu, "B": n_b, "Mo": n_mo
            }
            st.success(f"✅ ¡{nombre_nuevo} guardado! Ya puedes asignarle kilos a la izquierda.")
        else:
            st.error("⚠️ Por favor escribe un nombre comercial válido.")

# ==========================================
# BARRA LATERAL: CONTROL DE AGUA Y DOSIS MANUALES
# ==========================================
st.sidebar.header("💧 Volumen de Agua")
volumen_agua = st.sidebar.number_input("Volumen de agua total (Litros):", min_value=1, value=26000, step=1000)
denominador_agua = volumen_agua * 0.1

st.sidebar.header("⚖️ Control de Dosificación Manual (Kg)")
kg_calcinit = st.sidebar.number_input("YaraLiva CALCINIT (Kg):", min_value=0.0, value=5.20, step=0.1)
kg_pony = st.sidebar.number_input("Poly-Feed Pony 13-3-43 (Kg):", min_value=0.0, value=5.30, step=0.1)
kg_dkp = st.sidebar.number_input("Haifa DKP 0-41-54 (Kg):", min_value=0.0, value=4.76, step=0.1)
kg_soluk = st.sidebar.number_input("Sulfato de Potasio (Kg):", min_value=0.0, value=3.90, step=0.1)
kg_mkp = st.sidebar.number_input("Fosfato Monopotásico MKP (Kg):", min_value=0.0, value=0.00, step=0.1)
kg_magboro = st.sidebar.number_input("Van Iperen Magboro (Kg):", min_value=0.0, value=4.19, step=0.1)
kg_sulfmg = st.sidebar.number_input("Sulfato de Magnesio Sulmag (Kg):", min_value=0.0, value=3.17, step=0.1)
kg_nitamonio = st.sidebar.number_input("Nitrato de Amonio (Kg):", min_value=0.0, value=0.00, step=0.1)

# Renderizado dinámico para productos nuevos
pesos_nuevos = {}
if st.session_state.nuevos_fertilizantes:
    st.sidebar.markdown("---")
    st.sidebar.markdown("#### 📦 Nuevos Fertilizantes en Bodega")
    for prod_n in st.session_state.nuevos_fertilizantes.keys():
        pesos_nuevos[prod_n] = st.sidebar.number_input(f"{prod_n} (Kg):", min_value=0.0, value=0.0, step=0.1)

st.sidebar.header("🧪 Ingresa tus Micronutrientes Puros (En Gramos)")
g_fe = st.sidebar.number_input("Naturquel Fe (g):", min_value=0.0, value=1486.3, step=10.0)
g_b = st.sidebar.number_input("Klip Boro (g):", min_value=0.0, value=81.2, step=5.0)
g_cu = st.sidebar.number_input("Kellus Cu (g):", min_value=0.0, value=104.0, step=5.0)
g_zn = st.sidebar.number_input("Naturzinc (g):", min_value=0.0, value=172.0, step=5.0)
g_mn = st.sidebar.number_input("Naturmanganeso (g):", min_value=0.0, value=348.8, step=10.0)
g_mo = st.sidebar.number_input("Molibk (g):", min_value=0.0, value=2.8, step=0.5)

# ==========================================
# PANEL CENTRAL PASO 1: METAS MODIFICABLES
# ==========================================
st.markdown("---")
st.header("🎯 1. Tus Metas Teóricas Requeridas (PPM)")
col1, col2, col3, col4 = st.columns(4)
with col1:
    tgt_no3 = st.number_input("Meta Nitrato (NO₃⁻):", value=133.6, step=1.0)
    tgt_nh4 = st.number_input("Meta Amonio (NH₄⁺):", value=23.6, step=1.0)
    tgt_cao = st.number_input("Meta Calcio (CaO):", value=158.6, step=1.0)
with col2:
    tgt_p2o5 = st.number_input("Meta Fósforo (P₂O₅):", value=81.4, step=1.0)
    tgt_k2o = st.number_input("Meta Potasio (K₂O):", value=503.6, step=5.0)
    tgt_mgo = st.number_input("Meta Magnesio (MgO):", value=63.8, step=1.0)
with col3:
    tgt_fe = st.number_input("Meta Hierro (Fe):", value=3.43, step=0.1)
    tgt_mn = st.number_input("Meta Manganeso (Mn):", value=1.61, step=0.1)
    tgt_zn = st.number_input("Meta Zinc (Zn):", value=0.86, step=0.1)
with col4:
    tgt_b = st.number_input("Meta Boro (B):", value=0.64, step=0.1)
    tgt_cu = st.number_input("Meta Cobre (Cu):", value=0.54, step=0.1)
    tgt_mo = st.number_input("Meta Molibdeno (Mo):", value=0.0107, format="%.4f")
    tgt_so3 = st.number_input("Meta Azufre (SO₃):", value=45.0, step=1.0)

# ==========================================
# MATEMÁTICA PLANA DIRECTA DE TU CALCULADORA DE CAMPO
# ==========================================
ppm_cao_calcinit = ((kg_calcinit * 1000.0) * 26.0) / denominador_agua
ppm_p2o5_pony = ((kg_pony * 1000.0) * 3.0) / denominador_agua
ppm_k2o_pony = ((kg_pony * 1000.0) * 43.0) / denominador_agua
ppm_p2o5_dkp = ((kg_dkp * 1000.0) * 41.0) / denominador_agua
ppm_k2o_dkp = ((kg_dkp * 1000.0) * 54.0) / denominador_agua
ppm_k2o_soluk = ((kg_soluk * 1000.0) * 50.0) / denominador_agua
ppm_so3_soluk = ((kg_soluk * 1000.0) * 18.0) / denominador_agua
ppm_p2o5_mkp = ((kg_mkp * 1000.0) * 52.0) / denominador_agua
ppm_k2o_mkp = ((kg_mkp * 1000.0) * 34.0) / denominador_agua
ppm_mgo_magboro = ((kg_magboro * 1000.0) * 15.5) / denominador_agua
ppm_mgo_sulfmg = ((kg_sulfmg * 1000.0) * 16.4) / denominador_agua
ppm_so3_sulfmg = ((kg_sulfmg * 1000.0) * 13.0) # Corregido con el número directo del Sulmag escrito plano

# Nitrógeno Nítrico y Amoniacal Base de la Libreta
ppm_no3_calcinit = (kg_calcinit * 1000.0 * 14.4) / (2600.0 / (197.3 / 72.2))
ppm_no3_pony = (kg_pony * 1000.0 * 13.0) / (2600.0 / (197.3 / 72.2))
ppm_no3_magboro = (kg_magboro * 1000.0 * 10.8) / (2600.0 / (197.3 / 72.2))
ppm_no3_nitamonio = ((kg_nitamonio * 1000.0) * 17.0) / denominador_agua

ppm_nh4_calcinit = ((kg_calcinit * 1000.0) * 1.1) / denominador_agua
ppm_nh4_nitamonio = ((kg_nitamonio * 1000.0) * 17.0) / denominador_agua

# Acumuladores para marcas nuevas creadas por el usuario
extra_no3_crudo, extra_nh4, extra_cao, extra_p2o5, extra_k2o, extra_mgo, extra_so3 = 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0
extra_fe, extra_mn, extra_zn, extra_cu, extra_b, extra_mo = 0.0, 0.0, 0.0, 0.0, 0.0, 0.0

for prod_n, kg_n in pesos_nuevos.items():
    if kg_n > 0:
        db_n = st.session_state.nuevos_fertilizantes[prod_n]
        extra_cao += ((kg_n * 1000.0) * db_n.get("CaO", 0.0)) / denominador_agua
        extra_p2o5 += ((kg_n * 1000.0) * db_n.get("P2O5", 0.0)) / denominador_agua
        extra_k2o += ((kg_n * 1000.0) * db_n.get("K2O", 0.0)) / denominador_agua
        extra_mgo += ((kg_n * 1000.0) * db_n.get("MgO", 0.0)) / denominador_agua
        extra_so3 += ((kg_n * 1000.0) * db_n.get("SO3", 0.0)) / denominador_agua
        extra_nh4 += ((kg_n * 1000.0) * db_n.get("NH4", 0.0)) / denominador_agua
        extra_no3_crudo += ((kg_n * 1000.0) * db_n.get("NO3", 0.0)) / denominador_agua
        
        extra_fe += ((kg_n * 1000.0) * db_n.get("Fe", 0.0)) / denominador_agua
        extra_mn += ((kg_n * 1000.0) * db_n.get("Mn", 0.0)) / denominador_agua
        extra_zn += ((kg_n * 1000.0) * db_n.get("Zn", 0.0)) / denominador_agua
        extra_cu += ((kg_n * 1000.0) * db_n.get("Cu", 0.0)) / denominador_agua
        extra_b += ((kg_n * 1000.0) * db_n.get("B", 0.0)) / denominador_agua
        extra_mo += ((kg_n * 1000.0) * db_n.get("Mo", 0.0)) / denominador_agua

# CONSOLIDACIÓN FINAL TOTAL DE PPM LOGRADAS
