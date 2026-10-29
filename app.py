import streamlit as st

st.set_page_config(page_title="Depuración de Nitrógeno", layout="wide")

st.title("🧪 Prueba de Diagnóstico Directo de Nitrógeno")
st.write("Si este código funciona bien, habremos encontrado el error de la página web de raíz.")

# 1. Variables fijas de volumen y kilogramos idénticas a nuestro ejercicio manual
volumen_agua = 26000.0
denominador = volumen_agua * 0.1

kg_calcinit = 5.10
kg_pony = 5.30
kg_magboro = 4.19

# 2. Operaciones matemáticas puras sin condicionales ni diccionarios
ppm_no3_calcinit = (kg_calcinit * 1000.0 * 14.4) / denominador
ppm_no3_pony = (kg_pony * 1000.0 * 13.0) / denominador
ppm_no3_magboro = (kg_magboro * 1000.0 * 10.8) / denominador

# 3. Sumatoria total de Nitrógeno Nitratado
total_no3_real = ppm_no3_calcinit + ppm_no3_pony + ppm_no3_magboro

# ==========================================
# DESPLIEGUE EN PANTALLA
# ==========================================
st.markdown("---")
st.header("📊 Resultados de la Simulación en Tiempo Real")

st.write(f"• **Aporte NO₃⁻ del YaraLiva CALCINIT (5.10 Kg):** `{ppm_no3_calcinit:.1f}` PPM")
st.write(f"• **Aporte NO₃⁻ del Poly-Feed Pony (5.30 Kg):** `{ppm_no3_pony:.1f}` PPM")
st.write(f"• **Aporte NO₃⁻ del Van Iperen Magboro (4.19 Kg):** `{ppm_no3_magboro:.1f}` PPM")

st.markdown("### 🚨 TOTAL DE NITRÓGENO NITRATADO LOGRADO:")
st.success(f"**Resultado Final en Pantalla:** `{total_no3_real:.1f}` PPM")
st.write("*(El valor esperado que calculamos en la libreta es de 197.3 PPM)*")
