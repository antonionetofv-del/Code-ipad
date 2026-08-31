# Pórtico de entrada — II FENAGRO-MR

Três peças para o pórtico da entrada, no padrão visual do folder.

## Medidas

| Peça | Medida final | Arquivo a 96 dpi |
|---|---|---|
| Testeira (fachada superior) | 3,20 × 0,60 m | 12094 × 2267 px |
| Lateral esquerda | 0,60 × 5,00 m | 2267 × 18896 px |
| Lateral direita | 0,60 × 5,00 m | 2267 × 18896 px |

Margem de segurança de 6 cm em todos os lados; moldura dourada a 2,6 cm da borda.
**Não há sangria** — se a gráfica pedir (envelope, ilhós, acabamento), avise a
medida que eu regero.

## Conteúdo

- **Testeira** — logo, "II FENAGRO-MR", subtítulo, datas, local e os selos da
  XXIII Cavalgada dos Arrojados e da Cia de Rodeio Ninho dos Bons.
- **Lateral esquerda** — marca no topo e as atrações confirmadas dia a dia.
- **Lateral direita** — datas e local, a frase "O agro que movimenta, conecta e
  transforma!", o que o público encontra na feira, @fenagromr e o painel de
  realização, apoio e parceiros das palestras.

## Arquivos gerados (`arquivos/`)

- `<peça>-RGB.png` — referência e aprovação.
- `<peça>-CMYK.tif` — impressão, LZW, separação com GCR (preto no canal K).

A conversão para CMYK é genérica: **não há perfil ICC da gráfica aplicado**. Se
a gráfica informar o perfil (Coated FOGRA39, US Web Coated SWOP etc.), o ideal
é converter a partir do PNG RGB com esse perfil.

## Resolução das marcas

Os recortes de logo usados aqui vieram das artes de divulgação, não dos
arquivos originais. Na escala do pórtico eles ficam entre 13 e 37 dpi, o que
**não serve para impressão**. Apenas COOPAGI e AçaíTech, enviados como arquivo,
estão adequados (≈165 dpi).

Para fechar o arquivo de impressão são necessários, em vetor (PDF/AI/SVG) ou
PNG com pelo menos 2000 px de largura: FENAGRO-MR, SIPRUMAR, XXIII Cavalgada
dos Arrojados, Cia de Rodeio Ninho dos Bons, FAEPA, SEBRAE, Prefeitura de Mãe
do Rio, Governo do Pará e Banpará.

## Como regerar

```bash
python3 build_portico.py                      # monta o HTML
python3 render_portico.py <url-do-html> 96    # gera PNG RGB e TIFF CMYK
```

O conteúdo (shows, destaques, textos) fica nas listas no topo de
`build_portico.py`.
