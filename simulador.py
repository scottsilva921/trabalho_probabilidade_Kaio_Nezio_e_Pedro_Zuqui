#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simulador acadêmico - somente créditos fictícios
================================================
Trabalho I de Probabilidade e Estatística I (2026/2)
Bacharelado em Sistemas de Informação - IFES Campus Serra
Professor: Fidelis Zanetti de Castro

Módulo principal do simulador da Máquina Estatística de 3 rolos e 5 símbolos.
Implementa as regras públicas da Seção 5, a matemática exata da Seção 6,
os cinco experimentos obrigatórios da Seção 7 e os experimentos extras da Seção 10.
"""

from __future__ import annotations

import csv
import json
import math
import os
import platform
import random
import statistics
import sys
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional, Sequence, Tuple

AVISO_ACADEMICO = "Simulador acadêmico - somente créditos fictícios"

# Sequência circular oficial de cada rolo: R = (A, B, C, D, E) nas posições 0 a 4
ROLO_PADRAO: Tuple[str, ...] = ("A", "B", "C", "D", "E")

# Formas geométricas e nomes acessíveis (não dependem apenas de cor)
SIMBOLOS_ACESSIVEIS: Dict[str, str] = {
    "A": "● A (Círculo)",
    "B": "▲ B (Triângulo)",
    "C": "■ C (Quadrado)",
    "D": "◆ D (Losango)",
    "E": "★ E (Estrela)",
}

APOSTA_PADRAO: float = 1.0

# Tabela 1: Pagamentos brutos (P) para as 5 triplas centrais premiadas no modelo-base
TABELA_BASE: Dict[Tuple[str, str, str], float] = {
    ("A", "A", "A"): 5.0,
    ("B", "B", "B"): 10.0,
    ("C", "C", "C"): 15.0,
    ("D", "D", "D"): 25.0,
    ("E", "E", "E"): 50.0,
}

# Experimento 5: Tabela com prêmios aumentados em +10%
TABELA_MAIS_10: Dict[Tuple[str, str, str], float] = {
    tripla: round(valor * 1.10, 4) for tripla, valor in TABELA_BASE.items()
}

# Extra 2: Tabelas com a MESMA média (E[P] = 0,84; E[X] = -0,16; RTP = 84%), mas riscos diferentes
# Soma dos 5 prêmios deve ser 105 para que E[P] = 105 / 125 = 0,84.
TABELA_BAIXA_VOLATILIDADE: Dict[Tuple[str, str, str], float] = {
    ("A", "A", "A"): 21.0,
    ("B", "B", "B"): 21.0,
    ("C", "C", "C"): 21.0,
    ("D", "D", "D"): 21.0,
    ("E", "E", "E"): 21.0,
}

TABELA_ALTA_VOLATILIDADE: Dict[Tuple[str, str, str], float] = {
    ("A", "A", "A"): 2.0,
    ("B", "B", "B"): 3.0,
    ("C", "C", "C"): 5.0,
    ("D", "D", "D"): 10.0,
    ("E", "E", "E"): 85.0,
}

ORDEM_EVENTOS: List[str] = [
    "A-A-A",
    "B-B-B",
    "C-C-C",
    "D-D-D",
    "E-E-E",
    "Qualquer outra tripla",
]


@dataclass(frozen=True)
class ResultadoRodada:
    """Representa o estado completo de uma única rodada da máquina 3x3."""
    indice: int
    paradas: Tuple[int, int, int]
    tabuleiro: Tuple[Tuple[str, str, str], Tuple[str, str, str], Tuple[str, str, str]]
    linha_central: Tuple[str, str, str]
    evento: str
    premio: float
    lucro: float


def montar_coluna(parada_k: int, rolo: Sequence[str] = ROLO_PADRAO) -> Tuple[str, str, str]:
    """
    Transforma uma posição de parada K (0 a 4) em uma coluna (topo, centro, base).
    Regra da Seção 5:
      topo   = R_K
      centro = R_{(K+1) mod 5}
      base   = R_{(K+2) mod 5}
    """
    n = len(rolo)
    if not (0 <= parada_k < n):
        raise ValueError(f"Parada K inválida: {parada_k}. Esperado inteiro entre 0 e {n - 1}.")
    topo = rolo[parada_k]
    centro = rolo[(parada_k + 1) % n]
    base = rolo[(parada_k + 2) % n]
    return (topo, centro, base)


def classificar_evento(linha_central: Tuple[str, str, str]) -> str:
    """Identifica qual dos 6 eventos da Tabela 1 ocorreu na linha central."""
    s1, s2, s3 = linha_central
    if s1 == s2 == s3 and s1 in ROLO_PADRAO:
        return f"{s1}-{s2}-{s3}"
    return "Qualquer outra tripla"


def calcular_pagamento(
    linha_central: Tuple[str, str, str],
    tabela_pagamentos: Dict[Tuple[str, str, str], float] = TABELA_BASE,
    aposta: float = APOSTA_PADRAO,
) -> Tuple[float, float]:
    """
    Calcula o prêmio bruto P e o lucro líquido X = P - aposta para a linha central.
    Apenas a linha central gera pagamento, e somente quando seus três símbolos constam na tabela.
    """
    premio = float(tabela_pagamentos.get(linha_central, 0.0))
    lucro = premio - aposta
    return premio, lucro


def executar_rodada(
    rng: random.Random,
    indice: int = 1,
    tabela_pagamentos: Dict[Tuple[str, str, str], float] = TABELA_BASE,
    aposta: float = APOSTA_PADRAO,
    rolo: Sequence[str] = ROLO_PADRAO,
) -> ResultadoRodada:
    """
    Sorteia independentemente as paradas dos 3 rolos usando o gerador `rng` fornecido
    (sem reinicializar a semente!) e retorna o resultado completo da rodada.
    """
    n = len(rolo)
    # Sorteio discreto uniforme: cada posição 0, 1, 2, 3, 4 tem probabilidade 1/5
    k1 = rng.randrange(n)
    k2 = rng.randrange(n)
    k3 = rng.randrange(n)

    col1 = montar_coluna(k1, rolo)
    col2 = montar_coluna(k2, rolo)
    col3 = montar_coluna(k3, rolo)

    # Transpõe as 3 colunas para formar as 3 linhas (topo, centro, base) do tabuleiro 3x3
    linha_topo = (col1[0], col2[0], col3[0])
    linha_central = (col1[1], col2[1], col3[1])
    linha_base = (col1[2], col2[2], col3[2])
    tabuleiro = (linha_topo, linha_central, linha_base)

    evento = classificar_evento(linha_central)
    premio, lucro = calcular_pagamento(linha_central, tabela_pagamentos, aposta)

    return ResultadoRodada(
        indice=indice,
        paradas=(k1, k2, k3),
        tabuleiro=tabuleiro,
        linha_central=linha_central,
        evento=evento,
        premio=premio,
        lucro=lucro,
    )


def formatar_rodada_texto(rodada: ResultadoRodada, modo_acessivel: bool = False) -> str:
    """Formata visualmente o tabuleiro 3x3 e os indicadores da rodada para exibição textual."""
    linhas = [
        "=" * 62,
        f"  {AVISO_ACADEMICO}",
        "=" * 62,
        f"  Rodada #{rodada.indice} | Paradas sorteadas (K1, K2, K3) = {rodada.paradas}",
        "-" * 62,
    ]
    if modo_acessivel:
        linhas.append("  Coluna:        Rolo 1             Rolo 2             Rolo 3")
        for idx_linha, nome_linha in enumerate(["Topo  ", "CENTRO", "Base  "]):
            marcador = ">>" if idx_linha == 1 else "  "
            s1, s2, s3 = rodada.tabuleiro[idx_linha]
            c1 = SIMBOLOS_ACESSIVEIS.get(s1, s1).ljust(16)
            c2 = SIMBOLOS_ACESSIVEIS.get(s2, s2).ljust(16)
            c3 = SIMBOLOS_ACESSIVEIS.get(s3, s3).ljust(16)
            linhas.append(f"  {marcador} {nome_linha}: | {c1} | {c2} | {c3} |")
    else:
        linhas.append("               Rolo 1    Rolo 2    Rolo 3")
        linhas.append("             +---------+---------+---------+")
        for idx_linha, nome_linha in enumerate(["   Topo  ", "-> CENTRO", "   Base  "]):
            s1, s2, s3 = rodada.tabuleiro[idx_linha]
            destaque = "*" if idx_linha == 1 else " "
            linhas.append(
                f"  {nome_linha}  |   {destaque}{s1}{destaque}   |   {destaque}{s2}{destaque}   |   {destaque}{s3}{destaque}   |"
            )
            linhas.append("             +---------+---------+---------+")

    linhas.extend([
        f"  Linha central avaliada : {' - '.join(rodada.linha_central)} ({rodada.evento})",
        f"  Aposta                 : 1,00 crédito fictício",
        f"  Prêmio bruto (P)       : {rodada.premio:.2f} crédito(s)",
        f"  Lucro líquido (X = P-1): {rodada.lucro:+.2f} crédito(s)",
        "=" * 62,
    ])
    return "\n".join(linhas)


def calcular_parametros_teoricos(
    tabela_pagamentos: Dict[Tuple[str, str, str], float] = TABELA_BASE,
    aposta: float = APOSTA_PADRAO,
    n_simbolos: int = 5,
) -> Dict[str, float]:
    """
    Calcula os parâmetros teóricos exatos da distribuição discreta de P e X:
      - Total de triplas equiprováveis: n_simbolos^3 = 125
      - Probabilidade de prêmio: 5 / 125 = 0,04 (4%)
      - Esperança do prêmio E[P]
      - Esperança do lucro E[X] = E[P] - aposta
      - RTP teórico = E[P] / aposta
      - Variância e desvio-padrão populacional de X e P
    """
    total_triplas = n_simbolos ** 3
    prob_unitaria = 1.0 / total_triplas
    n_premiadas = len(tabela_pagamentos)
    prob_sem_premio = (total_triplas - n_premiadas) / total_triplas

    esperanca_p = sum(p * prob_unitaria for p in tabela_pagamentos.values())
    esperanca_x = esperanca_p - aposta
    rtp_teorico = esperanca_p / aposta

    # E[X^2] = sum((p - aposta)^2 * (1/125)) + (0 - aposta)^2 * (120/125)
    e_x2 = sum(((p - aposta) ** 2) * prob_unitaria for p in tabela_pagamentos.values())
    e_x2 += ((0.0 - aposta) ** 2) * prob_sem_premio
    var_x = e_x2 - (esperanca_x ** 2)
    dp_x = math.sqrt(var_x)

    return {
        "total_triplas": float(total_triplas),
        "n_premiadas": float(n_premiadas),
        "prob_premio": n_premiadas / total_triplas,
        "prob_sem_premio": prob_sem_premio,
        "esperanca_p": esperanca_p,
        "esperanca_x": esperanca_x,
        "rtp_teorico": rtp_teorico,
        "rtp_teorico_pct": rtp_teorico * 100.0,
        "vantagem_casa_pct": (1.0 - rtp_teorico) * 100.0,
        "variancia_x": var_x,
        "dp_teorico_x": dp_x,
    }


def simular_sequencia(
    n_rodadas: int,
    semente: int,
    tabela_pagamentos: Dict[Tuple[str, str, str], float] = TABELA_BASE,
    aposta: float = APOSTA_PADRAO,
) -> List[ResultadoRodada]:
    """
    Inicializa o gerador pseudoaleatório UMA ÚNICA VEZ com `semente` e executa `n_rodadas`.
    """
    rng = random.Random(semente)
    return [
        executar_rodada(rng, indice=i + 1, tabela_pagamentos=tabela_pagamentos, aposta=aposta)
        for i in range(n_rodadas)
    ]


# ==============================================================================
# EXPERIMENTO 1: As frequências acompanham as probabilidades?
# ==============================================================================
def executar_experimento_1(
    n_rodadas: int = 10_000,
    semente: int = 2026,
) -> Tuple[List[ResultadoRodada], Dict[str, object]]:
    """
    Executa 10.000 rodadas com semente 2026, sem saldo ou regra de parada.
    Conta os seis resultados da Tabela 1 e calcula média, RTP observado,
    proporção de rodadas premiadas e desvio-padrão amostral (divisor N - 1).
    """
    rodadas = simular_sequencia(n_rodadas=n_rodadas, semente=semente, tabela_pagamentos=TABELA_BASE)

    contagens: Dict[str, int] = {ev: 0 for ev in ORDEM_EVENTOS}
    for r in rodadas:
        contagens[r.evento] += 1

    soma_contagens = sum(contagens.values())
    assert soma_contagens == n_rodadas, f"Erro: soma das contagens ({soma_contagens}) != {n_rodadas}"

    info_eventos = [
        ("A-A-A", 5.0, 4.0, 1.0 / 125.0),
        ("B-B-B", 10.0, 9.0, 1.0 / 125.0),
        ("C-C-C", 15.0, 14.0, 1.0 / 125.0),
        ("D-D-D", 25.0, 24.0, 1.0 / 125.0),
        ("E-E-E", 50.0, 49.0, 1.0 / 125.0),
        ("Qualquer outra tripla", 0.0, -1.0, 120.0 / 125.0),
    ]

    tabela_linhas = []
    for ev, p_val, x_val, prob_teo in info_eventos:
        c = contagens[ev]
        freq_rel = c / n_rodadas
        tabela_linhas.append({
            "linha_central": ev,
            "premio_P": p_val,
            "lucro_X": x_val,
            "prob_teorica": prob_teo,
            "prob_teorica_pct": prob_teo * 100.0,
            "esperado_N": prob_teo * n_rodadas,
            "contagem_observada": c,
            "freq_relativa": freq_rel,
            "freq_relativa_pct": freq_rel * 100.0,
            "diferenca_pct": (freq_rel - prob_teo) * 100.0,
        })

    lucros = [r.lucro for r in rodadas]
    premios = [r.premio for r in rodadas]
    n_premiadas_obs = sum(1 for r in rodadas if r.premio > 0)

    lucro_medio = sum(lucros) / n_rodadas
    rtp_obs = sum(premios) / n_rodadas
    prop_premiadas = n_premiadas_obs / n_rodadas
    dp_amostral = statistics.stdev(lucros)  # Usa divisor N - 1 exatamente como pedido

    resumo = {
        "n_rodadas": n_rodadas,
        "semente": semente,
        "soma_contagens": soma_contagens,
        "n_premiadas_obs": n_premiadas_obs,
        "prop_premiadas": prop_premiadas,
        "prop_premiadas_pct": prop_premiadas * 100.0,
        "soma_premios": sum(premios),
        "soma_lucros": sum(lucros),
        "lucro_medio": lucro_medio,
        "rtp_observado": rtp_obs,
        "rtp_observado_pct": rtp_obs * 100.0,
        "dp_amostral_s": dp_amostral,
        "teorico": calcular_parametros_teoricos(TABELA_BASE),
        "tabela": tabela_linhas,
    }
    return rodadas, resumo


# ==============================================================================
# EXPERIMENTO 2: O que muda quando aumentamos a amostra?
# ==============================================================================
def executar_experimento_2(
    rodadas_2026: Optional[List[ResultadoRodada]] = None,
    sementes: Tuple[int, int, int] = (10, 2026, 123456),
    n_rodadas: int = 10_000,
    marcos: Tuple[int, int, int] = (100, 1_000, 10_000),
) -> Dict[str, object]:
    """
    Executa 3 sequências de 10.000 rodadas com sementes 10, 2026 e 123456
    (reutilizando a sequência de 2026 do Experimento 1).
    Registra a média acumulada após 100, 1.000 e 10.000 rodadas e confere
    a reprodutibilidade exata dos 10 primeiros resultados da semente 2026.
    """
    trajetorias: Dict[int, List[float]] = {}
    tabela_3x3: List[Dict[str, object]] = []

    for sem in sementes:
        if sem == 2026 and rodadas_2026 is not None and len(rodadas_2026) == n_rodadas:
            seq = rodadas_2026
        else:
            seq = simular_sequencia(n_rodadas=n_rodadas, semente=sem, tabela_pagamentos=TABELA_BASE)

        medias_acum: List[float] = []
        soma_atual = 0.0
        for idx, r in enumerate(seq, start=1):
            soma_atual += r.lucro
            medias_acum.append(soma_atual / idx)

        trajetorias[sem] = medias_acum
        linha_marco = {"semente": sem}
        for m in marcos:
            linha_marco[f"media_{m}"] = medias_acum[m - 1]
        tabela_3x3.append(linha_marco)

    # Verificação de reprodutibilidade da semente 2026 no mesmo ambiente
    seq_ref = rodadas_2026 if rodadas_2026 is not None else simular_sequencia(n_rodadas, 2026)
    seq_repetida = simular_sequencia(n_rodadas=10, semente=2026, tabela_pagamentos=TABELA_BASE)

    dez_primeiros_iguais = True
    comparacao_10_primeiros = []
    for r1, r2 in zip(seq_ref[:10], seq_repetida):
        igual = (
            r1.paradas == r2.paradas
            and r1.linha_central == r2.linha_central
            and r1.premio == r2.premio
            and r1.lucro == r2.lucro
        )
        if not igual:
            dez_primeiros_iguais = False
        comparacao_10_primeiros.append({
            "rodada": r1.indice,
            "paradas_exec1": f"{r1.paradas}",
            "central_exec1": "-".join(r1.linha_central),
            "lucro_exec1": r1.lucro,
            "paradas_exec2": f"{r2.paradas}",
            "central_exec2": "-".join(r2.linha_central),
            "lucro_exec2": r2.lucro,
            "reproduzido": igual,
        })

    return {
        "sementes": list(sementes),
        "marcos": list(marcos),
        "tabela_3x3": tabela_3x3,
        "trajetorias": trajetorias,
        "dez_primeiros_reproduzidos": dez_primeiros_iguais,
        "comparacao_10_primeiros": comparacao_10_primeiros,
    }


# ==============================================================================
# EXPERIMENTO 3: O que acontece com um saldo limitado?
# ==============================================================================
def executar_experimento_3(
    n_participantes: int = 100,
    saldo_inicial: float = 100.0,
    max_rodadas: int = 500,
    semente: int = 42,
    tabela_pagamentos: Dict[Tuple[str, str, str], float] = TABELA_BASE,
    aposta: float = APOSTA_PADRAO,
) -> Dict[str, object]:
    """
    Simula 100 participantes virtuais, cada um com saldo inicial de 100 créditos e aposta de 1.
    Cada sessão termina ao completar 500 rodadas ou quando o saldo fica abaixo de 1.
    Inicia o gerador com semente 42 UMA ÚNICA VEZ e continua a sequência entre participantes.
    """
    rng = random.Random(semente)
    participantes_dados = []
    trajetorias_5_primeiros: Dict[int, List[float]] = {}

    for id_part in range(1, n_participantes + 1):
        saldo = saldo_inicial
        historico_saldo = [saldo]  # Posição 0 = saldo inicial (100)
        rodadas_jogadas = 0
        esgotou = False

        for _ in range(1, max_rodadas + 1):
            if saldo < aposta:
                esgotou = True
                break
            res = executar_rodada(rng, indice=rodadas_jogadas + 1, tabela_pagamentos=tabela_pagamentos, aposta=aposta)
            saldo = saldo + res.lucro
            rodadas_jogadas += 1
            historico_saldo.append(saldo)
            if saldo < aposta:
                esgotou = True
                break

        # Se parou antes de 500 rodadas, preenche o gráfico mantendo o saldo constante
        historico_completo = list(historico_saldo)
        while len(historico_completo) < max_rodadas + 1:
            historico_completo.append(saldo)

        if id_part <= 5:
            trajetorias_5_primeiros[id_part] = historico_completo

        if saldo > saldo_inicial:
            categoria = "Ganho (Bf > 100)"
        elif saldo == saldo_inicial:
            categoria = "Empate (Bf = 100)"
        else:
            categoria = "Perda (Bf < 100)"

        participantes_dados.append({
            "participante": id_part,
            "saldo_inicial": saldo_inicial,
            "saldo_final": saldo,
            "lucro_sessao": saldo - saldo_inicial,
            "rodadas_jogadas": rodadas_jogadas,
            "esgotamento": esgotou,
            "categoria": categoria,
        })

    saldos_finais = [p["saldo_final"] for p in participantes_dados]
    rodadas_lista = [p["rodadas_jogadas"] for p in participantes_dados]

    n_ganho = sum(1 for s in saldos_finais if s > saldo_inicial)
    n_empate = sum(1 for s in saldos_finais if s == saldo_inicial)
    n_perda = sum(1 for s in saldos_finais if s < saldo_inicial)
    n_esgotamento = sum(1 for p in participantes_dados if p["esgotamento"])

    assert n_ganho + n_empate + n_perda == n_participantes, "Categorias de saldo não somam 100!"

    return {
        "n_participantes": n_participantes,
        "saldo_inicial": saldo_inicial,
        "max_rodadas": max_rodadas,
        "semente": semente,
        "n_ganho": n_ganho,
        "prop_ganho_pct": (n_ganho / n_participantes) * 100.0,
        "n_empate": n_empate,
        "prop_empate_pct": (n_empate / n_participantes) * 100.0,
        "n_perda": n_perda,
        "prop_perda_pct": (n_perda / n_participantes) * 100.0,
        "n_esgotamento": n_esgotamento,
        "prop_esgotamento_pct": (n_esgotamento / n_participantes) * 100.0,
        "prop_esgotamento_entre_perdas_pct": (n_esgotamento / n_perda * 100.0) if n_perda > 0 else 0.0,
        "media_saldo_final": statistics.mean(saldos_finais),
        "mediana_saldo_final": statistics.median(saldos_finais),
        "dp_saldo_final": statistics.stdev(saldos_finais),
        "min_saldo_final": min(saldos_finais),
        "max_saldo_final": max(saldos_finais),
        "media_rodadas": statistics.mean(rodadas_lista),
        "mediana_rodadas": statistics.median(rodadas_lista),
        "participantes": participantes_dados,
        "trajetorias_5_primeiros": trajetorias_5_primeiros,
    }


# ==============================================================================
# EXPERIMENTO 4: Depois de perder, aumenta a chance de ganhar?
# ==============================================================================
def executar_experimento_4(rodadas_e1: Sequence[ResultadoRodada]) -> Dict[str, object]:
    """
    Examina os 9.999 pares consecutivos das 10.000 rodadas do Experimento 1.
    Separa-os conforme a primeira rodada do par pagou (P_i > 0) ou não pagou prêmio (P_i = 0).
    Para cada grupo, calcula a proporção de vezes em que a rodada seguinte foi premiada (P_{i+1} > 0).
    Protege contra divisão por zero caso algum grupo tenha 0 pares.
    """
    n_total = len(rodadas_e1)
    total_pares = max(0, n_total - 1)

    pares_apos_premio = 0
    premios_apos_premio = 0

    pares_apos_perda = 0
    premios_apos_perda = 0

    for i in range(total_pares):
        atual_premiada = rodadas_e1[i].premio > 0
        seguinte_premiada = rodadas_e1[i + 1].premio > 0

        if atual_premiada:
            pares_apos_premio += 1
            if seguinte_premiada:
                premios_apos_premio += 1
        else:
            pares_apos_perda += 1
            if seguinte_premiada:
                premios_apos_perda += 1

    assert pares_apos_premio + pares_apos_perda == total_pares, "Soma dos pares diferente de N - 1!"

    prop_apos_premio: Optional[float] = (
        premios_apos_premio / pares_apos_premio if pares_apos_premio > 0 else None
    )
    prop_apos_perda: Optional[float] = (
        premios_apos_perda / pares_apos_perda if pares_apos_perda > 0 else None
    )
    prop_global: Optional[float] = (
        (premios_apos_premio + premios_apos_perda) / total_pares if total_pares > 0 else None
    )

    tabela = [
        {
            "resultado_anterior": "Com prêmio (G_i: P_i > 0)",
            "total_pares": pares_apos_premio,
            "premios_seguinte": premios_apos_premio,
            "proporcao_observada": prop_apos_premio,
            "proporcao_observada_str": f"{prop_apos_premio * 100:.4f}%" if prop_apos_premio is not None else "Não estimável",
            "referencia_teorica_pct": 4.0,
        },
        {
            "resultado_anterior": "Sem prêmio (G_i^c: P_i = 0)",
            "total_pares": pares_apos_perda,
            "premios_seguinte": premios_apos_perda,
            "proporcao_observada": prop_apos_perda,
            "proporcao_observada_str": f"{prop_apos_perda * 100:.4f}%" if prop_apos_perda is not None else "Não estimável",
            "referencia_teorica_pct": 4.0,
        },
        {
            "resultado_anterior": "Total de pares consecutivos",
            "total_pares": total_pares,
            "premios_seguinte": premios_apos_premio + premios_apos_perda,
            "proporcao_observada": prop_global,
            "proporcao_observada_str": f"{prop_global * 100:.4f}%" if prop_global is not None else "Não estimável",
            "referencia_teorica_pct": 4.0,
        },
    ]

    return {
        "total_pares": total_pares,
        "pares_apos_premio": pares_apos_premio,
        "premios_apos_premio": premios_apos_premio,
        "prop_apos_premio": prop_apos_premio,
        "pares_apos_perda": pares_apos_perda,
        "premios_apos_perda": premios_apos_perda,
        "prop_apos_perda": prop_apos_perda,
        "tabela": tabela,
    }


# ==============================================================================
# EXPERIMENTO 5: Prêmios maiores tornam o jogo favorável?
# ==============================================================================
def executar_experimento_5(rodadas_e1: Sequence[ResultadoRodada]) -> Dict[str, object]:
    """
    Aplica a Tabela Base e a Tabela Prêmios +10% aos MESMOS 10.000 resultados
    do Experimento 1 (sem sortear outra sequência).
    """
    n_total = len(rodadas_e1)
    teo_base = calcular_parametros_teoricos(TABELA_BASE)
    teo_10 = calcular_parametros_teoricos(TABELA_MAIS_10)

    premios_base = []
    lucros_base = []
    premios_10 = []
    lucros_10 = []
    n_premiadas = 0

    for r in rodadas_e1:
        p_b, x_b = calcular_pagamento(r.linha_central, TABELA_BASE, APOSTA_PADRAO)
        p_10, x_10 = calcular_pagamento(r.linha_central, TABELA_MAIS_10, APOSTA_PADRAO)
        premios_base.append(p_b)
        lucros_base.append(x_b)
        premios_10.append(p_10)
        lucros_10.append(x_10)
        if p_b > 0:
            n_premiadas += 1

    freq_premio = n_premiadas / n_total
    premio_medio_base = sum(premios_base) / n_total
    lucro_medio_base = sum(lucros_base) / n_total
    rtp_obs_base = premio_medio_base / APOSTA_PADRAO

    premio_medio_10 = sum(premios_10) / n_total
    lucro_medio_10 = sum(lucros_10) / n_total
    rtp_obs_10 = premio_medio_10 / APOSTA_PADRAO

    tabela_comparativa = [
        {
            "configuracao": "Tabela Base",
            "prob_premio_teorica_pct": teo_base["prob_premio"] * 100.0,
            "freq_premio_obs_pct": freq_premio * 100.0,
            "premio_medio_teorico": teo_base["esperanca_p"],
            "premio_medio_obs": premio_medio_base,
            "lucro_medio_teorico": teo_base["esperanca_x"],
            "lucro_medio_obs": lucro_medio_base,
            "rtp_teorico_pct": teo_base["rtp_teorico_pct"],
            "rtp_obs_pct": rtp_obs_base * 100.0,
            "dp_teorico_x": teo_base["dp_teorico_x"],
            "dp_obs_x": statistics.stdev(lucros_base),
        },
        {
            "configuracao": "Prêmios +10%",
            "prob_premio_teorica_pct": teo_10["prob_premio"] * 100.0,
            "freq_premio_obs_pct": freq_premio * 100.0,
            "premio_medio_teorico": teo_10["esperanca_p"],
            "premio_medio_obs": premio_medio_10,
            "lucro_medio_teorico": teo_10["esperanca_x"],
            "lucro_medio_obs": lucro_medio_10,
            "rtp_teorico_pct": teo_10["rtp_teorico_pct"],
            "rtp_obs_pct": rtp_obs_10 * 100.0,
            "dp_teorico_x": teo_10["dp_teorico_x"],
            "dp_obs_x": statistics.stdev(lucros_10),
        },
    ]

    return {
        "n_rodadas": n_total,
        "tabela_comparativa": tabela_comparativa,
        "teo_base": teo_base,
        "teo_10": teo_10,
    }


# ==============================================================================
# EXTRAS (Seção 10): Funções para os aprofundamentos opcionais (até 20 pts)
# ==============================================================================
def executar_extra_intervalos_confianca(
    rodadas_e1: Sequence[ResultadoRodada],
    m_execucoes: int = 100,
    n_por_execucao: int = 10_000,
    semente_inicial: int = 5000,
) -> Dict[str, object]:
    """
    Extra 1: Intervalos de confiança de 95% para E[X] e RTP.
    1) A partir da amostra única de N=10.000 do E1 (erro-padrão s / sqrt(N), z_{0.975} = 1.959964).
    2) A partir de M=100 execuções independentes de N=10.000 rodadas cada (sementes 5000..5099),
       verificando em quantas das 100 execuções o IC 95% contém o valor verdadeiro E[X] = -0,16.
    """
    z_95 = 1.959963984540054
    t_95_df99 = 1.9842169515086827  # t crítico bilateral 95% com gl = 99

    lucros_e1 = [r.lucro for r in rodadas_e1]
    n1 = len(lucros_e1)
    media_e1 = statistics.mean(lucros_e1)
    dp_e1 = statistics.stdev(lucros_e1)
    ep_e1 = dp_e1 / math.sqrt(n1)
    ic_e1_inf = media_e1 - z_95 * ep_e1
    ic_e1_sup = media_e1 + z_95 * ep_e1

    # M execuções independentes
    medias_execucoes = []
    rtps_execucoes = []
    coberturas = 0
    lista_execucoes = []

    for idx in range(m_execucoes):
        sem = semente_inicial + idx
        seq = simular_sequencia(n_por_execucao, sem, TABELA_BASE)
        lucros_k = [r.lucro for r in seq]
        m_k = statistics.mean(lucros_k)
        s_k = statistics.stdev(lucros_k)
        ep_k = s_k / math.sqrt(n_por_execucao)
        inf_k = m_k - z_95 * ep_k
        sup_k = m_k + z_95 * ep_k
        cobre = (inf_k <= -0.16 <= sup_k)
        if cobre:
            coberturas += 1
        medias_execucoes.append(m_k)
        rtps_execucoes.append((m_k + 1.0) * 100.0)
        lista_execucoes.append({
            "execucao": idx + 1,
            "semente": sem,
            "lucro_medio": m_k,
            "rtp_pct": (m_k + 1.0) * 100.0,
            "dp_amostral": s_k,
            "erro_padrao": ep_k,
            "ic95_inf": inf_k,
            "ic95_sup": sup_k,
            "contem_esperanca_teorica": cobre,
        })

    media_das_medias = statistics.mean(medias_execucoes)
    dp_das_medias = statistics.stdev(medias_execucoes)
    ep_entre_execucoes = dp_das_medias / math.sqrt(m_execucoes)
    ic_meta_inf = media_das_medias - t_95_df99 * ep_entre_execucoes
    ic_meta_sup = media_das_medias + t_95_df99 * ep_entre_execucoes

    return {
        "e1_media": media_e1,
        "e1_dp": dp_e1,
        "e1_erro_padrao": ep_e1,
        "e1_ic95_lucro": (ic_e1_inf, ic_e1_sup),
        "e1_ic95_rtp_pct": ((ic_e1_inf + 1.0) * 100.0, (ic_e1_sup + 1.0) * 100.0),
        "m_execucoes": m_execucoes,
        "n_por_execucao": n_por_execucao,
        "media_das_medias": media_das_medias,
        "dp_das_medias": dp_das_medias,
        "ep_teorico_esperado": calcular_parametros_teoricos(TABELA_BASE)["dp_teorico_x"] / math.sqrt(n_por_execucao),
        "ic95_meta_lucro": (ic_meta_inf, ic_meta_sup),
        "ic95_meta_rtp_pct": ((ic_meta_inf + 1.0) * 100.0, (ic_meta_sup + 1.0) * 100.0),
        "taxa_cobertura_pct": (coberturas / m_execucoes) * 100.0,
        "execucoes": lista_execucoes,
    }


def executar_extra_mesma_media_riscos_diferentes(
    rodadas_e1: Sequence[ResultadoRodada],
) -> Dict[str, object]:
    """
    Extra 2: Compara três tabelas com EXATAMENTE o mesmo RTP teórico (84%) e
    mesmo lucro esperado (-0,16), mas dispersões diferentes:
      1) Baixa Volatilidade: todas as 5 triplas pagam 21 créditos
      2) Tabela Base: 5, 10, 15, 25, 50
      3) Alta Volatilidade (Jackpot): 2, 3, 5, 10, 85
    Avalia tanto nos 10.000 sorteios do E1 quanto nas sessões de 100 participantes (E3, semente 42).
    """
    configs = [
        ("Baixa Volatilidade (21 fixo)", TABELA_BAIXA_VOLATILIDADE),
        ("Tabela Base (5 a 50)", TABELA_BASE),
        ("Alta Volatilidade (2 a 85)", TABELA_ALTA_VOLATILIDADE),
    ]
    comparacao = []
    sessoes_por_perfil = {}

    for nome, tab in configs:
        teo = calcular_parametros_teoricos(tab)
        lucros_obs = [calcular_pagamento(r.linha_central, tab)[1] for r in rodadas_e1]
        e3_sim = executar_experimento_3(
            n_participantes=100,
            saldo_inicial=100.0,
            max_rodadas=500,
            semente=42,
            tabela_pagamentos=tab,
        )
        sessoes_por_perfil[nome] = e3_sim
        comparacao.append({
            "perfil": nome,
            "pagamentos": "-".join(str(int(v)) for v in tab.values()),
            "esperanca_p_teorica": teo["esperanca_p"],
            "esperanca_x_teorica": teo["esperanca_x"],
            "rtp_teorico_pct": teo["rtp_teorico_pct"],
            "dp_teorico_x": teo["dp_teorico_x"],
            "lucro_medio_obs_e1": statistics.mean(lucros_obs),
            "rtp_obs_e1_pct": (statistics.mean(lucros_obs) + 1.0) * 100.0,
            "dp_obs_e1": statistics.stdev(lucros_obs),
            "e3_media_saldo": e3_sim["media_saldo_final"],
            "e3_mediana_saldo": e3_sim["mediana_saldo_final"],
            "e3_dp_saldo": e3_sim["dp_saldo_final"],
            "e3_ganhadores_pct": e3_sim["prop_ganho_pct"],
            "e3_esgotamento_pct": e3_sim["prop_esgotamento_pct"],
            "e3_max_saldo": e3_sim["max_saldo_final"],
        })

    return {
        "comparacao": comparacao,
        "sessoes_por_perfil": sessoes_por_perfil,
    }


def executar_extra_limites_exposicao(
    n_participantes: int = 100,
    saldo_inicial: float = 100.0,
    max_rodadas: int = 500,
    semente: int = 42,
) -> Dict[str, object]:
    """
    Extra 3: Compara 3 regras de parada definidas antes de simular (usando a mesma semente 42
    por participante ou sequência contínua):
      - Regra 1 (Sem limite adicional - padrão E3): joga até 500 rodadas ou esgotar (B_t = 0).
      - Regra 2 (Stop-Loss e Stop-Gain moderados): para se atingir lucro de +20 (B_t >= 120),
        perda de -30 (B_t <= 70) ou 200 rodadas.
      - Regra 3 (Orçamento estrito de tempo/exposição): para rigorosamente em 50 rodadas
        ou se perder 15 créditos (B_t <= 85).
    """
    regras = [
        {
            "nome": "Regra A: Padrão E3 (até 500 rodadas ou falência B=0)",
            "max_r": 500,
            "stop_loss_saldo": 0.0,
            "stop_gain_saldo": float("inf"),
        },
        {
            "nome": "Regra B: Limite Prudencial (Stop-Loss B<=70, Stop-Gain B>=120, máx 200 rodadas)",
            "max_r": 200,
            "stop_loss_saldo": 70.0,
            "stop_gain_saldo": 120.0,
        },
        {
            "nome": "Regra C: Exposição Curta (Stop-Loss B<=85, máx 50 rodadas)",
            "max_r": 50,
            "stop_loss_saldo": 85.0,
            "stop_gain_saldo": float("inf"),
        },
    ]

    resultados_regras = []
    detalhes_regras = {}

    for reg in regras:
        rng = random.Random(semente)
        saldos = []
        rodadas_feitas = []
        esgotados = 0
        ganhadores = 0
        perdedores = 0

        for _ in range(n_participantes):
            saldo = saldo_inicial
            r_count = 0
            for _ in range(reg["max_r"]):
                if saldo <= reg["stop_loss_saldo"] or saldo >= reg["stop_gain_saldo"] or saldo < 1.0:
                    break
                res = executar_rodada(rng, indice=r_count + 1, tabela_pagamentos=TABELA_BASE)
                saldo += res.lucro
                r_count += 1
                if saldo <= reg["stop_loss_saldo"] or saldo >= reg["stop_gain_saldo"] or saldo < 1.0:
                    break
            saldos.append(saldo)
            rodadas_feitas.append(r_count)
            if saldo < 1.0:
                esgotados += 1
            if saldo > saldo_inicial:
                ganhadores += 1
            elif saldo < saldo_inicial:
                perdedores += 1

        media_r = statistics.mean(rodadas_feitas)
        media_s = statistics.mean(saldos)
        perda_media = saldo_inicial - media_s
        perda_por_rodada = (media_s - saldo_inicial) / media_r if media_r > 0 else 0.0

        resumo_r = {
            "regra": reg["nome"],
            "media_rodadas": media_r,
            "mediana_rodadas": statistics.median(rodadas_feitas),
            "media_saldo_final": media_s,
            "mediana_saldo_final": statistics.median(saldos),
            "dp_saldo_final": statistics.stdev(saldos),
            "perda_media_sessao": perda_media,
            "lucro_medio_por_rodada_efetiva": perda_por_rodada,
            "wald_teorico_saldo": saldo_inicial - 0.16 * media_r,
            "prop_ganho_pct": (ganhadores / n_participantes) * 100.0,
            "prop_perda_pct": (perdedores / n_participantes) * 100.0,
            "prop_esgotamento_total_pct": (esgotados / n_participantes) * 100.0,
        }
        resultados_regras.append(resumo_r)
        detalhes_regras[reg["nome"]] = saldos

    return {
        "resumo_regras": resultados_regras,
        "detalhes_saldos": detalhes_regras,
    }


def executar_extra_analise_sensibilidade(
    rodadas_e1: Sequence[ResultadoRodada],
) -> List[Dict[str, object]]:
    """
    Extra 8: Análise de sensibilidade em 7 cenários sistemáticos (variando multiplicadores
    de pagamento e número de símbolos por rolo), incluindo o ponto de equilíbrio (break-even).
    """
    fatores = [
        ("Cenário 1: Prêmios -20% (RTP 67,2%)", 0.80, 5),
        ("Cenário 2: Modelo-Base (RTP 84,0%)", 1.00, 5),
        ("Cenário 3: Prêmios +10% - Exp. 5 (RTP 92,4%)", 1.10, 5),
        ("Cenário 4: Prêmios +15% (RTP 96,6%)", 1.15, 5),
        ("Cenário 5: Equilíbrio / Break-Even (+19,05%, RTP 100,0%)", 125.0 / 105.0, 5),
        ("Cenário 6: Favorável ao Jogador (+25%, RTP 105,0%)", 1.25, 5),
        ("Cenário 7: Expansão para 6 símbolos no rolo (Base, RTP 48,6%)", 1.00, 6),
    ]

    resultados = []
    for nome, fator, n_simb in fatores:
        tab = {k: v * fator for k, v in TABELA_BASE.items()}
        teo = calcular_parametros_teoricos(tab, aposta=1.0, n_simbolos=n_simb)

        if n_simb == 5:
            lucros_obs = [calcular_pagamento(r.linha_central, tab)[1] for r in rodadas_e1]
            lucro_obs_medio = statistics.mean(lucros_obs)
            rtp_obs_pct = (lucro_obs_medio + 1.0) * 100.0
        else:
            # Simula 10.000 rodadas com 6 símbolos (A..F) usando semente 2026
            rolo_6 = ("A", "B", "C", "D", "E", "F")
            rng6 = random.Random(2026)
            lucros_6 = [
                executar_rodada(rng6, i + 1, tab, 1.0, rolo=rolo_6).lucro
                for i in range(len(rodadas_e1))
            ]
            lucro_obs_medio = statistics.mean(lucros_6)
            rtp_obs_pct = (lucro_obs_medio + 1.0) * 100.0

        resultados.append({
            "cenario": nome,
            "fator_pagamento": round(fator, 6),
            "n_simbolos_rolo": n_simb,
            "espaco_amostral": int(teo["total_triplas"]),
            "prob_premio_pct": teo["prob_premio"] * 100.0,
            "soma_pagamentos": sum(tab.values()),
            "esperanca_p": teo["esperanca_p"],
            "esperanca_x": teo["esperanca_x"],
            "rtp_teorico_pct": teo["rtp_teorico_pct"],
            "vantagem_casa_pct": teo["vantagem_casa_pct"],
            "dp_teorico_x": teo["dp_teorico_x"],
            "lucro_medio_obs": lucro_obs_medio,
            "rtp_obs_pct": rtp_obs_pct,
        })

    return resultados


def obter_metadados_ambiente() -> Dict[str, str]:
    """Registra informações completas sobre o ambiente, versão do Python e gerador."""
    return {
        "aviso": AVISO_ACADEMICO,
        "python_version": sys.version.replace("\n", " "),
        "python_implementation": platform.python_implementation(),
        "sistema_operacional": f"{platform.system()} {platform.release()} ({platform.version()})",
        "arquitetura": platform.machine(),
        "biblioteca_gerador": "Módulo padrão Python `random` (classe `random.Random`, algoritmo Mersenne Twister MT19937 de período 2^19937 - 1)",
        "metodo_sorteio": "random.Random(semente).randrange(5) -> inteiros uniformes {0, 1, 2, 3, 4}",
    }


def _salvar_csv(caminho: str, linhas: List[Dict[str, object]]) -> None:
    """Utilitário para salvar lista de dicionários em CSV UTF-8."""
    if not linhas:
        return
    os.makedirs(os.path.dirname(caminho), exist_ok=True)
    campos = list(linhas[0].keys())
    with open(caminho, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=campos)
        writer.writeheader()
        writer.writerows(linhas)


def exportar_todos_resultados(diretorio_saida: str = "resultados") -> Dict[str, object]:
    """
    Executa todos os 5 experimentos obrigatórios e os experimentos extras,
    salva todas as tabelas em CSV e o resumo completo em JSON.
    """
    os.makedirs(diretorio_saida, exist_ok=True)
    meta = obter_metadados_ambiente()

    # Exemplo de 1 rodada isolada (semente 2026)
    rng_exemplo = random.Random(2026)
    rodada_exemplo = executar_rodada(rng_exemplo, indice=1)

    # Experimento 1
    rodadas_e1, res_e1 = executar_experimento_1(n_rodadas=10_000, semente=2026)
    _salvar_csv(os.path.join(diretorio_saida, "e1_tabela_frequencias.csv"), res_e1["tabela"])
    _salvar_csv(
        os.path.join(diretorio_saida, "e1_resumo_estatistico.csv"),
        [{
            "n_rodadas": res_e1["n_rodadas"],
            "semente": res_e1["semente"],
            "soma_contagens": res_e1["soma_contagens"],
            "rodadas_premiadas": res_e1["n_premiadas_obs"],
            "proporcao_premiadas_pct": round(res_e1["prop_premiadas_pct"], 4),
            "lucro_medio_observado": round(res_e1["lucro_medio"], 6),
            "esperanca_lucro_teorica": -0.16,
            "rtp_observado_pct": round(res_e1["rtp_observado_pct"], 4),
            "rtp_teorico_pct": 84.0,
            "desvio_padrao_amostral_s": round(res_e1["dp_amostral_s"], 6),
            "desvio_padrao_teorico_sigma": round(res_e1["teorico"]["dp_teorico_x"], 6),
        }],
    )

    # Experimento 2
    res_e2 = executar_experimento_2(rodadas_2026=rodadas_e1)
    _salvar_csv(os.path.join(diretorio_saida, "e2_medias_acumuladas_3x3.csv"), res_e2["tabela_3x3"])
    _salvar_csv(os.path.join(diretorio_saida, "e2_reproducao_10_primeiros_2026.csv"), res_e2["comparacao_10_primeiros"])

    # Experimento 3
    res_e3 = executar_experimento_3(n_participantes=100, saldo_inicial=100.0, max_rodadas=500, semente=42)
    _salvar_csv(os.path.join(diretorio_saida, "e3_sessoes_100_participantes.csv"), res_e3["participantes"])
    _salvar_csv(
        os.path.join(diretorio_saida, "e3_resumo_saldos.csv"),
        [{
            "semente": res_e3["semente"],
            "n_participantes": res_e3["n_participantes"],
            "saldo_inicial": res_e3["saldo_inicial"],
            "max_rodadas": res_e3["max_rodadas"],
            "prop_ganho_pct": res_e3["prop_ganho_pct"],
            "prop_empate_pct": res_e3["prop_empate_pct"],
            "prop_perda_pct": res_e3["prop_perda_pct"],
            "soma_categorias_pct": res_e3["prop_ganho_pct"] + res_e3["prop_empate_pct"] + res_e3["prop_perda_pct"],
            "prop_esgotamento_pct": res_e3["prop_esgotamento_pct"],
            "media_saldo_final": round(res_e3["media_saldo_final"], 4),
            "mediana_saldo_final": round(res_e3["mediana_saldo_final"], 4),
            "dp_saldo_final": round(res_e3["dp_saldo_final"], 4),
            "min_saldo_final": res_e3["min_saldo_final"],
            "max_saldo_final": res_e3["max_saldo_final"],
            "media_rodadas_jogadas": round(res_e3["media_rodadas"], 2),
            "mediana_rodadas_jogadas": round(res_e3["mediana_rodadas"], 2),
        }],
    )

    # Experimento 4
    res_e4 = executar_experimento_4(rodadas_e1)
    _salvar_csv(os.path.join(diretorio_saida, "e4_probabilidade_condicional.csv"), res_e4["tabela"])

    # Experimento 5
    res_e5 = executar_experimento_5(rodadas_e1)
    _salvar_csv(os.path.join(diretorio_saida, "e5_comparacao_tabelas.csv"), res_e5["tabela_comparativa"])

    # Extras
    res_extra_ic = executar_extra_intervalos_confianca(rodadas_e1)
    _salvar_csv(os.path.join(diretorio_saida, "extra1_intervalos_confianca_100_execucoes.csv"), res_extra_ic["execucoes"])

    res_extra_riscos = executar_extra_mesma_media_riscos_diferentes(rodadas_e1)
    _salvar_csv(os.path.join(diretorio_saida, "extra2_mesma_media_riscos_diferentes.csv"), res_extra_riscos["comparacao"])

    res_extra_limites = executar_extra_limites_exposicao()
    _salvar_csv(os.path.join(diretorio_saida, "extra3_limites_exposicao.csv"), res_extra_limites["resumo_regras"])

    res_extra_sens = executar_extra_analise_sensibilidade(rodadas_e1)
    _salvar_csv(os.path.join(diretorio_saida, "extra8_analise_sensibilidade.csv"), res_extra_sens)

    # Salva sumário consolidado em JSON (sem as listas gigantes de 10.000 pontos das trajetórias para manter legibilidade)
    consolidado = {
        "metadados_ambiente": meta,
        "rodada_exemplo_semente_2026": asdict(rodada_exemplo),
        "experimento_1": res_e1,
        "experimento_2": {
            k: v for k, v in res_e2.items() if k != "trajetorias"
        },
        "experimento_3": {
            k: v for k, v in res_e3.items() if k not in ("participantes", "trajetorias_5_primeiros")
        },
        "experimento_4": res_e4,
        "experimento_5": res_e5,
        "extra_1_intervalos_confianca": {
            k: v for k, v in res_extra_ic.items() if k != "execucoes"
        },
        "extra_2_mesma_media_riscos_diferentes": {
            "comparacao": res_extra_riscos["comparacao"],
        },
        "extra_3_limites_exposicao": {
            "resumo_regras": res_extra_limites["resumo_regras"],
        },
        "extra_8_analise_sensibilidade": res_extra_sens,
    }

    with open(os.path.join(diretorio_saida, "resumo_completo.json"), "w", encoding="utf-8") as f:
        json.dump(consolidado, f, ensure_ascii=False, indent=2)

    return {
        "metadados": meta,
        "rodada_exemplo": rodada_exemplo,
        "rodadas_e1": rodadas_e1,
        "e1": res_e1,
        "e2": res_e2,
        "e3": res_e3,
        "e4": res_e4,
        "e5": res_e5,
        "extra_ic": res_extra_ic,
        "extra_riscos": res_extra_riscos,
        "extra_limites": res_extra_limites,
        "extra_sensibilidade": res_extra_sens,
    }


def imprimir_relatorio_terminal(dados: Dict[str, object], modo_acessivel: bool = False) -> None:
    """Exibe no console uma rodada completa e o resumo de todos os 5 experimentos e extras."""
    print(formatar_rodada_texto(dados["rodada_exemplo"], modo_acessivel=modo_acessivel))
    meta = dados["metadados"]
    print(f"\n[AMBIENTE] Python: {meta['python_version']}")
    print(f"[GERADOR]  {meta['biblioteca_gerador']}")

    e1 = dados["e1"]
    print("\n" + "=" * 78)
    print("EXPERIMENTO 1: As frequências acompanham as probabilidades? (N=10.000, seed=2026)")
    print("=" * 78)
    print(f"{'Linha Central':<24} | {'P':>4} | {'X':>4} | {'Prob. Teór.':>11} | {'Contagem':>8} | {'Freq. Obs.':>10}")
    print("-" * 78)
    for row in e1["tabela"]:
        print(
            f"{row['linha_central']:<24} | {row['premio_P']:>4.0f} | {row['lucro_X']:>4.0f} | "
            f"{row['prob_teorica_pct']:>10.2f}% | {row['contagem_observada']:>8d} | {row['freq_relativa_pct']:>9.2f}%"
        )
    print("-" * 78)
    print(f"Soma das contagens         : {e1['soma_contagens']} (conferido == 10.000)")
    print(f"Proporção de prêmios obs.  : {e1['prop_premiadas_pct']:.2f}% ({e1['n_premiadas_obs']}/10.000) [Teórico: 4,00%]")
    print(f"Lucro médio observado (X_m): {e1['lucro_medio']:+.4f} créditos [Esperança E[X]: -0,1600]")
    print(f"RTP observado              : {e1['rtp_observado_pct']:.2f}% [RTP Teórico: 84,00%]")
    print(f"Desvio-padrão amostral (s) : {e1['dp_amostral_s']:.4f} créditos [DP Teórico sigma: {e1['teorico']['dp_teorico_x']:.4f}]")

    e2 = dados["e2"]
    print("\n" + "=" * 78)
    print("EXPERIMENTO 2: O que muda quando aumentamos a amostra? (Médias Acumuladas)")
    print("=" * 78)
    print(f"{'Semente':<12} | {'Após 100 rodadas':>18} | {'Após 1.000 rodadas':>18} | {'Após 10.000 rodadas':>19}")
    print("-" * 78)
    for row in e2["tabela_3x3"]:
        print(
            f"{row['semente']:<12} | {row['media_100']:>+18.4f} | {row['media_1000']:>+18.4f} | {row['media_10000']:>+19.4f}"
        )
    print(f"Reprodução dos 10 primeiros resultados (semente 2026): {'SIM (10/10 idênticos)' if e2['dez_primeiros_reproduzidos'] else 'FALHOU'}")

    e3 = dados["e3"]
    print("\n" + "=" * 78)
    print("EXPERIMENTO 3: O que acontece com um saldo limitado? (100 pessoas, B0=100, seed=42)")
    print("=" * 78)
    print(f"Proporção de Ganho (Bf > 100)  : {e3['prop_ganho_pct']:5.1f}% ({e3['n_ganho']} participantes)")
    print(f"Proporção de Empate (Bf = 100) : {e3['prop_empate_pct']:5.1f}% ({e3['n_empate']} participantes)")
    print(f"Proporção de Perda (Bf < 100)  : {e3['prop_perda_pct']:5.1f}% ({e3['n_perda']} participantes)")
    print(f"Soma das categorias            : {e3['prop_ganho_pct'] + e3['prop_empate_pct'] + e3['prop_perda_pct']:5.1f}%")
    print(f"Proporção de Esgotamento (Bf=0): {e3['prop_esgotamento_pct']:5.1f}% ({e3['n_esgotamento']} participantes)")
    print(f"Média dos saldos finais        : {e3['media_saldo_final']:.2f} créditos (DP = {e3['dp_saldo_final']:.2f})")
    print(f"Mediana dos saldos finais      : {e3['mediana_saldo_final']:.2f} créditos (Mín = {e3['min_saldo_final']:.0f}, Máx = {e3['max_saldo_final']:.0f})")
    print(f"Duração média das sessões      : {e3['media_rodadas']:.2f} rodadas (Mediana = {e3['mediana_rodadas']:.1f})")

    e4 = dados["e4"]
    print("\n" + "=" * 78)
    print("EXPERIMENTO 4: Depois de perder, aumenta a chance de ganhar? (9.999 pares)")
    print("=" * 78)
    print(f"{'Resultado Anterior':<30} | {'Total Pares':>12} | {'Prêmios Seg.':>12} | {'Proporção Obs.':>15}")
    print("-" * 78)
    for row in e4["tabela"]:
        print(
            f"{row['resultado_anterior']:<30} | {row['total_pares']:>12d} | "
            f"{row['premios_seguinte']:>12d} | {row['proporcao_observada_str']:>15}"
        )

    e5 = dados["e5"]
    print("\n" + "=" * 78)
    print("EXPERIMENTO 5: Prêmios maiores (+10%) tornam o jogo favorável?")
    print("=" * 78)
    print(f"{'Configuração':<16} | {'Prob/Freq Prêmio':>18} | {'E[P] / P_med':>15} | {'E[X] / X_med':>17} | {'RTP Teór / Obs':>16}")
    print("-" * 78)
    for row in e5["tabela_comparativa"]:
        prob_str = f"{row['prob_premio_teorica_pct']:.2f}% / {row['freq_premio_obs_pct']:.2f}%"
        p_str = f"{row['premio_medio_teorico']:.3f} / {row['premio_medio_obs']:.3f}"
        x_str = f"{row['lucro_medio_teorico']:+.3f} / {row['lucro_medio_obs']:+.3f}"
        rtp_str = f"{row['rtp_teorico_pct']:.1f}% / {row['rtp_obs_pct']:.2f}%"
        print(f"{row['configuracao']:<16} | {prob_str:>18} | {p_str:>15} | {x_str:>17} | {rtp_str:>16}")
    print("=" * 78)


def menu_interativo_acessivel() -> None:
    """
    Extra 6: Interface textual interativa por teclado, com alto contraste e
    codificação multimodal (formas + letras + descrição textual).
    """
    print("\n" + "=" * 70)
    print(f"  {AVISO_ACADEMICO}")
    print("  MODO INTERATIVO ACESSÍVEL (Navegação por Teclado / Alto Contraste)")
    print("=" * 70)
    semente_str = input("Digite uma semente inteira [Enter para 2026]: ").strip()
    semente = int(semente_str) if semente_str.isdigit() else 2026
    rng = random.Random(semente)
    rodada_idx = 0
    saldo = 100.0

    while True:
        print(f"\n[SALDO ATUAL: {saldo:.2f} créditos fictícios | Semente inicial: {semente} | Rodadas: {rodada_idx}]")
        print("Comandos por teclado: [Enter/1] Girar 1 rodada | [2] Girar 10 rodadas | [3] Executar todos os 5 experimentos | [0/Q] Sair")
        opcao = input("Sua escolha: ").strip().lower()
        if opcao in ("0", "q", "sair"):
            print("Encerrando o simulador acadêmico. Até logo!")
            break
        elif opcao in ("", "1"):
            rodada_idx += 1
            res = executar_rodada(rng, indice=rodada_idx)
            saldo += res.lucro
            print(formatar_rodada_texto(res, modo_acessivel=True))
        elif opcao == "2":
            for _ in range(10):
                rodada_idx += 1
                res = executar_rodada(rng, indice=rodada_idx)
                saldo += res.lucro
            print(formatar_rodada_texto(res, modo_acessivel=True))
        elif opcao == "3":
            dados = exportar_todos_resultados()
            imprimir_relatorio_terminal(dados, modo_acessivel=True)
        else:
            print("Opção não reconhecida. Use 1, 2, 3 ou 0.")


def main() -> None:
    """Ponto de entrada CLI do simulador."""
    modo_acessivel = "--acessivel" in sys.argv
    modo_interativo = "--interativo" in sys.argv

    if modo_interativo:
        menu_interativo_acessivel()
        return

    diretorio_base = os.path.dirname(os.path.abspath(__file__))
    dir_resultados = os.path.join(diretorio_base, "resultados")
    dados = exportar_todos_resultados(diretorio_saida=dir_resultados)
    imprimir_relatorio_terminal(dados, modo_acessivel=modo_acessivel)
    print(f"\n[OK] Tabelas CSV e resumo JSON exportados em: {dir_resultados}")


if __name__ == "__main__":
    main()
