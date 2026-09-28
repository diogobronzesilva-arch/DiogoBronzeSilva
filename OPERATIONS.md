# Estado operacional e dependências

**Verificado em:** 28 de setembro de 2026  
**Repositório:** [diogobronzesilva-arch/DiogoBronzeSilva](https://github.com/diogobronzesilva-arch/DiogoBronzeSilva)  
**Produção:** [diogobronzesilva.com](https://diogobronzesilva.com/)

Este registo descreve a configuração efetiva do website e separa o que foi confirmado do que ainda depende de propagação ou acompanhamento. Confirma os painéis dos fornecedores antes de alterações futuras.

## Arquitetura e responsabilidades

| Parte | Serviço | Estado |
| --- | --- | --- |
| Código do website | GitHub, `main` | Fonte de verdade; alterações passam por pull request e pelo check `Site checks`. |
| Publicação web | Cloudflare Pages, `diogobronzesilva` | Publicação automática de `main`; build `python3 scripts/build_pages.py`, saída `dist`. |
| DNS autoritativo | Cloudflare | Setup Full; o domínio e `www` apontam para Pages. |
| Registo e renovação | Hostinger | `diogobronzesilva.com` continua registado na Hostinger; renovação automática e bloqueio de transferência estão ativos. |
| Email de entrada | Cloudflare Email Routing | Catch-all e regras para `diogo@` e `hello@` encaminham para a caixa pessoal Gmail. |
| Email de saída | Resend via Gmail | Gmail envia como `diogo@diogobronzesilva.com` pelo SMTP do Resend; envio e receção foram testados. |
| Newsletter | Buttondown | Só recebe dados de quem subscreve através dos formulários do site. |
| Fotografia | Bronze Art, `bronzeart.pt` | Website separado deste projeto. |

### Independência da Hostinger

A Hostinger já não serve o website, não é o DNS autoritativo e não fornece o email ativo do domínio. GitHub fornece o código, Cloudflare Pages serve o site, Cloudflare gere o DNS e encaminhamento de entrada, e Resend permite o envio autenticado. A dependência intencional que permanece na Hostinger é o registo e renovação de `diogobronzesilva.com`.

O plano partilhado da Hostinger mantém outros websites, domínios e serviços. Esta migração não requer cancelar o plano nem transferir o domínio. Não alteres contas, ficheiros ou DNS de outros projetos como parte da manutenção deste site.

## Publicação

O fluxo normal é:

```text
branch → pull request → Site checks → merge para main → publicação automática no Cloudflare Pages
```

Configuração confirmada:

- Branch de produção: `main`.
- Comando de build: `python3 scripts/build_pages.py`.
- Pasta de saída: `dist`.
- Domínios ligados: `diogobronzesilva.com` e `www.diogobronzesilva.com`.
- O domínio sem `www` é canónico; uma Redirect Rule preserva caminho e parâmetros.
- `_headers` aplica os cabeçalhos de segurança e a política de revalidação.
- `404.html` fornece a página de erro do Pages.
- Não são necessários Wrangler, Workers, servidor de aplicação, base de dados ou segredos de build.

A PR [#38](https://github.com/diogobronzesilva-arch/DiogoBronzeSilva/pull/38) passou os checks e foi integrada em 28 de setembro de 2026. O painel Pages confirmou o deployment de produção do commit `5c1bff4` como concluído. A PR removeu `.htaccess`, configuração Apache sem efeito no artefacto Pages; as funções relevantes já estão cobertas pela regra de redirecionamento, `_headers` e `404.html`.

A auditoria pública anterior confirmou as 17 rotas do sitemap, cabeçalhos de segurança, o redirecionamento `www` preservando caminho e query, e o estado 404. A alteração mais recente foi documental e o deployment correspondente de `main` concluiu com sucesso.

## DNS e segurança do domínio

A zona Cloudflare usa configuração Full e os nameservers delegados na Hostinger são os da Cloudflare. O domínio continua ativo na Hostinger, com renovação automática e bloqueio de transferência ligados.

**DNSSEC:** o registo DS fornecido pela Cloudflare foi adicionado na Hostinger. Em 28 de setembro de 2026, o painel Cloudflare confirmou: “Success! diogobronzesilva.com is protected with DNSSEC.” A validação concluiu e o DNSSEC está ativo.

Dois resíduos do alojamento e email antigos foram removidos apenas da zona `diogobronzesilva.com` no Cloudflare em 28 de setembro de 2026:

- O registo A `ftp.diogobronzesilva.com`.
- O registo DKIM `titan1._domainkey.diogobronzesilva.com` do Titan antigo.

Os registos ativos de Pages, Cloudflare Email Routing e Resend foram mantidos. Não foi alterado qualquer outro domínio.

## Email

**Entrada:** os MX do domínio são tratados pelo Cloudflare Email Routing. O catch-all e as regras explícitas `diogo@` e `hello@` encaminham para o Gmail. Um teste de entrada já aparecia como encaminhado no registo de atividade do Cloudflare.

**Saída:** o domínio está verificado no Resend e o Gmail está configurado para usar o SMTP do Resend ao enviar como `diogo@diogobronzesilva.com`. Em 28 de setembro de 2026 foi enviada uma mensagem de teste deste alias para a caixa Gmail pessoal; a mensagem chegou e o cabeçalho recebido confirmou o remetente `diogo@diogobronzesilva.com`.

A caixa postal continua a ser o Gmail pessoal. Cloudflare Email Routing encaminha mensagens e Resend envia mensagens autenticadas; nenhum dos dois é uma caixa postal. Não guardes endereços privados de destino, passwords, códigos, credenciais SMTP ou chaves API neste repositório.

O registo DMARC observado está em modo de monitorização (`p=none`). Mantém essa política enquanto recolhes e avalias relatórios; uma política mais restritiva requer primeiro verificar que todos os emissores legítimos estão alinhados.

## AEO, crawlers e descoberta

A estratégia editorial e as afirmações sobre crawlers foram revistas em [AEO_GEO_STRATEGY.md](AEO_GEO_STRATEGY.md). As recomendações atuais não prometem posições nem citações por sistemas de IA. O ficheiro `llms.txt` é uma página de contexto legível, não uma garantia de indexação ou ranking.

## Verificações de manutenção

Antes de uma alteração ao site:

```sh
python3 scripts/build_pages.py
python3 scripts/check_pages_output.py
```

Depois de a alteração chegar à produção:

```sh
python3 scripts/check_production.py
```

A auditoria de produção compara o código local com o site público; executa-a a partir de `main` depois do deployment, não numa branch ainda não publicada.
