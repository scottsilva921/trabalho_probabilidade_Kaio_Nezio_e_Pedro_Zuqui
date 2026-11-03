# Máquina Estatística: Probabilidade, Apostas e Pensamento Crítico

> **Aviso Obrigatório:** `Simulador acadêmico - somente créditos fictícios`

Pacote completo de entrega do **Trabalho I de Probabilidade e Estatística I (2026/2)** do curso de **Bacharelado em Sistemas de Informação** do **Instituto Federal do Espírito Santo (IFES) – Campus Serra**, sob orientação do **Prof. Fidelis Zanetti de Castro**.

---

## 1. Identificação da Equipe

* **Instituição:** Instituto Federal do Espírito Santo (IFES) – Campus Serra
* **Curso / Disciplina:** Bacharelado em Sistemas de Informação — Probabilidade e Estatística I (2026/2)
* **Professor:** Fidelis Zanetti de Castro
* **Integrante(s):** Pedro Vitor Zuqui e Kaio Henrique da Silva Nezio 
* **Data de Entrega:** 29 de outubro de 2026

---

## 2. Ambiente de Execução, Gerador e Sementes Registradas

Para garantir **reprodutibilidade determinística exata** (Seção 5 e Seção 7):

* **Linguagem e Interpretador:** `Python 3.12.7 (tags/v3.12.7:0b05ead, Oct 1 2024, MSC v.1941 64 bit AMD64)` — Implementação oficial `CPython`.
* **Sistema Operacional:** Windows 11 (`10.0.26200`, arquitetura `AMD64`).
* **Biblioteca e Algoritmo Gerador Pseudoaleatório:** Módulo padrão `random` da Python Standard Library [16], instanciado via `random.Random(semente)`, que implementa o algoritmo **Mersenne Twister (`MT19937`)** com período $2^{19937} - 1$.
* **Método de Sorteio Discreto Uniforme:** `rng.randrange(5)`, que sorteia inteiros equiprováveis $K \in \{0, 1, 2, 3, 4\}$ com probabilidade exata $1/5 = 0{,}20$.
* **Regra de Inicialização da Semente:** A semente é inicializada **uma única vez no início de cada experimento**, nunca antes de cada rodada individual.
* **Sementes Registradas:**
  * **Experimento 1, Experimento 4 e Experimento 5:** `semente = 2026` ($N = 10.000$ rodadas). *(Nota: a Rodada #1 da semente `2026` sorteia exatamente as paradas $K = (0, 2, 4)$, reproduzindo o tabuleiro da Figura 2 do enunciado com linha central `B - D - A`).*
  * **Experimento 2:** `sementes = (10, 2026, 123456)` ($3 \times 10.000$ rodadas, reutilizando a sequência `2026` do Experimento 1 e auditando os 10 primeiros resultados).
  * **Experimento 3, Extra 2 e Extra 3:** `semente = 42` (inicializada uma única vez e continuada sequencialmente entre os $100$ participantes virtuais com saldo inicial $B_0 = 100$ e limite de $500$ rodadas).
  * **Extra 1 (Intervalos de Confiança):** `sementes = 5000 a 5099` ($M = 100$ execuções independentes de $N = 10.000$ rodadas cada).
* **Bibliotecas Auxiliares (Gráficos e Relatório PDF):** `matplotlib 3.11.2`, `numpy 2.5.4`, `reportlab 5.1.0`.

---

## 3. Estrutura e Localização dos Arquivos Entregáveis

```text
maquina_estatistica/
├── README.md                                     # Este documento (instruções, ambiente, mapa e declaração de IA)
├── relatorio.pdf                                 # Relatório final em PDF (9 páginas de conteúdo + Referências e Anexo Extras)
├── relatorio.tex                                 # Código-fonte LaTeX correspondente ao relatório
├── simulador.py                                  # Simulador principal (regras, rodada 3x3, Exp. 1 a 5 e Extras)
├── gerar_graficos.py                             # Gerador dos gráficos científicos acessíveis (PNG 300 DPI e PDF vetorial)
├── gerar_relatorio_pdf.py                        # Compilador automatizado do relatório acadêmico em PDF
├── test_simulador.py                             # Suite de validação automatizada com 8 testes (Extra 7)
├── notebook_maquina_estatistica.ipynb            # Jupyter Notebook interativo com os experimentos
├── educacao_cientifica_acessivel.html            # Página web de Educação Científica (3 min) e Simulador Acessível (Extras 5 e 6)
├── auditoria_fontes_publicas.md                  # Auditoria metodológica das afirmações quantitativas públicas (Extra 4)
└── resultados/
    ├── resumo_completo.json                      # Metadados do ambiente e resultados consolidados em JSON
    ├── e1_tabela_frequencias.csv                 # Tabela do Experimento 1 (6 categorias, contagens somando 10.000)
    ├── e1_resumo_estatistico.csv                 # Média, RTP observado, proporção de prêmios e DP amostral s (E1)
    ├── e2_medias_acumuladas_3x3.csv              # Tabela 3x3 das médias acumuladas em 100, 1.000 e 10.000 rodadas (E2)
    ├── e2_reproducao_10_primeiros_2026.csv       # Auditoria de reprodução dos 10 primeiros resultados da semente 2026 (E2)
    ├── e3_sessoes_100_participantes.csv          # Dados individuais dos 100 participantes virtuais (E3, semente 42)
    ├── e3_resumo_saldos.csv                      # Proporções de ganho/empate/perda (100%), esgotamento, média e mediana (E3)
    ├── e4_probabilidade_condicional.csv          # Tabela dos 9.999 pares consecutivos pós-prêmio e pós-perda (E4)
    ├── e5_comparacao_tabelas.csv                 # Comparação Tabela Base vs. Prêmios +10% nos mesmos 10.000 sorteios (E5)
    ├── extra1_intervalos_confianca_100_execucoes.csv  # 100 execuções independentes e cobertura de 97% do IC 95% (Extra 1)
    ├── extra2_mesma_media_riscos_diferentes.csv  # Comparação de 3 tabelas com mesmo RTP=84% e dispersões distintas (Extra 2)
    ├── extra3_limites_exposicao.csv              # Comparação de 3 regras de parada pré-definidas (Extra 3)
    ├── extra8_analise_sensibilidade.csv          # 7 cenários de sensibilidade e cálculo do ponto de equilíbrio (Extra 8)
    └── graficos/
        ├── fig01_modelo_teorico.png / .pdf       # Figura 1: Distribuição teórica de X e contribuição para E[X] = -0,16
        ├── fig02_e1_frequencias.png / .pdf       # Figura 2: Experimento 1 (Teoria vs. Observação em N=10.000)
        ├── fig03_e2_convergencia.png / .pdf      # Figura 3: Experimento 2 (Trajetórias das 3 sementes e LGN)
        ├── fig04_e3_saldo_limitado.png / .pdf    # Figura 4: Experimento 3 (5 primeiros participantes e histograma de Bf)
        ├── fig05_e4_condicional.png / .pdf       # Figura 5: Experimento 4 (Probabilidade condicional nos 9.999 pares)
        ├── fig06_e5_comparacao_tabelas.png / .pdf# Figura 6: Experimento 5 (Tabela Base vs. Prêmios +10%)
        └── fig07_extras_aprofundamento.png / .pdf# Figura 7: Painel quádruplo dos experimentos extras (Seção 10)
```

---

## 4. Instruções de Execução

### 4.1 Executar uma rodada demonstrativa e todos os 5 experimentos + extras (gerando os CSVs)
```bash
python simulador.py
```
* Para exibir o tabuleiro no **Modo Acessível Multimodal** (formas geométricas `● ▲ ■ ◆ ★` + letras + descrições textuais):
  ```bash
  python simulador.py --acessivel
  ```
* Para iniciar o **Modo Interativo por Teclado no Terminal** (girar rodadas passo a passo):
  ```bash
  python simulador.py --interativo
  ```

### 4.2 Executar a suite de Validação Automatizada (Extra 7 – 8 testes unitários)
```bash
python -m unittest test_simulador.py -v
```

### 4.3 Regerar todos os gráficos científicos (PNG e PDF vetorial)
```bash
python gerar_graficos.py
```

### 4.4 Regerar o Relatório em PDF (`relatorio.pdf`)
```bash
python gerar_relatorio_pdf.py
```

### 4.5 Abrir a Interface Web Acessível e Guia de Educação Científica (Extras 5 e 6)
Basta abrir o arquivo `educacao_cientifica_acessivel.html` em qualquer navegador web moderno. A página funciona 100% offline, suporta navegação por teclado (`Alt+1`, `Alt+2`, `Alt+R`, `Alt+C` para Alto Contraste WCAG AAA) e leitor de tela (`aria-live="polite"`).

---

## 5. Conferência Antes da Entrega (Checklist da Seção 9)

- [x] **Pagamento das cinco triplas e prêmio zero nas demais:** Verificado analiticamente e por teste exaustivo das $125$ triplas em `test_01_espaco_amostral_125_triplas_e_pagamentos`.
- [x] **Desconto da aposta no lucro ($X = P - 1$):** Verificado em todas as rodadas (prêmio $0 \implies X = -1$; prêmios $5, 10, 15, 25, 50 \implies X = 4, 9, 14, 24, 49$).
- [x] **Reprodução pela semente:** Verificado que a repetição da semente `2026` no mesmo ambiente reproduz 10/10 dos dez primeiros resultados (`e2_reproducao_10_primeiros_2026.csv`).
- [x] **Soma de 10.000 contagens no Experimento 1:** $77 + 88 + 78 + 88 + 81 + 9.588 = 10.000$ (`e1_tabela_frequencias.csv`).
- [x] **Categorias de saldo somando 100 pessoas no Experimento 3:** $23\text{ (ganho)} + 2\text{ (empate)} + 75\text{ (perda)} = 100\text{ participantes}$ ($100{,}0\%$), sendo o esgotamento ($67$ participantes, $67{,}0\%$) subconjunto das perdas (`e3_resumo_saldos.csv`).
- [x] **Soma de 9.999 pares no Experimento 4:** $412\text{ (após prêmio)} + 9.587\text{ (após perda)} = 9.999\text{ pares consecutivos}$ (`e4_probabilidade_condicional.csv`).
- [x] **Figuras com número, legenda e fonte fora da imagem:** Todas as 7 figuras de `relatorio.pdf` e `relatorio.tex` possuem número, legenda explicativa e fonte compostos no texto do relatório, fora da imagem gráfica.

---

## 6. Declaração de Uso de Inteligência Artificial (Transparência e Autoria)

Em conformidade com as diretrizes das Seções 4 e 9 da especificação do trabalho:

1. **Onde a IA auxiliou:** Ferramentas de Inteligência Artificial generativa foram utilizadas como suporte para a organização modular do código-fonte em Python (`simulador.py`, `gerar_graficos.py`, `test_simulador.py` e `gerar_relatorio_pdf.py`), estruturação do layout acessível em HTML/CSS (`educacao_cientifica_acessivel.html`), diagramação tipográfica em PDF/LaTeX e revisão redacional.
2. **O que foi conferido e validado pelo grupo:**
   * Todas as fórmulas probabilísticas e estatísticas ($\Omega = 125$, $\Pr(\text{prêmio}) = 4\%$, $\mathbb{E}[P] = 0{,}84$, $\mathbb{E}[X] = -0{,}16$, $\sigma_X = 5{,}2052$, $\text{RTP} = 84\%$ na base e $\text{RTP}_{+10\%} = 92{,}4\%$, $\mathbb{E}[X_{+10\%}] = -0{,}076$).
   * A implementação correta do sorteio circular $\mathcal{R}_K, \mathcal{R}_{(K+1)\bmod 5}, \mathcal{R}_{(K+2)\bmod 5}$ e o controle externo da semente sem reinicialização entre rodadas.
   * Todos os resultados numéricos das tabelas CSV, os testes unitários automatizados e a precisão na interpretação das fontes documentais (distinção entre normas legais, decisões/pleitos judiciais, fluxos Pix do BCB, receita bruta do TCU, custos sociais modelados pelo IEPS e prevalências epidemiológicas da *The Lancet Public Health* e do LENAD III).
   * Todos os integrantes compreendem e subscrevem integralmente o código, os cálculos e a argumentação crítica apresentada no relatório.
