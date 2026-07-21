import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# ==================================================
# CONFIGURACIÓN DE LA PÁGINA
# ==================================================

st.set_page_config(
    page_title="Dashboard Comercial - BancaServicios",
    page_icon="📊",
    layout="wide"
)

# ==================================================
# ESTILOS
# ==================================================

st.markdown("""
<style>

.main{
    background-color:#f5f7fa;
}

div[data-testid="metric-container"]{
    background-color:white;
    border-radius:12px;
    padding:20px;
    box-shadow:0px 2px 8px rgba(0,0,0,0.10);
}

h1{
    color:#003366;
}

</style>
""", unsafe_allow_html=True)

# ==================================================
# CARGAR DATOS
# ==================================================

@st.cache_data
def cargar_datos():
    return pd.read_csv("consulta6.csv")

df = cargar_datos()

# ==================================================
# SIDEBAR
# ==================================================

st.sidebar.title("📌 Filtros")

regional = st.sidebar.selectbox(
    "Regional",
    ["Todas"] + sorted(df["regional"].unique())
)

if regional != "Todas":
    df = df[df["regional"] == regional]

# ==================================================
# TÍTULO
# ==================================================

st.title("📊 Dashboard Comercial - BancaServicios")

st.caption(
    "Monitoreo comercial para Directores Regionales"
)

st.write(
    f"**Última actualización:** {datetime.now().strftime('%d/%m/%Y')}"
)

st.divider()

# ==================================================
# KPIs
# ==================================================

total_polizas = int(df["polizas_vigentes"].sum())

prima_total = df["prima_total_vigente"].sum()

efectividad = df["tasa_efectividad"].mean()

kpi1, kpi2, kpi3 = st.columns(3)

kpi1.metric(
    "📄 Pólizas Vigentes",
    f"{total_polizas:,}"
)

kpi2.metric(
    "💰 Prima Total Vigente",
    f"${prima_total:,.0f}"
)

kpi3.metric(
    "📈 Efectividad Promedio",
    f"{efectividad:.2f}%"
)

st.divider()

# ==================================================
# GRÁFICO
# ==================================================

st.subheader("Prima Total Vigente por Regional")

grafico = (
    df.groupby("regional", as_index=False)
      .agg({"prima_total_vigente":"sum"})
)

fig = px.bar(

    grafico,

    x="regional",

    y="prima_total_vigente",

    text_auto=".2s",

    color="prima_total_vigente",

    color_continuous_scale="Blues"

)

fig.update_layout(

    xaxis_title="Regional",

    yaxis_title="Prima Total",

    plot_bgcolor="white"

)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.divider()

# ==================================================
# TOP 10
# ==================================================

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

]

top10["prima_total_vigente"] = top10["prima_total_vigente"].map(

    lambda x:f"${x:,.0f}"

)

top10["tasa_efectividad"] = top10["tasa_efectividad"].map(

    lambda x:f"{x:.2f}%"

)

st.dataframe(

    top10,

    use_container_width=True,

    hide_index=True

)

st.divider()

# ==================================================
# INSIGHTS
# ==================================================

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

Prima total: **${mejor_regional['prima_total_vigente']:,.0f}**

"""

)

st.info(

    f"""

**Asesor con mayor prima vigente:** **{mejor_asesor['asesor']}**

Regional: **{mejor_asesor['regional']}**

Prima: **${mejor_asesor['prima_total_vigente']:,.0f}**

Efectividad: **{mejor_asesor['tasa_efectividad']:.2f}%**

"""

)

st.divider()

# ==================================================
# TABLA GENERAL
# ==================================================

st.subheader("Detalle General")

tabla = df.copy()

tabla["prima_total_vigente"] = tabla["prima_total_vigente"].map(

    lambda x:f"${x:,.0f}"

)

tabla["tasa_efectividad"] = tabla["tasa_efectividad"].map(

    lambda x:f"{x:.2f}%"

)

st.dataframe(

    tabla,

    use_container_width=True,

    hide_index=True

)