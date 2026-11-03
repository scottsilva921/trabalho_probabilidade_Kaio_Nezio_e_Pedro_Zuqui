#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gerador de Gráficos Científicos e Acessíveis (Vetoriais PDF e PNG de Alta Resolução)
====================================================================================
Segue rigorosamente as diretrizes da Seção 9 e do Extra 6:
  - Sem títulos/legendas editoriais embutidos dentro da imagem (número, título e fonte
    ficam fora da imagem, no documento PDF/LaTeX).
  - Dentro do gráfico: apenas rótulos de eixos com unidades, categorias, legendas de séries
    e anotações numéricas diretas.
  - Paleta Okabe-Ito (segura para daltonismo) combinada com hachuras, estilos de linha
    (sólida, tracejada, pontilhada) e marcadores geométricos distintos.
"""

import os
from typing import Dict, List

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

import simulador as sim

# Configuração tipográfica limpa e de alto contraste
plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["DejaVu Sans", "Arial", "Helvetica"],
    "font.size": 10,
    "axes.labelsize": 10.5,
    "axes.titlesize": 10.5,
    "xtick.labelsize": 9.5,
    "ytick.labelsize": 9.5,
    "legend.fontsize": 9.0,
    "axes.edgecolor": "#222222",
    "axes.linewidth": 0.9,
    "grid.color": "#CCCCCC",
    "grid.linestyle": "--",
    "grid.linewidth": 0.6,
    "figure.dpi": 300,
    "savefig.dpi": 300,
    "savefig.bbox": "tight",
})

# Paleta Okabe-Ito (acessível para deuteranopia, protanopia e tritanopia)
COR_AZUL_ESCURO = "#0072B2"
COR_LARANJA = "#D55E00"
COR_VERDE_AZULADO = "#009E73"
COR_AMARELO_OURO = "#E69F00"
COR_ROXO = "#CC79A7"
COR_AZUL_CLARO = "#56B4E9"
COR_CINZA_ESCURO = "#2B2B2B"
COR_CINZA_MEDIO = "#7F7F7F"


def _salvar_figura(fig: plt.Figure, dir_saida: str, nome_base: str) -> List[str]:
    """Exporta a figura em PNG (300 DPI) e PDF vetorial."""
    os.makedirs(dir_saida, exist_ok=True)
    caminho_png = os.path.join(dir_saida, f"{nome_base}.png")
    caminho_pdf = os.path.join(dir_saida, f"{nome_base}.pdf")
    fig.savefig(caminho_png, format="png", dpi=300)
    fig.savefig(caminho_pdf, format="pdf")
    plt.close(fig)
    return [caminho_png, caminho_pdf]


def gerar_fig01_modelo_teorico(dir_saida: str) -> List[str]:
    """Figura 1: Distribuição teórica de X (%) e contribuições x*Pr(X=x) para E[X] = -0,16."""
    lucros_x = [-1, 4, 9, 14, 24, 49]
    categorias = ["-1\n(Sem prêmio)", "4\n(A-A-A)", "9\n(B-B-B)", "14\n(C-C-C)", "24\n(D-D-D)", "49\n(E-E-E)"]
    probs_pct = [96.0, 0.8, 0.8, 0.8, 0.8, 0.8]
    contribs = [x * (p / 100.0) for x, p in zip(lucros_x, probs_pct)]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.0, 4.2))

    # Painel Esquerdo: Probabilidade (%)
    x_pos = np.arange(len(categorias))
    cores_1 = [COR_CINZA_ESCURO] + [COR_AZUL_ESCURO] * 5
    barras1 = ax1.bar(x_pos, probs_pct, width=0.58, color=cores_1, edgecolor="black", linewidth=0.8)
    for idx, b in enumerate(barras1):
        if idx > 0:
            b.set_hatch("//")
        altura = b.get_height()
        ax1.text(
            b.get_x() + b.get_width() / 2.0,
            altura + 2.0,
            f"{altura:.1f}%".replace(".", ","),
            ha="center",
            va="bottom",
            fontsize=8.8,
            fontweight="bold",
        )
    ax1.set_xticks(x_pos)
    ax1.set_xticklabels(categorias)
    ax1.set_ylim(0, 108)
    ax1.set_ylabel("Probabilidade teórica (%)")
    ax1.set_xlabel("Lucro líquido X por rodada (créditos)")
    ax1.yaxis.grid(True, alpha=0.6)
    ax1.set_axisbelow(True)
    ax1.spines["top"].set_visible(False)
    ax1.spines["right"].set_visible(False)

    # Painel Direito: Contribuição para E[X]
    cores_2 = [COR_LARANJA if c < 0 else COR_VERDE_AZULADO for c in contribs]
    barras2 = ax2.bar(x_pos, contribs, width=0.58, color=cores_2, edgecolor="black", linewidth=0.8)
    for idx, (b, c) in enumerate(zip(barras2, contribs)):
        b.set_hatch("\\\\" if c < 0 else "..")
        offset = -0.075 if c < 0 else 0.025
        va = "top" if c < 0 else "bottom"
        ax2.text(
            b.get_x() + b.get_width() / 2.0,
            c + offset,
            f"{c:+.3f}".replace(".", ","),
            ha="center",
            va=va,
            fontsize=8.8,
            fontweight="bold",
        )
    ax2.axhline(0, color="black", linewidth=0.9)
    ax2.axhline(-0.16, color=COR_AZUL_ESCURO, linestyle="--", linewidth=1.3, label="Soma E[X] = -0,16 crédito")
    ax2.set_xticks(x_pos)
    ax2.set_xticklabels(categorias)
    ax2.set_ylim(-1.12, 0.52)
    ax2.set_ylabel("Parcela x · Pr(X = x) (créditos)")
    ax2.set_xlabel("Lucro líquido X por rodada (créditos)")
    ax2.legend(loc="lower right", frameon=True)
    ax2.yaxis.grid(True, alpha=0.6)
    ax2.set_axisbelow(True)
    ax2.spines["top"].set_visible(False)
    ax2.spines["right"].set_visible(False)

    fig.tight_layout()
    return _salvar_figura(fig, dir_saida, "fig01_modelo_teorico")


def gerar_fig02_e1_frequencias(dados_e1: Dict[str, object], dir_saida: str) -> List[str]:
    """Figura 2 (Experimento 1): Comparação entre Probabilidade Teórica e Frequência Relativa Observada."""
    tabela = dados_e1["tabela"]
    eventos = [r["linha_central"].replace("Qualquer outra tripla", "Sem prêmio\n(X = -1)") for r in tabela]
    probs_teo = [r["prob_teorica_pct"] for r in tabela]
    freqs_obs = [r["freq_relativa_pct"] for r in tabela]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.2, 4.3), gridspec_kw={"width_ratios": [1.15, 1.35]})

    # Painel (a): Todas as 6 categorias
    x_all = np.arange(len(eventos))
    larg = 0.36
    b1 = ax1.bar(x_all - larg / 2, probs_teo, larg, label="Probabilidade teórica (%)", color=COR_AZUL_ESCURO, edgecolor="black")
    b2 = ax1.bar(x_all + larg / 2, freqs_obs, larg, label="Frequência observada (%)", color=COR_LARANJA, edgecolor="black", hatch="//")
    for b in b1:
        v = b.get_height()
        ax1.text(b.get_x() + b.get_width() / 2, v + 1.8, f"{v:.2f}%".replace(".", ","), ha="center", va="bottom", fontsize=7.5, rotation=90)
    for b in b2:
        v = b.get_height()
        ax1.text(b.get_x() + b.get_width() / 2, v + 1.8, f"{v:.2f}%".replace(".", ","), ha="center", va="bottom", fontsize=7.5, rotation=90, fontweight="bold")

    ax1.set_xticks(x_all)
    ax1.set_xticklabels([e.split("\n")[0] for e in eventos], rotation=20, ha="right")
    ax1.set_ylim(0, 114)
    ax1.set_ylabel("Proporção das rodadas (%)")
    ax1.set_xlabel("Evento na linha central (visão global)")
    ax1.legend(loc="upper left", frameon=True)
    ax1.yaxis.grid(True, alpha=0.6)
    ax1.set_axisbelow(True)
    ax1.spines["top"].set_visible(False)
    ax1.spines["right"].set_visible(False)

    # Painel (b): Zoom nas 5 triplas premiadas (para visualização precisa de 0,80% vs observado)
    ev_prem = [f"{r['linha_central']}\n(X=+{int(r['lucro_X'])})" for r in tabela[:5]]
    teo_prem = probs_teo[:5]
    obs_prem = freqs_obs[:5]
    cont_prem = [r["contagem_observada"] for r in tabela[:5]]
    x_p = np.arange(len(ev_prem))

    bp1 = ax2.bar(x_p - larg / 2, teo_prem, larg, label="Teórica (0,80% = 80/10.000)", color=COR_AZUL_ESCURO, edgecolor="black")
    bp2 = ax2.bar(x_p + larg / 2, obs_prem, larg, label="Observada (semente 2026)", color=COR_LARANJA, edgecolor="black", hatch="//")
    ax2.axhline(0.80, color=COR_AZUL_ESCURO, linestyle="--", linewidth=1.0)

    for b, c in zip(bp2, cont_prem):
        v = b.get_height()
        ax2.text(
            b.get_x() + b.get_width() / 2,
            v + 0.025,
            f"{v:.2f}%\n({c})".replace(".", ","),
            ha="center",
            va="bottom",
            fontsize=8.0,
            fontweight="bold",
        )

    ax2.set_xticks(x_p)
    ax2.set_xticklabels(ev_prem)
    ax2.set_ylim(0, 1.26)
    ax2.set_ylabel("Frequência nas triplas premiadas (%)")
    ax2.set_xlabel("Triplas premiadas (escala ampliada)")
    ax2.legend(loc="upper right", frameon=True)
    ax2.yaxis.grid(True, alpha=0.6)
    ax2.set_axisbelow(True)
    ax2.spines["top"].set_visible(False)
    ax2.spines["right"].set_visible(False)

    fig.tight_layout()
    return _salvar_figura(fig, dir_saida, "fig02_e1_frequencias")


def gerar_fig03_e2_convergencia(dados_e2: Dict[str, object], dir_saida: str) -> List[str]:
    """Figura 3 (Experimento 2): Trajetórias da média acumulada de lucro para as 3 sementes."""
    trajetorias = dados_e2["trajetorias"]
    n_total = len(next(iter(trajetorias.values())))
    eixo_n = np.arange(1, n_total + 1)

    fig, ax = plt.subplots(figsize=(9.5, 4.4))

    estilos = {
        10: (COR_AZUL_ESCURO, "-", "Semente 10 (X̄₁₀₀ = -0,7000; X̄₁₀₀₀₀ = -0,0960)"),
        2026: (COR_LARANJA, "--", "Semente 2026 (X̄₁₀₀ = +0,2000; X̄₁₀₀₀₀ = -0,1315)"),
        123456: (COR_VERDE_AZULADO, "-.", "Semente 123456 (X̄₁₀₀ = +0,2000; X̄₁₀₀₀₀ = -0,2215)"),
    }

    for sem in [10, 2026, 123456]:
        cor, ls, rotulo = estilos[sem]
        y = np.array(trajetorias[sem])
        ax.plot(eixo_n, y, color=cor, linestyle=ls, linewidth=1.4, label=rotulo, alpha=0.92)
        # Marca os pontos N = 100, 1.000 e 10.000
        for marco in (100, 1000, 10000):
            ax.scatter([marco], [y[marco - 1]], color=cor, edgecolors="black", s=38, zorder=5)

    ax.axhline(-0.16, color="black", linestyle=":", linewidth=1.6, label="Esperança matemática E[X] = -0,16 crédito")
    ax.axhline(0.0, color=COR_CINZA_MEDIO, linestyle="-", linewidth=0.7, alpha=0.6)

    # Linhas verticais nos marcos de avaliação
    for marco in (100, 1000, 10000):
        ax.axvline(marco, color="#BBBBBB", linestyle="--", linewidth=0.8, zorder=1)

    ax.set_xlim(1, n_total)
    ax.set_ylim(-1.05, 0.85)
    ax.set_xlabel("Número acumulado de rodadas (n)")
    ax.set_ylabel("Lucro líquido médio acumulado X̄_n (créditos/rodada)")
    ax.legend(loc="upper right", frameon=True)
    ax.grid(True, alpha=0.5)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    fig.tight_layout()
    return _salvar_figura(fig, dir_saida, "fig03_e2_convergencia")


def gerar_fig04_e3_saldo_limitado(dados_e3: Dict[str, object], dir_saida: str) -> List[str]:
    """
    Figura 4 (Experimento 3):
      - Painel esquerdo: Trajetórias dos 5 primeiros participantes (mantendo saldo 0 constante após parada).
      - Painel direito: Distribuição dos saldos finais dos 100 participantes (média vs mediana).
    """
    traj5 = dados_e3["trajetorias_5_primeiros"]
    participantes_info = {p["participante"]: p for p in dados_e3["participantes"]}
    saldos_finais = [p["saldo_final"] for p in dados_e3["participantes"]]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.2, 4.4), gridspec_kw={"width_ratios": [1.3, 1.0]})

    paleta_5 = [COR_AZUL_ESCURO, COR_LARANJA, COR_VERDE_AZULADO, COR_ROXO, COR_AMARELO_OURO]
    estilos_5 = ["-", "--", "-.", ":", "-"]
    marcadores_5 = ["o", "s", "^", "D", "v"]

    eixo_t = np.arange(0, dados_e3["max_rodadas"] + 1)
    for idx, part_id in enumerate([1, 2, 3, 4, 5]):
        serie = traj5[part_id]
        p_info = participantes_info[part_id]
        status_str = f"esgotou na rod. {p_info['rodadas_jogadas']}" if p_info["esgotamento"] else f"Bf = {p_info['saldo_final']:.0f} (500 rod.)"
        rotulo = f"Participante {part_id} ({status_str})"
        ax1.plot(
            eixo_t,
            serie,
            color=paleta_5[idx],
            linestyle=estilos_5[idx],
            linewidth=1.5,
            markevery=100,
            marker=marcadores_5[idx],
            markersize=4.5,
            label=rotulo,
        )

    ax1.axhline(100.0, color="black", linestyle=":", linewidth=1.1, label="Saldo inicial B₀ = 100 créditos")
    ax1.axhline(0.0, color="#AA0000", linestyle="-", linewidth=0.9, alpha=0.7)
    ax1.set_xlim(0, 500)
    ax1.set_xlabel("Rodada da sessão (t)")
    ax1.set_ylabel("Saldo B_t (créditos fictícios)")
    ax1.legend(loc="upper right", frameon=True, fontsize=8.2)
    ax1.grid(True, alpha=0.5)
    ax1.spines["top"].set_visible(False)
    ax1.spines["right"].set_visible(False)

    # Painel direito: Histograma dos 100 saldos finais
    bins = [0, 1, 50, 100, 150, 200, 250, 300, 350, 400]
    ax2.hist(saldos_finais, bins=20, color=COR_AZUL_CLARO, edgecolor="black", linewidth=0.8, alpha=0.85)
    ax2.axvline(dados_e3["mediana_saldo_final"], color=COR_LARANJA, linestyle="-", linewidth=2.0,
                label=f"Mediana = {dados_e3['mediana_saldo_final']:.1f} créditos (67% com Bf = 0)")
    ax2.axvline(dados_e3["media_saldo_final"], color=COR_AZUL_ESCURO, linestyle="--", linewidth=2.0,
                label=f"Média = {dados_e3['media_saldo_final']:.2f} créditos")
    ax2.axvline(100.0, color="black", linestyle=":", linewidth=1.3, label="Empate (B₀ = 100 créditos)")

    ax2.set_xlabel("Saldo final B_f ao encerrar a sessão (créditos)")
    ax2.set_ylabel("Número de participantes virtuais (total = 100)")
    ax2.legend(loc="upper right", frameon=True, fontsize=8.2)
    ax2.grid(True, alpha=0.5)
    ax2.spines["top"].set_visible(False)
    ax2.spines["right"].set_visible(False)

    fig.tight_layout()
    return _salvar_figura(fig, dir_saida, "fig04_e3_saldo_limitado")


def gerar_fig05_e4_condicional(dados_e4: Dict[str, object], dir_saida: str) -> List[str]:
    """Figura 5 (Experimento 4): Probabilidade condicional observada vs referência de independência (4%)."""
    grupos = [
        f"Após prêmio (G_i)\n[n = {dados_e4['pares_apos_premio']} pares]",
        f"Após perda (G_i^c)\n[n = {dados_e4['pares_apos_perda']} pares]",
        f"Global (Todos os pares)\n[n = {dados_e4['total_pares']} pares]",
    ]
    valores_pct = [
        dados_e4["prop_apos_premio"] * 100.0,
        dados_e4["prop_apos_perda"] * 100.0,
        (dados_e4["premios_apos_premio"] + dados_e4["premios_apos_perda"]) / dados_e4["total_pares"] * 100.0,
    ]
    contagens_num = [
        f"{dados_e4['premios_apos_premio']}/{dados_e4['pares_apos_premio']}",
        f"{dados_e4['premios_apos_perda']}/{dados_e4['pares_apos_perda']}",
        f"{dados_e4['premios_apos_premio'] + dados_e4['premios_apos_perda']}/{dados_e4['total_pares']}",
    ]

    # Erro-padrão binomial sqrt(p*(1-p)/n) para visualizar a diferença de precisão pelo tamanho do grupo
    ns = [dados_e4["pares_apos_premio"], dados_e4["pares_apos_perda"], dados_e4["total_pares"]]
    ic95_meia_largura = [1.96 * np.sqrt(0.04 * 0.96 / n) * 100.0 for n in ns]

    fig, ax = plt.subplots(figsize=(7.8, 4.2))
    x_pos = np.arange(len(grupos))
    cores = [COR_LARANJA, COR_AZUL_ESCURO, COR_VERDE_AZULADO]
    hachuras = ["//", "\\\\", ".."]

    barras = ax.bar(
        x_pos,
        valores_pct,
        width=0.46,
        color=cores,
        edgecolor="black",
        linewidth=0.9,
        yerr=ic95_meia_largura,
        capsize=6,
        error_kw={"elinewidth": 1.2, "ecolor": "#222222"},
    )
    for b, h, v, c_str in zip(barras, hachuras, valores_pct, contagens_num):
        b.set_hatch(h)
        ax.text(
            b.get_x() + b.get_width() / 2,
            v + 0.25,
            f"{v:.2f}%\n({c_str})".replace(".", ","),
            ha="center",
            va="bottom",
            fontsize=9.0,
            fontweight="bold",
        )

    ax.axhline(4.0, color="black", linestyle="--", linewidth=1.5, label="Referência teórica de independência: Pr(G_{i+1}) = 4,00%")
    ax.set_xticks(x_pos)
    ax.set_xticklabels(grupos)
    ax.set_ylim(0, 7.2)
    ax.set_ylabel("Frequência de prêmio na rodada i+1 (%)")
    ax.set_xlabel("Condição observada na rodada imediatamente anterior (i)")
    ax.legend(loc="upper right", frameon=True)
    ax.yaxis.grid(True, alpha=0.6)
    ax.set_axisbelow(True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    fig.tight_layout()
    return _salvar_figura(fig, dir_saida, "fig05_e4_condicional")


def gerar_fig06_e5_comparacao_tabelas(dados_e5: Dict[str, object], dir_saida: str) -> List[str]:
    """Figura 6 (Experimento 5): Comparação entre Tabela Base e Tabela Prêmios +10%."""
    tab = dados_e5["tabela_comparativa"]
    base, mais10 = tab[0], tab[1]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.5, 4.1))

    # Painel 1: RTP Teórico, RTP Observado e Chance de Prêmio (%)
    metricas = ["Chance de Prêmio\nPr(P > 0)", "RTP Teórico\nE[P] / aposta", "RTP Observado\n(N = 10.000)"]
    vals_base = [base["prob_premio_teorica_pct"], base["rtp_teorico_pct"], base["rtp_obs_pct"]]
    vals_10 = [mais10["prob_premio_teorica_pct"], mais10["rtp_teorico_pct"], mais10["rtp_obs_pct"]]

    x = np.arange(len(metricas))
    larg = 0.34
    b1 = ax1.bar(x - larg / 2, vals_base, larg, label="Tabela Base", color=COR_AZUL_ESCURO, edgecolor="black")
    b2 = ax1.bar(x + larg / 2, vals_10, larg, label="Prêmios +10%", color=COR_VERDE_AZULADO, edgecolor="black", hatch="//")
    ax1.axhline(100.0, color="#AA0000", linestyle=":", linewidth=1.3, label="Equilíbrio (RTP = 100%)")

    for b in list(b1) + list(b2):
        v = b.get_height()
        ax1.text(b.get_x() + b.get_width() / 2, v + 1.8, f"{v:.2f}%".replace(".", ","), ha="center", va="bottom", fontsize=8.3, fontweight="bold")

    ax1.set_xticks(x)
    ax1.set_xticklabels(metricas)
    ax1.set_ylim(0, 115)
    ax1.set_ylabel("Porcentagem (%)")
    ax1.set_xlabel("Indicadores percentuais")
    ax1.legend(loc="upper left", frameon=True, fontsize=8.5)
    ax1.yaxis.grid(True, alpha=0.6)
    ax1.set_axisbelow(True)
    ax1.spines["top"].set_visible(False)
    ax1.spines["right"].set_visible(False)

    # Painel 2: Lucro Médio Teórico E[X] e Observado X̄ (em créditos)
    metricas_x = ["Lucro Esperado\nTeórico E[X]", "Lucro Médio\nObservado X̄"]
    x_base = [base["lucro_medio_teorico"], base["lucro_medio_obs"]]
    x_10 = [mais10["lucro_medio_teorico"], mais10["lucro_medio_obs"]]
    x2 = np.arange(len(metricas_x))

    bx1 = ax2.bar(x2 - larg / 2, x_base, larg, label="Tabela Base", color=COR_AZUL_ESCURO, edgecolor="black")
    bx2 = ax2.bar(x2 + larg / 2, x_10, larg, label="Prêmios +10%", color=COR_VERDE_AZULADO, edgecolor="black", hatch="//")
    ax2.axhline(0.0, color="black", linestyle="-", linewidth=1.0, label="Jogo justo (E[X] = 0)")

    for b in list(bx1) + list(bx2):
        v = b.get_height()
        ax2.text(b.get_x() + b.get_width() / 2, v - 0.012, f"{v:+.4f}".replace(".", ","), ha="center", va="top", fontsize=8.5, fontweight="bold")

    ax2.set_xticks(x2)
    ax2.set_xticklabels(metricas_x)
    ax2.set_ylim(-0.22, 0.04)
    ax2.set_ylabel("Lucro líquido por rodada (créditos)")
    ax2.set_xlabel("Resultado financeiro por crédito apostado")
    ax2.legend(loc="lower right", frameon=True, fontsize=8.5)
    ax2.yaxis.grid(True, alpha=0.6)
    ax2.set_axisbelow(True)
    ax2.spines["top"].set_visible(False)
    ax2.spines["right"].set_visible(False)

    fig.tight_layout()
    return _salvar_figura(fig, dir_saida, "fig06_e5_comparacao_tabelas")


def gerar_fig07_extras_aprofundamento(
    extra_ic: Dict[str, object],
    extra_riscos: Dict[str, object],
    extra_limites: Dict[str, object],
    extra_sens: List[Dict[str, object]],
    dir_saida: str,
) -> List[str]:
    """Figura 7 (Seção 10 - Extras): Painel quádruplo com evidências visuais dos aprofundamentos."""
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(11.5, 8.2))

    # (a) Extra 1: Intervalos de confiança de 95% nas primeiras 25 execuções independentes
    execs_25 = extra_ic["execucoes"][:25]
    ids = [e["execucao"] for e in execs_25]
    medias = [e["lucro_medio"] for e in execs_25]
    erros = [1.96 * e["erro_padrao"] for e in execs_25]
    cores_ic = [COR_AZUL_ESCURO if e["contem_esperanca_teorica"] else COR_LARANJA for e in execs_25]

    for x_i, m_i, err_i, c_i in zip(ids, medias, erros, cores_ic):
        ax1.errorbar(x_i, m_i, yerr=err_i, fmt="o", color=c_i, ecolor=c_i, elinewidth=1.2, capsize=3, markersize=4.5)
    ax1.axhline(-0.16, color="black", linestyle="--", linewidth=1.4, label=f"E[X] = -0,16 (Cobertura em 100 exec.: {extra_ic['taxa_cobertura_pct']:.0f}%)")
    ax1.set_xlabel("Execução independente (N = 10.000 cada)")
    ax1.set_ylabel("Lucro médio X̄ e IC 95% (créditos)")
    ax1.legend(loc="upper right", frameon=True, fontsize=8.2)
    ax1.grid(True, alpha=0.5)
    ax1.spines["top"].set_visible(False)
    ax1.spines["right"].set_visible(False)

    # (b) Extra 2: Mesma média (RTP 84%), riscos diferentes
    perfis = ["Baixa Volat.\n(21 fixo)", "Tabela Base\n(5 a 50)", "Alta Volat.\n(2 a 85)"]
    comp_r = extra_riscos["comparacao"]
    dp_teo = [c["dp_teorico_x"] for c in comp_r]
    esgot_pct = [c["e3_esgotamento_pct"] for c in comp_r]
    x_r = np.arange(len(perfis))
    larg = 0.34
    ax2_twin = ax2.twinx()
    b_dp = ax2.bar(x_r - larg / 2, dp_teo, larg, color=COR_AZUL_ESCURO, edgecolor="black", label="DP teórico σ_X (créditos)")
    b_esg = ax2_twin.bar(x_r + larg / 2, esgot_pct, larg, color=COR_LARANJA, edgecolor="black", hatch="//", label="Esgotamento no E3 (%)")
    for b in b_dp:
        ax2.text(b.get_x() + b.get_width() / 2, b.get_height() + 0.2, f"{b.get_height():.2f}".replace(".", ","), ha="center", va="bottom", fontsize=8.2, fontweight="bold")
    for b in b_esg:
        ax2_twin.text(b.get_x() + b.get_width() / 2, b.get_height() + 2.0, f"{b.get_height():.0f}%", ha="center", va="bottom", fontsize=8.2, fontweight="bold")
    ax2.set_xticks(x_r)
    ax2.set_xticklabels(perfis)
    ax2.set_ylim(0, 9.5)
    ax2_twin.set_ylim(0, 105)
    ax2.set_ylabel("Desvio-padrão por rodada σ_X (créditos)")
    ax2_twin.set_ylabel("Taxa de esgotamento B_f = 0 (%)")
    ax2.set_xlabel("Tabelas com mesmo RTP = 84% e E[X] = -0,16")
    linhas1, labels1 = ax2.get_legend_handles_labels()
    linhas2, labels2 = ax2_twin.get_legend_handles_labels()
    ax2.legend(linhas1 + linhas2, labels1 + labels2, loc="upper left", frameon=True, fontsize=8.0)
    ax2.yaxis.grid(True, alpha=0.5)
    ax2.spines["top"].set_visible(False)

    # (c) Extra 3: Limites de exposição (Regra A, Regra B, Regra C)
    regras_nomes = ["Regra A\n(Até 500 rod.)", "Regra B\n(Stop -30/+20)", "Regra C\n(Curta 50 rod.)"]
    res_lim = extra_limites["resumo_regras"]
    rod_medias = [r["media_rodadas"] for r in res_lim]
    perdas_medianas = [100.0 - r["mediana_saldo_final"] for r in res_lim]
    x_l = np.arange(len(regras_nomes))
    ax3_twin = ax3.twinx()
    bl1 = ax3.bar(x_l - larg / 2, rod_medias, larg, color=COR_VERDE_AZULADO, edgecolor="black", label="Exposição média (rodadas)")
    bl2 = ax3_twin.bar(x_l + larg / 2, perdas_medianas, larg, color=COR_ROXO, edgecolor="black", hatch="\\\\", label="Perda mediana na sessão (créditos)")
    for b in bl1:
        ax3.text(b.get_x() + b.get_width() / 2, b.get_height() + 8, f"{b.get_height():.1f}".replace(".", ","), ha="center", va="bottom", fontsize=8.2, fontweight="bold")
    for b in bl2:
        ax3_twin.text(b.get_x() + b.get_width() / 2, b.get_height() + 2.0, f"-{b.get_height():.0f} cr.", ha="center", va="bottom", fontsize=8.2, fontweight="bold")
    ax3.set_xticks(x_l)
    ax3.set_xticklabels(regras_nomes)
    ax3.set_ylim(0, 415)
    ax3_twin.set_ylim(0, 118)
    ax3.set_ylabel("Número médio de rodadas jogadas (exposição)")
    ax3_twin.set_ylabel("Perda mediana da sessão (créditos)")
    ax3.set_xlabel("Regras de parada pré-definidas (semente 42)")
    l3_1, lb3_1 = ax3.get_legend_handles_labels()
    l3_2, lb3_2 = ax3_twin.get_legend_handles_labels()
    ax3.legend(l3_1 + l3_2, lb3_1 + lb3_2, loc="upper right", frameon=True, fontsize=8.0)
    ax3.yaxis.grid(True, alpha=0.5)
    ax3.spines["top"].set_visible(False)

    # (d) Extra 8: Análise de sensibilidade (Multiplicador de prêmios vs RTP)
    cenarios_5simb = [c for c in extra_sens if c["n_simbolos_rolo"] == 5]
    fatores_pct = [c["fator_pagamento"] * 100.0 for c in cenarios_5simb]
    rtp_teo = [c["rtp_teorico_pct"] for c in cenarios_5simb]
    rtp_obs = [c["rtp_obs_pct"] for c in cenarios_5simb]

    ax4.plot(fatores_pct, rtp_teo, "-o", color=COR_AZUL_ESCURO, linewidth=1.8, label="RTP Teórico (%)")
    ax4.plot(fatores_pct, rtp_obs, "--s", color=COR_LARANJA, linewidth=1.5, label="RTP Observado (N=10.000)")
    ax4.axhline(100.0, color="black", linestyle=":", linewidth=1.3, label="Limiar de jogo justo (RTP = 100%)")
    ax4.axvline(119.0476, color=COR_VERDE_AZULADO, linestyle="-.", linewidth=1.3, label="Equilíbrio: +19,05% (Soma P = 125)")
    ax4.set_xlabel("Escala da tabela de prêmios (% da Tabela Base)")
    ax4.set_ylabel("Retorno ao Jogador - RTP (%)")
    ax4.legend(loc="lower right", frameon=True, fontsize=8.0)
    ax4.grid(True, alpha=0.5)
    ax4.spines["top"].set_visible(False)
    ax4.spines["right"].set_visible(False)

    fig.tight_layout()
    return _salvar_figura(fig, dir_saida, "fig07_extras_aprofundamento")


def gerar_todos_os_graficos(dir_saida: str = "resultados/graficos") -> List[str]:
    """Executa o simulador e exporta todos os gráficos em PNG e PDF."""
    dados = sim.exportar_todos_resultados(
        diretorio_saida=os.path.dirname(dir_saida) if os.path.dirname(dir_saida) else "resultados"
    )
    arquivos = []
    arquivos.extend(gerar_fig01_modelo_teorico(dir_saida))
    arquivos.extend(gerar_fig02_e1_frequencias(dados["e1"], dir_saida))
    arquivos.extend(gerar_fig03_e2_convergencia(dados["e2"], dir_saida))
    arquivos.extend(gerar_fig04_e3_saldo_limitado(dados["e3"], dir_saida))
    arquivos.extend(gerar_fig05_e4_condicional(dados["e4"], dir_saida))
    arquivos.extend(gerar_fig06_e5_comparacao_tabelas(dados["e5"], dir_saida))
    arquivos.extend(
        gerar_fig07_extras_aprofundamento(
            dados["extra_ic"],
            dados["extra_riscos"],
            dados["extra_limites"],
            dados["extra_sensibilidade"],
            dir_saida,
        )
    )
    return arquivos


if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    out_dir = os.path.join(base_dir, "resultados", "graficos")
    gerados = gerar_todos_os_graficos(out_dir)
    print(f"[OK] {len(gerados)} arquivos gráficos exportados em: {out_dir}")
    for g in gerados:
        print(f"  - {os.path.basename(g)}")
