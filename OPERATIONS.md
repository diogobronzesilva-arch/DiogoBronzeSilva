# Estado operacional e dependências

**Verificado em:** 6 de outubro de 2026  
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

O plano partilhado da Hostinger mantém outros websites, domínios e serviços. Esta migração não requer cancelar o plano nem transferir o domínio. No painel consultado em 28 de setembro de 2026, o domínio tinha validade até 19 de agosto de 2027, com renovação automática ativa e bloqueio de transferência ativo. Mantém apenas a renovação do domínio na Hostinger; não alteres contas, ficheiros ou DNS de outros projetos como parte da manutenção deste site.

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

A auditoria pública confirmou as 17 rotas do sitemap, os cabeçalhos de segurança, o redirecionamento `www` preservando caminho e query, e o estado 404. A PR [#39](https://github.com/diogobronzesilva-arch/DiogoBronzeSilva/pull/39) passou o check obrigatório `Site checks` e foi integrada em 28 de setembro de 2026. O painel Cloudflare Pages confirmou como concluído o deployment de produção do commit `fc1e56c` (`main`). A alteração desta PR é documental; não muda o artefacto público.

A PR [#40](https://github.com/diogobronzesilva-arch/DiogoBronzeSilva/pull/40) atualizou este registo e o README, passou o check obrigatório `Site checks` e foi integrada em 28 de setembro de 2026. Após o merge, o painel Cloudflare Pages confirmou como concluído o deployment de produção do commit `6eca4f1` (`main`). Esta é uma confirmação histórica desse deployment; o painel Pages mostra sempre a publicação mais recente.

A PR [#41](https://github.com/diogobronzesilva-arch/DiogoBronzeSilva/pull/41) corrigiu este histórico, passou `Site checks` e foi integrada no mesmo dia. Cloudflare Pages confirmou como concluído o deployment de produção do commit `d13cb31` (`main`).

A PR [#44](https://github.com/diogobronzesilva-arch/DiogoBronzeSilva/pull/44) protegeu os links `mailto:` com marcadores `<!--email_off-->`, adicionou o workflow semanal `production-audit.yml` aos domingos e alinhou a auditoria de produção.

A PR [#47](https://github.com/diogobronzesilva-arch/DiogoBronzeSilva/pull/47) refinou a grelha editorial, introduziu o destaque visual de notas recentes (`entry--featured`), chamadas de ação para conversas gravadas (`entry__action`) e atualizou a versão de cache de estilos para `20260930-1`.

A PR [#48](https://github.com/diogobronzesilva-arch/DiogoBronzeSilva/pull/48) removeu a imagem de Photography da página inicial, unificou o texto da hero (`hero__welcome`), otimizou a leitura LCP do retrato (`fetchpriority="high"`) e assegurou touch targets móveis de 44px.

Em outubro de 2026, foi restaurada a cadeia bidirecional de avanço entre notas (`the-work-that-holds-the-rest` para `the-life-i-would-not-trade`), gerados cartões Open Graph dedicados para ambas as notas e automatizada a verificação de sequência de artigos em `scripts/check_site.py`.

O workflow `Production audit` executa semanalmente a partir da branch `main` e pode ser acionado manualmente. Valida as rotas públicas e a respetiva paridade com o código, os cabeçalhos, o RSS, o sitemap, o redirecionamento canónico, os links de email sem dependência de JavaScript e os registos DNS públicos usados pelo email. Este check é de leitura e não altera DNS nem envia mensagens.

## DNS e segurança do domínio

A zona Cloudflare usa configuração Full e os nameservers delegados na Hostinger são os da Cloudflare. O domínio continua ativo na Hostinger, com renovação automática e bloqueio de transferência ligados.

**DNSSEC:** o registo DS fornecido pela Cloudflare foi adicionado na Hostinger. Em 28 de setembro de 2026, o painel Cloudflare confirmou: “Success! diogobronzesilva.com is protected with DNSSEC.” A validação concluiu e o DNSSEC está ativo.

Dois resíduos do alojamento e email antigos foram removidos apenas da zona `diogobronzesilva.com` no Cloudflare em 28 de setembro de 2026:

- O registo A `ftp.diogobronzesilva.com`.
- O registo DKIM `titan1._domainkey.diogobronzesilva.com` do Titan antigo.

Os registos ativos de Pages, Cloudflare Email Routing e Resend foram mantidos. Não foi alterado qualquer outro domínio.

## Email

**Entrada:** os MX do domínio são tratados pelo Cloudflare Email Routing. O catch-all e as regras explícitas `diogo@` e `hello@` encaminham para o Gmail. Em 28 de setembro de 2026, o painel de Email Routing mostrava 3 mensagens recebidas e 3 entregues/encaminhadas na janela dos últimos sete dias.

**Saída:** o domínio está verificado no Resend e o Gmail está configurado para usar o SMTP do Resend ao enviar como `diogo@diogobronzesilva.com`. Em 28 de setembro de 2026 foi enviada uma mensagem de teste deste alias para a caixa Gmail pessoal; a mensagem chegou e o cabeçalho recebido confirmou o remetente `diogo@diogobronzesilva.com`.

A caixa postal continua a ser o Gmail pessoal. Cloudflare Email Routing encaminha mensagens e Resend envia mensagens autenticadas; nenhum dos dois é uma caixa postal. Não guardes endereços privados de destino, passwords, códigos, credenciais SMTP ou chaves API neste repositório.

O registo DMARC está em modo de monitorização (`p=none`). Em 28 de setembro de 2026, a gestão de relatórios DMARC da Cloudflare foi ativada e o registo TXT `_dmarc` recebeu um destino agregado de relatórios gerido pela Cloudflare. A política `p=none` foi mantida; isto não bloqueia nem põe em quarentena mensagens. No momento da ativação, o painel ainda aguardava o primeiro relatório, que pode demorar até 24 horas a aparecer. Revisa os relatórios durante algumas semanas. Antes de passar para `quarantine` ou `reject`, confirma o alinhamento SPF/DKIM do Resend, do Buttondown caso envie mensagens com este domínio e de qualquer outro emissor legítimo.

Os links `mailto:` públicos de Work e Contact usam os comentários `email_off` da Cloudflare para manter o endereço clicável e evitar a injeção do script de descodificação. A exceção é apenas para o endereço público do site; a ofuscação global da zona não precisa de ser desativada.

## AEO, crawlers e descoberta

A estratégia editorial e as afirmações sobre crawlers foram revistas em [AEO_GEO_STRATEGY.md](AEO_GEO_STRATEGY.md). As recomendações atuais não prometem posições nem citações por sistemas de IA. O ficheiro `llms.txt` é uma página de contexto legível, não uma garantia de indexação ou ranking.

## Branches e limpeza do repositório

Em 28 de setembro de 2026, as branches associadas a PRs integradas foram removidas. Também foram apagadas `preview` e `cleanup-home-css`: ambas estavam 0 commits à frente de `main`, pelo que não continham alterações exclusivas. A listagem GitHub ficou com `main` e estas duas branches não principais:

- `fix/production-audit-2026-09-07` — tem um commit exclusivo; não foi encontrada uma PR integrada. Mantida para revisão.
- `post/a-impossibilidade-de-separar-costumes-e-economia` — tem um commit exclusivo; a PR [#30](https://github.com/diogobronzesilva-arch/DiogoBronzeSilva/pull/30) foi fechada sem merge. Mantida para revisão.

Nenhuma destas duas branches participa no deployment, que publica exclusivamente `main`. Foram preservadas porque contêm trabalho que não está integrado; revê esse conteúdo antes de decidir se apagas ou recuperas alguma.

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

A auditoria de produção compara o código local com o site público; executa-a a partir de `main` depois do deployment, não numa branch ainda não publicada. O workflow semanal executa o mesmo check contra a versão atual de `main`.
