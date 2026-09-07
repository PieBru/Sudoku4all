// tests/readability.test.mjs — the language-budget gate (spec 000 FR-008).
// Kid pages (chapters 00/01 + their index rows): every sentence ≤ 15 words,
// page average ≤ 10, banned jargon only inside "For grown-ups" asides.
// Plain pages (chapters 02+ and the rest of the index): every sentence ≤ 25 words.
// ponytail: naive sentence splitter (block tags → boundaries) per proposal §7 —
// upgrade only if it misfires on real content.
import { readFileSync, readdirSync } from "node:fs";
import { join } from "node:path";
import { fileURLToPath } from "node:url";

const dir = fileURLToPath(new URL("../lessons/", import.meta.url));
const pages = readdirSync(dir).filter((f) => f.endsWith(".html"));
const BANNED = [
  /\bcand(idates?)?\b/i,
  /\beliminat/i,
  /\bconstraints?\b/i,
  /\bsubsets?\b/i,
  /\bintersections?\b/i,
  /\bbivalue\b/i,
  /\bbilocation\b/i,
  /\bchains?\b/i,
  /\bfish\b/i,
  /\bwings?\b/i,
  /\buniqueness\b/i,
  /pencil[- ]?marks?/i,
];
const fails = [];
const complain = (page, why) => fails.push(`${page}: ${why}`);

function toText(html, { stripAsides = false } = {}) {
  let t = html.replace(/<script[\s\S]*?<\/script>/gi, " ");
  t = t.replace(/<style[\s\S]*?<\/style>/gi, " ");
  if (stripAsides) t = t.replace(/<aside[\s\S]*?<\/aside>/gi, " ");
  t = t.replace(/<\/(p|h1|h2|h3|h4|li|figcaption|td|th|div|button|summary|strong|em|a)>/gi, ".\n");
  t = t.replace(/<[^>]+>/g, " ");
  t = t
    .replace(/&amp;/g, "&")
    .replace(/&lt;/g, "<")
    .replace(/&gt;/g, ">")
    .replace(/&quot;/g, '"')
    .replace(/&#(\d+);/g, (_, d) => String.fromCharCode(+d));
  return t;
}

function sentences(text) {
  return text
    .split(/\n+|(?<=[.!?])\s+/)
    .map((s) => s.replace(/\s+/g, " ").trim())
    .filter((s) => /[A-Za-z]/.test(s));
}

const words = (s) => s.split(/\s+/).filter(Boolean).length;

function checkKid(page, text) {
  const sents = sentences(text);
  for (const s of sents) {
    const n = words(s);
    if (n > 15) complain(page, `kid sentence ${n} words (>15): "${s}"`);
    for (const re of BANNED)
      if (re.test(s)) complain(page, `kid jargon "${re}" in: "${s}"`);
  }
  if (sents.length) {
    const avg = sents.reduce((a, s) => a + words(s), 0) / sents.length;
    if (avg > 10) complain(page, `kid average ${avg.toFixed(1)} words (>10)`);
  }
}

function checkPlain(page, text) {
  for (const s of sentences(text))
    if (words(s) > 25) complain(page, `plain sentence ${words(s)} words (>25): "${s}"`);
}

for (const page of pages) {
  const html = readFileSync(join(dir, page), "utf8");
  const isKidPage = /^0[01]-/.test(page);
  if (isKidPage) checkKid(page, toText(html, { stripAsides: true }));
  else if (page === "index.html") {
    // kid rules for the rows describing chapters 00 and 01; plain for the rest
    const rows = html.match(/<li data-chapter="\d\d">[\s\S]*?<\/li>/g) || [];
    for (const row of rows) {
      const n = row.match(/data-chapter="(\d\d)"/)[1];
      if (n === "00" || n === "01") checkKid(page, toText(row));
    }
    checkPlain(page, toText(html.replace(/<li data-chapter="\d\d">[\s\S]*?<\/li>/g, " ")));
  } else checkPlain(page, toText(html));
}

if (fails.length) {
  console.error(`readability gate: ${fails.length} violation(s)`);
  for (const f of fails) console.error("  FAIL | " + f);
  process.exit(1);
}
console.log(`readability gate: all pass (${pages.length} page(s))`);
