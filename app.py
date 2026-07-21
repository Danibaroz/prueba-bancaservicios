import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# Configuracion de la pgina
st.set_page_config(
    page_title="Dashboard Comercial - BancaServicios",
    page_icon="📊",
    layout="wide"
)

# Estilos
st.markdown("""
<style>
.main{
    background-color:#f5f7fa;
}

div[data-testid="metric-container"]{
    background-color:white;
    border-radius:12px;
    padding:18px;
    box-shadow:0px 2px 8px rgba(0,0,0,0.10);
}

h1{
    color:#003366;
}
</style>
""", unsafe_allow_html=True)

# Cargar datos
@st.cache_data
def cargar_datos():
    return pd.read_csv("consulta6.csv")

df = cargar_datos()

# Función para formato de moneda
def formato_moneda(valor):
    return f"$ {valor:,.0f}".replace(",", ".")

# ------------------------
# Sidebar
# ------------------------

st.sidebar.title("📌 Filtros")

# Filtro por Regional
regionales = ["Todas"] + sorted(df["regional"].unique().tolist())

regional = st.sidebar.selectbox(
    "Regional",
    regionales
)

if regional != "Todas":
    df = df[df["regional"] == regional]

# Filtro por Asesor
asesores = ["Todos"] + sorted(df["asesor"].unique().tolist())

asesor = st.sidebar.selectbox(
    "Asesor",
    asesores
)

if asesor != "Todos":
    df = df[df["asesor"] == asesor]

# ------------------------
# Titulo
# ------------------------

st.title("📊 Dashboard Comercial - BancaServicios")

st.caption("Monitoreo comercial para Directores Regionales")

st.write(
    f"**Última actualización:** {datetime.now().strftime('%d/%m/%Y')}"
)

st.divider()

# ------------------------
# KPIs
# ------------------------

total_polizas = int(df["polizas_vigentes"].sum())
prima_total = df["prima_total_vigente"].sum()
efectividad = df["tasa_efectividad"].mean()

col1, col2, col3 = st.columns(3)

col1.metric(
    "📄 Pólizas Vigentes",
    f"{total_polizas:,}".replace(",", ".")
)

col2.metric(
    "💰 Prima Total Vigente",
    formato_moneda(prima_total)
)

col3.metric(
    "📈 Efectividad Promedio",
    f"{efectividad:.2f}%"
)

st.caption("Los indicadores cambian automáticamente según los filtros seleccionados.")

st.divider()

# ------------------------
# Grafico
# ------------------------

st.subheader("Prima Total Vigente por Regional")

grafico = (
    df.groupby("regional", as_index=False)
      .agg({"prima_total_vigente": "sum"})
)

fig = px.bar(
    grafico,
    x="prima_total_vigente",
    y="regional",
    orientation="h",
    color="prima_total_vigente",
    color_continuous_scale="Blues",
    text="prima_total_vigente"
)

fig.update_traces(
    texttemplate="$ %{text:,.0f}",
    textposition="outside"
)

fig.update_layout(
    xaxis_title="Prima Total Vigente",
    yaxis_title="Regional",
    coloraxis_showscale=False,
    plot_bgcolor="white"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.divider()

# ------------------------
# Top 10
# ------------------------

st.subheader("🏆 Top 10 Asesores por Prima Vigente")

top10 = (
    df.sort_values(
        "prima_total_vigente",
        ascending=False
    )
    .head(10)
)

top10 = top10[
    [
        "asesor",
        "regional",
        "polizas_vigentes",
        "prima_total_vigente",
        "tasa_efectividad"
    ]
].copy()

top10["prima_total_vigente"] = top10["prima_total_vigente"].apply(formato_moneda)

top10["tasa_efectividad"] = top10["tasa_efectividad"].map(
    lambda x: f"{x:.2f}%"
)

st.dataframe(
    top10,
    use_container_width=True,
    hide_index=True
)

st.divider()

# ------------------------
# Hallazgos
# ------------------------

st.subheader("💡 Hallazgos Automáticos")

mejor_regional = (
    grafico.sort_values(
        "prima_total_vigente",
        ascending=False
    )
    .iloc[0]
)

mejor_asesor = (
    df.sort_values(
        "prima_total_vigente",
        ascending=False
    )
    .iloc[0]
)

st.success(
    f"""
**Regional con mayor prima vigente:** **{mejor_regional['regional']}**

**Prima total:** **{formato_moneda(mejor_regional['prima_total_vigente'])}**
"""
)

st.info(
    f"""
**Asesor con mayor prima vigente:** **{mejor_asesor['asesor']}**

**Regional:** **{mejor_asesor['regional']}**

**Prima vigente:** **{formato_moneda(mejor_asesor['prima_total_vigente'])}**

**Efectividad:** **{mejor_asesor['tasa_efectividad']:.2f}%**
"""
)

st.divider()

# ------------------------
# Tabla General
# ------------------------

st.subheader("Detalle General")

tabla = df.copy()

tabla["prima_total_vigente"] = tabla["prima_total_vigente"].apply(formato_moneda)

tabla["tasa_efectividad"] = tabla["tasa_efectividad"].map(
    lambda x: f"{x:.2f}%"
)

st.dataframe(
    tabla,
    use_container_width=True,
    hide_index=True
)

st.divider()

# ------------------------
# Resumen Ejecutivo
# ------------------------

st.subheader("📌 Resumen Ejecutivo")

st.markdown(f"""
- Se analizaron **{len(df)} asesores** según los filtros seleccionados.
- La **regional con mayor prima vigente** es **{mejor_regional['regional']}**.
- El **asesor con mayor prima vigente** es **{mejor_asesor['asesor']}**.
- La **prima total vigente** asciende a **{formato_moneda(prima_total)}**.
- La **efectividad promedio** es de **{efectividad:.2f}%**.
""")
