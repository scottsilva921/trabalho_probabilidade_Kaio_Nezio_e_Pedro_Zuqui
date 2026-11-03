#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Suite de Validação Automatizada (Extra - Seção 10)
==================================================
Implementa 8 verificações automatizadas abrangentes para o Simulador Acadêmico:
  1. Pagamento correto das 5 triplas premiadas e prêmio zero nas 120 demais (125 triplas).
  2. Desconto exato da aposta no lucro líquido (X = P - 1) em tabelas inteiras e fracionárias.
  3. Transformação da parada K na janela circular (R_K, R_{(K+1) mod 5}, R_{(K+2) mod 5}),
     incluindo o caso-limite da Figura 3 (K = 4 -> E, A, B).
  4. Reprodutibilidade determinística pela semente (mesma semente gera idêntica sequência;
     não há reinicialização da semente entre rodadas).
  5. Conservação dos totais: soma das 6 categorias no Experimento 1 igual a 10.000;
     soma das 3 categorias de saldo no Experimento 3 igual a 100 participantes;
     soma dos pares no Experimento 4 igual a 9.999.
  6. Caso-limite de probabilidade condicional (Experimento 4): sequência sem prêmios
     não causa divisão por zero e registra proporção como None ("Não estimável").
  7. Caso-limite de sessão com saldo insuficiente (Experimento 3): saldo inicial < 1
     encerra imediatamente com 0 rodadas jogadas e esgotamento = True.
  8. Exatidão algébrica da esperança matemática, RTP e variância (Tabela Base, +10% e Extra 2).

Como executar:
  python -m unittest test_simulador.py -v
"""

import math
import random
import unittest

import simulador as sim


class TestSimuladorMaquinaEstatistica(unittest.TestCase):
    """Testes unitários e de integração para validação da Máquina Estatística."""

    def test_01_espaco_amostral_125_triplas_e_pagamentos(self):
        """Verifica todas as 125 triplas possíveis: 5 premiadas e 120 com prêmio zero."""
        simbolos = sim.ROLO_PADRAO
        todas_triplas = [
            (s1, s2, s3)
            for s1 in simbolos
            for s2 in simbolos
            for s3 in simbolos
        ]
        self.assertEqual(len(todas_triplas), 125)

        premiadas = 0
        sem_premio = 0
        soma_premios = 0.0

        for tripla in todas_triplas:
            p, x = sim.calcular_pagamento(tripla, sim.TABELA_BASE, aposta=1.0)
            self.assertAlmostEqual(x, p - 1.0, places=9)
            if tripla[0] == tripla[1] == tripla[2]:
                premiadas += 1
                self.assertGreater(p, 0.0)
                soma_premios += p
            else:
                sem_premio += 1
                self.assertEqual(p, 0.0)
                self.assertEqual(x, -1.0)

        self.assertEqual(premiadas, 5)
        self.assertEqual(sem_premio, 120)
        self.assertAlmostEqual(soma_premios, 5 + 10 + 15 + 25 + 50, places=9)

    def test_02_desconto_aposta_e_tabela_fracionaria_mais_10(self):
        """Verifica o lucro líquido X = P - 1 tanto na Tabela Base quanto na Tabela +10%."""
        esperados_10 = {
            ("A", "A", "A"): (5.5, 4.5),
            ("B", "B", "B"): (11.0, 10.0),
            ("C", "C", "C"): (16.5, 15.5),
            ("D", "D", "D"): (27.5, 26.5),
            ("E", "E", "E"): (55.0, 54.0),
            ("B", "D", "A"): (0.0, -1.0),
        }
        for tripla, (p_esp, x_esp) in esperados_10.items():
            p, x = sim.calcular_pagamento(tripla, sim.TABELA_MAIS_10, aposta=1.0)
            self.assertAlmostEqual(p, p_esp, places=6)
            self.assertAlmostEqual(x, x_esp, places=6)

    def test_03_montagem_coluna_circular_e_caso_limite_k4(self):
        """Verifica a janela circular para K=0..4, incluindo K=4 -> (E, A, B) da Figura 3."""
        janelas_esperadas = {
            0: ("A", "B", "C"),
            1: ("B", "C", "D"),
            2: ("C", "D", "E"),
            3: ("D", "E", "A"),
            4: ("E", "A", "B"),
        }
        for k, janela in janelas_esperadas.items():
            self.assertEqual(sim.montar_coluna(k), janela)

        with self.assertRaises(ValueError):
            sim.montar_coluna(-1)
        with self.assertRaises(ValueError):
            sim.montar_coluna(5)

    def test_04_reprodutibilidade_semente_e_nao_reinicializacao(self):
        """Confere que a mesma semente reproduz exatamente a sequência e que rodadas avançam o estado."""
        seq1 = sim.simular_sequencia(50, semente=2026)
        seq2 = sim.simular_sequencia(50, semente=2026)
        self.assertEqual(seq1, seq2)

        # Verifica que as rodadas dentro de uma mesma execução não são todas iguais
        paradas_distintas = {r.paradas for r in seq1}
        self.assertGreater(len(paradas_distintas), 20)

    def test_05_totais_experimentos_1_3_e_4(self):
        """Confere somas exatas: 10.000 contagens no E1, 100 pessoas no E3 e 9.999 pares no E4."""
        rodadas_e1, res_e1 = sim.executar_experimento_1(n_rodadas=10_000, semente=2026)
        self.assertEqual(res_e1["soma_contagens"], 10_000)
        self.assertAlmostEqual(
            sum(r["freq_relativa"] for r in res_e1["tabela"]), 1.0, places=9
        )

        res_e3 = sim.executar_experimento_3(n_participantes=100, saldo_inicial=100.0, max_rodadas=500, semente=42)
        self.assertEqual(res_e3["n_ganho"] + res_e3["n_empate"] + res_e3["n_perda"], 100)
        self.assertAlmostEqual(
            res_e3["prop_ganho_pct"] + res_e3["prop_empate_pct"] + res_e3["prop_perda_pct"],
            100.0,
            places=9,
        )
        self.assertLessEqual(res_e3["n_esgotamento"], res_e3["n_perda"])

        res_e4 = sim.executar_experimento_4(rodadas_e1)
        self.assertEqual(res_e4["total_pares"], 9_999)
        self.assertEqual(res_e4["pares_apos_premio"] + res_e4["pares_apos_perda"], 9_999)

    def test_06_caso_limite_probabilidade_condicional_sem_divisao_por_zero(self):
        """Verifica que o Experimento 4 trata grupo vazio sem dividir por zero."""
        # Cria sequência artificial de 5 rodadas todas sem prêmio
        rodadas_sem_premio = [
            sim.ResultadoRodada(
                indice=i,
                paradas=(0, 1, 2),
                tabuleiro=(("A", "B", "C"), ("B", "C", "D"), ("C", "D", "E")),
                linha_central=("B", "C", "D"),
                evento="Qualquer outra tripla",
                premio=0.0,
                lucro=-1.0,
            )
            for i in range(1, 6)
        ]
        res_vazio = sim.executar_experimento_4(rodadas_sem_premio)
        self.assertEqual(res_vazio["total_pares"], 4)
        self.assertEqual(res_vazio["pares_apos_premio"], 0)
        self.assertIsNone(res_vazio["prop_apos_premio"])
        self.assertEqual(res_vazio["tabela"][0]["proporcao_observada_str"], "Não estimável")
        self.assertEqual(res_vazio["prop_apos_perda"], 0.0)

    def test_07_caso_limite_saldo_inicial_insuficiente(self):
        """Verifica caso-limite no Experimento 3 quando saldo inicial é zero (< 1 crédito)."""
        res_zero = sim.executar_experimento_3(
            n_participantes=5, saldo_inicial=0.0, max_rodadas=500, semente=42
        )
        for p in res_zero["participantes"]:
            self.assertEqual(p["rodadas_jogadas"], 0)
            self.assertEqual(p["saldo_final"], 0.0)
            self.assertTrue(p["esgotamento"])

    def test_08_exatidao_matematica_esperanca_rtp_e_extra2(self):
        """Confere valores teóricos exatos de E[P], E[X], RTP e igualdade de médias no Extra 2."""
        teo_base = sim.calcular_parametros_teoricos(sim.TABELA_BASE)
        self.assertAlmostEqual(teo_base["esperanca_p"], 0.84, places=9)
        self.assertAlmostEqual(teo_base["esperanca_x"], -0.16, places=9)
        self.assertAlmostEqual(teo_base["rtp_teorico_pct"], 84.0, places=9)

        teo_10 = sim.calcular_parametros_teoricos(sim.TABELA_MAIS_10)
        self.assertAlmostEqual(teo_10["esperanca_p"], 0.924, places=9)
        self.assertAlmostEqual(teo_10["esperanca_x"], -0.076, places=9)
        self.assertAlmostEqual(teo_10["rtp_teorico_pct"], 92.4, places=9)

        teo_baixa = sim.calcular_parametros_teoricos(sim.TABELA_BAIXA_VOLATILIDADE)
        teo_alta = sim.calcular_parametros_teoricos(sim.TABELA_ALTA_VOLATILIDADE)
        self.assertAlmostEqual(teo_baixa["esperanca_x"], -0.16, places=9)
        self.assertAlmostEqual(teo_alta["esperanca_x"], -0.16, places=9)
        self.assertLess(teo_baixa["dp_teorico_x"], teo_base["dp_teorico_x"])
        self.assertGreater(teo_alta["dp_teorico_x"], teo_base["dp_teorico_x"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
