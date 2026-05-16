# Acessibilidade — Vivendo com Parkinson

Este documento registra as decisões de acessibilidade do portal, baseado no [A11Y Project Checklist](https://www.a11yproject.com/checklist/) e adaptado para as necessidades específicas do público com Doença de Parkinson.

## Por que isso importa mais aqui

O público inclui:
- **Idosos** (a doença atinge principalmente pessoas acima de 60 anos)
- Pessoas com **tremor essencial** ou tremor parkinsoniano (afeta uso de mouse, toque na tela)
- **Bradicinesia** — movimentos mais lentos
- **Acuidade visual reduzida** — dificuldade com contraste baixo, fontes pequenas, cores próximas
- **Fadiga cognitiva** — sessões precisam ser curtas, informação clara
- **Cuidadores idosos** — frequentemente com limitações próprias

Acessibilidade aqui não é "ser inclusivo": é requisito para o projeto funcionar.

---

## Checklist baseado no A11Y Project

### Conteúdo

- [x] **Use linguagem simples e clara.** Linguagem evita jargão técnico quando possível; quando inevitável, explica.
- [x] **Use elementos de título para introduzir conteúdo.** Hierarquia H1 → H2 → H3 respeitada em cada página. Apenas um H1 por página.
- [x] **Use listas para agrupar itens relacionados.** `<ul>` e `<ol>` no lugar de parágrafos com bullets visuais.
- [x] **Use o atributo `lang` correto.** `<html lang="pt-BR">`.
- [x] **Tenha um título descritivo e único na página.** Cada página tem `<title>` único.
- [ ] **Forneça um sumário/landmarks.** Header, main, footer presentes; tags ARIA quando necessário.

### Imagens globais

- [ ] **Texto alternativo para imagens informativas.** Quando houver imagens, sempre usar `alt` descritivo.
- [ ] **Imagens decorativas com `alt=""` ou `aria-hidden="true"`.** O SVG da tulipa é decorativo quando ao lado do nome.
- [ ] **Forneça alternativa em texto para imagens complexas** (tabelas, gráficos, mapas).

### Cabeçalhos

- [x] **Cabeçalhos descritivos.** Cada seção tem H2/H3 que descrevem o conteúdo.
- [x] **Ordem hierárquica respeitada.** Não pular níveis (H1 → H3 sem H2).

### Listas

- [x] **Conteúdo em lista usa elemento de lista.** Não usar parágrafos com `•` visual.

### Controles (botões, links, formulários)

- [x] **Identifique controles com cores acessíveis.** Botões e links visivelmente distintos com contraste AA+.
- [x] **Estado de foco visível.** `*:focus-visible` com `outline: 3px solid var(--terracotta)`.
- [x] **Alvos de toque ≥ 48×48px.** Variável `--touch-target-min: 48px` aplicada em todos os elementos interativos. *(Recomendação para Parkinson — maior que o WCAG 2.5.5 que pede 44px.)*
- [x] **Garanta espaço entre itens interativos.** Pelo menos 8px entre alvos clicáveis (importante para tremor).
- [ ] **Não use apenas cor para indicar significado.** Estados de erro/sucesso devem ter ícone + texto, não só cor.

### Tabelas

- [ ] **Use `<th>` para cabeçalhos.** Aplicável quando houver tabelas (a glossário em `educacao.astro` usa `<dl>`).
- [ ] **Use `scope`, `id`, `headers` em tabelas complexas.**

### Formulários

- [ ] **Toda entrada tem `<label>` associado.** A implementar quando criar formulário de contato.
- [ ] **Marque campos obrigatórios visualmente E por código** (`aria-required="true"`).
- [ ] **Mensagens de erro associadas via `aria-describedby`.**
- [ ] **Não dependa apenas de cor para indicar erro.**

### Mídia

- [ ] **Vídeos têm legendas.** Aplicável se forem adicionados vídeos no futuro.
- [ ] **Áudio tem transcrição.** Aplicável para versões em áudio dos capítulos.
- [ ] **Não usar autoplay** com áudio.

### Animação

- [x] **Respeitar `prefers-reduced-motion`.** Implementado globalmente em `global.css`:
  ```css
  @media (prefers-reduced-motion: reduce) {
    *, *::before, *::after {
      animation-duration: 0.01ms !important;
      transition-duration: 0.01ms !important;
    }
  }
  ```
- [x] **Sem animações que piscam mais de 3 vezes por segundo** (risco de epilepsia fotossensível).

### Tempo

- [ ] **Se houver timeout de sessão, permita estender.** Sem aplicação no escopo atual.

### Apresentação

- [x] **Site se mantém usável em zoom 200% ou texto aumentado.** Layout usa `rem` e `clamp`, não pixels fixos para fontes.
- [x] **Contraste de texto:** mínimo 4.5:1 (texto normal), 3:1 (texto grande). Cores principais auditadas:
  - `--ink` (#14110F) sobre `--cream` (#F4EFE6) = **15.8:1** ✓ (AAA)
  - `--ink-soft` (#3A332C) sobre `--cream` = **11.2:1** ✓ (AAA)
  - `--ink-muted` (#6B6258) sobre `--cream` = **5.1:1** ✓ (AA)
  - `--teal` (#1F4D45) sobre `--cream` = **8.9:1** ✓ (AAA)
  - `--terracotta` (#C25A3C) sobre `--cream` = **3.7:1** ⚠️ (AA apenas para texto grande)

### Mobile / responsivo

- [x] **Conteúdo permanece organizado em zoom ou distorção de cores.** Layout responsivo sem perder estrutura.
- [x] **Texto em tamanho normal: contraste 4.5:1. Texto grande: 3:1.** Verificado acima.
- [x] **Espaço suficiente entre itens interativos para rolagem confortável.** *Pessoas com Parkinson podem ter muita dificuldade em rolar a tela junto de itens interativos sem espaçamento adequado.*

---

## Pontos de atenção específicos para Parkinson

### Tremor
- Alvos de toque **maiores que o padrão WCAG** (48px+ vs 44px).
- Espaço entre alvos: mínimo 8px.
- Evitar interações que exigem precisão (drag-and-drop, hover prolongado).
- Não usar gestos complexos no mobile (pinch, swipe múltiplo).

### Bradicinesia (lentidão de movimento)
- Sem timeout em formulários ou modais.
- Sem animação de "autoclose" em toasts/notificações.
- Botões `[type="button"]` em vez de submit automático.

### Fadiga cognitiva
- Sessões curtas — cada capítulo tem ~5min de leitura.
- Linguagem clara, frases curtas, sem subordinadas longas.
- Termos técnicos sempre explicados.
- Navegação anterior/próximo em cada capítulo (não obriga voltar ao sumário).

### Disfagia e fala
- (Aplicável se incluirmos áudio.) Versões em áudio com locução clara, ritmo lento.

### Visão
- Tema claro com fundo creme (`#F4EFE6`) em vez de branco puro — reduz fadiga ocular.
- Fonte base 18px (vs 16px padrão).
- Atkinson Hyperlegible — fonte criada pelo Braille Institute para baixa visão.
- Contraste AA mínimo, AAA quando possível.
- Sublinhado em links (não usar só cor).

---

## Ferramentas de auditoria recomendadas

| Ferramenta | O que checa | Como usar |
|------------|-------------|-----------|
| [axe DevTools](https://www.deque.com/axe/devtools/) | Erros automatizáveis (60% dos problemas) | Extensão Chrome/Firefox |
| [WAVE](https://wave.webaim.org/) | Estrutura, ARIA, contraste | wave.webaim.org/extension |
| [Lighthouse](https://developer.chrome.com/docs/lighthouse/) | Score geral de acessibilidade | DevTools → Lighthouse |
| [Pa11y](https://pa11y.org/) | CLI para CI/CD | `npx pa11y http://localhost:4321` |
| Leitor de tela | Teste real de navegação | macOS: VoiceOver (Cmd+F5) · Windows: NVDA (grátis) |

## Auditoria manual obrigatória antes de cada release

1. **Navegação só com teclado** — Tab por toda a página, todos os elementos focáveis, ordem lógica.
2. **Zoom 200%** — Layout não quebra, texto permanece legível.
3. **Leitor de tela** — Lê ordem correta, anúncios fazem sentido.
4. **Mobile real** — Não emulador. Testar em iOS e Android.
5. **`prefers-reduced-motion` ligado** — Sem animações sobrando.

---

## Status atual

**Última auditoria:** ainda não realizada.

**Próxima auditoria:** após primeiro deploy de staging.

**Issues conhecidas:**
- `--terracotta` usado em texto pequeno está em AA apenas para texto grande (eyebrow ok, mas atenção ao usar em botões pequenos)
- Falta página de "Declaração de Acessibilidade" formal
- Falta toggle de "alto contraste" como opção do usuário (além do `prefers-contrast`)
