// Gera icon-192.png, icon-512.png e icon-512-maskable.png a partir do favicon.svg.
// Uso: node scripts/generate-pwa-icons.mjs
import sharp from 'sharp';
import { readFileSync, mkdirSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dir = dirname(fileURLToPath(import.meta.url));
const root = join(__dir, '..');
const outDir = join(root, 'public', 'icons');
mkdirSync(outDir, { recursive: true });

const BG = '#F4EFE6';   // --cream
const TULIP_SVG = readFileSync(join(root, 'public', 'favicon.svg'), 'utf8');

// Cria SVG quadrado com fundo creme e a tulipa centralizada.
// padding: porcentagem do lado reservada como margem (0–0.5).
function buildSquareSvg(size, padding) {
  const inner = size * (1 - padding * 2);
  // Tulipa tem viewBox 24×32 — centramos em inner×inner com aspect ratio preservado.
  const scaleX = inner / 24;
  const scaleY = inner / 32;
  const scale = Math.min(scaleX, scaleY);
  const w = 24 * scale;
  const h = 32 * scale;
  const x = (size - w) / 2;
  const y = (size - h) / 2;

  return `<svg xmlns="http://www.w3.org/2000/svg" width="${size}" height="${size}" viewBox="0 0 ${size} ${size}">
  <rect width="${size}" height="${size}" fill="${BG}"/>
  <g transform="translate(${x.toFixed(2)} ${y.toFixed(2)}) scale(${scale.toFixed(4)})">
    ${TULIP_SVG.replace(/<svg[^>]*>/, '').replace('</svg>', '')}
  </g>
</svg>`;
}

const jobs = [
  { file: 'icon-192.png',          size: 192, padding: 0.10 },
  { file: 'icon-512.png',          size: 512, padding: 0.10 },
  { file: 'icon-512-maskable.png', size: 512, padding: 0.20 }, // 20% safe zone
];

for (const { file, size, padding } of jobs) {
  const svg = buildSquareSvg(size, padding);
  const out = join(outDir, file);
  await sharp(Buffer.from(svg))
    .png({ compressionLevel: 9 })
    .toFile(out);
  console.log(`✓ ${file}`);
}

console.log('Ícones gerados em public/icons/');
