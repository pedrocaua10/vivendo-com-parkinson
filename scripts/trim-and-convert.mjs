/**
 * Recorta bordas excessivas e converte para WebP.
 * Uso: node scripts/trim-and-convert.mjs
 *
 * Estratégia de trim em duas passadas:
 *  1ª: remove borda escura (cabeçalho preto do PDF) se existir no canto
 *  2ª: remove margens brancas restantes
 * Após trim: adiciona 12px de padding branco para não cortar rente ao conteúdo.
 */

import sharp from 'sharp';
import { readFileSync, writeFileSync, statSync } from 'fs';
import { resolve } from 'path';

const DIR = resolve('public/assets/figuras');
const PADDING = 12;        // px de respiro após o trim
const MAX_WIDTH = 1200;    // largura máxima do resultado
const WEBP_QUALITY = 85;
const TRIM_THRESHOLD = 20; // margem de tolerância de cor (0–255)

const FILES = [
  'neuronio-dopaminergico.png',
  'postura-parkinsoniana.png',
  'alteracoes-sensoriais.png',
  'alteracoes-autonomicas.png',
  'heimlich-sozinho.png',
  'heimlich-com-ajuda.png',
  'apb-atividades.png',
];

async function getTopLeftPixel(buf) {
  const { data } = await sharp(buf)
    .extract({ left: 0, top: 0, width: 1, height: 1 })
    .raw()
    .toBuffer({ resolveWithObject: true });
  return { r: data[0], g: data[1], b: data[2] };
}

function isDark(px) {
  return px.r < 40 && px.g < 40 && px.b < 40;
}

async function trimToContent(inputBuf) {
  let buf = inputBuf;

  // 1ª passada: remove borda escura (se o canto for escuro)
  const px1 = await getTopLeftPixel(buf);
  if (isDark(px1)) {
    buf = await sharp(buf)
      .trim({ threshold: TRIM_THRESHOLD })
      .toBuffer();
  }

  // 2ª passada: remove margens brancas
  const px2 = await getTopLeftPixel(buf);
  // Se o novo canto ainda não for branco, force uma análise mais ampla
  // usando threshold alto para pegar tons de cinza claro também
  const whiteThreshold = (px2.r > 200 && px2.g > 200 && px2.b > 200) ? TRIM_THRESHOLD : 60;
  buf = await sharp(buf)
    .trim({ threshold: whiteThreshold })
    .toBuffer();

  // Adiciona padding branco ao redor do conteúdo recortado
  buf = await sharp(buf)
    .extend({
      top: PADDING, bottom: PADDING,
      left: PADDING, right: PADDING,
      background: { r: 255, g: 255, b: 255, alpha: 1 },
    })
    .toBuffer();

  // Limita largura a MAX_WIDTH
  buf = await sharp(buf)
    .resize({ width: MAX_WIDTH, withoutEnlargement: true })
    .png({ compressionLevel: 9 })
    .toBuffer();

  return buf;
}

async function processFile(filename) {
  const pngPath = resolve(DIR, filename);
  const webpPath = pngPath.replace('.png', '.webp');

  const originalBuf = readFileSync(pngPath);
  const originalKB = Math.round(originalBuf.length / 1024);
  const originalMeta = await sharp(originalBuf).metadata();

  const trimmedBuf = await trimToContent(originalBuf);
  const trimmedMeta = await sharp(trimmedBuf).metadata();
  const trimmedKB = Math.round(trimmedBuf.length / 1024);

  // Salva PNG recortado (sobrescreve)
  writeFileSync(pngPath, trimmedBuf);

  // Gera e salva WebP
  const webpBuf = await sharp(trimmedBuf)
    .webp({ quality: WEBP_QUALITY })
    .toBuffer();
  const webpKB = Math.round(webpBuf.length / 1024);
  writeFileSync(webpPath, webpBuf);

  return {
    file: filename.replace('.png', ''),
    'antes (KB)': originalKB,
    'PNG recortado (KB)': trimmedKB,
    'WebP (KB)': webpKB,
    'antes (px)': `${originalMeta.width}×${originalMeta.height}`,
    'depois (px)': `${trimmedMeta.width}×${trimmedMeta.height}`,
    'redução WebP': `${Math.round((1 - webpKB / originalKB) * 100)}%`,
  };
}

async function main() {
  console.log('\nProcessando imagens...\n');
  const results = [];

  for (const file of FILES) {
    process.stdout.write(`  ${file.replace('.png', '')} ... `);
    try {
      const r = await processFile(file);
      console.log(`OK  ${r['depois (px)']}`);
      results.push(r);
    } catch (e) {
      console.log(`ERRO: ${e.message}`);
    }
  }

  console.log('\n--- Resultados ---\n');
  console.table(results);

  const totalWebP = results.reduce((s, r) => s + r['WebP (KB)'], 0);
  const totalPng  = results.reduce((s, r) => s + r['PNG recortado (KB)'], 0);
  console.log(`Total PNG recortado : ${totalPng} KB`);
  console.log(`Total WebP          : ${totalWebP} KB (servido para 99% dos users)`);
}

main().catch(e => { console.error(e); process.exit(1); });
