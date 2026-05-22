import streamlit as st
import pandas as pd
from io import BytesIO
from datetime import datetime


# ============================================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================================

st.set_page_config(
    page_title="Consolidação M. Dias",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CSS
# ============================================================

st.markdown("""
<style>
/* ===== BASE ===== */
.stApp {
    background: #f6f8fb;
    color: #111827;
}

.block-container {
    max-width: 1180px;
    padding-top: 2rem;
    padding-left: 2rem;
    padding-right: 2rem;
}

/* ===== SIDEBAR ===== */
section[data-testid="stSidebar"] {
    background: #ffffff;
    border-right: 1px solid #e5e7eb;
}

section[data-testid="stSidebar"] * {
    color: #111827 !important;
}

/* ===== HERO ===== */
.hero {
    background: #ffffff;
    border: 1px solid #e5e7eb;
    border-radius: 18px;
    padding: 28px 32px;
    margin-bottom: 28px;
    box-shadow: 0 8px 24px rgba(15, 23, 42, 0.04);
}

.hero h1 {
    font-size: 30px;
    line-height: 1.2;
    font-weight: 800;
    color: #111827;
    margin: 0 0 8px 0;
}

.hero span {
    color: #2563eb;
}

.hero p {
    color: #6b7280;
    font-size: 15px;
    margin: 0;
}

/* ===== TÍTULOS ===== */
h2, h3 {
    color: #111827 !important;
}

h2 {
    font-size: 26px !important;
    margin-bottom: 18px !important;
}

/* ===== CARDS ===== */
.upload-card,
.action-card {
    background: #ffffff;
    border: 1px solid #e5e7eb;
    border-radius: 16px;
    padding: 20px;
    height: 170px;
    box-shadow: 0 6px 18px rgba(15, 23, 42, 0.04);
}

.upload-card h3,
.action-card h2 {
    color: #111827;
    font-size: 19px;
    line-height: 1.25;
    margin: 14px 0 8px 0;
}

.upload-card p,
.action-card p {
    color: #64748b;
    font-size: 14px;
    line-height: 1.5;
    margin: 0;
}

.badge {
    display: inline-block;
    background: #eff6ff;
    color: #1d4ed8;
    padding: 5px 10px;
    border-radius: 999px;
    font-size: 12px;
    font-weight: 700;
}

/* ===== UPLOADERS ===== */
[data-testid="stFileUploader"] {
    background: #ffffff;
    border: 1px dashed #cbd5e1;
    border-radius: 14px;
    padding: 10px 12px;
    min-height: 110px;
}

[data-testid="stFileUploader"] section {
    padding: 8px !important;
}

[data-testid="stFileUploader"] button {
    border-radius: 10px;
    height: 38px;
    font-size: 14px;
}

/* ===== BOTÕES ===== */
.stButton > button {
    height: 48px;
    width: 100%;
    border-radius: 12px;
    border: none;
    background: #2563eb;
    color: #ffffff;
    font-size: 15px;
    font-weight: 700;
}

.stButton > button:hover {
    background: #1d4ed8;
}

.stDownloadButton > button {
    height: 46px;
    width: 100%;
    border-radius: 12px;
    border: none;
    background: #16a34a;
    color: #ffffff;
    font-size: 15px;
    font-weight: 700;
}

/* ===== ALERTAS / STATUS ===== */
div[data-testid="stAlert"] {
    border-radius: 12px;
    padding: 12px 14px;
}

/* ===== MÉTRICAS ===== */
div[data-testid="stMetric"] {
    background: #ffffff;
    border: 1px solid #e5e7eb;
    padding: 16px;
    border-radius: 14px;
    box-shadow: 0 6px 18px rgba(15, 23, 42, 0.04);
}

/* ===== TABELA ===== */
[data-testid="stDataFrame"] {
    border-radius: 14px;
    border: 1px solid #e5e7eb;
    overflow: hidden;
}

/* ===== LIMPEZA STREAMLIT ===== */
#MainMenu,
footer,
header {
    visibility: hidden;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# FUNÇÕES DE APOIO
# ============================================================

def normalizar_colunas(df):
    df.columns = (
        df.columns.astype(str)
        .str.strip()
        .str.replace("\n", " ", regex=False)
        .str.replace("\r", " ", regex=False)
    )
    return df


def normalizar_texto(texto):
    return (
        str(texto)
        .lower()
        .strip()
        .replace("\n", " ")
        .replace("\r", " ")
        .replace("_", " ")
        .replace("-", " ")
        .replace("º", "")
        .replace("°", "")
        .replace("ã", "a")
        .replace("á", "a")
        .replace("à", "a")
        .replace("â", "a")
        .replace("é", "e")
        .replace("ê", "e")
        .replace("í", "i")
        .replace("ó", "o")
        .replace("ô", "o")
        .replace("õ", "o")
        .replace("ú", "u")
        .replace("ç", "c")
    )


def encontrar_coluna(df, possibilidades):
    mapa = {}

    for coluna in df.columns:
        mapa[normalizar_texto(coluna)] = coluna

    for possibilidade in possibilidades:
        possibilidade_norm = normalizar_texto(possibilidade)

        for coluna_norm, coluna_original in mapa.items():
            if possibilidade_norm in coluna_norm:
                return coluna_original

    return None


def limpar_remessa(valor):
    if pd.isna(valor):
        return ""

    valor = str(valor).strip()
    valor = valor.replace(".0", "")
    valor = "".join(filter(str.isdigit, valor))

    return valor.lstrip("0") if valor else ""


def remover_linhas_vazias(df):
    return df.dropna(how="all")


def converter_numero(valor):
    if pd.isna(valor):
        return 0

    valor = str(valor).strip()

    if valor == "":
        return 0

    valor = valor.replace(".", "")
    valor = valor.replace(",", ".")

    return pd.to_numeric(valor, errors="coerce")


# ============================================================
# LEITURA DOS RELATÓRIOS
# ============================================================

def ler_base_principal(arquivo):
    excel = pd.ExcelFile(arquivo)

    if "Remessa" in excel.sheet_names:
        df = pd.read_excel(arquivo, sheet_name="Remessa", dtype=str)
        df = normalizar_colunas(df)
        df = remover_linhas_vazias(df)
        return df

    for aba in excel.sheet_names:
        df = pd.read_excel(arquivo, sheet_name=aba, dtype=str)
        df = normalizar_colunas(df)
        df = remover_linhas_vazias(df)

        if encontrar_coluna(df, ["Remessa", "Remessas", "ID Remessa"]):
            return df

    raise ValueError("não encontrei nenhuma aba com coluna de remessa na base principal.")


def ler_relatorio_gm(arquivo):
    for header in range(0, 10):
        df = pd.read_excel(
            arquivo,
            sheet_name=0,
            header=header,
            dtype=str
        )

        df = normalizar_colunas(df)
        df = remover_linhas_vazias(df)

        if encontrar_coluna(df, ["Remessa", "Remessas", "ID Remessa"]):
            return df

    raise ValueError("não encontrei a coluna de remessa no relatório GM Ana.")


def ler_relatorio_gw(arquivo):
    for header in range(0, 12):
        df = pd.read_excel(
            arquivo,
            sheet_name=0,
            header=header,
            dtype=str
        )

        df = normalizar_colunas(df)
        df = remover_linhas_vazias(df)

        if encontrar_coluna(
            df,
            [
                "Remessa",
                "Remessas",
                "ID Remessa",
                "Numero Carga",
                "Número Carga",
                "Carga"
            ]
        ):
            return df

    raise ValueError("não encontrei a coluna de remessa no relatório GW.")


# ============================================================
# CONSOLIDAÇÃO
# ============================================================

def consolidar_bases(base_principal, relatorio_gm, relatorio_gw):
    base = ler_base_principal(base_principal)
    gm = ler_relatorio_gm(relatorio_gm)
    gw = ler_relatorio_gw(relatorio_gw)

    col_base = encontrar_coluna(
        base,
        ["Remessa", "Remessas", "ID Remessa"]
    )

    col_gm = encontrar_coluna(
        gm,
        ["Remessa", "Remessas", "ID Remessa"]
    )

    col_gw = encontrar_coluna(
        gw,
        [
            "Remessa",
            "Remessas",
            "ID Remessa",
            "Numero Carga",
            "Número Carga",
            "Carga"
        ]
    )

    if not col_base:
        raise ValueError("não encontrei a coluna de remessa na base principal.")

    if not col_gm:
        raise ValueError("não encontrei a coluna de remessa no relatório GM Ana.")

    if not col_gw:
        raise ValueError("não encontrei a coluna de remessa no relatório GW.")

    base["Remessa_Chave"] = base[col_base].apply(limpar_remessa)
    gm["Remessa_Chave"] = gm[col_gm].apply(limpar_remessa)
    gw["Remessa_Chave"] = gw[col_gw].apply(limpar_remessa)

    base = base[base["Remessa_Chave"] != ""]
    gm = gm[gm["Remessa_Chave"] != ""]
    gw = gw[gw["Remessa_Chave"] != ""]

    # ========================================================
    # RELATÓRIO ANA
    # mantém todas as linhas, porque cada linha é uma entrega
    # ========================================================

    colunas_gm = [
        "Remessa_Chave",
        encontrar_coluna(gm, ["Cidade Origem", "Cidade Remetente"]),
        encontrar_coluna(gm, ["Cliente", "Nome Cliente"]),
        encontrar_coluna(gm, ["Cidade Destino"]),
        encontrar_coluna(gm, ["Estado Destino", "Estado Destinatario", "Estado Destinatário"]),
        encontrar_coluna(gm, ["Volume", "Volumes"]),
        encontrar_coluna(gm, ["Placa", "PLACA"]),
        encontrar_coluna(gm, ["Motorista", "Condutor", "Nome Motorista", "Nome Condutor"]),
        encontrar_coluna(gm, ["Dt Oferta", "Data Oferta", "Data Ofertada"]),
        encontrar_coluna(gm, ["Data Liberação", "Data Liberacao"]),
        encontrar_coluna(gm, ["KM Original"]),
        encontrar_coluna(gm, ["KM Complementar", "Complementar"]),
        encontrar_coluna(gm, ["Dt Inicio Rota", "Data Inicio Rota", "Inicio Rota", "Início Rota"]),
        encontrar_coluna(gm, ["Dt Fim Rota", "Data Fim Rota", "Fim Rota"]),
    ]

    colunas_gm = [coluna for coluna in colunas_gm if coluna is not None]

    gm_final = gm[colunas_gm].copy()

    # renomeia placa e motorista do GM para evitar conflito com base/GW
    col_placa_gm = encontrar_coluna(gm_final, ["Placa", "PLACA"])
    col_motorista_gm = encontrar_coluna(gm_final, ["Motorista", "Condutor", "Nome Motorista", "Nome Condutor"])

    renomear_gm = {}

    if col_placa_gm:
        renomear_gm[col_placa_gm] = "Placa_Ana"

    if col_motorista_gm:
        renomear_gm[col_motorista_gm] = "Motorista_Ana"

    gm_final = gm_final.rename(columns=renomear_gm)

    # ========================================================
    # RELATÓRIO GW
    # mantém uma linha por carga/remessa
    # usado principalmente para emissão
    # ========================================================

    colunas_gw = [
        "Remessa_Chave",
        encontrar_coluna(gw, ["Emissão CT-e", "Emissao CT-e", "Dt emissão CTE", "Data emissão CTE"]),
        encontrar_coluna(gw, ["Data Chegada"]),
        encontrar_coluna(gw, ["Data Entrega"]),
    ]

    colunas_gw = [coluna for coluna in colunas_gw if coluna is not None]

    gw_final = gw[colunas_gw].drop_duplicates(subset=["Remessa_Chave"])

    # ========================================================
    # MERGES
    # base + ana: pode multiplicar linhas para trazer entregas
    # gw: complementa por remessa/carga
    # ========================================================

    consolidado = base.merge(
        gm_final,
        on="Remessa_Chave",
        how="inner",
        suffixes=("", "_Base")
    )   

    consolidado = consolidado.merge(
        gw_final,
        on="Remessa_Chave",
        how="left",
        suffixes=("", "_GW")
    )

    # ========================================================
    # MAPA FINAL
    # ========================================================

    mapa_final = {
        "Remessas": encontrar_coluna(
            consolidado,
            ["Remessa", "Remessas", "ID Remessa"]
        ),

        "Cidade Remetente": encontrar_coluna(
            consolidado,
            ["Cidade Origem", "Cidade Remetente"]
        ),

        "Nome Cliente": encontrar_coluna(
            consolidado,
            ["Cliente", "Nome Cliente"]
        ),

        "Cidade Destino": encontrar_coluna(
            consolidado,
            ["Cidade Destino"]
        ),

        "Número de Cidades": encontrar_coluna(
            consolidado,
            ["Número de cidades", "Numero de cidades"]
        ),

        "Número de Paradas": encontrar_coluna(
            consolidado,
            ["Número de Paradas", "Numero de Paradas"]
        ),

        "Estado Destino": encontrar_coluna(
            consolidado,
            ["Estado Destino", "Estado Destinatario", "Estado Destinatário"]
        ),

        "Volumes": encontrar_coluna(
            consolidado,
            ["Volumes", "Volume"]
        ),

        "Peso Bruto": encontrar_coluna(
            consolidado,
            ["Peso Bruto"]
        ),

        "Dt de emissão": encontrar_coluna(
            consolidado,
            ["Dt emissão CTE", "Data emissão CTE", "Emissão CT-e", "Emissao CT-e"]
        ),

        "Inicio Rota": encontrar_coluna(
            consolidado,
            ["Dt Inicio Rota", "Data Inicio Rota", "Inicio Rota", "Início Rota"]
        ),

        "Fim Rota": encontrar_coluna(
            consolidado,
            ["Dt Fim Rota", "Data Fim Rota", "Fim Rota"]
        ),

        "Região": encontrar_coluna(
            consolidado,
            ["Região", "Regiao"]
        ),

        "Cidades": encontrar_coluna(
            consolidado,
            ["Cidades"]
        ),

        "KM Original": encontrar_coluna(
            consolidado,
            ["KM Original"]
        ),

        "Complementar": encontrar_coluna(
            consolidado,
            ["KM Complementar", "Complementar"]
        ),

        "Custo Total": encontrar_coluna(
            consolidado,
            ["Custo Total"]
        ),

        "Tipo Veículo": encontrar_coluna(
            consolidado,
            ["Tipo Veículo", "Tipo Veiculo"]
        ),

        "Data Oferta": encontrar_coluna(
            consolidado,
            ["Dt Oferta", "Data Oferta", "Data Ofertada"]
        ),

        "Data Liberação": encontrar_coluna(
            consolidado,
            ["Data Liberação", "Data Liberacao"]
        ),

        "Data OTM": encontrar_coluna(
            consolidado,
            ["Data OTM"]
        ),

        # prioridade total para o relatório Ana
        "Motorista": encontrar_coluna(
            consolidado,
            ["Motorista_Ana", "Motorista", "Condutor", "Nome Motorista", "Nome Condutor"]
        ),

        # prioridade total para o relatório Ana
        "Placa": encontrar_coluna(
            consolidado,
            ["Placa_Ana", "Placa", "PLACA"]
        ),
    }

    base_final = pd.DataFrame()

    for nome_final, coluna_origem in mapa_final.items():
        if coluna_origem and coluna_origem in consolidado.columns:
            base_final[nome_final] = consolidado[coluna_origem]
        else:
            base_final[nome_final] = ""

    # ========================================================
    # KM TOTAL
    # ========================================================

    base_final["KM Original"] = base_final["KM Original"].apply(converter_numero)
    base_final["Complementar"] = base_final["Complementar"].apply(converter_numero)

    base_final["KM Total"] = (
        base_final["KM Original"].fillna(0)
        +
        base_final["Complementar"].fillna(0)
    )

    ordem_final = [
        "Remessas",
        "Cidade Remetente",
        "Nome Cliente",
        "Cidade Destino",
        "Número de Cidades",
        "Número de Paradas",
        "Estado Destino",
        "Volumes",
        "Peso Bruto",
        "Dt de emissão",
        "Inicio Rota",
        "Fim Rota",
        "Região",
        "Cidades",
        "KM Original",
        "Complementar",
        "KM Total",
        "Custo Total",
        "Tipo Veículo",
        "Data Oferta",
        "Data Liberação",
        "Data OTM",
        "Motorista",
        "Placa",
    ]

    return base_final[ordem_final]


# ============================================================
# GERAR EXCEL
# ============================================================

def gerar_excel_download(df):
    saida = BytesIO()

    with pd.ExcelWriter(saida, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Base Consolidada")

        ws = writer.sheets["Base Consolidada"]
        ws.freeze_panes = "A2"
        ws.auto_filter.ref = ws.dimensions

        for coluna in ws.columns:
            maior = 0
            letra = coluna[0].column_letter

            for celula in coluna:
                if celula.value:
                    maior = max(maior, len(str(celula.value)))

            ws.column_dimensions[letra].width = min(maior + 3, 45)

    return saida.getvalue()


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:
    st.markdown("## 📊 M. Dias")
    st.markdown("### Consolidação")
    st.markdown("---")
    st.markdown("🏠 **Início**")
    st.markdown("📁 **Importar relatórios**")
    st.markdown("🧩 **Consolidar base**")
    st.markdown("---")
    st.info("Ferramenta interna para consolidar relatórios operacionais.")


# ============================================================
# INTERFACE
# ============================================================

st.markdown("""
<div class="hero">
    <h1>Consolidação de Relatórios <span>M. Dias</span></h1>
    <p>Importe os relatórios operacionais e gere uma base final consolidada para análise.</p>
</div>
""", unsafe_allow_html=True)


st.markdown("## 1. Importar relatórios")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="upload-card">
        <span class="badge">Arquivo 01</span>
        <h3>Base principal / Remessas</h3>
        <p>Base com as remessas que serão enriquecidas.</p>
    </div>
    """, unsafe_allow_html=True)

    base_principal = st.file_uploader(
        "Selecionar base principal",
        type=["xlsx", "xls"],
        key="base_principal"
    )

with col2:
    st.markdown("""
    <div class="upload-card">
        <span class="badge">Arquivo 02</span>
        <h3>Relatório GM Ana</h3>
        <p>Relatório com entregas, cidade destino, placa e motorista.</p>
    </div>
    """, unsafe_allow_html=True)

    relatorio_gm = st.file_uploader(
        "Selecionar relatório GM Ana",
        type=["xlsx", "xls"],
        key="relatorio_gm"
    )

with col3:
    st.markdown("""
    <div class="upload-card">
        <span class="badge">Arquivo 03</span>
        <h3>Relatório GW</h3>
        <p>Relatório com carga e emissão do CT-e.</p>
    </div>
    """, unsafe_allow_html=True)

    relatorio_gw = st.file_uploader(
        "Selecionar relatório GW",
        type=["xlsx", "xls"],
        key="relatorio_gw"
    )


st.markdown("## Status dos arquivos")

s1, s2, s3 = st.columns(3)

with s1:
    if base_principal:
        st.success("Base principal carregada")
    else:
        st.warning("Base principal pendente")

with s2:
    if relatorio_gm:
        st.success("Relatório GM Ana carregado")
    else:
        st.warning("Relatório GM Ana pendente")

with s3:
    if relatorio_gw:
        st.success("Relatório GW carregado")
    else:
        st.warning("Relatório GW pendente")


st.markdown("""
<div class="action-card">
    <h2>2. Consolidar base</h2>
    <p>Clique no botão abaixo para cruzar os relatórios e gerar o arquivo final.</p>
</div>
""", unsafe_allow_html=True)


botao = st.button("🚀 Consolidar relatórios")

if botao:
    if not base_principal or not relatorio_gm or not relatorio_gw:
        st.error("Envie os três arquivos antes de consolidar.")
    else:
        try:
            with st.spinner("Consolidando relatórios..."):
                df_consolidado = consolidar_bases(
                    base_principal,
                    relatorio_gm,
                    relatorio_gw
                )

                arquivo_excel = gerar_excel_download(df_consolidado)

            st.success("Base consolidada com sucesso.")

            k1, k2, k3 = st.columns(3)

            with k1:
                st.metric("Linhas geradas", len(df_consolidado))

            with k2:
                st.metric("Colunas finais", len(df_consolidado.columns))

            with k3:
                st.metric("Status", "Concluído")

            st.markdown("### Prévia da base consolidada")
            st.dataframe(df_consolidado.head(50), use_container_width=True)

            st.download_button(
                label="⬇️ Baixar BASE_CONSOLIDADA_MDIAS.xlsx",
                data=arquivo_excel,
                file_name="BASE_CONSOLIDADA_MDIAS.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

        except Exception as erro:
            st.error(f"Erro ao consolidar: {erro}")


# ============================================================
# RODAPÉ
# ============================================================

st.markdown("---")

arquivos_enviados = sum([
    base_principal is not None,
    relatorio_gm is not None,
    relatorio_gw is not None
])

r1, r2, r3 = st.columns(3)

with r1:
    st.metric("Arquivos enviados", f"{arquivos_enviados}/3")

with r2:
    st.metric(
        "Status",
        "Pronto" if arquivos_enviados == 3 else "Aguardando"
    )

with r3:
    st.metric("Versão", "1.0")

st.caption(
    f"Sistema interno • Consolidação operacional M. Dias • {datetime.now().strftime('%d/%m/%Y')}"
)
