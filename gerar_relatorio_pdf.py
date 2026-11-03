#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gerador do Relatório Acadêmico em PDF (relatorio.pdf)
=====================================================
Constrói o relatório técnico-científico completo do Trabalho I de
Probabilidade e Estatística I (IFES - Campus Serra, 2026/2).

Utiliza fontes TrueType Unicode completas (DejaVu Sans) para renderização
matemática perfeita (X̄, P̄, τ̄, ℝ, Ω, σ, ∑, √, ≈, ≤, ≥) e células com
quebra automática de linha em todas as tabelas.
"""

import os
import matplotlib
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    HRFlowable,
    Image,
    KeepTogether,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Table,
    TableStyle,
)

# Registra a família de fontes TrueType Unicode DejaVuSans (incluída no matplotlib)
_TTF_DIR = os.path.join(os.path.dirname(matplotlib.__file__), "mpl-data", "fonts", "ttf")
pdfmetrics.registerFont(TTFont("DejaVu", os.path.join(_TTF_DIR, "DejaVuSans.ttf")))
pdfmetrics.registerFont(TTFont("DejaVu-Bold", os.path.join(_TTF_DIR, "DejaVuSans-Bold.ttf")))
pdfmetrics.registerFont(TTFont("DejaVu-Oblique", os.path.join(_TTF_DIR, "DejaVuSans-Oblique.ttf")))
pdfmetrics.registerFont(TTFont("DejaVu-BoldOblique", os.path.join(_TTF_DIR, "DejaVuSans-BoldOblique.ttf")))
pdfmetrics.registerFontFamily(
    "DejaVu",
    normal="DejaVu",
    bold="DejaVu-Bold",
    italic="DejaVu-Oblique",
    boldItalic="DejaVu-BoldOblique",
)

PAGINA_FIM_CONTEUDO = 9


def construir_estilos():
    """Define a folha de estilos tipográficos acadêmicos do relatório com suporte Unicode completo."""
    base = getSampleStyleSheet()

    estilos = {
        "InstCabecalho": ParagraphStyle(
            "InstCabecalho",
            parent=base["Normal"],
            fontName="DejaVu-Bold",
            fontSize=9.2,
            leading=11.5,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#1E293B"),
        ),
        "TituloPrincipal": ParagraphStyle(
            "TituloPrincipal",
            parent=base["Title"],
            fontName="DejaVu-Bold",
            fontSize=12.5,
            leading=15.5,
            alignment=TA_CENTER,
            spaceBefore=3,
            spaceAfter=2,
            textColor=colors.HexColor("#0F172A"),
        ),
        "Subtitulo": ParagraphStyle(
            "Subtitulo",
            parent=base["Normal"],
            fontName="DejaVu",
            fontSize=8.8,
            leading=11.2,
            alignment=TA_CENTER,
            spaceAfter=4,
            textColor=colors.HexColor("#334155"),
        ),
        "SecaoH1": ParagraphStyle(
            "SecaoH1",
            parent=base["Heading1"],
            fontName="DejaVu-Bold",
            fontSize=10.5,
            leading=13.2,
            spaceBefore=7,
            spaceAfter=3,
            textColor=colors.HexColor("#004B87"),
            keepWithNext=True,
        ),
        "SecaoH2": ParagraphStyle(
            "SecaoH2",
            parent=base["Heading2"],
            fontName="DejaVu-Bold",
            fontSize=9.2,
            leading=11.8,
            spaceBefore=5,
            spaceAfter=2,
            textColor=colors.HexColor("#0F172A"),
            keepWithNext=True,
        ),
        "Corpo": ParagraphStyle(
            "Corpo",
            parent=base["BodyText"],
            fontName="DejaVu",
            fontSize=8.4,
            leading=11.4,
            alignment=TA_JUSTIFY,
            spaceBefore=0,
            spaceAfter=3.8,
            textColor=colors.HexColor("#111827"),
        ),
        "Equacao": ParagraphStyle(
            "Equacao",
            parent=base["BodyText"],
            fontName="DejaVu-Oblique",
            fontSize=8.4,
            leading=11.5,
            alignment=TA_CENTER,
            spaceBefore=2,
            spaceAfter=3,
            textColor=colors.HexColor("#0F172A"),
        ),
        "CaixaDestaque": ParagraphStyle(
            "CaixaDestaque",
            parent=base["BodyText"],
            fontName="DejaVu",
            fontSize=8.1,
            leading=11.0,
            alignment=TA_JUSTIFY,
            backColor=colors.HexColor("#F1F5F9"),
            borderColor=colors.HexColor("#94A3B8"),
            borderWidth=0.7,
            borderPadding=5,
            spaceBefore=3,
            spaceAfter=4,
        ),
        "LegendaTitulo": ParagraphStyle(
            "LegendaTitulo",
            parent=base["Normal"],
            fontName="DejaVu",
            fontSize=7.9,
            leading=10.2,
            alignment=TA_JUSTIFY,
            spaceBefore=2.5,
            spaceAfter=1.5,
            textColor=colors.HexColor("#1E293B"),
            keepWithNext=True,
        ),
        "LegendaFonte": ParagraphStyle(
            "LegendaFonte",
            parent=base["Normal"],
            fontName="DejaVu-Oblique",
            fontSize=7.4,
            leading=9.5,
            alignment=TA_LEFT,
            spaceBefore=1.0,
            spaceAfter=4.0,
            textColor=colors.HexColor("#475569"),
        ),
        "CelulaTabela": ParagraphStyle(
            "CelulaTabela",
            parent=base["Normal"],
            fontName="DejaVu",
            fontSize=7.5,
            leading=9.6,
            alignment=TA_LEFT,
        ),
        "CelulaTabelaDir": ParagraphStyle(
            "CelulaTabelaDir",
            parent=base["Normal"],
            fontName="DejaVu",
            fontSize=7.5,
            leading=9.6,
            alignment=TA_RIGHT,
        ),
        "CelulaTabelaCentro": ParagraphStyle(
            "CelulaTabelaCentro",
            parent=base["Normal"],
            fontName="DejaVu",
            fontSize=7.5,
            leading=9.6,
            alignment=TA_CENTER,
        ),
        "CelulaCabecalho": ParagraphStyle(
            "CelulaCabecalho",
            parent=base["Normal"],
            fontName="DejaVu-Bold",
            fontSize=7.6,
            leading=9.6,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#0F172A"),
        ),
        "RefItem": ParagraphStyle(
            "RefItem",
            parent=base["Normal"],
            fontName="DejaVu",
            fontSize=7.7,
            leading=10.2,
            alignment=TA_JUSTIFY,
            leftIndent=14,
            firstLineIndent=-14,
            spaceAfter=2.5,
        ),
    }
    return estilos


def estilo_tabela_academica():
    """Retorna um TableStyle no padrão booktabs acadêmico."""
    return TableStyle([
        ("LINEABOVE", (0, 0), (-1, 0), 1.1, colors.HexColor("#0F172A")),
        ("LINEBELOW", (0, 0), (-1, 0), 0.8, colors.HexColor("#334155")),
        ("LINEBELOW", (0, -1), (-1, -1), 1.1, colors.HexColor("#0F172A")),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#F1F5F9")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 2.8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2.8),
        ("LEFTPADDING", (0, 0), (-1, -1), 4.0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4.0),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8FAFC")]),
    ])


def converter_linhas_tabela(linhas_brutas, alinhamentos, est):
    """Converte strings simples em objetos Paragraph com o alinhamento indicado para evitar overflow."""
    mapa_est = {
        "LEFT": est["CelulaTabela"],
        "RIGHT": est["CelulaTabelaDir"],
        "CENTER": est["CelulaTabelaCentro"],
    }
    tabela_formatada = [linhas_brutas[0]]
    for linha in linhas_brutas[1:]:
        nova_linha = []
        for idx, cel in enumerate(linha):
            if isinstance(cel, Paragraph):
                nova_linha.append(cel)
            else:
                al = alinhamentos[idx] if idx < len(alinhamentos) else "LEFT"
                nova_linha.append(Paragraph(str(cel), mapa_est[al]))
        tabela_formatada.append(nova_linha)
    return tabela_formatada


def bloco_figura(caminho_png: str, largura_cm: float, altura_cm: float, numero: int, legenda: str, fonte: str, est):
    """Insere uma figura com número, legenda e fonte FORA da imagem."""
    img = Image(caminho_png, width=largura_cm * cm, height=altura_cm * cm)
    img.hAlign = "CENTER"
    p_leg = Paragraph(f"<b>Figura {numero}.</b> {legenda}", est["LegendaTitulo"])
    p_fnt = Paragraph(f"<b>Fonte:</b> {fonte}", est["LegendaFonte"])
    return KeepTogether([img, p_leg, p_fnt])


def desenhar_cabecalho_rodape(canvas, doc):
    """Adiciona cabeçalho e rodapé institucionais no estilo do documento do IFES."""
    canvas.saveState()
    largura, altura = A4
    margem_esq = 1.8 * cm
    margem_dir = largura - 1.8 * cm

    if doc.page > 1:
        canvas.setFont("DejaVu", 7.6)
        canvas.setFillColor(colors.HexColor("#334155"))
        canvas.drawString(margem_esq, altura - 1.22 * cm, "IFES – Campus Serra")
        canvas.drawCentredString(largura / 2.0, altura - 1.22 * cm, "Probabilidade e Estatística I – Máquina Estatística")
        canvas.drawRightString(margem_dir, altura - 1.22 * cm, "Trabalho I – 2026/2")
        canvas.setStrokeColor(colors.HexColor("#64748B"))
        canvas.setLineWidth(0.5)
        canvas.line(margem_esq, altura - 1.35 * cm, margem_dir, altura - 1.35 * cm)

    canvas.setStrokeColor(colors.HexColor("#CBD5E1"))
    canvas.setLineWidth(0.4)
    canvas.line(margem_esq, 1.30 * cm, margem_dir, 1.30 * cm)
    canvas.setFont("DejaVu", 7.6)
    canvas.setFillColor(colors.HexColor("#475569"))
    canvas.drawString(margem_esq, 0.90 * cm, "Simulador acadêmico - somente créditos fictícios")
    tipo_pag = f"Conteúdo Principal ({doc.page}/{PAGINA_FIM_CONTEUDO})" if doc.page <= PAGINA_FIM_CONTEUDO else "Referências e Anexos Extras"
    canvas.drawRightString(margem_dir, 0.90 * cm, f"Página {doc.page} – {tipo_pag}")
    canvas.restoreState()


def gerar_pdf(caminho_pdf: str, dir_graficos: str) -> None:
    """Compila o relatório completo em PDF."""
    est = construir_estilos()
    doc = SimpleDocTemplate(
        caminho_pdf,
        pagesize=A4,
        leftMargin=1.8 * cm,
        rightMargin=1.8 * cm,
        topMargin=1.65 * cm,
        bottomMargin=1.55 * cm,
        title="Máquina Estatística: Probabilidade, Apostas e Pensamento Crítico",
        author="Grupo Acadêmico - Bacharelado em Sistemas de Informação - IFES Campus Serra",
        subject="Trabalho I de Probabilidade e Estatística I (2026/2)",
    )

    story = []

    # ==========================================================================
    # CABEÇALHO INSTITUCIONAL (Sem capa isolada, conforme Seção 4)
    # ==========================================================================
    story.append(Paragraph("Instituto Federal do Espírito Santo – Campus Serra", est["InstCabecalho"]))
    story.append(Paragraph("Bacharelado em Sistemas de Informação | Probabilidade e Estatística I – Trabalho I (2026/2)", est["Subtitulo"]))
    story.append(Paragraph("MÁQUINA ESTATÍSTICA: PROBABILIDADE, APOSTAS E PENSAMENTO CRÍTICO", est["TituloPrincipal"]))
    story.append(
        Paragraph(
            "<b>Professor:</b> Fidelis Zanetti de Castro &nbsp;&nbsp;|&nbsp;&nbsp; "
            "<b>Entrega:</b> 29 de outubro de 2026 &nbsp;&nbsp;|&nbsp;&nbsp; "
            "<b>Aviso:</b> <i>Simulador acadêmico - somente créditos fictícios</i>",
            est["Subtitulo"],
        )
    )
    story.append(HRFlowable(width="100%", thickness=1.0, color=colors.HexColor("#0F172A"), spaceBefore=2, spaceAfter=5))

    # ==========================================================================
    # SEÇÃO 1: CONTEXTO, PROBLEMÁTICA E FONTES NO TEMPO
    # ==========================================================================
    story.append(Paragraph("1. Contexto, problemática e situação das fontes no tempo", est["SecaoH1"]))
    story.append(
        Paragraph(
            "A rápida difusão das apostas digitais no Brasil conectou algoritmos de sorteio instantâneo, meios de pagamento "
            "imediato (como o Pix), publicidade intensiva por influenciadores digitais e uso contínuo do telefone celular. "
            "Entre os produtos de maior apelo visual destacam-se as máquinas virtuais de rolos (<i>online slots</i>), "
            "popularmente associadas ao chamado “jogo do tigrinho” [18, 20]. Embora animações, efeitos sonoros e vitórias "
            "ocasionais tornem cada rodada intuitiva, a interface gráfica não explicita ao usuário a probabilidade real de "
            "obter um prêmio nem o comportamento financeiro acumulado de repetir a aposta centenas de vezes. Este trabalho "
            "investiga a pergunta central proposta na especificação: <b>como ganhos ocasionais podem coexistir com uma "
            "perda esperada para o jogador, e o que essa diferença nos ajuda a compreender sobre as apostas na sociedade?</b>",
            est["Corpo"],
        )
    )
    story.append(
        Paragraph(
            "Para responder a essa questão com rigor metodológico, é indispensável separar dois planos analíticos: "
            "(i) a <b>demonstração matemática e computacional</b> de uma máquina didática com regras públicas (Seções 2 e 3), "
            "que descreve propriedades exatas do modelo probabilístico e resultados de participantes virtuais com créditos "
            "fictícios; e (ii) a <b>análise documental e epidemiológica</b> sobre saúde pública, orçamento familiar e "
            "regulação estatal (Seção 4), uma vez que simulações computacionais não medem prevalência clínica de "
            "transtornos nem estimam o impacto macroeconômico nacional.",
            est["Corpo"],
        )
    )
    story.append(
        Paragraph(
            "<b>Evolução regulatória e distinção epistemológica das fontes (2023–setembro de 2026).</b> O quadro "
            "institucional brasileiro alterou-se substancialmente em curto período. Em 29 de dezembro de 2023, a "
            "<b>Lei nº 14.790/2023</b> [6] (norma legal publicada) regulamentou as apostas de quota fixa em eventos "
            "esportivos e jogos on-line. Em 19 de maio de 2026, o <b>Tribunal de Contas da União (Acórdão nº 1296/2026 – "
            "Plenário)</b> [12] (auditoria institucional) apontou falhas de coordenação governamental e limitações técnicas "
            "no bloqueio de operadores clandestinos. Diante do agravamento dos indicadores sanitários e financeiros, em "
            "<b>25 de setembro de 2026</b> foi editada a <b>Medida Provisória nº 1.394/2026</b> [7, 8] (norma publicada com "
            "força de lei imediata, sujeita à apreciação do Congresso Nacional), proibindo a exploração, oferta, "
            "intermediação e publicidade de apostas de quota fixa e jogos on-line no país, preservadas apenas as "
            "modalidades lotéricas clássicas autorizadas em lei. Três dias depois, em <b>28 de setembro de 2026</b>, "
            "ocorreram dois fatos jurídicos de natureza distinta reportados pela Agência Brasil: a União ajuizou Ação "
            "Civil Pública contra 17 plataformas pedindo no mínimo R$ 1 bilhão por danos morais coletivos e ressarcimento "
            "ao SUS [9], enquanto as associações empresariais ANJL e IBJR acionaram o Supremo Tribunal Federal (STF) "
            "pleiteando a suspensão da MP sob argumentos de insegurança jurídica, prejuízo a investimentos e ausência de "
            "urgência [10]. Cumpre distinguir com precisão: os pedidos da União e as petições da ANJL/IBJR constituem "
            "<b>alegações e pleitos das partes em litígio</b>, não equivalendo a condenação transitada em julgado nem a "
            "decisão definitiva do STF. Do mesmo modo, a leitura crítica exige <b>não somar nem confundir</b> as três "
            "grandes cifras nacionais, pois referem-se a períodos, universos e definições contábeis incompatíveis (Tabela 1).",
            est["Corpo"],
        )
    )

    dados_tab_contexto = [
        [
            Paragraph("<b>Indicador / Medida</b>", est["CelulaCabecalho"]),
            Paragraph("<b>Fonte e Gênero Documental</b>", est["CelulaCabecalho"]),
            Paragraph("<b>Período / Universo</b>", est["CelulaCabecalho"]),
            Paragraph("<b>Interpretação Correta e Limites Metodológicos</b>", est["CelulaCabecalho"]),
        ],
        [
            "R$ 18 a 21 bilhões mensais",
            "Banco Central do Brasil (NT 513/2024; EE 119/2024) [11] – Nota técnica oficial",
            "Jan–Ago 2024; pessoas físicas via Pix para plataformas identificadas",
            "Mede <b>transferências brutas</b> enviadas via Pix. Não desconta prêmios sacados nem reapostas; não equivale automaticamente à perda líquida das famílias.",
        ],
        [
            "R$ 17,4 bilhões no semestre",
            "TCU (Acórdão 1296/2026) [12] – Auditoria de controle externo",
            "1º semestre de 2025; mercado autorizado (SPA/MF)",
            "Mede a <b>receita bruta de jogos (GGR)</b>: total apostado menos prêmios pagos. Difere de depósitos brutos e do lucro líquido empresarial após tributos e marketing.",
        ],
        [
            "R$ 38,8 bilhões anuais (R$ 30,6 bi saúde)",
            "Rosa et al. / IEPS (2025) [13] – Dossiê de pesquisa econômico-sanitária",
            "Projeção anualizada (base 2023–2025); população brasileira afetada",
            "Estimativa de <b>custos sociais</b> (monetários e valoração de perda de qualidade de vida/QALYs) extrapolada de parâmetros britânicos (OHID/PHE [14]) por PPC; <b>não é</b> despesa orçamentária paga pelo SUS.",
        ],
        [
            "15,8% (IC 95%: 10,7%–21,6%)",
            "Wardle et al., <i>The Lancet Public Health</i> (2024) [2] – Revisão sistemática e meta-análise",
            "Síntese internacional; <b>adultos que usaram cassino/rolos on-line</b>",
            "O denominador é restrito aos <b>usuários da modalidade</b> (cassino/slots on-line), e não a toda a população adulta brasileira.",
        ],
    ]
    t_ctx = Table(
        converter_linhas_tabela(dados_tab_contexto, ["LEFT", "LEFT", "LEFT", "LEFT"], est),
        colWidths=[2.9 * cm, 3.6 * cm, 3.2 * cm, 7.7 * cm],
    )
    t_ctx.setStyle(estilo_tabela_academica())
    story.append(Paragraph("<b>Tabela 1.</b> Distinção conceitual, temporal e metodológica entre as medidas macroeconômicas e epidemiológicas de referência.", est["LegendaTitulo"]))
    story.append(t_ctx)
    story.append(Paragraph("<b>Fonte:</b> Elaboração própria a partir de Banco Central [11], TCU [12], IEPS [13], OHID/PHE [14] e Wardle et al. [2].", est["LegendaFonte"]))

    # ==========================================================================
    # SEÇÃO 2: O MODELO DA MÁQUINA E SUA MATEMÁTICA EXATA
    # ==========================================================================
    story.append(Paragraph("2. Modelo da máquina didática e fundamentação matemática", est["SecaoH1"]))
    story.append(
        Paragraph(
            "<b>Regras públicas, montagem das colunas e estrutura de dependência.</b> O modelo-base utiliza cinco "
            "símbolos discretos, identificados por <b>A, B, C, D e E</b>, dispostos na mesma sequência circular "
            "<i>R = (A, B, C, D, E)</i> nas posições indexadas de 0 a 4 em cada um dos três rolos. Em cada rodada, "
            "o jogador realiza uma aposta fixa de <b>1 crédito fictício</b> e o programa sorteia três paradas "
            "independentes <i>K</i><sub>1</sub>, <i>K</i><sub>2</sub>, <i>K</i><sub>3</sub> ∈ {0, 1, 2, 3, 4} com "
            "distribuição discreta uniforme: cada posição <i>K</i> possui probabilidade exata de 1/5 = 0,20. "
            "Para uma parada <i>K</i> em determinado rolo, a coluna do tabuleiro 3 × 3 exibe <i>R<sub>K</sub></i> no "
            "topo, <i>R</i><sub>(<i>K</i>+1) mod 5</sub> no centro e <i>R</i><sub>(<i>K</i>+2) mod 5</sub> na base "
            "(por exemplo, para <i>K</i> = 4, a janela exibe E no topo, A no centro e B na base; na 1ª rodada da "
            "semente 2026, o gerador sorteia as paradas <i>K</i> = (0, 2, 4), formando as colunas (A,B,C), (C,D,E) e "
            "(E,A,B), cuja linha central é B–D–A, exatamente como ilustrado na Figura 2 do enunciado).",
            est["Corpo"],
        )
    )
    story.append(
        Paragraph(
            "Essa construção geométrica ensina uma distinção probabilística fundamental: <b>as células de uma mesma "
            "coluna vertical não são independentes</b>, pois são posições vizinhas rigidamente determinadas pela mesma "
            "parada <i>K</i> (saber que o topo é E implica, com probabilidade 1, que o centro é A e a base é B). "
            "Em contrapartida, como os três rolos são sorteados separadamente e a aplicação da função bijetora "
            "<i>f(K) = (K + 1) mod 5</i> preserva a equiprobabilidade de 1/5 para cada símbolo na posição central, "
            "<b>as três células da linha central são mutuamente independentes</b>, assim como resultados de rodadas "
            "distintas são independentes entre si.",
            est["Corpo"],
        )
    )
    story.append(
        Paragraph(
            "<b>Espaço amostral, variáveis aleatórias discretas, esperança e RTP.</b> O espaço amostral restrito à "
            "linha central avaliada possui cardinalidade |Ω| = 5<sup>3</sup> = <b>125 triplas centrais equiprováveis</b>. "
            "Pela independência entre os três rolos, a probabilidade de qualquer tripla específica (<i>s</i><sub>1</sub>, "
            "<i>s</i><sub>2</sub>, <i>s</i><sub>3</sub>) é o produto das probabilidades marginais: (1/5) × (1/5) × (1/5) = "
            "<b>1/125 = 0,008 (0,80%)</b>. Apenas as cinco triplas formadas por três símbolos idênticos (A–A–A, B–B–B, "
            "C–C–C, D–D–D e E–E–E) geram pagamento. Como são cinco eventos mutuamente exclusivos de probabilidade "
            "1/125 cada, a probabilidade total de receber algum prêmio em uma rodada é:",
            est["Corpo"],
        )
    )
    story.append(
        Paragraph(
            "Pr(Prêmio) = Pr(P &gt; 0) = 5 / 125 = 1 / 25 = 0,04 (4,00%), &nbsp;&nbsp;&nbsp;&nbsp; "
            "Pr(Sem prêmio) = Pr(P = 0) = 120 / 125 = 0,96 (96,00%).",
            est["Equacao"],
        )
    )
    story.append(
        Paragraph(
            "Definimos duas variáveis aleatórias discretas associadas a cada rodada: o <b>prêmio bruto</b> <i>P</i> "
            "(com suporte {0, 5, 10, 15, 25, 50}) e o <b>lucro líquido do jogador</b> <i>X = P − 1</i> (com suporte "
            "{−1, 4, 9, 14, 24, 49}), em créditos fictícios. É essencial distinguir a <i>variável aleatória</i> "
            "(função mensurável <i>X</i>: Ω → ℝ definida antes do sorteio, caracterizada por toda a sua distribuição "
            "de probabilidade) do <i>valor observado</i> <i>x<sub>i</sub></i> (número concreto realizado após girar os "
            "rolos na rodada <i>i</i>). Pela definição de valor esperado (esperança matemática) e pela propriedade de "
            "linearidade da esperança:",
            est["Corpo"],
        )
    )
    story.append(
        Paragraph(
            "E[P] = (5 + 10 + 15 + 25 + 50) / 125 = 105 / 125 = 0,84 crédito, &nbsp;&nbsp;&nbsp;&nbsp; "
            "E[X] = E[P − 1] = E[P] − 1 = 0,84 − 1 = −0,16 crédito.",
            est["Equacao"],
        )
    )
    story.append(
        Paragraph(
            "A variância teórica do lucro por rodada é Var(<i>X</i>) = E[<i>X</i><sup>2</sup>] − (E[<i>X</i>])<sup>2</sup> = "
            "[(−1)<sup>2</sup>(120) + 4<sup>2</sup> + 9<sup>2</sup> + 14<sup>2</sup> + 24<sup>2</sup> + 49<sup>2</sup>]/125 "
            "− (−0,16)<sup>2</sup> = 3390/125 − 0,0256 = 27,12 − 0,0256 = <b>27,0944 créditos<sup>2</sup></b>, resultando em "
            "um desvio-padrão populacional elevado de <b>σ<sub>X</sub> = √27,0944 ≈ 5,2052 créditos</b> (mais de 32 vezes a "
            "magnitude da esperança |E[<i>X</i>]| = 0,16). Em uma sequência de <i>n</i> rodadas <b>fixas</b>, a linearidade "
            "da esperança garante que o lucro acumulado tem esperança E[∑<sub><i>i</i>=1</sub><sup><i>n</i></sup> <i>X<sub>i</sub></i>] "
            "= <i>n</i> · E[<i>X</i>] = <b>−0,16<i>n</i></b>. O <b>Retorno ao Jogador (RTP)</b> é a razão E[<i>P</i>]/aposta = "
            "0,84/1 = <b>84,00%</b>, complementar à vantagem esperada do operador (<i>house edge</i>) de <b>16,00%</b>. "
            "Como documenta a UK Gambling Commission [17], o RTP de 84% <b>não é</b> a probabilidade de vencer uma rodada "
            "(que é 4%), nem uma garantia de que o jogador sairá de uma sessão com 84% de seu depósito inicial, pois o "
            "indicador incide sobre todo o volume bruto apostado ao longo do tempo (incluindo ganhos intermediários "
            "reapostados).",
            est["Corpo"],
        )
    )

    story.append(
        bloco_figura(
            os.path.join(dir_graficos, "fig01_modelo_teorico.png"),
            largura_cm=16.5,
            altura_cm=5.8,
            numero=1,
            legenda=(
                "Distribuição teórica de probabilidade do lucro líquido X por rodada (à esquerda) e contribuição "
                "ponderada x · Pr(X = x) de cada resultado para a formação da esperança matemática E[X] = −0,16 crédito (à direita)."
            ),
            fonte="Elaboração própria a partir das regras públicas da Seção 5 e Tabela 1 do enunciado.",
            est=est,
        )
    )

    # ==========================================================================
    # SEÇÃO 3: OS CINCO EXPERIMENTOS COMPUTACIONAIS
    # ==========================================================================
    story.append(Paragraph("3. Cinco experimentos computacionais: procedimento, resultados e interpretação", est["SecaoH1"]))
    story.append(
        Paragraph(
            "Todas as simulações foram executadas em <b>Python 3.12.7</b> (implementação oficial CPython 64 bits em "
            "Windows 11), utilizando o gerador pseudoaleatório padrão <code>random.Random(semente)</code> baseado no "
            "algoritmo <b>Mersenne Twister (MT19937)</b> de período 2<sup>19937</sup> − 1 [16], com sorteio discreto via "
            "<code>randrange(5)</code>. Em estrita conformidade com as regras metodológicas, a semente é inicializada "
            "uma única vez no início de cada experimento e nenhum resultado inesperado foi descartado ou ajustado.",
            est["Corpo"],
        )
    )

    # --- EXPERIMENTO 1 ---
    story.append(Paragraph("3.1 Experimento 1 – As frequências acompanham as probabilidades?", est["SecaoH2"]))
    story.append(
        Paragraph(
            "<b>Procedimento.</b> Inicializou-se o gerador com a <b>semente 2026</b> e simularam-se <i>N</i> = 10.000 "
            "rodadas independentes sem restrição de saldo ou regra de parada. Contabilizaram-se as ocorrências absolutas "
            "e as frequências relativas dos seis eventos da Tabela 1, bem como o lucro médio amostral <i>X̄</i> = (∑<i>X<sub>i</sub></i>)/<i>N</i>, "
            "o RTP observado <i>RTP̂</i> = (∑<i>P<sub>i</sub></i>)/<i>N</i>, a proporção de rodadas premiadas e o desvio-padrão "
            "amostral <i>s</i> com divisor <i>N</i> − 1.",
            est["Corpo"],
        )
    )

    dados_tab_e1 = [
        [
            Paragraph("<b>Linha Central</b>", est["CelulaCabecalho"]),
            Paragraph("<b>Prêmio P (cr.)</b>", est["CelulaCabecalho"]),
            Paragraph("<b>Lucro X (cr.)</b>", est["CelulaCabecalho"]),
            Paragraph("<b>Prob. Teórica</b>", est["CelulaCabecalho"]),
            Paragraph("<b>Esperado (10.000)</b>", est["CelulaCabecalho"]),
            Paragraph("<b>Contagem Obs.</b>", est["CelulaCabecalho"]),
            Paragraph("<b>Freq. Relativa Obs.</b>", est["CelulaCabecalho"]),
            Paragraph("<b>Diferença (p.p.)</b>", est["CelulaCabecalho"]),
        ],
        ["A–A–A", "5", "+4", "1/125 (0,80%)", "80,0", "77", "0,0077 (0,77%)", "−0,03 p.p."],
        ["B–B–B", "10", "+9", "1/125 (0,80%)", "80,0", "88", "0,0088 (0,88%)", "+0,08 p.p."],
        ["C–C–C", "15", "+14", "1/125 (0,80%)", "80,0", "78", "0,0078 (0,78%)", "−0,02 p.p."],
        ["D–D–D", "25", "+24", "1/125 (0,80%)", "80,0", "88", "0,0088 (0,88%)", "+0,08 p.p."],
        ["E–E–E", "50", "+49", "1/125 (0,80%)", "80,0", "81", "0,0081 (0,81%)", "+0,01 p.p."],
        ["Qualquer outra tripla", "0", "−1", "120/125 (96,00%)", "9.600,0", "9.588", "0,9588 (95,88%)", "−0,12 p.p."],
        ["<b>Total / Resumo</b>", "—", "—", "<b>125/125 (100,00%)</b>", "<b>10.000,0</b>", "<b>10.000</b>", "<b>1,0000 (100,00%)</b>", "<b>0,00 p.p.</b>"],
    ]
    t_e1 = Table(
        converter_linhas_tabela(dados_tab_e1, ["LEFT", "RIGHT", "RIGHT", "RIGHT", "RIGHT", "RIGHT", "RIGHT", "RIGHT"], est),
        colWidths=[3.1 * cm, 1.8 * cm, 1.7 * cm, 2.5 * cm, 2.2 * cm, 1.9 * cm, 2.4 * cm, 1.8 * cm],
    )
    t_e1.setStyle(estilo_tabela_academica())
    story.append(Paragraph("<b>Tabela 2.</b> Distribuição teórica e resultados empíricos do Experimento 1 (N = 10.000 rodadas, semente 2026).", est["LegendaTitulo"]))
    story.append(t_e1)
    story.append(Paragraph("<b>Fonte:</b> Resultados da simulação computacional (arquivo <code>resultados/e1_tabela_frequencias.csv</code>).", est["LegendaFonte"]))

    story.append(
        bloco_figura(
            os.path.join(dir_graficos, "fig02_e1_frequencias.png"),
            largura_cm=16.5,
            altura_cm=5.8,
            numero=2,
            legenda=(
                "Comparação entre probabilidade teórica (%) e frequência relativa observada (%) no Experimento 1 "
                "(N = 10.000, semente 2026): visão global das seis categorias (à esquerda) e escala ampliada nas cinco triplas premiadas (à direita)."
            ),
            fonte="Elaboração própria com dados do Experimento 1 (semente 2026).",
            est=est,
        )
    )

    story.append(
        Paragraph(
            "<b>Resultados e interpretação.</b> As seis contagens observadas somam exatamente <b>10.000 rodadas</b> "
            "(412 rodadas premiadas e 9.588 sem prêmio). Os indicadores globais observados foram: <b>proporção de "
            "rodadas premiadas = 4,12%</b> (vs. 4,00% teórico); <b>lucro médio amostral <i>X̄</i> = −0,1315 crédito/rodada</b> "
            "(soma de lucros = −1.315 créditos, vs. E[<i>X</i>] = −0,1600); <b>RTP observado <i>RTP̂</i> = 86,85%</b> (soma de "
            "prêmios = 8.685 créditos, vs. 84,00% teórico); e <b>desvio-padrão amostral <i>s</i> = 5,2750 créditos</b> "
            "(vs. σ<sub>X</sub> = 5,2052 créditos). A média <i>X̄</i> = −0,1315 crédito indica o centro de gravidade "
            "financeiro da amostra (perda média de ~13,15 centavos de crédito por giro), enquanto o desvio-padrão <i>s</i> = 5,2750 "
            "créditos quantifica a intensa dispersão de cada rodada individual em torno dessa média, decorrente do contraste "
            "entre perdas frequentes de −1 crédito e prêmios raros de até +49 créditos de lucro. As frequências relativas "
            "(0,77% a 0,88%) aproximam-se de 0,80%, mas não coincidem de forma exata porque em qualquer amostra finita "
            "opera a <b>variabilidade amostral</b>: o número de ocorrências de cada tripla segue uma distribuição Binomial(10.000; 0,008) "
            "com desvio-padrão √(10000 × 0,008 × 0,992) ≈ 8,91 ocorrências (±0,09 p.p.). Pelo mesmo motivo, a diferença de "
            "+0,0285 crédito entre <i>X̄</i> (−0,1315) e E[<i>X</i>] (−0,1600) equivale a apenas 0,54 erro-padrão (EP = <i>s</i>/√<i>N</i> "
            "= 0,0528), sendo flutuação aleatória perfeitamente normal (especificamente devido a 8 ocorrências extras nas "
            "triplas B–B–B e D–D–D e 1 extra em E–E–E), o que jamais autoriza alterar dados ou trocar a semente. Por fim, "
            "fica evidente por que a <b>proporção de prêmios (4,12%) não se confunde com o RTP (86,85%)</b>: a proporção "
            "de prêmios conta apenas a frequência de eventos {<i>P<sub>i</sub></i> &gt; 0} (em que 1 rodada premiada vale "
            "1 contagem), ao passo que o RTP pondera cada vitória pela magnitude monetária do prêmio pago (5 a 50 créditos).",
            est["Corpo"],
        )
    )

    # --- EXPERIMENTO 2 ---
    story.append(Paragraph("3.2 Experimento 2 – O que muda quando aumentamos a amostra?", est["SecaoH2"]))
    story.append(
        Paragraph(
            "<b>Procedimento.</b> Executaram-se três sequências independentes de <i>N</i> = 10.000 rodadas com as "
            "sementes <b>10, 2026 e 123456</b> (reutilizando integralmente a sequência da semente 2026 do Experimento 1). "
            "Registrou-se a média acumulada <i>X̄<sub>n</sub></i> = (1/<i>n</i>)∑<sub><i>i</i>=1</sub><sup><i>n</i></sup> <i>X<sub>i</sub></i> "
            "nos marcos <i>n</i> = 100, 1.000 e 10.000 rodadas (Tabela 3) e ao longo de toda a trajetória (Figura 3). "
            "Adicionalmente, reexecutou-se a semente 2026 no mesmo ambiente para auditar a reprodução exata dos dez "
            "primeiros resultados.",
            est["Corpo"],
        )
    )

    dados_tab_e2 = [
        [
            Paragraph("<b>Semente do Gerador</b>", est["CelulaCabecalho"]),
            Paragraph("<b>Média Acumulada após 100 rodadas (cr.)</b>", est["CelulaCabecalho"]),
            Paragraph("<b>Média Acumulada após 1.000 rodadas (cr.)</b>", est["CelulaCabecalho"]),
            Paragraph("<b>Média Acumulada após 10.000 rodadas (cr.)</b>", est["CelulaCabecalho"]),
            Paragraph("<b>Diferença em N=10.000 (X̄ − E[X])</b>", est["CelulaCabecalho"]),
        ],
        ["Semente 10", "−0,7000", "−0,0550", "−0,0960", "+0,0640"],
        ["Semente 2026 (E1)", "+0,2000", "−0,2200", "−0,1315", "+0,0285"],
        ["Semente 123456", "+0,2000", "−0,0700", "−0,2215", "−0,0615"],
        ["<b>Referência Teórica E[X]</b>", "<b>−0,1600</b>", "<b>−0,1600</b>", "<b>−0,1600</b>", "<b>0,0000</b>"],
    ]
    t_e2 = Table(
        converter_linhas_tabela(dados_tab_e2, ["LEFT", "RIGHT", "RIGHT", "RIGHT", "RIGHT"], est),
        colWidths=[3.4 * cm, 3.6 * cm, 3.6 * cm, 3.6 * cm, 3.2 * cm],
    )
    t_e2.setStyle(estilo_tabela_academica())
    story.append(Paragraph("<b>Tabela 3.</b> Matriz 3 × 3 das médias acumuladas de lucro líquido por rodada nas três sementes avaliadas.", est["LegendaTitulo"]))
    story.append(t_e2)
    story.append(Paragraph("<b>Fonte:</b> Resultados da simulação computacional (arquivo <code>resultados/e2_medias_acumuladas_3x3.csv</code>).", est["LegendaFonte"]))

    story.append(
        bloco_figura(
            os.path.join(dir_graficos, "fig03_e2_convergencia.png"),
            largura_cm=16.0,
            altura_cm=6.2,
            numero=3,
            legenda=(
                "Trajetórias da média acumulada de lucro por rodada (X̄_n) ao longo de 10.000 rodadas para as sementes "
                "10, 2026 e 123456, confrontadas com a referência horizontal da esperança matemática E[X] = −0,16 crédito."
            ),
            fonte="Elaboração própria com dados do Experimento 2.",
            est=est,
        )
    )

    story.append(
        Paragraph(
            "<b>Auditoria de reprodutibilidade e interpretação pela Lei dos Grandes Números (LGN).</b> A repetição da "
            "semente 2026 no mesmo ambiente reproduziu <b>100% dos dez primeiros resultados</b> de forma idêntica "
            "(Rodada 1: paradas (0,2,4), linha B–D–A, <i>X</i> = −1; Rodada 2: (4,0,1), A–B–C, <i>X</i> = −1; Rodada 3: "
            "(4,4,4), tripla premiada A–A–A, <i>P</i> = 5, <i>X</i> = +4; Rodadas 4 a 10: (3,4,4) E–A–A, (3,4,3) E–A–E, "
            "(1,0,4) C–B–A, (0,0,2) B–B–D, (0,3,0) B–E–B, (3,2,1) E–D–C e (3,2,2) E–D–D, todas com <i>X</i> = −1; "
            "arquivo <code>e2_reproducao_10_primeiros_2026.csv</code>). A Tabela 3 e a Figura 3 demonstram o mecanismo "
            "da simulação de Monte Carlo e da LGN: em amostras pequenas (<i>n</i> = 100), o erro-padrão da média é alto "
            "(σ/√100 ≈ 0,5205 crédito), permitindo que tanto a semente 2026 quanto a 123456 apresentem <b>lucro médio "
            "positivo de +0,2000 crédito/rodada</b> (total de +20 créditos em 100 giros), enquanto a semente 10 registra "
            "forte prejuízo (−0,7000). Quando a amostra cresce para 1.000 (EP ≈ 0,1646) e 10.000 rodadas (EP ≈ 0,0521), "
            "o funil de dispersão estreita-se à razão de 1/√<i>n</i> e todas as três trajetórias convergem para a "
            "vizinhança negativa de E[<i>X</i>] = −0,16 (−0,0960, −0,1315 e −0,2215). Nota-se que a LGN garante "
            "convergência em probabilidade no limite assintótico, mas <b>não impõe aproximação monotônica</b> (na semente "
            "123456, a média estava em −0,0700 em <i>n</i> = 1.000, mais próxima de −0,16 do que em <i>n</i> = 10.000, "
            "onde ficou em −0,2215) nem fixa um erro máximo determinístico em 10.000 rodadas. Acima de tudo, uma sequência "
            "inicial favorável (+0,2000 nos primeiros 100 giros) <b>não altera a distribuição das próximas rodadas</b>, "
            "pois os sorteios futuros permanecem independentes com E[<i>X</i>] = −0,16; o efeito do início favorável é "
            "simplesmente diluído na divisão por <i>n</i> à medida que <i>n</i> cresce.",
            est["Corpo"],
        )
    )

    # --- EXPERIMENTO 3 ---
    story.append(Paragraph("3.3 Experimento 3 – O que acontece com um saldo limitado?", est["SecaoH2"]))
    story.append(
        Paragraph(
            "<b>Procedimento.</b> Inicializou-se o gerador uma única vez com a <b>semente 42</b>, mantendo a sequência "
            "contínua entre <b>100 participantes virtuais</b>. Cada participante iniciou com saldo <i>B</i><sub>0</sub> = "
            "100 créditos e aposta unitária (<i>B<sub>t+1</sub> = B<sub>t</sub> + X<sub>t+1</sub></i>), encerrando sua "
            "sessão ao completar 500 rodadas ou assim que o saldo ficasse abaixo de 1 crédito (<i>B<sub>t</sub></i> = 0, "
            "esgotamento/ruína, sem empréstimo ou reposição).",
            est["Corpo"],
        )
    )

    dados_tab_e3 = [
        [
            Paragraph("<b>Categoria / Indicador da Sessão</b>", est["CelulaCabecalho"]),
            Paragraph("<b>Contagem / Valor</b>", est["CelulaCabecalho"]),
            Paragraph("<b>Proporção / Unidade</b>", est["CelulaCabecalho"]),
            Paragraph("<b>Significado Empírico no Modelo (B₀ = 100, máx. 500 rodadas)</b>", est["CelulaCabecalho"]),
        ],
        [
            "Ganho líquido ao final (Bf > 100)",
            "23 participantes",
            "23,00%",
            "Terminaram as 500 rodadas com lucro (máximo observado: Bf = 390 créditos).",
        ],
        [
            "Empate exato ao final (Bf = 100)",
            "2 participantes",
            "2,00%",
            "Terminaram as 500 rodadas exatamente com os 100 créditos iniciais.",
        ],
        [
            "Perda líquida ao final (Bf < 100)",
            "75 participantes",
            "75,00%",
            "Terminaram abaixo do saldo inicial (soma das 3 categorias = 100,00%).",
        ],
        [
            "→ Subconjunto: Esgotamento (Bf = 0)",
            "67 participantes",
            "67,00% do total",
            "Faliram antes ou na 500ª rodada (representam 89,33% dentre os 75 que perderam).",
        ],
        [
            "Média vs. Mediana do saldo final Bf",
            "52,10 vs. 0,00",
            "créditos (DP = 93,51)",
            "Assimetria positiva extrema: mais da metade faliu (mediana 0), mas a cauda direita puxa a média.",
        ],
        [
            "Duração das sessões (rodadas jogadas)",
            "Média: 339,90",
            "Mediana: 340,0 rod.",
            "O esgotamento precoce abrevia a sessão (mínimo: 105 rodadas; máximo: 500 rodadas).",
        ],
    ]
    t_e3 = Table(
        converter_linhas_tabela(dados_tab_e3, ["LEFT", "RIGHT", "RIGHT", "LEFT"], est),
        colWidths=[4.2 * cm, 2.5 * cm, 2.8 * cm, 7.9 * cm],
    )
    t_e3.setStyle(estilo_tabela_academica())
    story.append(Paragraph("<b>Tabela 4.</b> Resumo estatístico das 100 sessões com saldo limitado no Experimento 3 (semente 42).", est["LegendaTitulo"]))
    story.append(t_e3)
    story.append(Paragraph("<b>Fonte:</b> Resultados da simulação computacional (arquivos <code>e3_resumo_saldos.csv</code> e <code>e3_sessoes_100_participantes.csv</code>).", est["LegendaFonte"]))

    story.append(
        bloco_figura(
            os.path.join(dir_graficos, "fig04_e3_saldo_limitado.png"),
            largura_cm=16.5,
            altura_cm=5.8,
            numero=4,
            legenda=(
                "Trajetórias completas do saldo B_t dos cinco primeiros participantes virtuais sem seleção por desfecho "
                "(à esquerda, mantendo saldo 0 constante após o esgotamento) e histograma dos saldos finais dos 100 participantes destacando média e mediana (à direita)."
            ),
            fonte="Elaboração própria com dados do Experimento 3 (semente 42).",
            est=est,
        )
    )

    story.append(
        Paragraph(
            "<b>Interpretação.</b> Apesar de a esperança por rodada ser negativa (−0,16), <b>23% dos participantes "
            "terminaram com ganho</b> (como o Participante 1, com <i>B<sub>f</sub></i> = 105, e o Participante 4, com "
            "<i>B<sub>f</sub></i> = 240 na Figura 4). Isso ocorre porque, em um horizonte finito de até 500 rodadas, "
            "o desvio-padrão acumulado é muito elevado (para 500 rodadas, σ<sub>500</sub> = √500 × 5,2052 ≈ 116,39 "
            "créditos), superando a perda esperada de 80 créditos; assim, jogadores que sorteiam duas ou três triplas "
            "E–E–E (+49 créditos cada) encerram a sessão no lucro. Contudo, a comparação entre a <b>média (52,10 "
            "créditos)</b> e a <b>mediana (0,00 crédito)</b> revela a grave distorção produzida por um relato isolado "
            "de sucesso: o resultado típico (mediano) do grupo é a <b>perda total dos 100 créditos (67% de esgotamento)</b>, "
            "como ocorreu com o Participante 2 (esgotado na rodada 240) e o Participante 5 (esgotado na rodada 205). "
            "A média (52,10) fica artificialmente distante de zero apenas porque a barreira absorvente em <i>B<sub>t</sub></i> = 0 "
            "trunca as perdas em −100 créditos, enquanto os ganhos raros não têm teto superior (chegando a 390 créditos). "
            "Pelo mesmo motivo matemático (parada aleatória na barreira zero), a duração média das sessões foi de "
            "<b><i>τ̄</i> = 339,90 rodadas</b> (e não 500); logo, como adverte o enunciado, <b>não se deve tomar "
            "100 − 500(0,16) = 20 créditos como referência automática</b> para a média final. Pela Identidade de Wald "
            "para tempos de parada (E[<i>B<sub>τ</sub> − B</i><sub>0</sub>] = E[τ] · E[<i>X</i>]), a perda esperada "
            "correspondente à exposição média de 339,90 rodadas é 339,90 × (−0,16) = −54,38 créditos, projetando saldo "
            "médio de 100 − 54,38 = <b>45,62 créditos</b> (muito próximo dos 52,10 observados). Ressalta-se, por fim, "
            "que a taxa de 67% de esgotamento descreve exclusivamente as propriedades matemáticas deste modelo sob "
            "<i>B</i><sub>0</sub> = 100 e horizonte de 500 giros, não constituindo estimativa da insolvência de famílias brasileiras.",
            est["Corpo"],
        )
    )

    # --- EXPERIMENTO 4 ---
    story.append(Paragraph("3.4 Experimento 4 – Depois de perder, aumenta a chance de ganhar?", est["SecaoH2"]))
    story.append(
        Paragraph(
            "<b>Procedimento.</b> Reutilizaram-se as 10.000 rodadas do Experimento 1 (semente 2026) e inspecionaram-se "
            "todos os <b>9.999 pares consecutivos</b> (<i>i</i>, <i>i</i>+1) para <i>i</i> = 1, …, 9.999. Os pares foram "
            "particionados segundo o evento da primeira rodada: grupo <i>G<sub>i</sub></i> = {<i>P<sub>i</sub></i> &gt; 0} "
            "(rodada anterior premiada) e grupo complementar <i>G<sub>i</sub><sup>c</sup></i> = {<i>P<sub>i</sub></i> = 0} "
            "(rodada anterior sem prêmio). Calculou-se, em cada subgrupo, a frequência relativa condicional de prêmio "
            "na rodada seguinte <i>G<sub>i+1</sub></i> (Tabela 5 e Figura 5).",
            est["Corpo"],
        )
    )

    dados_tab_e4 = [
        [
            Paragraph("<b>Resultado da Rodada Anterior (i)</b>", est["CelulaCabecalho"]),
            Paragraph("<b>Total de Pares (Denominador)</b>", est["CelulaCabecalho"]),
            Paragraph("<b>Prêmios na Rodada Seguinte (i+1)</b>", est["CelulaCabecalho"]),
            Paragraph("<b>Proporção Condicional Observada</b>", est["CelulaCabecalho"]),
            Paragraph("<b>Referência Teórica de Independência</b>", est["CelulaCabecalho"]),
        ],
        ["Com prêmio (G_i: P_i > 0)", "412", "17", "17 / 412 = 4,1262%", "Pr(G_{i+1} | G_i) = 4,0000%"],
        ["Sem prêmio (G_i^c: P_i = 0)", "9.587", "395", "395 / 9.587 = 4,1202%", "Pr(G_{i+1} | G_i^c) = 4,0000%"],
        ["<b>Total de pares consecutivos</b>", "<b>9.999</b>", "<b>412</b>", "<b>412 / 9.999 = 4,1204%</b>", "<b>Pr(G_{i+1}) = 4,0000%</b>"],
    ]
    t_e4 = Table(
        converter_linhas_tabela(dados_tab_e4, ["LEFT", "RIGHT", "RIGHT", "RIGHT", "RIGHT"], est),
        colWidths=[4.2 * cm, 3.0 * cm, 3.2 * cm, 3.5 * cm, 3.5 * cm],
    )
    t_e4.setStyle(estilo_tabela_academica())
    story.append(Paragraph("<b>Tabela 5.</b> Frequências condicionais de prêmio na rodada seguinte nos 9.999 pares consecutivos (Experimento 4).", est["LegendaTitulo"]))
    story.append(t_e4)
    story.append(Paragraph("<b>Fonte:</b> Resultados da simulação computacional (arquivo <code>resultados/e4_probabilidade_condicional.csv</code>).", est["LegendaFonte"]))

    story.append(
        bloco_figura(
            os.path.join(dir_graficos, "fig05_e4_condicional.png"),
            largura_cm=13.0,
            altura_cm=5.7,
            numero=5,
            legenda=(
                "Proporção observada de prêmio na rodada i+1 condicionada ao resultado da rodada anterior i (barras "
                "com intervalos de variação amostral de 95%), comparada à referência teórica de independência de 4,00%."
            ),
            fonte="Elaboração própria com dados do Experimento 4 (semente 2026).",
            est=est,
        )
    )

    story.append(
        Paragraph(
            "<b>Interpretação e refutação da falácia do jogador.</b> A soma dos denominadores é exatamente 412 + 9.587 = "
            "<b>9.999 pares</b> (pois a 1ª rodada do Experimento 1 não foi premiada, logo todos os 412 prêmios do E1 "
            "aparecem como segunda rodada de algum par, e como a 10.000ª rodada também não teve prêmio, todos os 412 "
            "prêmios iniciam um par). As proporções observadas após prêmio (<b>4,1262%</b>) e após perda (<b>4,1202%</b>) "
            "diferem em apenas 0,006 ponto percentual e estão ambas aderentes à referência teórica de independência "
            "Pr(<i>G<sub>i+1</sub></i> | <i>G<sub>i</sub></i>) = Pr(<i>G<sub>i+1</sub></i> | <i>G<sub>i</sub><sup>c</sup></i>) "
            "= Pr(<i>G<sub>i+1</sub></i>) = <b>4,00%</b>. Como indicado pelas barras de erro na Figura 5, o grupo “após "
            "prêmio” possui denominador cerca de 23 vezes menor (<i>n</i> = 412) do que o grupo “após perda” (<i>n</i> = 9.587), "
            "o que faz seu erro-padrão amostral ser muito maior (√(0,04 × 0,96 / 412) ≈ 0,97 p.p. contra 0,20 p.p. após perda). "
            "Consequentemente, qualquer diferença amostral entre as duas taxas reflete apenas variabilidade de amostragem, "
            "e não alteração das regras do algoritmo. Fica empiricamente refutada a <b>falácia do jogador</b> (<i>gambler's "
            "fallacy</i>): como os sorteios são independentes, a máquina não possui memória nem “acumula dívida” após uma "
            "sequência de derrotas; dobrar apostas ou insistir esperando compensação imediata apenas acelera a ruína financeira.",
            est["Corpo"],
        )
    )

    # --- EXPERIMENTO 5 ---
    story.append(Paragraph("3.5 Experimento 5 – Prêmios maiores tornam o jogo favorável?", est["SecaoH2"]))
    story.append(
        Paragraph(
            "<b>Procedimento.</b> Aplicaram-se duas tabelas de pagamentos aos <b>mesmos 10.000 sorteios</b> do Experimento 1 "
            "(semente 2026), mantendo inalterados os símbolos sorteados, suas probabilidades e a aposta de 1 crédito: "
            "a <b>Tabela Base</b> (5, 10, 15, 25, 50) e a <b>Tabela Prêmios +10%</b> (5,5; 11; 16,5; 27,5; 55 créditos).",
            est["Corpo"],
        )
    )

    dados_tab_e5 = [
        [
            Paragraph("<b>Configuração</b>", est["CelulaCabecalho"]),
            Paragraph("<b>Prob. / Freq. Prêmio</b>", est["CelulaCabecalho"]),
            Paragraph("<b>E[P] Teórico (cr.)</b>", est["CelulaCabecalho"]),
            Paragraph("<b>P̄ Observado (cr.)</b>", est["CelulaCabecalho"]),
            Paragraph("<b>E[X] Teórico (cr.)</b>", est["CelulaCabecalho"]),
            Paragraph("<b>X̄ Observado (cr.)</b>", est["CelulaCabecalho"]),
            Paragraph("<b>RTP Teórico</b>", est["CelulaCabecalho"]),
            Paragraph("<b>RTP̂ Observado</b>", est["CelulaCabecalho"]),
        ],
        ["Tabela Base", "4,00% / 4,12%", "0,8400", "0,8685", "−0,1600", "−0,1315", "84,00%", "86,85%"],
        ["Prêmios +10%", "4,00% / 4,12%", "0,9240", "0,9554", "−0,0760", "−0,0447", "92,40%", "95,54%"],
        ["<b>Variação (+10%)</b>", "<b>0,00 p.p.</b>", "<b>+0,0840</b>", "<b>+0,0869</b>", "<b>+0,0840</b>", "<b>+0,0869</b>", "<b>+8,40 p.p.</b>", "<b>+8,69 p.p.</b>"],
    ]
    t_e5 = Table(
        converter_linhas_tabela(dados_tab_e5, ["LEFT", "RIGHT", "RIGHT", "RIGHT", "RIGHT", "RIGHT", "RIGHT", "RIGHT"], est),
        colWidths=[2.7 * cm, 2.4 * cm, 2.1 * cm, 2.1 * cm, 2.1 * cm, 2.1 * cm, 1.9 * cm, 2.0 * cm],
    )
    t_e5.setStyle(estilo_tabela_academica())
    story.append(Paragraph("<b>Tabela 6.</b> Comparação analítica e empírica sob as mesmas condições (N = 10.000, semente 2026) no Experimento 5.", est["LegendaTitulo"]))
    story.append(t_e5)
    story.append(Paragraph("<b>Fonte:</b> Resultados da simulação computacional (arquivo <code>resultados/e5_comparacao_tabelas.csv</code>).", est["LegendaFonte"]))

    story.append(
        bloco_figura(
            os.path.join(dir_graficos, "fig06_e5_comparacao_tabelas.png"),
            largura_cm=16.2,
            altura_cm=5.6,
            numero=6,
            legenda=(
                "Comparação entre a Tabela Base e a Tabela Prêmios +10% aplicadas aos mesmos 10.000 sorteios do "
                "Experimento 1: indicadores percentuais de chance de prêmio e RTP (à esquerda) e lucro médio por rodada (à direita)."
            ),
            fonte="Elaboração própria com dados do Experimento 5 (semente 2026).",
            est=est,
        )
    )

    story.append(
        Paragraph(
            "<b>Interpretação.</b> Pela propriedade de homogeneidade da esperança matemática, multiplicar todos os "
            "pagamentos brutos por <i>c</i> = 1,10 implica E[<i>P</i><sub>+10%</sub>] = E[1,10<i>P</i>] = 1,10 · E[<i>P</i>] "
            "= 1,10 × 0,84 = <b>0,924 crédito</b>, elevando o RTP teórico exatamente para <b>92,40%</b> (e o observado de "
            "86,85% para 95,535%). O lucro líquido esperado passa a ser E[<i>X</i><sub>+10%</sub>] = 0,924 − 1 = "
            "<b>−0,076 crédito/rodada</b> (e o observado passa de −0,1315 para −0,04465 crédito). Este experimento "
            "demonstra que <b>pagar mais</b> (elevar os valores de <i>P</i> em +10%), <b>pagar com maior frequência</b> "
            "(elevar Pr(<i>P</i> &gt; 0), que permaneceu rigorosamente inalterada em 4,00% teórica e 4,12% observada) "
            "e <b>produzir lucro esperado positivo</b> (E[<i>X</i>] &gt; 0) são três afirmações matematicamente distintas. "
            "Como demonstrado na Análise de Sensibilidade (Anexo Extra 8), sob rolos equiprováveis de 5 símbolos, o jogo "
            "só deixaria de ser desfavorável ao jogador se a soma dos cinco prêmios superasse 125 créditos (aumento "
            "superior a +19,05% sobre a Tabela Base, onde ∑<i>P</i> = 105).",
            est["Corpo"],
        )
    )

    # ==========================================================================
    # SEÇÃO 4: DA EVIDÊNCIA À DISCUSSÃO CRÍTICA (4 EIXOS DA SEÇÃO 8)
    # ==========================================================================
    story.append(Paragraph("4. Da evidência à discussão crítica: matemática, saúde e políticas públicas", est["SecaoH1"]))
    story.append(
        Paragraph(
            "Conectamos agora os três níveis exigidos pela investigação — <b>o que foi calculado no modelo</b>, "
            "<b>o que foi observado nos experimentos</b> e <b>o que as fontes documentais permitem afirmar sobre a "
            "sociedade brasileira</b> — estruturados nos quatro eixos analíticos propostos na Seção 8.",
            est["Corpo"],
        )
    )

    story.append(Paragraph("4.1 Mecanismo probabilístico e percepção cognitiva do apostador", est["SecaoH2"]))
    story.append(
        Paragraph(
            "A coexistência entre vitórias visíveis e perda esperada explica-se pela combinação de uma <b>esperança "
            "negativa moderada por rodada (E[<i>X</i>] = −0,16 crédito; RTP = 84%)</b> com um <b>desvio-padrão "
            "individual mais de trinta vezes maior (σ<sub>X</sub> = 5,2052 créditos)</b>. Nos resultados experimentais, "
            "essa assimetria manifestou-se em dois fenômenos complementares: (1) no <b>Experimento 2</b>, duas das três "
            "sementes testadas (2026 e 123456) exibiram lucro médio positivo (+0,2000 crédito/giro) após 100 rodadas "
            "antes de convergirem para perdas acumuladas (−0,1315 e −0,2215) em 10.000 rodadas; e (2) no <b>Experimento 3</b>, "
            "mesmo após até 500 rodadas, <b>23% dos participantes saíram com saldo final positivo</b> (chegando a "
            "390 créditos), ao passo que <b>67% sofreram esgotamento total (saldo zero) e a mediana do grupo foi 0,00 crédito</b>. "
            "No ambiente digital, opera um severo <b>viés de seleção e visibilidade</b>: os 23% de ganhadores ocasionais "
            "(ou influenciadores em sessões curtas/demonstrativas [18, 20]) divulgam capturas de tela de prêmios altos "
            "(como a tripla E–E–E de 50 créditos), enquanto o desfecho mediano (falência da banca de 67% dos usuários) "
            "permanece silencioso. Adicionalmente, como demonstraram Newall e colaboradores [5] em experimentos "
            "controlados com apostadores britânicos, a forma de comunicar essa matemática altera substancialmente a "
            "percepção de risco: informar que um jogo possui “RTP de 84%” (ou 92,4% no Experimento 5) é frequentemente "
            "mal interpretado pelo público como alta chance de ganhar, enquanto a formulação algebricamente equivalente "
            "“esta máquina retém, em média, 16% de todo o valor apostado a cada giro” comunica a desvantagem econômica "
            "com muito maior clareza — embora avisos isolados, por si sós, não eliminem os danos do produto [5].",
            est["Corpo"],
        )
    )

    story.append(Paragraph("4.2 Renda familiar, saúde pública e limites da inferência", est["SecaoH2"]))
    story.append(
        Paragraph(
            "Por que perdas que parecem pequenas por rodada (−0,16 crédito) comprometem recursos familiares essenciais na "
            "vida real? A resposta reside na velocidade e na disponibilidade contínua do produto digital [1, 2]: como "
            "uma rodada em celular dura poucos segundos, centenas de rodadas são executadas em uma única sessão "
            "(multiplicando a esperança negativa por <i>n</i>) e a falácia do jogador (refutada no <b>Experimento 4</b>, "
            "onde a chance de prêmio após derrota permaneceu em 4,12%) induz o usuário a realizar novos depósitos via Pix "
            "para tentar “recuperar” o saldo esgotado. Aqui é crucial demarcar a fronteira metodológica: <b>uma rodada "
            "perdida ou uma banca virtual zerada na simulação não é um diagnóstico clínico nem mede o orçamento das "
            "famílias</b>. O conhecimento sobre danos reais provém de estudos empíricos com populações humanas. "
            "Nos Estados Unidos, Baker et al. [4] analisaram registros de transações financeiras familiares após a "
            "legalização de apostas esportivas e documentaram redução líquida da poupança, realocação de gastos básicos e "
            "aumento do endividamento em cartão de crédito, sobretudo em famílias de menor renda — estudo que formula "
            "hipóteses relevantes sobre orçamento doméstico, mas cuja modalidade (apostas esportivas norte-americanas) "
            "não pode ser mecanicamente transposta para os cassinos virtuais no Brasil sem considerar diferenças de "
            "renda e crédito.",
            est["Corpo"],
        )
    )
    story.append(
        Paragraph(
            "No campo epidemiológico, a Organização Mundial da Saúde [1] classifica máquinas eletrônicas e jogos de "
            "cassino on-line entre os produtos de maior potencial aditivo, relacionando-os a sofrimento mental, conflitos "
            "familiares e danos a terceiros mesmo na ausência de transtorno diagnosticado. A Comissão da <i>The Lancet "
            "Public Health</i> [2] estimou que <b>15,8% (IC 95%: 10,7% a 21,6%) dos adultos que utilizaram cassinos ou "
            "rolos on-line</b> apresentam jogo problemático ou transtorno do jogo. A leitura estatística rigorosa exige "
            "atenção ao <b>denominador</b>: 15,8% refere-se à subpopulação exposta à modalidade (usuários de cassino/slots "
            "em estudos internacionais reunidos pela meta-análise), e não a 15,8% de toda a população adulta brasileira. "
            "Para o contexto nacional, o <b>Caderno Temático LENAD III (UNIFESP/UNIAD, 2025)</b> [3] realizou amostragem "
            "probabilística domiciliar da população de 14 anos ou mais e aplicou o módulo específico de apostas a uma "
            "subamostra de <b>4.914 participantes</b>, utilizando a escala validada <b>PGSI (<i>Problem Gambling Severity "
            "Index</i>)</b>. Do ponto de vista estatístico, o PGSI é um instrumento psicométrico de <b>rastreamento "
            "populacional</b> (<i>screening</i> de gravidade de risco), que não substitui avaliação e diagnóstico "
            "psiquiátrico individual.",
            est["Corpo"],
        )
    )

    story.append(Paragraph("4.3 Políticas públicas, interesses em disputa e avaliação da força das evidências", est["SecaoH2"]))
    story.append(
        Paragraph(
            "O debate brasileiro em setembro de 2026 polarizou-se em torno da edição da <b>MP nº 1.394/2026</b> [7]. "
            "De um lado, o <b>argumento favorável à restrição severa e à proibição da oferta/publicidade</b> — sustentado "
            "pelo Ministério da Saúde [8], pela Advocacia-Geral da União na ação contra 17 plataformas [9], por "
            "pesquisadores de saúde coletiva no dossiê do IEPS [13], por psiquiatras [18] e por especialistas em audiência "
            "na TV Senado [19] — apoia-se no princípio da proteção da saúde pública e de grupos financeiramente vulneráveis. "
            "A evidência que sustenta a existência de dano sanitário e drenagem de liquidez das famílias é <b>forte e "
            "convergente</b>: combina dados administrativos observados do Banco Central (R$ 18–21 bilhões/mês em fluxos "
            "Pix [11]) e do TCU (R$ 17,4 bilhões de receita bruta retida pelas operadoras em apenas um semestre [12]) com "
            "evidência epidemiológica internacional robusta (OMS [1]; <i>Lancet Commission</i> [2]) e levantamento "
            "probabilístico nacional (LENAD III [3]). Por outro lado, a avaliação científica exige escrutínio crítico "
            "inclusive sobre as estimativas usadas a favor da restrição: os <b>R$ 38,8 bilhões anuais em custos sociais</b> "
            "calculados pelo IEPS [13] (dos quais R$ 30,6 bilhões em saúde) constituem uma <b>estimativa modelada</b> "
            "(e não despesa contábil executada pelo SUS), construída pela aplicação de parâmetros da revisão britânica do "
            "OHID/PHE [14] convertidos por paridade de poder de compra, sujeita — como os próprios autores declaram nas "
            "páginas 33–35 do dossiê [13] — a lacunas de mensuração e ao uso de associações observacionais que não provam, "
            "isoladamente, causalidade direta em todos os desfechos.",
            est["Corpo"],
        )
    )
    story.append(
        Paragraph(
            "De outro lado, o <b>argumento crítico à proibição total</b> reúne dois tipos de fontes com pesos "
            "probatórios muito diferentes. As alegações das associações empresariais <b>ANJL e IBJR</b> perante o STF [10] "
            "— invocando liberdade econômica, segurança jurídica dos investimentos feitos sob a Lei 14.790/2023 [6] e "
            "suposta ausência de urgência — representam <b>defesa legítima de interesses econômicos setoriais</b>, mas "
            "possuem baixa força científica quando minimizam a urgência sanitária amplamente documentada. Todavia, há um "
            "argumento técnico sobre <b>capacidade de implementação e fiscalização</b> que possui <b>alta força "
            "evidencial</b> porque provém de auditoria independente do <b>Tribunal de Contas da União (Acórdão "
            "1296/2026)</b> [12]: o TCU comprovou que o Estado brasileiro já enfrentava severas limitações tecnológicas "
            "e de coordenação entre Fazenda, Anatel e Banco Central para impedir o funcionamento de milhares de sites "
            "clandestinos hospedados no exterior. Portanto, uma análise madura conclui que o simples decreto de proibição "
            "legal (MP 1.394/2026), se não for acompanhado de bloqueio efetivo de meios de pagamento (Pix para "
            "intermediadoras não autorizadas), restrição de publicidade digital e rede de acolhimento psicossocial no SUS, "
            "corre o risco real de deslocar apostadores dependentes para o mercado clandestino totalmente desregulado — "
            "problema prático de implementação que deve integrar o desenho da política pública sem jamais servir de "
            "pretexto para negar os graves danos sociais das apostas.",
            est["Corpo"],
        )
    )

    story.append(Paragraph("4.4 Responsabilidade profissional em Sistemas de Informação e conclusão educativa", est["SecaoH2"]))
    story.append(
        Paragraph(
            "Para bacharéis em Sistemas de Informação, a Máquina Estatística demonstra que decisões de arquitetura de "
            "software, interface de usuário (UI/UX) e comunicação de dados nunca são eticamente neutras. Sistemas "
            "comerciais frequentemente empregam padrões de design manipulativos (<i>dark patterns</i>): exibição de "
            "“quase-vitórias” nas linhas superior e inferior (explorando a dependência vertical da coluna que modelamos "
            "na Seção 2 para criar a falsa impressão de que o prêmio “passou perto”), celebrações audiovisuais em prêmios "
            "menores que a aposta, ocultação do saldo líquido acumulado da sessão e destaque exclusivo para o RTP "
            "percentual sem explicitar a perda esperada por giro [5, 17]. A responsabilidade técnica e ética do "
            "profissional de computação exige transparência algorítmica, interfaces acessíveis que informem claramente a "
            "vantagem da casa e o histórico líquido de perdas, travas efetivas de limite de exposição (como demonstramos "
            "no Anexo Extra 3) e recusa em implementar mecanismos de indução comportamental ao endividamento.",
            est["Corpo"],
        )
    )
    story.append(
        Paragraph(
            "<b>Conclusão educativa síntese:</b> <i>Em jogos de rolos com esperança matemática negativa (E[X] = −0,16 "
            "crédito; RTP = 84%), a ocorrência de prêmios ocasionais e de ganhadores de curto prazo (23% das sessões no "
            "Experimento 3) é uma consequência natural da alta variância por rodada (σ<sub>X</sub> = 5,21 créditos), mas "
            "a repetição das rodadas faz o resultado médio convergir inexoravelmente para a perda esperada (Lei dos "
            "Grandes Números), levando a maioria dos participantes com saldo finito ao esgotamento (67% no Experimento 3, "
            "com saldo mediano zero), sem que derrotas passadas aumentem a chance de ganho futuro (independência de 4,00% "
            "no Experimento 4). Compreender essa matemática protege o cidadão contra falsas promessas de renda fácil e "
            "evidencia que o sofrimento financeiro e mental associado às apostas digitais não decorre de “falta de sorte” "
            "ou falha moral individual, mas da exposição massiva a um produto matematicamente desenhado para transferir "
            "renda do apostador para o operador, exigindo regulação rigorosa, fiscalização financeira efetiva e políticas "
            "públicas de saúde e educação científica.</i>",
            est["CaixaDestaque"],
        )
    )

    story.append(PageBreak())

    # ==========================================================================
    # SEÇÃO 5: REFERÊNCIAS BIBLIOGRÁFICAS E TRANSPARÊNCIA (FORA DA CONTAGEM DE 6-10 PÁG.)
    # ==========================================================================
    story.append(Paragraph("5. Referências bibliográficas e classificação de gênero documental", est["SecaoH1"]))
    referencias = [
        "[1] WORLD HEALTH ORGANIZATION (OMS). <i>Gambling: Fact Sheet</i>. Genebra: WHO, 2 dez. 2024. <b>[Gênero: Síntese institucional internacional de saúde pública]</b>.",
        "[2] WARDLE, H. et al. The Lancet Public Health Commission on gambling. <i>The Lancet Public Health</i>, v. 9, p. e950–e994, 2024. DOI: 10.1016/S2468-2667(24)00167-1. <b>[Gênero: Artigo científico / Comissão de revisão sistemática e meta-análise]</b>.",
        "[3] UNIVERSIDADE FEDERAL DE SÃO PAULO (UNIFESP); UNIAD. <i>Caderno Temático LENAD III: jogos de aposta na população brasileira – Resultados 2023</i>. São Paulo: UNIFESP, 2025. <b>[Gênero: Levantamento epidemiológico nacional com amostragem probabilística, n = 4.914 no módulo PGSI]</b>.",
        "[4] BAKER, S. R.; BALTHROP, J.; JOHNSON, M. J.; KOTTER, J. D.; PISCIOTTA, K. <i>Gambling Away Stability: Sports Betting's Impact on Vulnerable Households</i>. NBER Working Paper 33108, nov. 2024. DOI: 10.3386/w33108. <b>[Gênero: Pesquisa acadêmica empírica em economia financeira]</b>.",
        "[5] NEWALL, P. W. S.; WALASEK, L.; LUDVIG, E. A. Equivalent gambling warning labels are perceived differently. <i>Addiction</i>, v. 115, n. 9, p. 1762–1767, 2020. DOI: 10.1111/add.14954. <b>[Gênero: Artigo científico experimental sobre cognição e comunicação de risco]</b>.",
        "[6] BRASIL. <i>Lei nº 14.790, de 29 de dezembro de 2023</i>. Dispõe sobre a modalidade lotérica denominada apostas de quota fixa. Diário Oficial da União, Brasília, DF, 2023. <b>[Gênero: Norma legal publicada]</b>.",
        "[7] BRASIL. Congresso Nacional. <i>Medida Provisória nº 1.394, de 25 de setembro de 2026</i>. Estabelece a proibição da exploração, oferta, intermediação e publicidade de apostas de quota fixa e jogos on-line. Brasília, DF, 25 set. 2026. <b>[Gênero: Norma jurídica publicada com força de lei]</b>.",
        "[8] BRASIL. Ministério da Saúde. <i>Presidente Lula assina Medida Provisória que proíbe as bets no Brasil</i>. Brasília, DF, 25 set. 2026. <b>[Gênero: Comunicação institucional oficial do Poder Executivo]</b>.",
        "[9] RICHTER, A. Governo cobra na Justiça gastos do SUS com tratamento de apostadores. <i>Agência Brasil</i>, Brasília, 28 set. 2026. <b>[Gênero: Notícia jornalística sobre ação judicial e pedidos da União]</b>.",
        "[10] PONTES, F. Associações de jogos acionam STF contra MP que proibiu apostas online. <i>Agência Brasil</i>, Brasília, 28 set. 2026. <b>[Gênero: Notícia jornalística sobre petição judicial e argumentos das partes ANJL/IBJR]</b>.",
        "[11] BANCO CENTRAL DO BRASIL (BCB). <i>Análise técnica sobre o mercado de apostas online no Brasil e o perfil dos apostadores</i>. Estudo Especial nº 119/2024 e Nota Técnica nº 513/2024. Brasília: BCB, set. 2024. <b>[Gênero: Estudo técnico-institucional de autoridade monetária]</b>.",
        "[12] TRIBUNAL DE CONTAS DA UNIÃO (TCU). <i>Tribunal analisa enfrentamento a casas de apostas ilegais – Acórdão nº 1296/2026 – Plenário</i>. Brasília: TCU, 19 maio 2026. <b>[Gênero: Acórdão de auditoria institucional e controle externo]</b>.",
        "[13] ROSA, D. et al. <i>A saúde dos brasileiros em jogo: análise político-econômica da regulamentação de apostas online e seus impactos para a saúde da população brasileira</i>. São Paulo: IEPS; FPSM; Umane, dez. 2025, 40 p. <b>[Gênero: Dossiê de pesquisa de políticas públicas e economia da saúde]</b>.",
        "[14] OFFICE FOR HEALTH IMPROVEMENT AND DISPARITIES (OHID); PUBLIC HEALTH ENGLAND (PHE). <i>Gambling-related harms: evidence review</i>. Londres: GOV.UK, 2021 (atualizado em 11 jan. 2023). <b>[Gênero: Revisão governamental internacional de evidências e custos sociais]</b>.",
        "[15] ILLOWSKY, B.; DEAN, S. <i>Introductory Statistics</i>. 2. ed. Houston: OpenStax, 2023. Capítulos 1–4 e 8. <b>[Gênero: Livro-texto acadêmico de referência em Probabilidade e Estatística]</b>.",
        "[16] PYTHON SOFTWARE FOUNDATION. <i>random — Generate pseudo-random numbers</i>. Documentação oficial do Python 3.12.7, 2024. <b>[Gênero: Documentação técnica oficial de software]</b>.",
        "[17] GAMBLING COMMISSION. <i>Return to player: how much gaming machines payout</i>. Birmingham: UK Gambling Commission, atualizado em 16 jun. 2021. <b>[Gênero: Guia técnico de órgão regulador]</b>.",
        "[18] RIBAS, N. M. et al. “Jogo do Tigrinho” e os perigos do Jogo patológico. <i>Debates em Psiquiatria</i>, v. 15, e1393, p. 1–5, 17 jan. 2025. DOI: 10.25118/2763-9037.2025.v15.1393. <b>[Gênero: Carta científica ao editor / comentário clínico]</b>.",
        "[19] SENADO FEDERAL. TV Senado. <i>Vício em bets: proibição das apostas online, saúde pública e endividamento das famílias</i>. Brasília, 25 set. 2026. <b>[Gênero: Debate público parlamentar]</b>.",
        "[20] PACETE, L. G. Conheça quem está por trás do Jogo do Tigrinho. <i>Forbes Brasil</i>, 25 jun. 2024. <b>[Gênero: Reportagem jornalística de contexto histórico empresarial]</b>.",
    ]
    for r in referencias:
        story.append(Paragraph(r, est["RefItem"]))

    story.append(Paragraph("6. Ambiente de execução, reprodutibilidade e declaração de transparência (IA)", est["SecaoH1"]))
    story.append(
        Paragraph(
            "<b>Parâmetros técnicos e reprodutibilidade:</b> Todos os experimentos foram executados em <b>Python 3.12.7</b> "
            "(CPython, MSC v.1941 64 bits AMD64, Windows 11 10.0.26200), utilizando exclusivamente a classe "
            "<code>random.Random(semente)</code> da biblioteca padrão (algoritmo Mersenne Twister MT19937) com sorteio "
            "<code>randrange(5)</code>. Sementes utilizadas: <b>2026</b> (Experimentos 1, 4 e 5), <b>10, 2026 e 123456</b> "
            "(Experimento 2), <b>42</b> (Experimento 3 e Extras 2 e 3) e <b>5000 a 5099</b> (Extra 1). Os gráficos foram "
            "exportados via <code>matplotlib 3.11.2</code> e <code>numpy 2.5.4</code>.",
            est["Corpo"],
        )
    )
    story.append(
        Paragraph(
            "<b>Declaração transparente sobre uso de Inteligência Artificial (Seção 4 e Seção 9):</b> Em cumprimento às "
            "normas de autoria e transparência do enunciado, declara-se que ferramentas de IA generativa (assistente de "
            "codificação e revisão) foram utilizadas como apoio na estruturação modular do código Python "
            "(<code>simulador.py</code>, <code>gerar_graficos.py</code> e <code>test_simulador.py</code>), na formatação "
            "tipográfica do documento PDF/LaTeX e da página web acessível, e na revisão gramatical. <b>Todo o "
            "equacionamento algébrico (espaço amostral de 125 triplas, esperanças E[P] = 0,84 e E[X] = −0,16, variância "
            "27,0944 e RTP de 84% e 92,4%), todas as contagens empíricas (soma de 10.000 no E1, 100 sessões no E3 e "
            "9.999 pares no E4), a reprodutibilidade das sementes e a distinção crítica das fontes documentais foram "
            "integralmente conferidos, validados por testes automatizados e subscritos pelos integrantes.</b>",
            est["CaixaDestaque"],
        )
    )

    # ==========================================================================
    # ANEXO: EVIDÊNCIAS DOS ITENS EXTRAS (SEÇÃO 10 - ATÉ 20 PONTOS EXTRAS)
    # ==========================================================================
    story.append(Paragraph("Anexo – Aprofundamentos opcionais (Seção 10: Evidências para os 20 pontos extras)", est["SecaoH1"]))
    story.append(
        Paragraph(
            "Para aprofundar a investigação além dos requisitos básicos, foram implementadas e documentadas no pacote "
            "de entrega todas as oito possibilidades da Seção 10 (totalizando o teto de 20 pontos extras). Abaixo "
            "apresentam-se os métodos, resultados e localização dos artefatos correspondentes.",
            est["Corpo"],
        )
    )

    story.append(
        bloco_figura(
            os.path.join(dir_graficos, "fig07_extras_aprofundamento.png"),
            largura_cm=16.5,
            altura_cm=10.5,
            numero=7,
            legenda=(
                "Painel síntese dos experimentos extras: (superior esquerdo) Intervalos de Confiança de 95% nas primeiras "
                "25 execuções independentes de N=10.000 rodadas; (superior direito) Comparação de dispersão σ_X e taxa de "
                "esgotamento entre três tabelas com mesmo RTP = 84%; (inferior esquerdo) Exposição média em rodadas e perda "
                "mediana sob três regras de parada; (inferior direito) Curva de sensibilidade do RTP em função do multiplicador de prêmios."
            ),
            fonte="Elaboração própria com dados dos módulos extras (arquivos <code>extra1_*.csv</code>, <code>extra2_*.csv</code>, <code>extra3_*.csv</code> e <code>extra8_*.csv</code>).",
            est=est,
        )
    )

    dados_tab_extras = [
        [
            Paragraph("<b>Item Extra (Seção 10)</b>", est["CelulaCabecalho"]),
            Paragraph("<b>Evidência no Pacote</b>", est["CelulaCabecalho"]),
            Paragraph("<b>Método, Hipóteses e Principais Resultados Obtidos</b>", est["CelulaCabecalho"]),
        ],
        [
            "<b>1. Intervalos de confiança</b> (até 4 pts)",
            "<code>extra1_intervalos_confianca_100_execucoes.csv</code>; Figura 7(a)",
            "Pelo Teorema Central do Limite (N = 10.000 rodadas i.i.d. com variância finita), <i>X̄</i> ~ N(μ, σ²/N). "
            "No E1 (semente 2026), EP = s/√10.000 = 0,05275 cr., gerando <b>IC 95% para E[X] = [−0,2349; −0,0281] cr.</b> "
            "(e <b>IC 95% para RTP = [76,51%; 97,19%]</b>), que contém −0,16 e exclui 0 (jogo desfavorável). "
            "Repetindo M = 100 execuções independentes de N = 10.000 (sementes 5000 a 5099), a média das 100 médias "
            "foi −0,1584 cr. (IC 95% meta: [−0,1677; −0,1490]) e <b>97 dos 100 intervalos cobriram o parâmetro "
            "verdadeiro −0,16 (taxa de cobertura empírica de 97,0% ≈ 95%)</b>.",
        ],
        [
            "<b>2. Mesma média, riscos diferentes</b> (até 4 pts)",
            "<code>extra2_mesma_media_riscos_diferentes.csv</code>; Figura 7(b)",
            "Construíram-se duas novas tabelas mantendo ∑P = 105 (logo, <b>mesmo E[P] = 0,84, E[X] = −0,16 e RTP = 84,00%</b>): "
            "(i) <i>Baixa Volatilidade</i> (todas as 5 triplas pagam 21 cr., σ_X = 4,1151 cr.) e (ii) <i>Alta Volatilidade / Jackpot</i> "
            "(pagamentos 2, 3, 5, 10 e 85 cr., σ_X = 7,6288 cr., vs. Base σ_X = 5,2052 cr.). Sob o protocolo do E3 (semente 42), "
            "a tabela de Baixa Volatilidade reduziu o esgotamento para 63% (saldo máximo 356 cr.), enquanto a de Alta Volatilidade "
            "elevou o esgotamento para 67%, o desvio-padrão do saldo final para 136,29 cr. e o ganho máximo para 599 cr.",
        ],
        [
            "<b>3. Limites de exposição</b> (até 3 pts)",
            "<code>extra3_limites_exposicao.csv</code>; Figura 7(c)",
            "Compararam-se 3 regras pré-definidas (semente 42, 100 participantes): <b>Regra A</b> (padrão E3, até 500 rod. ou B=0: "
            "exposição média <i>τ̄</i> = 339,9 rod., mediana Bf = 0, esgotamento = 67%); <b>Regra B</b> (Stop-Loss em B≤70, Stop-Gain em "
            "B≥120, máx. 200 rod.: <i>τ̄</i> = 31,32 rod., mediana Bf = 70 cr., <b>esgotamento total = 0%</b>); e <b>Regra C</b> (Stop-Loss em B≤85, "
            "máx. 50 rod.: <i>τ̄</i> = 28,60 rod., mediana Bf = 85 cr., <b>esgotamento total = 0%</b>). Demonstra-se que limites de parada "
            "não mudam a esperança por rodada (−0,16), mas <b>reduzem drasticamente a exposição E[τ]</b> e eliminam a falência total.",
        ],
        [
            "<b>4. Auditoria de afirmação pública</b> (até 3 pts)",
            "Seção 1 (Tabela 1), Seção 4.3 e <code>auditoria_fontes_publicas.md</code>",
            "Auditoria metodológica detalhada da Nota Técnica 513/2024 do BCB [11], do Acórdão 1296/2026 do TCU [12], "
            "das páginas 33–35 do Dossiê IEPS [13] (conversão PPC sobre revisão britânica OHID/PHE [14]) e da estimativa "
            "de 15,8% da <i>Lancet Commission</i> [2], verificando população, denominador, período e limites causais.",
        ],
        [
            "<b>5. Educação científica</b> (até 3 pts)",
            "<code>educacao_cientifica_acessivel.html</code>",
            "Página interativa de divulgação científica (tempo de leitura de 3 minutos) voltada ao público não especializado, "
            "desmistificando 3 mitos comuns sobre apostas com os resultados próprios dos Experimentos 1 a 5 e fontes verificáveis.",
        ],
        [
            "<b>6. Interface acessível</b> (até 3 pts)",
            "<code>simulador.py --acessivel</code>; <code>educacao_cientifica_acessivel.html</code>",
            "Navegação completa por teclado (atalhos Alt+1, Alt+2, Alt+R, Alt+C), modo de Alto Contraste WCAG AAA, "
            "regiões <code>aria-live</code> para leitores de tela, símbolos com tripla codificação (formas ●▲■◆★ + letras + nomes) "
            "e gráficos em paleta Okabe-Ito com hachuras e linhas tracejadas distintas.",
        ],
        [
            "<b>7. Validação automatizada</b> (até 3 pts)",
            "<code>test_simulador.py</code> (8 testes <code>unittest</code>)",
            "Suite com 8 testes automatizados cobrindo: (1) pagamentos nas 125 triplas; (2) desconto da aposta em tabelas inteiras e "
            "fracionárias; (3) janela circular em K=0..4; (4) reprodutibilidade pela semente; (5) somas exatas de 10.000 no E1, "
            "100 no E3 e 9.999 no E4; (6) caso-limite sem prêmio no E4 sem divisão por zero; (7) caso-limite de saldo zero no E3; "
            "e (8) exatidão algébrica de E[P], E[X], RTP e variância.",
        ],
        [
            "<b>8. Análise de sensibilidade</b> (até 3 pts)",
            "<code>extra8_analise_sensibilidade.csv</code>; Figura 7(d)",
            "Avaliação analítica e empírica de 7 cenários: multiplicadores de 0,80× (RTP 67,2%, E[X]=−0,328), 1,00× (Base, RTP 84,0%), "
            "1,10× (E5, RTP 92,4%), 1,15× (RTP 96,6%), <b>1,190476× (+19,05%, Ponto de Equilíbrio onde ∑P = 125, RTP = 100,0%, E[X] = 0,000)</b>, "
            "1,25× (RTP 105,0%, favorável ao jogador com E[X]=+0,050) e expansão do rolo para 6 símbolos (5/216 = 2,31% de chance de "
            "prêmio, derrubando o RTP da Tabela Base para 48,61% e E[X] para −0,5139 cr.).",
        ],
    ]
    t_ext = Table(
        converter_linhas_tabela(dados_tab_extras, ["LEFT", "LEFT", "LEFT"], est),
        colWidths=[3.5 * cm, 3.5 * cm, 10.4 * cm],
    )
    t_ext.setStyle(estilo_tabela_academica())
    story.append(Paragraph("<b>Tabela 7.</b> Síntese metodológica, localização de evidências e resultados dos 8 aprofundamentos opcionais (Seção 10).", est["LegendaTitulo"]))
    story.append(t_ext)
    story.append(Paragraph("<b>Fonte:</b> Elaboração própria a partir dos experimentos adicionais executados por <code>simulador.py</code>.", est["LegendaFonte"]))

    doc.build(story, onFirstPage=desenhar_cabecalho_rodape, onLaterPages=desenhar_cabecalho_rodape)


if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    pdf_out = os.path.join(base_dir, "relatorio.pdf")
    graf_dir = os.path.join(base_dir, "resultados", "graficos")
    gerar_pdf(pdf_out, graf_dir)
    print(f"[OK] Relatório PDF gerado com sucesso em: {pdf_out}")
