// Entry point for the news-image-20261126 make.fun submission.
// Renders the front page with the Python generator and writes the
// result to MAKEFUN_OUTPUT_DIR (or ./out when unset).
import { execFileSync } from "node:child_process";
import { createHash } from "node:crypto";
import { existsSync, mkdirSync, readFileSync, statSync } from "node:fs";
import { join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const here = resolve(fileURLToPath(new URL(".", import.meta.url)));
const outDir = resolve(process.env.MAKEFUN_OUTPUT_DIR ?? join(here, "out"));
mkdirSync(outDir, { recursive: true });

const outPath = join(outDir, "entry.png");
execFileSync("python3", [join(here, "generate_image.py"), outPath], {
  stdio: "inherit",
  env: { ...process.env, PYTHONHASHSEED: "0" },
});

if (!existsSync(outPath)) {
  throw new Error(`generator did not produce ${outPath}`);
}

// Verify the output is really a 1024x1024 PNG before reporting success:
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
const sha256 = createHash("sha256").update(bytes).digest("hex");
console.log(`entry.png: ${statSync(outPath).size} bytes, ${width}x${height}, sha256 ${sha256} -> ${outPath}`);
