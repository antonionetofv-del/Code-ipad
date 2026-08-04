# Viares Fotografia — peças de captação

Três peças para abrir a campanha descrita em `../../captacao/`. Mesmo padrão do
resto do repositório: o **HTML autocontido** é a fonte da verdade (fontes e fundo
embutidos em base64, importável no Canva) e o **PNG** é o export para publicação.

## Peças

| Arquivo | Formato | Uso |
| --- | --- | --- |
| `viares-diadospais-stories-1080x1920.png` | **Stories** | **Ensaio de Dia dos Pais — 09/08/2026. Campanha ativa** |
| `viares-oferta-mini-ensaio-stories-1080x1920.png` | Stories | Oferta de entrada — 10 fotos, vagas limitadas |
| `viares-lancamento-design-1080x1350.png` | Feed 4:5 | Anuncia a linha de design gráfico. Post-chave da semana 2 do calendário |
| `viares-stories-enquete-1080x1920.png` | Stories | Enquete de qualificação. Quem responde "celular" vira lead |
| `viares-oferta-mini-ensaio-1080x1350.png` | Feed 4:5 | Versão anterior da oferta (5 fotos, feed). Mantida como histórico |

Cada PNG tem um `.html` correspondente com o mesmo nome.

### A peça de oferta em Stories

Redesenho completo da oferta, seguindo a filosofia visual **Luz Medida**
(`FILOSOFIA-luz-medida.md`), que empresta a linguagem dos instrumentos de
medição fotográfica — folha de contato, escala de degraus, índices numerados.

O que mudou em relação à versão de feed:

- **A quantidade virou desenho.** As 10 fotos são 10 quadros em proporção 4:5,
  numerados de `01` a `10`, com densidade crescente. Quem fotografa reconhece a
  folha de contato; quem não fotografa vê uma série rigorosa. Em vez de ler um
  número, a pessoa **conta** — e contar prende o olho por mais tempo.
- **Tipografia nova.** Italiana (serifada de contraste alto) no monumento e IBM
  Plex Mono em corpo mínimo para todos os rótulos. Sem tamanhos intermediários:
  a hierarquia é um salto, não uma rampa.
- **Campo escuro com vinheta** em vez de fundo chapado — a luz se concentra no
  centro, como num laboratório de revelação.
- **Área segura do Stories respeitada.** Tudo vive entre 250px e 1670px, onde a
  interface do Instagram não cobre. Por isso o topo e a base parecem vazios
  quando a imagem é vista fora do app — é intencional.
- **Chamada em bloco sólido dourado.** Numa peça elegante e escura, a conversão
  precisa de um ponto de contraste inequívoco.

### Como usar o Stories

A faixa entre ~1230px e ~1580px foi deixada **vazia de propósito**: é onde entra a
figurinha de enquete do Instagram, com as opções *"Profissional"* e *"Foto de
celular"*. Depois, responda no direct todo mundo que votar na segunda — é o
script B4 do plano.

### A peça de Dia dos Pais

**Dia dos Pais 2026 cai em domingo, 09/08.** A peça é construída em torno desse
prazo, não em torno do serviço — numa campanha sazonal a data é o argumento.

Os três quadros são **encaixes de foto**, não decoração: têm marcas de corte nos
cantos e cruz de registro no centro, a linguagem da folha de contato. Isso faz a
peça se sustentar visualmente antes das imagens entrarem — e no Canva basta
arrastar a foto sobre cada quadro para preencher. As legendas (`PAI & FILHOS`,
`RETRATO`, `FAMÍLIA`) indicam o que vai em cada um e ao mesmo tempo comunicam o
que o ensaio entrega.

A linha de números virou tabela de três colunas — `30 MIN` · `15 FOTOS` ·
`R$ 250` — com filetes verticais separando. Na versão anterior o preço aparecia
sob o rótulo "PARA ENTREGA", herdado da coluna de prazo; cada número agora tem
o rótulo certo.

> Detalhe técnico: a Italiana não traz o glifo do cifrão — `R$` renderiza como
> `RS`. Por isso as unidades (`MIN`, `R$`) saem na monoespaçada, dentro da
> classe `.u`.

## Editar antes de publicar

**Dia dos Pais** — topo de `src/build_diadospais.py`:

```python
DATA_PAIS = '09 DE AGOSTO'          # prazo da agenda
VAGAS, MINUTOS, FOTOS, PRECO = '05', '30', '15', '250'
PALAVRA   = 'PAI'                   # palavra-chave pedida no direct
LEGENDAS  = ['PAI & FILHOS', 'RETRATO', 'FAMÍLIA']
```

`LEGENDAS` controla quantos encaixes existem — três nomes, três quadros.

**Peça de oferta (Stories)** — topo de `src/build_oferta_stories.py`:

```python
VAGAS   = '05'
FOTOS   = 10
MINUTOS = '20'
PRAZO   = '48'
MES     = 'AGOSTO'
DATA    = 'SÁB · 16 AGO'
```

Mudar `FOTOS` redesenha a folha de contato sozinho — os quadros e a numeração
são gerados a partir desse número.

**Demais peças** — topo de `src/build_viares.py`:

```python
VAGAS        = '5'
DATA_OFERTA  = 'SÁBADO · 16 DE AGOSTO'
MES_AGENDA   = 'AGENDA · AGOSTO'
HANDLE       = '@viaresfotografia'
```

## Paletas

**Luz Medida** — peça de oferta em Stories:

| Cor | Hex | Uso |
| --- | --- | --- |
| Preto quente | `#12100C` → `#0A0907` | Campo, com grão fino e vinheta |
| Osso quente | `#F4EFE7` | O que se lê |
| Dourado envelhecido | `#BE9A62` | O que se mede — filetes, índices, chamada |

**Peças anteriores:**

| Cor | Hex | Uso |
| --- | --- | --- |
| Areia | `#EFE8DF` → `#DED3C6` | Fundo claro, com textura de papel procedural |
| Preto quente | `#17140F` | Texto principal e fundo escuro |
| Dourado suave | `#A8814F` | Acento, palavra-chave do CTA, filetes |

Tipografia — **Italiana** + **IBM Plex Mono** na peça de oferta; **Anton** +
**Poppins** nas demais. Todas SIL Open Font License.

## Regenerar

```bash
pip install pillow numpy playwright

python3 src/build_diadospais.py       # Dia dos Pais
python3 src/shoot_diadospais.py

python3 src/build_oferta_stories.py    # oferta em Stories
python3 src/shoot_oferta.py

python3 src/build_viares.py           # demais peças
python3 src/shoot.py
```

`src/shoot.py` procura um Chromium já instalado em `/opt/pw-browsers/`; se não
achar, usa o do próprio Playwright.
