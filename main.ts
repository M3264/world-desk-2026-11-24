import { mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { resolve } from 'node:path';

// The editor rasterizes the finished plate before committing. The judging
// container needs neither fonts nor a renderer, so its output cannot vary.
const plate = readFileSync(new URL('./entry.png', import.meta.url));
const limit = 1024 * 1024;
if (plate.length > limit || plate.subarray(0, 8).toString('hex') !== '89504e470d0a1a0a') {
  throw new Error('Expected a PNG plate no greater than 1 MiB');
}
const outputDirectory = resolve(process.env.MAKEFUN_OUTPUT_DIR ?? '/output');
mkdirSync(outputDirectory, { recursive: true });
writeFileSync(resolve(outputDirectory, 'entry.png'), plate);
