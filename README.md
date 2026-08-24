# Diogo Silva — diogobronzesilva.com

Website pessoal de Diogo Silva. HTML e CSS estáticos, sem framework, sem build system e sem JavaScript.

Domínio: **diogobronzesilva.com**  
Email público: **hello@diogobronzesilva.com**

## Estrutura

```text
index.html                         → /
work/index.html                    → /work/
notes/index.html                   → /notes/
notes/<slug>/index.html            → /notes/<slug>/
notes/_template.html               → molde para novas notas
contact/index.html                 → /contact/
404.html                           → página de erro
feed.xml                           → /feed.xml
sitemap.xml                        → /sitemap.xml
robots.txt                         → /robots.txt
llms.txt                           → /llms.txt
assets/css/site.css                → folha de estilos única
assets/img/                        → fotografia, Open Graph e vinhetas
scripts/check_site.py              → validação técnica do site
.github/workflows/site-checks.yml  → CI para PRs e main
```

A raiz deste repositório é a fonte de verdade do site. Não deve existir uma pasta intermédia com uma cópia datada do website.

## Arquitectura editorial

A navegação principal é:

**Home · Work · Photography ↗ · Notes · Contact**

- **Home** é a porta de entrada pessoal. Deve manter-se curta.
- **Work** reúne experiência e pensamento sobre vendas, tecnologia, decisão e relações humanas.
- **Photography** aponta directamente para `bronzeart.pt`.
- **Notes** é a biblioteca de textos e, quando aplicável, participações seleccionadas em podcasts e entrevistas ao vivo sob `Podcasts and Live Interviews`.
- **Contact** é deliberadamente simples: email, LinkedIn e Bronze Art.

O site não deve transformar-se num CV online, landing page comercial ou exercício de personal branding.

## Princípios de Work

A página Work organiza-se em torno de três ideias:

1. **Sales is conversation.**
2. **Good salespeople help people decide. They don't decide for them.**
3. **AI should remove the work around the conversation, not the conversation itself.**

A experiência profissional serve para sustentar estas ideias, não para transformar a página numa cronologia de cargos. Para a cronologia completa, o site aponta para LinkedIn.

## Publicar uma nota nova

1. Criar `notes/<slug>/index.html` a partir de `notes/_template.html`.
2. Actualizar título, descrição, canonical, Open Graph, JSON-LD, data, língua e conteúdo.
3. Adicionar a entrada no topo da secção de notas recentes em `notes/index.html`.
4. Adicionar a URL a `sitemap.xml`.
5. Adicionar um `<item>` no topo de `feed.xml`.
6. Quando existirem três notas recentes, trocar `Selected Notes` na Home por `Latest Notes` e mostrar as três mais recentes.

O RSS contém apenas textos publicados. Participações em podcasts ou entrevistas não entram no feed.

## Podcasts and Live Interviews

Participações seleccionadas em podcasts e entrevistas ao vivo sobre filosofia, teologia, cultura, vendas ou outros temas editoriais pertencem a **Notes**, numa secção `Podcasts and Live Interviews`, acima de `Handwritten Notes`.

Não criar uma página de podcasts separada enquanto existirem apenas algumas participações. Evitar embeds, usar links externos simples para manter o site leve e sem JavaScript.

## Newsletter

Os formulários apontam para Buttondown:

`https://buttondown.com/api/emails/embed-subscribe/bronze_da_silva`

O formulário aparece na Home, no índice de Notes e no fim de cada artigo. Usa validação HTML nativa e abre a confirmação num novo separador.

## SEO e partilha

Manter em cada página publicada:

- `<title>` e meta description
- canonical
- Open Graph e Twitter card
- JSON-LD apropriado
- imagem OG 1200×630 quando disponível

`sitemap.xml`, `robots.txt`, RSS e `llms.txt` devem ser actualizados quando a arquitectura ou o conteúdo publicado muda.

## Design

- Papel: `#FBFAF7`
- Tinta: `#191814`
- Bronze: `#8A6A3C`
- Serif: Newsreader
- Sans: Instrument Sans

A estética deve continuar editorial, calma, clássica e com muito espaço negativo. Evitar elementos visuais típicos de SaaS, animações gratuitas, cartões excessivos e componentes que façam o site parecer um template.

## Privacidade e dependências

Não há analytics nem tracking instalados.

As fontes são actualmente carregadas através de Google Fonts. Se um dia se quiser eliminar esse pedido externo, fazer self-host dos `.woff2` e substituir os links por `@font-face` locais.

Buttondown só recebe dados de quem opta por subscrever a newsletter.

## Engenharia e publicação

O site é composto apenas por ficheiros estáticos. O conteúdo publicado no alojamento deve corresponder à raiz deste repositório.

O fluxo normal é:

`branch → pull request → Site checks → squash merge para main → deploy automático Hostinger`

A branch `main` está protegida. Alterações devem ser feitas numa branch e submetidas por pull request. O check obrigatório `Site checks` valida links internos, assets, metadata, canonical/Open Graph, JSON-LD, sitemap, RSS, `llms.txt`, `robots.txt`, acessibilidade básica, placeholders do template e consistência da versão do CSS antes de permitir merge.

Depois do merge, a Hostinger faz deployment automático da `main`. Existe ainda um check semanal de produção para detectar divergências entre o repositório e o website público.
