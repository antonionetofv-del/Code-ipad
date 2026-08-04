# Viares Fotografia — peças de captação

Três peças para abrir a campanha descrita em `../../captacao/`. Mesmo padrão do
resto do repositório: o **HTML autocontido** é a fonte da verdade (fontes e fundo
embutidos em base64, importável no Canva) e o **PNG** é o export para publicação.

## Peças

| Arquivo | Formato | Uso |
| --- | --- | --- |
| `viares-lancamento-design-1080x1350.png` | Feed 4:5 | Anuncia a linha de design gráfico. Post-chave da semana 2 do calendário |
| `viares-oferta-mini-ensaio-1080x1350.png` | Feed 4:5 | Oferta de entrada com vagas limitadas |
| `viares-stories-enquete-1080x1920.png` | Stories | Enquete de qualificação. Quem responde "celular" vira lead |

Cada PNG tem um `.html` correspondente com o mesmo nome.

### Como usar o Stories

A faixa entre ~1230px e ~1580px foi deixada **vazia de propósito**: é onde entra a
figurinha de enquete do Instagram, com as opções *"Profissional"* e *"Foto de
celular"*. Depois, responda no direct todo mundo que votar na segunda — é o
script B4 do plano.

## Editar antes de publicar

Os campos variáveis ficam no topo de `src/build_viares.py`:

```python
VAGAS        = '5'
DATA_OFERTA  = 'SÁBADO · 16 DE AGOSTO'
MES_AGENDA   = 'AGENDA · AGOSTO'
HANDLE       = '@viaresfotografia'
```

Ajuste, regenere e reexporte.

## Paleta

| Cor | Hex | Uso |
| --- | --- | --- |
| Areia | `#EFE8DF` → `#DED3C6` | Fundo claro, com textura de papel procedural |
| Preto quente | `#17140F` | Texto principal e fundo escuro |
| Dourado suave | `#A8814F` | Acento, palavra-chave do CTA, filetes |
| Off-white | `#F6F1EA` | Texto sobre fundo escuro |
| Apoio | `#6B6055` | Texto secundário sobre areia |

Tipografia: **Anton** nos títulos, **Poppins** (400/600/700) no resto — as mesmas
já usadas no repositório, ambas SIL Open Font License.

## Regenerar

```bash
pip install pillow numpy playwright
python3 src/build_viares.py   # gera os 3 .html + as texturas de fundo
python3 src/shoot.py          # renderiza os 3 .png na resolução exata
```

`src/shoot.py` procura um Chromium já instalado em `/opt/pw-browsers/`; se não
achar, usa o do próprio Playwright.
