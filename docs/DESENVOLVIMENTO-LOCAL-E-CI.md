# Desenvolvimento local e gestão de GitHub Actions — 26/10/2026

Decisão expressa de Diogo no chat Codex 01a1799d-2cdc-7b62-a675-ecdc46d82c26: aplicar as correções de consumo em todos os projetos e informar o AntiGravity.

- Diogo pede alterações normalmente. Codex/AntiGravity tratam da pasta, revisão, testes e sincronização; os atalhos locais são opcionais.
- Conferir branch, alterações existentes e remoto; preservar trabalho concorrente e usar a pasta canónica partilhada. Não editar os mesmos ficheiros simultaneamente nas duas ferramentas.
- Validar localmente durante a tarefa e sincronizar o resultado por tarefa concluída. Não enviar cada pequeno ajuste nem voltar a executar testes pesados só para guardar o relatório final.
- Os workflows de CI automáticos abrangem main e pull requests para main. Pushes de branches de trabalho não iniciam uma segunda cópia do CI. Execuções obsoletas da mesma branch/PR são canceladas.
- Uma comparação leve distingue documentação de código. Apenas Markdown na raiz, docs/ e recibos explicitamente identificados dispensam os trabalhos pesados. Código, configurações, workflows, dependências, dados publicados e ficheiros desconhecidos mantêm validação completa. Renomes incluem os dois caminhos. API incompleta, erro, comparação truncada ou evento manual obrigam a validação completa.
- A verificação leve ainda consome uma pequena execução Linux; não afirmar custo ou minutos zero. Não usar [skip ci] como fluxo normal nem contornar checks obrigatórios.
- Manter o orçamento Actions de 0 USD com bloqueio; foi confirmado no painel em 26/10/2026. Não aumentar limites, contratar planos ou criar runners/serviços por iniciativa própria.
- Publicar domínios, alterar serviços ou instalar apps exige âmbito autorizado. Não confundir sincronização Git com publicação, nem um CI documental com aprovação de uma entrega.

Site checks conserva o nome exigido pelo ruleset e conclui a verificação documental sem saltar o workflow inteiro. HTML, assets, llms.txt, configurações e ficheiros desconhecidos continuam a exigir build e validação. A auditoria semanal continua ativa. Main continua a publicar automaticamente no Cloudflare Pages; esta política não autoriza uma publicação de conteúdo por inferência.

## Validação desta alteração

Workflows verificados localmente com actionlint 1.7.12 e 188 casos de comportamento/configuração, incluindo alterações documentais, código misturado, renomes, comparação incompleta e validação manual. Nenhuma subscrição ou orçamento foi alterado.
Build Pages e verificação dos 64 ficheiros públicos aprovados localmente. Conteúdo público preservado.
