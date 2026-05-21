# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Projeto

Portal PWA **Vivendo com Parkinson** — educação em saúde sobre a Doença de Parkinson, parceria UnB-FCTS × Associação Parkinson Brasília. Baseado no Manual *Cuidando do Paciente com Parkinson* (Pereira & Furia, 2ª ed., Kognos, 2021). Aprovação ética CEP-FCTS nº 6.376.222.

## Comandos

```bash
npm run dev      # servidor de desenvolvimento em http://localhost:4321
npm run build    # build de produção (output: dist/)
npm run preview  # preview do build de produção
```

PWA exige HTTPS para instalação mobile — funciona em `localhost` e em HTTPS (Cloudflare Pages).

Utilitários em `scripts/` (executar diretamente, não são parte do bundle):
- `node scripts/generate-pwa-icons.mjs` — gera ícones PWA a partir de `public/favicon.svg`
- `node scripts/trim-and-convert.mjs` — recorta, redimensiona e converte imagens para WebP via sharp
- `python scripts/extract-figures.py` — extrai figuras de PDF usando PyMuPDF
- `npx pa11y http://localhost:4321` — auditoria de acessibilidade automatizada

## Stack

- **Astro 4** — SSG, zero JS no cliente por padrão
- **@vite-pwa/astro** — service worker + manifest (configurado em `astro.config.mjs`)
- **CSS puro** com design tokens em variáveis (não usar Tailwind nem styled-components)
- **TypeScript** strict mode, path alias `~/*` → `src/*`
- **@astrojs/mdx** + **@astrojs/sitemap** — prontos para content collections

## Arquitetura

### Hierarquia de layouts

```
BaseLayout.astro        ← <html lang="pt-BR">, head, Header, skip-link, Footer
  └─ SectionLayout.astro  ← sidebar de sumário + prev/next + slot de conteúdo
       └─ src/pages/*.astro  ← cada arquivo = uma rota (/doenca, /sintomas, …)
```

- `index.astro` usa `BaseLayout` diretamente (hero, stats, grade de cards).
- As 13 páginas de conteúdo usam `SectionLayout`.

### SectionLayout — detalhes críticos

O array `sections` em `SectionLayout.astro` é **hardcoded** — define a ordem da sidebar e da navegação prev/next. Ao adicionar uma nova página:

1. Criar `src/pages/<slug>.astro` com `<SectionLayout section="<slug>" title="…">`
2. Adicionar entrada no array `sections` de `SectionLayout.astro`
3. Se quiser no menu principal: adicionar em `navItems` de `Header.astro`
4. Adicionar card na grade da `index.astro`

### Componentes disponíveis

**`<Figure>`** — imagens com WebP automático:
```astro
<Figure
  src="/assets/figuras/neuronio-dopaminergico.png"  <!-- gera .webp automaticamente -->
  alt="Neurônio dopaminérgico e progressão da perda celular"
  caption="Figura 3 — Neurônio dopaminérgico"
  variant="inline"   <!-- 'inline' (padrão, 65ch) | 'wide' (100%) | 'aside' (float direita) -->
  credit="Manual, 2021"
/>
```

**`<Tulip>`** — SVG da tulipa vermelha (símbolo internacional do DP):
```astro
<Tulip size="2em" ariaLabel="Símbolo da tulipa vermelha" />
<!-- sem ariaLabel = decorativo (aria-hidden) -->
```

**`Header.astro`** — usa `Astro.url.pathname` para marcar a página ativa com `aria-current="page"`.

### Imagens disponíveis em `public/assets/figuras/`

Cada figura existe em `.png` e `.webp`: `alteracoes-autonomicas`, `alteracoes-sensoriais`, `apb-atividades`, `heimlich-com-ajuda`, `heimlich-sozinho`, `neuronio-dopaminergico`, `postura-parkinsoniana`.

## Design system

Tokens definidos em `src/styles/global.css`. **Sempre usar variáveis CSS, nunca hex hardcoded.**

Cores principais: `--cream` (fundo), `--ink` (texto), `--teal` (links/CTAs), `--terracotta` (acento/foco), `--tulip` (símbolo).

Tipografia: `var(--font-serif)` = Fraunces (títulos), `var(--font-sans)` = Atkinson Hyperlegible (corpo). Base 18px.

Espaçamento: escala `--space-1` (0.25rem) … `--space-24` (6rem).

## Acessibilidade — não negociável

O público inclui idosos, pessoas com tremor, bradicinesia, baixa visão e fadiga cognitiva. Consulte `docs/ACCESSIBILITY.md` para o checklist completo.

Regras críticas:
- **Alvos de toque ≥ 48px:** `min-height: var(--touch-target-min)` em todos os elementos interativos
- **Espaço entre alvos:** mínimo 8px (para tremor)
- **Foco visível:** `*:focus-visible { outline: 3px solid var(--terracotta) }` — não remover
- **`--terracotta`** (#C25A3C) atinge apenas AA para texto grande — não usar em texto pequeno
- **`prefers-reduced-motion`** já coberto globalmente em `global.css` — não adicionar animações sem verificar
- **Sem timeout** em modais ou formulários (bradicinesia)
- Tema claro é obrigatório; dark mode foi rejeitado por dificuldade de leitura

## Convenções

- Indentação: 2 espaços
- Strings: aspas simples em JS/TS, aspas duplas em HTML
- Nomes de arquivo: kebab-case (`minha-pagina.astro`)
- Componentes Astro: PascalCase (`Header.astro`)
- Classes CSS: kebab-case, BEM-style (`card--primary`, `card__title`)
- Conteúdo médico inserido fora do manual original: marcar com `<!-- TODO: revisar com equipe técnica -->`
- Imagens: `<picture>` com fallbacks WebP, `loading="lazy"` fora do hero, `alt` descritivo sempre
- Performance: site deve funcionar em 3G/4G — evitar JS pesado e fontes adicionais além das duas já carregadas
