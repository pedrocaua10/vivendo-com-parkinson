# Vivendo com Parkinson

> Portal PWA de pesquisa, educação em saúde e acolhimento sobre a Doença de Parkinson — parceria entre o Departamento de Fonoaudiologia da Universidade de Brasília (UnB-FCE) e a Associação Parkinson Brasília.

## Sobre o projeto

Iniciativa nascida a partir do Manual *Cuidando do Paciente com Parkinson* (Pereira & Furia, 2ª ed., Kognos, 2021). Reúne em formato digital, multilíngue e acessível, o conteúdo do manual mais frentes novas — Tecnologia e Parkinson, Educação em Saúde como hub e Contato e Ajuda expandido.

**Aprovação ética:** Comitê de Ética em Pesquisa UNB/FCE — parecer 2.279.574.

## Stack técnica

- **[Astro 4](https://astro.build)** — gerador de site estático com hidratação parcial. Pouquíssimo JavaScript no client, ótimo para abrir rápido em 3G/4G.
- **[Vite PWA](https://vite-pwa-org.netlify.app/)** — service worker, manifest e cache offline.
- **CSS puro** com design tokens em variáveis (sem framework de UI).
- **Markdown/MDX** para conteúdo (futuro — hoje as páginas estão em `.astro`).
- **TypeScript** (configurado, mas pouco usado por enquanto).

## Como rodar localmente

Pré-requisitos: Node.js 18+ e npm.

```bash
# 1. Instalar dependências
npm install

# 2. Servidor de desenvolvimento (http://localhost:4321)
npm run dev

# 3. Build de produção
npm run build

# 4. Preview do build
npm run preview
```

## Estrutura do projeto

```
vivendo-com-parkinson/
├── astro.config.mjs          # configuração Astro + PWA
├── package.json
├── tsconfig.json
│
├── public/                   # arquivos estáticos servidos como /
│   ├── favicon.svg           # tulipa, símbolo da DP
│   └── icons/                # ícones PWA (a gerar — ver README dentro da pasta)
│
├── src/
│   ├── layouts/
│   │   ├── BaseLayout.astro      # <html>, head, header, footer
│   │   └── SectionLayout.astro   # layout dos capítulos com sidebar
│   │
│   ├── components/
│   │   ├── Header.astro          # navegação principal + mobile menu
│   │   ├── Footer.astro          # rodapé com parceiros e contato
│   │   └── Tulip.astro           # SVG da tulipa (símbolo)
│   │
│   ├── pages/                # cada arquivo = uma rota
│   │   ├── index.astro       # / (home - hub do PWA)
│   │   ├── sobre.astro       # /sobre
│   │   ├── apb.astro         # /apb (Associação)
│   │   ├── doenca.astro      # /doenca
│   │   ├── sintomas.astro    # /sintomas
│   │   ├── diagnostico.astro
│   │   ├── tratamento.astro
│   │   ├── equipe.astro
│   │   ├── cuidador.astro
│   │   ├── direitos.astro
│   │   ├── educacao.astro
│   │   ├── tecnologia.astro
│   │   ├── depoimentos.astro
│   │   └── contato.astro
│   │
│   ├── styles/
│   │   └── global.css        # design tokens + reset + base
│   │
│   └── content/secoes/       # (reservado para conteúdo em Markdown futuramente)
│
└── docs/
    ├── CLAUDE.md             # instruções pro Claude Code
    └── ACCESSIBILITY.md      # checklist de acessibilidade do projeto
```

## Design system — princípios

### Tipografia
- **Títulos:** Fraunces (serifa moderna, dá autoridade editorial)
- **Corpo:** Atkinson Hyperlegible (criada pelo Braille Institute para alta legibilidade)
- **Base 18px** (maior que o padrão para conforto de leitura)

### Cores
| Token            | Hex       | Uso                              |
|------------------|-----------|----------------------------------|
| `--cream`        | `#F4EFE6` | Fundo principal (não branco puro)|
| `--cream-warm`   | `#EDE6D9` | Fundo de cards e seções          |
| `--ink`          | `#14110F` | Texto principal                  |
| `--ink-soft`     | `#3A332C` | Texto secundário                 |
| `--teal`         | `#1F4D45` | Cor primária (CTAs, links)       |
| `--terracotta`   | `#C25A3C` | Cor de acento (eyebrows, foco)   |
| `--tulip`        | `#B83A2C` | Símbolo da tulipa                |

### Acessibilidade
- Tamanho base de fonte: 18px
- Alvos de toque: ≥ 48×48 px (importante para usuários com tremor)
- Contraste WCAG AA mínimo, AAA quando possível
- `prefers-reduced-motion` respeitado
- Skip link visível ao focar
- Foco visível obrigatório (3px outline)
- Veja `docs/ACCESSIBILITY.md` para checklist completo

## Roadmap

### Fase atual (scaffold)
- [x] Estrutura Astro com 13 páginas
- [x] Design system implementado em CSS variables
- [x] Layout base + layout de seção com sidebar
- [x] Configuração PWA inicial (manifest, service worker)
- [x] Conteúdo dos capítulos com base no Manual 2ª ed.

### Próximos passos
- [ ] Gerar ícones PWA (192, 512, 512-maskable)
- [ ] Adicionar logos reais da UnB e da APB
- [ ] Migrar conteúdo das `.astro` para `.md` em content collections (facilita edição)
- [ ] Página de Acessibilidade declarando conformidade
- [ ] Página de Privacidade (LGPD)
- [ ] Formulário de contato funcional
- [ ] Glossário interativo (com busca)
- [ ] Modo "alto contraste" como toggle (além do `prefers-contrast`)
- [ ] Versão em áudio dos capítulos principais
- [ ] Testes de acessibilidade automatizados (axe-core)

## Hospedagem recomendada

**Cloudflare Pages** — gratuito, rápido no Brasil, deploy automático via GitHub.

```bash
# Build command:    npm run build
# Output directory: dist
```

## Créditos

**Autoria do conteúdo (Manual original):**
- Naira Rúbia Rodrigues Pereira (Fonoaudióloga, Mestranda UnB)
- Profa. Dra. Cristina Lemos Barbosa Furia (UnB-FCE)

**Revisão técnica:**
- Profa. Dra. Letícia Corrêa Celeste
- Dr. Pedro Renato de Paula Brandão (Neurologista)
- Profa. Dra. Juliana Onofre de Lira

**Instituição coparticipante:** Associação Parkinson Brasília

**Editora do manual:** Kognos Publish, Brasília, 2ª ed., 2021.

## Licença

Conteúdo editorial © UnB-FCE / APB. Código do portal: a definir.
