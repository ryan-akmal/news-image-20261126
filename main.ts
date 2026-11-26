// Entry point for the news-image-20261126 make.fun submission.
//
// The front page is rendered ahead of time and committed as entry.png.
// At grade time this program only copies that committed file to
// MAKEFUN_OUTPUT_DIR (or ./out when unset) and verifies it — it never
// runs the generator, so it needs nothing but node and the repo itself.
import { createHash } from "node:crypto";
import {
  copyFileSync,
  existsSync,
  mkdirSync,
  readFileSync,
  statSync,
} from "node:fs";
import { join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const here = resolve(fileURLToPath(new URL(".", import.meta.url)));
const srcPath = join(here, "entry.png");
if (!existsSync(srcPath)) {
  throw new Error(
    `committed entry.png not found next to main.ts: ${srcPath} (the grader copies the whole repo to /bot, so this file must be committed)`,
  );
}

const outDir = resolve(process.env.MAKEFUN_OUTPUT_DIR ?? join(here, "out"));
mkdirSync(outDir, { recursive: true });

const outPath = join(outDir, "entry.png");
copyFileSync(srcPath, outPath);

// Verify the output is really the committed 1024x1024 PNG, under 1 MiB:
// PNG signature is 8 bytes, then the IHDR chunk holds width/height
// as big-endian uint32 at offsets 16 and 20.
const bytes = readFileSync(outPath);
const isPng = bytes.subarray(0, 8).equals(
  Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]),
);
const width = bytes.readUInt32BE(16);
const height = bytes.readUInt32BE(20);
if (!isPng || width !== 1024 || height !== 1024) {
  throw new Error(`bad output: png=${isPng} ${width}x${height}, want 1024x1024`);
}
if (bytes.length > 1024 * 1024) {
  throw new Error(`output too large: ${bytes.length} bytes, limit 1 MiB`);
}
const sha256 = createHash("sha256").update(bytes).digest("hex");
// The copy must be byte-identical to the committed file: hash the source
// too and refuse to report success on a partial or corrupted copy.
const srcSha256 = createHash("sha256")
  .update(readFileSync(srcPath))
  .digest("hex");
if (srcSha256 !== sha256) {
  throw new Error(
    `copy mismatch: source sha256 ${srcSha256} != output sha256 ${sha256}`,
  );
}
console.log(
  `entry.png: ${statSync(outPath).size} bytes, ${width}x${height}, sha256 ${sha256} -> ${outPath}`,
);
