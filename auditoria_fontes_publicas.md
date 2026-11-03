# Auditoria Metodológica de Afirmações Quantitativas Públicas (Extra 4 – Seção 10)

Este documento aprofunda a verificação metodológica nas fontes originais de quatro alegações quantitativas centrais do debate público brasileiro e internacional sobre apostas digitais, examinando **definição operacional, população/universo, denominador, período de referência, método de estimação e limites de inferência causal**.

---

## 1. Alegação Auditada 1: *"Brasileiros transferem de R$ 18 a 21 bilhões por mês para casas de apostas via Pix"*

* **Fonte primária:** BANCO CENTRAL DO BRASIL (BCB). *Análise técnica sobre o mercado de apostas online no Brasil e o perfil dos apostadores*. Estudo Especial nº 119/2024 e Nota Técnica nº 513/2024 (setembro de 2024), especialmente p. 1–2 [11].
* **Gênero documental:** Nota técnica institucional de autoridade monetária e supervisão financeira.
* **Período de referência:** Janeiro a agosto de 2024 (com foco nas estimativas mensais consolidadas do 1º semestre e 3º trimestre de 2024).
* **População e universo observado:** Pessoas físicas detentoras de contas transacionais no Sistema de Pagamentos Instantâneos (SPI/Pix) que realizaram transferências para um conjunto mapeado de empresas intermediadoras de pagamento e operadoras de apostas identificadas pelo BCB.
* **Definição operacional da medida:** **Fluxo bruto de saída (transferências brutas enviadas)** via Pix dos apostadores para as plataformas identificadas.
* **Método de mensuração:** Rastreamento administrativo de transações no SPI para chaves Pix e CNPJs de instituições de pagamento/intermediadoras associadas a plataformas de apostas de quota fixa e jogos on-line.
* **Limites metodológicos e erros frequentes de interpretação pública:**
  1. **Fluxo bruto $\neq$ Perda líquida (GGR):** O valor de R\$ 18–21 bilhões mensais mede o *turnover* de depósitos via Pix, e **não** a perda líquida das famílias. Parte substancial desse montante retorna aos apostadores sob a forma de prêmios pagos e é subsequentemente **reapostada** múltiplas vezes dentro do mesmo mês (efeito multiplicador de giro decorrente do RTP). Na própria Nota Técnica, o BCB estima que a retenção líquida (apostas menos prêmios devolvidos) representa uma fração menor (da ordem de 10% a 15% do fluxo bruto, dependendo da modalidade).
  2. **Incerteza na identificação de destinatários:** Como muitas plataformas operavam no exterior em 2024 por meio de intermediadoras de pagamento (*payment facilitators*) que também processavam outros serviços digitais, o próprio Banco Central qualifica o número como **estimativa preliminar** sujeita a sub-identificação (operadores clandestinos não mapeados) ou sobre-identificação (intermediadoras multipropósito).

---

## 2. Alegação Auditada 2: *"A receita bruta das apostas autorizadas foi de R$ 17,4 bilhões no 1º semestre de 2025"*

* **Fonte primária:** TRIBUNAL DE CONTAS DA UNIÃO (TCU). *Acórdão nº 1296/2026 – Plenário* (Sessão de 19 de maio de 2026), com base em dados da Secretaria de Prêmios e Apostas do Ministério da Fazenda (SPA/MF) [12].
* **Gênero documental:** Acórdão de auditoria operacional de controle externo.
* **Período de referência:** 1º semestre de 2025 (6 meses, correspondente ao início da operação do mercado regulado sob a Lei nº 14.790/2023).
* **População e universo observado:** Operadoras de apostas de quota fixa e jogos on-line formalmente autorizadas pela SPA/MF no Brasil.
* **Definição operacional da medida:** **Receita Bruta de Jogos (*Gross Gaming Revenue* – GGR)**, definida legalmente como o total de apostas arrecadadas menos o total de prêmios efetivamente pagos aos apostadores no período ($\sum \text{Apostas} - \sum \text{Prêmios}$). No nosso modelo didático da Máquina Estatística, o GGR corresponde exatamente a $\sum (1 - P_i) = -\sum X_i$, cuja esperança é $+0{,}16n$ para o operador.
* **Limites metodológicos:**
  1. **Exclusão do mercado ilegal:** O valor de R\$ 17,4 bilhões abrange exclusivamente o **mercado autorizado**. Como o próprio Acórdão 1296/2026 demonstra, uma parcela expressiva do mercado continuou operando na clandestinidade em 2025–2026 devido a limitações técnicas de bloqueio de domínios pela Anatel e de rastreamento de contas-laranja pelo sistema financeiro.
  2. **GGR $\neq$ Lucro líquido empresarial:** O GGR representa a perda líquida agregada dos apostadores no mercado regulado (média de ~R\$ 2,9 bilhões/mês no 1º sem/2025), mas não equivale ao lucro líquido contábil das empresas após descontar tributação federal/setorial, taxas de meios de pagamento, custos de servidores e despesas de publicidade.

---

## 3. Alegação Auditada 3: *"As apostas online geram R$ 38,8 bilhões anuais em custos para o Brasil, sendo R$ 30,6 bilhões na saúde"*

* **Fonte primária:** ROSA, D. et al. (IEPS; FPSM; Umane). *A saúde dos brasileiros em jogo: análise político-econômica da regulamentação de apostas online e seus impactos para a saúde da população brasileira*. Dezembro de 2025, 40 p. (especialmente a seção metodológica nas páginas 33–35) [13], apoiada nos parâmetros de OHID / Public Health England (2021/2023) [14].
* **Gênero documental:** Dossiê técnico-científico de avaliação de políticas de saúde.
* **Período e população:** Estimativa anualizada para a população adulta brasileira (base demográfica e socioeconômica 2023–2025).
* **Definição operacional e método de cálculo (p. 33–35):**
  1. O estudo **não** soma notas fiscais ou ordens bancárias do Fundo Nacional de Saúde (SUS). Trata-se de uma **estimativa de custos sociais e econômicos totais**, dividida em:
     * **Custos diretos e indiretos tangíveis (~R\$ 8,2 bilhões):** perda de produtividade laboral, desemprego associado, custos do sistema de justiça/segurança e assistência social.
     * **Custos associados à saúde (~R\$ 30,6 bilhões):** incluem tanto a estimativa de atenção a transtornos mentais/depressão/suicídio quanto a **valoração monetária intangível de anos de vida ajustados por qualidade perdidos (QALYs / DALYs)**.
  2. Como o Brasil carecia de coortes longitudinais próprias que medissem o risco relativo atribuível exclusivamente às apostas em cada desfecho, os autores utilizaram o método de **extrapolação de parâmetros internacionais**: aplicaram os pesos e custos unitários estimados na Inglaterra pelo *Office for Health Improvement and Disparities* (OHID/PHE [14]), convertidos por Paridade de Poder de Compra (PPC) e ajustados pela estrutura demográfica e prevalência estimada no Brasil.
* **Limites metodológicos explicitados nas páginas 33–35 do dossiê:**
  1. **Não é despesa orçamentária do SUS:** Reproduzir o número de R\$ 30,6 bilhões como se fosse "gasto financeiro pago pelo caixa do SUS" é um erro conceitual grave; a maior fração decorre da valoração econômica de perdas de bem-estar e saúde (QALYs).
  2. **Associação vs. Causalidade:** Os estudos de base que alimentam o modelo de custos (incluindo OHID [14]) apoiam-se majoritariamente em levantamentos transversais onde comorbidades (como depressão prévia, uso de álcool e vulnerabilidade socioeconômica) coexistem com o jogo problemático, não permitindo isolar 100% da fração atribuível como efeito causal estrito.

---

## 4. Alegação Auditada 4: *"15,8% dos apostadores de cassino/rolos online desenvolvem transtorno do jogo"*

* **Fonte primária:** WARDLE, H. et al. *The Lancet Public Health Commission on gambling*. The Lancet Public Health, v. 9, p. e950–e994, 2024 [2]; em diálogo com o levantamento nacional **LENAD III (UNIFESP/UNIAD, 2025)** [3].
* **Método e denominador:** Meta-análise de prevalência agrupada (*pooled prevalence*) de estudos internacionais. A taxa puntual de **15,8%** possui um **Intervalo de Confiança de 95% amplo, de 10,7% a 21,6%**, refletindo heterogeneidade entre países e instrumentos psicométricos.
* **Importância crítica do denominador:**
  * O denominador de 15,8% é o subgrupo de **adultos que consumiram especificamente produtos de cassino on-line ou máquinas de rolos digitais (*online slots*) nos últimos 12 meses**.
  * Aplicar 15,8% sobre a população total brasileira (~160 milhões de adultos) produziria uma superestimativa grosseira.
* **Rastreamento psicométrico (PGSI no LENAD III) vs. Diagnóstico Clínico:** No Brasil, o LENAD III [3] avaliou uma subamostra probabilística de **4.914 participantes** no módulo de apostas utilizando a escala **PGSI (*Problem Gambling Severity Index*)**, composta por 9 itens pontuados de 0 a 27 (classificando em sem risco, risco baixo, risco moderado e jogo problemático com escore $\ge 8$). Do ponto de vista estatístico e médico, o escore PGSI $\ge 8$ é um **indicador epidemiológico de rastreamento (*screening*)**, e não um diagnóstico clínico individual pelo DSM-5 ou CID-11.

---

## 5. Síntese Comparativa: Por que não se pode somar os números?

| Medida | Natureza Contábil / Estatística | Período Temporal | Universo / Denominador | Pode ser somada às demais? |
| :--- | :--- | :--- | :--- | :--- |
| **R$ 18–21 bi/mês (BCB)** | Fluxo bruto de pagamentos (inclui reapostas) | Mensal (2024) | Transferências Pix identificadas | **Não** (é fluxo bruto de caixa, não perda líquida nem custo social) |
| **R$ 17,4 bi (TCU)** | Receita bruta das operadoras ($\text{Apostas} - \text{Prêmios}$) | Semestral (1º sem. 2025) | Mercado formalmente autorizado | **Não** (é um subconjunto líquido do fluxo apostado em outro período) |
| **R$ 38,8 bi/ano (IEPS)** | Custo social modelado (tangível + intangível/QALYs) | Anualizado (projeção) | Sociedade brasileira (externalidades) | **Não** (mede impacto econômico-sanitário indireto e intangível) |
