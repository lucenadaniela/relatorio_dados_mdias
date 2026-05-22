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
    initial_sidebar_state="expanded",
)


# ============================================================
# CSS
# ============================================================

st.markdown(
    """
<style>
:root {
    --bg: #f5f7fa;
    --surface: #ffffff;
    --surface-soft: #f8fafc;
    --text: #111827;
    --muted: #64748b;
    --line: #e2e8f0;
    --line-strong: #cbd5e1;
    --primary: #1f5eff;
    --primary-dark: #1747c8;
    --success: #15803d;
    --warning: #b45309;
    --danger: #b91c1c;
    --radius: 12px;
}

html, body, [class*="css"] {
    font-family: Inter, "Segoe UI", system-ui, -apple-system, BlinkMacSystemFont, sans-serif;
}

.stApp {
    background:
        linear-gradient(180deg, #f8fafc 0%, #f5f7fa 32%, #f5f7fa 100%);
    color: var(--text);
}

.block-container {
    max-width: 1240px;
    padding: 32px 40px 28px;
}

h1, h2, h3, p {
    letter-spacing: 0;
}

h2 {
    color: var(--text) !important;
    font-size: 21px !important;
    line-height: 1.25 !important;
    font-weight: 750 !important;
    margin: 0 0 16px !important;
}

h3 {
    color: var(--text) !important;
    font-size: 16px !important;
    font-weight: 700 !important;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #ffffff;
    border-right: 1px solid var(--line);
}

section[data-testid="stSidebar"] > div {
    padding: 28px 20px;
}

section[data-testid="stSidebar"] * {
    color: var(--text) !important;
}

.brand {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 26px;
}

.brand-mark {
    width: 34px;
    height: 34px;
    border-radius: 10px;
    display: grid;
    place-items: center;
    color: #ffffff;
    font-weight: 800;
    font-size: 12px;
    background: linear-gradient(135deg, #1646d8, #22a06b);
}

.brand-title {
    font-size: 17px;
    font-weight: 780;
    line-height: 1.1;
}

.brand-subtitle {
    color: var(--muted) !important;
    font-size: 12px;
    margin-top: 3px;
}

.side-nav {
    display: grid;
    gap: 6px;
    margin: 18px 0 28px;
}

.side-item {
    display: flex;
    align-items: center;
    gap: 10px;
    height: 40px;
    padding: 0 12px;
    border-radius: 10px;
    color: #334155 !important;
    font-size: 14px;
    font-weight: 650;
}

.side-item.active {
    background: #eef4ff;
    color: #1747c8 !important;
}

.side-note {
    border: 1px solid var(--line);
    background: var(--surface-soft);
    border-radius: var(--radius);
    padding: 14px;
    color: var(--muted) !important;
    font-size: 13px;
    line-height: 1.45;
}

/* Header */
.topbar {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    gap: 24px;
    margin-bottom: 26px;
}

.eyebrow {
    color: var(--primary);
    font-size: 12px;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: .08em;
    margin-bottom: 9px;
}

.page-title {
    color: var(--text);
    font-size: 34px;
    line-height: 1.08;
    font-weight: 820;
    margin: 0;
}

.page-copy {
    color: var(--muted);
    max-width: 680px;
    font-size: 15px;
    line-height: 1.55;
    margin: 12px 0 0;
}

.run-date {
    min-width: 154px;
    text-align: right;
    color: var(--muted);
    font-size: 13px;
    padding-top: 4px;
}

/* Panels */
.panel {
    background: var(--surface);
    border: 1px solid var(--line);
    border-radius: var(--radius);
    padding: 20px;
}

.panel + .panel {
    margin-top: 18px;
}

.section-head {
    display: flex;
    justify-content: space-between;
    gap: 16px;
    align-items: flex-end;
    margin-bottom: 14px;
}

.section-kicker {
    color: var(--muted);
    font-size: 13px;
    margin-top: -8px;
}

.upload-intro {
    border: 1px solid var(--line);
    border-radius: var(--radius);
    padding: 16px;
    min-height: 132px;
    background: #ffffff;
}

.file-step {
    display: inline-flex;
    align-items: center;
    height: 26px;
    padding: 0 10px;
    border-radius: 999px;
    background: #eef4ff;
    color: #1747c8;
    font-size: 12px;
    font-weight: 750;
    margin-bottom: 14px;
}

.upload-intro h3 {
    margin: 0 0 8px;
}

.upload-intro p {
    margin: 0;
    color: var(--muted);
    font-size: 13px;
    line-height: 1.48;
}

/* File uploader */
[data-testid="stFileUploader"] {
    background: #ffffff !important;
    border: 1px dashed var(--line-strong) !important;
    border-radius: var(--radius) !important;
    padding: 12px !important;
    margin-top: 10px;
}

[data-testid="stFileUploader"] section {
    background: #ffffff !important;
    border: 0 !important;
    padding: 0 !important;
}

[data-testid="stFileUploader"] section > div {
    color: var(--muted) !important;
}

[data-testid="stFileUploader"] label {
    color: #334155 !important;
    font-size: 13px !important;
    font-weight: 650 !important;
}

[data-testid="stFileUploader"] small {
    color: var(--muted) !important;
}

[data-testid="stFileUploader"] button {
    background: #f8fafc !important;
    color: var(--text) !important;
    border: 1px solid var(--line-strong) !important;
    border-radius: 9px !important;
    font-weight: 700 !important;
    min-height: 36px !important;
}

[data-testid="stFileUploader"] button:hover {
    border-color: #94a3b8 !important;
    background: #f1f5f9 !important;
}

/* Status */
.status-grid {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 12px;
}

.status-chip {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
    border: 1px solid var(--line);
    border-radius: 10px;
    padding: 12px 14px;
    background: var(--surface-soft);
}

.status-label {
    font-size: 13px;
    font-weight: 700;
    color: #334155;
}

.status-pill {
    border-radius: 999px;
    padding: 5px 9px;
    font-size: 12px;
    font-weight: 800;
}

.status-ok {
    background: #dcfce7;
    color: #166534;
}

.status-wait {
    background: #fff7ed;
    color: #9a3412;
}

/* Buttons */
.stButton > button,
.stDownloadButton > button {
    width: 100%;
    min-height: 46px;
    border-radius: 10px;
    border: 1px solid transparent;
    font-size: 14px;
    font-weight: 760;
    box-shadow: none;
}

.stButton > button {
    background: var(--primary);
    color: #ffffff;
}

.stButton > button:hover {
    background: var(--primary-dark);
    color: #ffffff;
    border-color: var(--primary-dark);
}

.stDownloadButton > button {
    background: var(--success);
    color: #ffffff;
}

.stDownloadButton > button:hover {
    background: #166534;
    color: #ffffff;
}

div[data-testid="stAlert"] {
    border-radius: 10px;
    border: 1px solid var(--line);
}

div[data-testid="stMetric"] {
    background: #ffffff;
    border: 1px solid var(--line);
    border-radius: 10px;
    padding: 14px 16px;
}

div[data-testid="stMetric"] label {
    color: var(--muted) !important;
}

[data-testid="stDataFrame"] {
    border: 1px solid var(--line);
    border-radius: 10px;
    overflow: hidden;
}

.footer {
    color: var(--muted);
    font-size: 12px;
    margin-top: 24px;
    padding-top: 18px;
    border-top: 1px solid var(--line);
}

#MainMenu, footer, header {
    visibility: hidden;
}

@media (max-width: 900px) {
    .block-container {
        padding: 22px 18px;
    }

    .topbar {
        display: block;
    }

    .run-date {
        text-align: left;
        margin-top: 14px;
    }

    .page-title {
        font-size: 28px;
    }

    .status-grid {
        grid-template-columns: 1fr;
    }
}
</style>
""",
    unsafe_allow_html=True,
)


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


def status_badge(carregado):
    classe = "status-ok" if carregado else "status-wait"
    texto = "Carregado" if carregado else "Pendente"
    return f'<span class="status-pill {classe}">{texto}</span>'


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

    raise ValueError("Não encontrei nenhuma aba com coluna de remessa na base principal.")


def ler_relatorio_gm(arquivo):
    for header in range(0, 10):
        df = pd.read_excel(
            arquivo,
            sheet_name=0,
            header=header,
            dtype=str,
        )

        df = normalizar_colunas(df)
        df = remover_linhas_vazias(df)

        if encontrar_coluna(df, ["Remessa", "Remessas", "ID Remessa"]):
            return df

    raise ValueError("Não encontrei a coluna de remessa no relatório GM Ana.")


def ler_relatorio_gw(arquivo):
    for header in range(0, 12):
        df = pd.read_excel(
            arquivo,
            sheet_name=0,
            header=header,
            dtype=str,
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
                "Carga",
            ],
        ):
            return df

    raise ValueError("Não encontrei a coluna de remessa no relatório GW.")


# ============================================================
# CONSOLIDAÇÃO
# ============================================================

def consolidar_bases(base_principal, relatorio_gm, relatorio_gw):
    base = ler_base_principal(base_principal)
    gm = ler_relatorio_gm(relatorio_gm)
    gw = ler_relatorio_gw(relatorio_gw)

    col_base = encontrar_coluna(base, ["Remessa", "Remessas", "ID Remessa"])
    col_gm = encontrar_coluna(gm, ["Remessa", "Remessas", "ID Remessa"])
    col_gw = encontrar_coluna(
        gw,
        [
            "Remessa",
            "Remessas",
            "ID Remessa",
            "Numero Carga",
            "Número Carga",
            "Carga",
        ],
    )

    if not col_base:
        raise ValueError("Não encontrei a coluna de remessa na base principal.")

    if not col_gm:
        raise ValueError("Não encontrei a coluna de remessa no relatório GM Ana.")

    if not col_gw:
        raise ValueError("Não encontrei a coluna de remessa no relatório GW.")

    base["Remessa_Chave"] = base[col_base].apply(limpar_remessa)
    gm["Remessa_Chave"] = gm[col_gm].apply(limpar_remessa)
    gw["Remessa_Chave"] = gw[col_gw].apply(limpar_remessa)

    base = base[base["Remessa_Chave"] != ""]
    gm = gm[gm["Remessa_Chave"] != ""]
    gw = gw[gw["Remessa_Chave"] != ""]

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

    col_placa_gm = encontrar_coluna(gm_final, ["Placa", "PLACA"])
    col_motorista_gm = encontrar_coluna(
        gm_final,
        ["Motorista", "Condutor", "Nome Motorista", "Nome Condutor"],
    )

    renomear_gm = {}

    if col_placa_gm:
        renomear_gm[col_placa_gm] = "Placa_Ana"

    if col_motorista_gm:
        renomear_gm[col_motorista_gm] = "Motorista_Ana"

    gm_final = gm_final.rename(columns=renomear_gm)

    colunas_gw = [
        "Remessa_Chave",
        encontrar_coluna(gw, ["Emissão CT-e", "Emissao CT-e", "Dt emissão CTE", "Data emissão CTE"]),
        encontrar_coluna(gw, ["Data Chegada"]),
        encontrar_coluna(gw, ["Data Entrega"]),
    ]

    colunas_gw = [coluna for coluna in colunas_gw if coluna is not None]
    gw_final = gw[colunas_gw].drop_duplicates(subset=["Remessa_Chave"])

    consolidado = base.merge(
        gm_final,
        on="Remessa_Chave",
        how="inner",
        suffixes=("", "_Base"),
    )

    consolidado = consolidado.merge(
        gw_final,
        on="Remessa_Chave",
        how="left",
        suffixes=("", "_GW"),
    )

    mapa_final = {
        "Remessas": encontrar_coluna(consolidado, ["Remessa", "Remessas", "ID Remessa"]),
        "Cidade Remetente": encontrar_coluna(consolidado, ["Cidade Origem", "Cidade Remetente"]),
        "Nome Cliente": encontrar_coluna(consolidado, ["Cliente", "Nome Cliente"]),
        "Cidade Destino": encontrar_coluna(consolidado, ["Cidade Destino"]),
        "Número de Cidades": encontrar_coluna(consolidado, ["Número de cidades", "Numero de cidades"]),
        "Número de Paradas": encontrar_coluna(consolidado, ["Número de Paradas", "Numero de Paradas"]),
        "Estado Destino": encontrar_coluna(consolidado, ["Estado Destino", "Estado Destinatario", "Estado Destinatário"]),
        "Volumes": encontrar_coluna(consolidado, ["Volumes", "Volume"]),
        "Peso Bruto": encontrar_coluna(consolidado, ["Peso Bruto"]),
        "Dt de emissão": encontrar_coluna(consolidado, ["Dt emissão CTE", "Data emissão CTE", "Emissão CT-e", "Emissao CT-e"]),
        "Inicio Rota": encontrar_coluna(consolidado, ["Dt Inicio Rota", "Data Inicio Rota", "Inicio Rota", "Início Rota"]),
        "Fim Rota": encontrar_coluna(consolidado, ["Dt Fim Rota", "Data Fim Rota", "Fim Rota"]),
        "Região": encontrar_coluna(consolidado, ["Região", "Regiao"]),
        "Cidades": encontrar_coluna(consolidado, ["Cidades"]),
        "KM Original": encontrar_coluna(consolidado, ["KM Original"]),
        "Complementar": encontrar_coluna(consolidado, ["KM Complementar", "Complementar"]),
        "Custo Total": encontrar_coluna(consolidado, ["Custo Total"]),
        "Tipo Veículo": encontrar_coluna(consolidado, ["Tipo Veículo", "Tipo Veiculo"]),
        "Data Oferta": encontrar_coluna(consolidado, ["Dt Oferta", "Data Oferta", "Data Ofertada"]),
        "Data Liberação": encontrar_coluna(consolidado, ["Data Liberação", "Data Liberacao"]),
        "Data OTM": encontrar_coluna(consolidado, ["Data OTM"]),
        "Motorista": encontrar_coluna(consolidado, ["Motorista_Ana", "Motorista", "Condutor", "Nome Motorista", "Nome Condutor"]),
        "Placa": encontrar_coluna(consolidado, ["Placa_Ana", "Placa", "PLACA"]),
    }

    base_final = pd.DataFrame()

    for nome_final, coluna_origem in mapa_final.items():
        if coluna_origem and coluna_origem in consolidado.columns:
            base_final[nome_final] = consolidado[coluna_origem]
        else:
            base_final[nome_final] = ""

    base_final["KM Original"] = base_final["KM Original"].apply(converter_numero)
    base_final["Complementar"] = base_final["Complementar"].apply(converter_numero)

    base_final["KM Total"] = (
        base_final["KM Original"].fillna(0)
        + base_final["Complementar"].fillna(0)
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
    st.markdown(
        """
        <div class="brand">
            <div class="brand-mark">MD</div>
            <div>
                <div class="brand-title">M. Dias</div>
                <div class="brand-subtitle">Consolidação operacional</div>
            </div>
        </div>
        <div class="side-nav">
            <div class="side-item active">Inicio</div>
            <div class="side-item">Importar relatórios</div>
            <div class="side-item">Consolidar base</div>
        </div>
        <div class="side-note">
            Ferramenta interna para cruzar remessas, entregas, cargas e dados de emissão em uma base final.
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# INTERFACE
# ============================================================

st.markdown(
    f"""
    <div class="topbar">
        <div>
            <div class="eyebrow">Base consolidada</div>
            <h1 class="page-title">Consolidação de relatórios M. Dias</h1>
            <p class="page-copy">
                Importe os três relatórios operacionais, valide o status dos arquivos
                e gere uma planilha final pronta para análise.
            </p>
        </div>
        <div class="run-date">
            Atualizado em<br><strong>{datetime.now().strftime("%d/%m/%Y")}</strong>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.container(border=True):
    st.markdown(
        """
        <div class="section-head">
            <div>
                <h2>Importar relatórios</h2>
                <div class="section-kicker">Envie os arquivos em Excel para iniciar a consolidação.</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns(3, gap="large")

    with col1:
        st.markdown(
            """
            <div class="upload-intro">
                <span class="file-step">Arquivo 01</span>
                <h3>Base principal / Remessas</h3>
                <p>Base com as remessas que serão enriquecidas pelos demais relatórios.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        base_principal = st.file_uploader(
            "Selecionar base principal",
            type=["xlsx", "xls"],
            key="base_principal",
        )

    with col2:
        st.markdown(
            """
            <div class="upload-intro">
                <span class="file-step">Arquivo 02</span>
                <h3>Relatório GM Ana</h3>
                <p>Relatório com entregas, cidade destino, placa, motorista e rota.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        relatorio_gm = st.file_uploader(
            "Selecionar relatório GM Ana",
            type=["xlsx", "xls"],
            key="relatorio_gm",
        )

    with col3:
        st.markdown(
            """
            <div class="upload-intro">
                <span class="file-step">Arquivo 03</span>
                <h3>Relatório GW</h3>
                <p>Relatório com carga, emissão de CT-e e datas complementares.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        relatorio_gw = st.file_uploader(
            "Selecionar relatório GW",
            type=["xlsx", "xls"],
            key="relatorio_gw",
        )

arquivos_enviados = sum(
    [
        base_principal is not None,
        relatorio_gm is not None,
        relatorio_gw is not None,
    ]
)

with st.container(border=True):
    st.markdown(
        f"""
        <div class="section-head">
            <div>
                <h2>Status dos arquivos</h2>
                <div class="section-kicker">{arquivos_enviados} de 3 arquivos enviados.</div>
            </div>
        </div>
        <div class="status-grid">
            <div class="status-chip">
                <span class="status-label">Base principal</span>
                {status_badge(base_principal is not None)}
            </div>
            <div class="status-chip">
                <span class="status-label">Relatório GM Ana</span>
                {status_badge(relatorio_gm is not None)}
            </div>
            <div class="status-chip">
                <span class="status-label">Relatório GW</span>
                {status_badge(relatorio_gw is not None)}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with st.container(border=True):
    st.markdown(
        """
        <div class="section-head">
            <div>
                <h2>Consolidar base</h2>
                <div class="section-kicker">Cruze os relatórios e gere o Excel final.</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    botao = st.button("Consolidar relatórios", type="primary")

    if botao:
        if not base_principal or not relatorio_gm or not relatorio_gw:
            st.error("Envie os três arquivos antes de consolidar.")
        else:
            try:
                with st.spinner("Consolidando relatórios..."):
                    df_consolidado = consolidar_bases(
                        base_principal,
                        relatorio_gm,
                        relatorio_gw,
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
                    label="Baixar BASE_CONSOLIDADA_MDIAS.xlsx",
                    data=arquivo_excel,
                    file_name="BASE_CONSOLIDADA_MDIAS.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                )

            except Exception as erro:
                st.error(f"Erro ao consolidar: {erro}")

st.markdown(
    f"""
    <div class="footer">
        Sistema interno | Consolidação operacional M. Dias | Versão 1.0 | {datetime.now().strftime("%d/%m/%Y")}
    </div>
    """,
    unsafe_allow_html=True,
)
