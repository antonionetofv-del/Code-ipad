# Folder dobrável — II FENAGRO-MR

Folder de 3 dobras (frente e verso) da II FENAGRO-MR — Feira de Negócios do Agro
de Mãe do Rio/PA, 17 a 20 de setembro, Espaço Cuia.

## Formato

Duas faces de **303 × 216 mm** (30,3 × 21,6 cm), conforme o modelo da gráfica.
Margem de segurança de 9 mm em todas as colunas.

| Face | Painel (esq. → dir.) | Largura | Conteúdo |
|------|----------------------|---------|----------|
| Externa | 1 | 100 mm | Atrações confirmadas (aba que dobra para dentro) |
| Externa | 2 | 100 mm | Contracapa — convite, destaques, contato, patrocínio |
| Externa | 3 | 103 mm | Capa |
| Interna | 1 | 103 mm | Programação oficial — 17 e 18/09 |
| Interna | 2 | 100 mm | Programação oficial — 19 e 20/09 |
| Interna | 3 | 100 mm | Cronograma de palestras |

## Arquivos

- `build_folder.py` — gera o HTML; todo o conteúdo (programação, palestras,
  atrações) fica nas listas no topo do script.
- `folder-fenagro.html` — folder pronto, autocontido (imagens em base64),
  para importar no Adobe Express.
- `assets/` — recortes gráficos extraídos das artes oficiais.
- `FENAGRO-face-externa.png`, `FENAGRO-face-interna.png` — prévias em 2x.

## Como regerar

```bash
python3 build_folder.py
```

## Tipografia

Anton (títulos) e Montserrat (texto), via Adobe Fonts (kit `oia8csk`).

## Paleta

| Cor | Uso |
|-----|-----|
| `#01270E` | verde escuro (fundo capa/contracapa e faixas) |
| `#14713A` | verde médio (pílulas, horários) |
| `#FBF7EB` | creme (fundo dos painéis de conteúdo) |
| `#E3B45A` | dourado (destaques) |
