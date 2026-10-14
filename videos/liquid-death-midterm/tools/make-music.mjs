// Deterministic procedural music bed + SFX for the Liquid Death midterm film.
// Output: assets/music.wav (48 kHz, 16-bit stereo, 385 s).
// Restrained by design: it must sit under a live voice.
import { writeFileSync } from "node:fs";

const SR = 48000;
const DUR = 385;
const N = SR * DUR;
const L = new Float32Array(N);
const R = new Float32Array(N);

// seeded PRNG (mulberry32) so every build is identical
let seed = 0x1d0c0de;
function rnd() {
  seed |= 0;
  seed = (seed + 0x6d2b79f5) | 0;
  let t = Math.imul(seed ^ (seed >>> 15), 1 | seed);
  t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
  return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
}

const TAU = Math.PI * 2;
const lerp = (a, b, x) => a + (b - a) * x;
const smooth = (x) => (x <= 0 ? 0 : x >= 1 ? 1 : x * x * (3 - 2 * x));

// Section energy envelope (time → level), piecewise smooth
const keys = [
  [0, 0.0], [2.5, 0.18], [8, 0.16], [14, 0.32], [34.5, 0.34], [35.5, 0.26],
  [118, 0.28], [120, 0.42], [178, 0.46], [181, 0.28], [272, 0.28], [276, 0.14],
  [338, 0.14], [342, 0.3], [362, 0.36], [369, 0.06], [372, 0.05], [385, 0.0],
];
function env(t) {
  for (let i = 0; i < keys.length - 1; i++) {
    const [t0, v0] = keys[i];
    const [t1, v1] = keys[i + 1];
    if (t >= t0 && t <= t1) return lerp(v0, v1, smooth((t - t0) / (t1 - t0)));
  }
  return 0;
}

function add(i, l, r) {
  if (i >= 0 && i < N) {
    L[i] += l;
    R[i] += r;
  }
}

// 1) Drone: A1 + E2 with a few soft harmonics, slow beating and stereo detune
{
  let lpL = 0;
  let lpR = 0;
  for (let i = 0; i < N; i++) {
    const t = i / SR;
    const e = env(t);
    if (e <= 0) continue;
    const breathe = 0.75 + 0.25 * Math.sin(TAU * 0.05 * t);
    let sL = 0;
    let sR = 0;
    const freqs = [55, 82.41, 110, 164.8];
    const amps = [1, 0.55, 0.35, 0.12];
    for (let k = 0; k < freqs.length; k++) {
      sL += amps[k] * Math.sin(TAU * freqs[k] * t + 0.3 * Math.sin(TAU * 0.07 * t));
      sR += amps[k] * Math.sin(TAU * (freqs[k] * 1.003) * t + 0.3 * Math.sin(TAU * 0.06 * t + 1));
    }
    // filtered noise air
    const n = rnd() * 2 - 1;
    lpL += 0.02 * (n - lpL);
    lpR += 0.02 * ((rnd() * 2 - 1) - lpR);
    add(i, e * breathe * (0.22 * sL + 0.9 * lpL), e * breathe * (0.22 * sR + 0.9 * lpR));
  }
}

// 2) Pulse: soft ticks under scenes 2–3 and 5–6; full kick + riff in scene 4
function kick(t0, gain) {
  const i0 = Math.floor(t0 * SR);
  const len = Math.floor(0.45 * SR);
  let ph = 0;
  for (let j = 0; j < len; j++) {
    const t = j / SR;
    const f = 45 + 75 * Math.exp(-t * 28);
    ph += TAU * f / SR;
    const a = gain * Math.exp(-t * 9);
    const s = a * Math.sin(ph);
    add(i0 + j, s, s);
  }
}
function tick(t0, gain) {
  const i0 = Math.floor(t0 * SR);
  const len = Math.floor(0.05 * SR);
  let hp = 0;
  let prev = 0;
  for (let j = 0; j < len; j++) {
    const n = rnd() * 2 - 1;
    hp = 0.6 * (hp + n - prev);
    prev = n;
    const a = gain * Math.exp(-(j / SR) * 90);
    add(i0 + j, a * hp, a * hp * 0.8);
  }
}
// scenes 2–3 (35–120) and 5–6 (180–275): quiet tick at 80 bpm
for (const [a, b, g] of [[36, 119, 0.05], [181, 274, 0.045]]) {
  for (let t = a; t < b; t += 60 / 80) tick(t, g);
}
// scene 4 (120–180): 96 bpm kick + offbeat ticks
{
  const beat = 60 / 96;
  for (let t = 123.5, k = 0; t < 179; t += beat, k++) {
    kick(t, k % 4 === 0 ? 0.5 : 0.36);
    tick(t + beat / 2, 0.09);
  }
  // distorted low riff: E1 E1 G1 A1 per bar
  const notes = [41.2, 41.2, 49.0, 55.0];
  let ph = 0;
  for (let t = 123.5; t < 179; t += beat) {
    const bar = Math.floor((t - 123.5) / beat) % 4;
    const f = notes[bar];
    const i0 = Math.floor(t * SR);
    const len = Math.floor(beat * 0.9 * SR);
    for (let j = 0; j < len; j++) {
      ph += f / SR;
      const saw = 2 * (ph - Math.floor(ph)) - 1;
      const a = 0.11 * Math.min(1, j / 400) * Math.exp(-(j / SR) * 2.2);
      const s = a * Math.tanh(3.2 * saw);
      add(i0 + j, s, s * 0.92);
    }
  }
}

// 3) Accents
function metalHit(t0, gain) {
  const i0 = Math.floor(t0 * SR);
  const len = Math.floor(3.2 * SR);
  const partials = [[523, 1], [1307, 0.6], [2210, 0.35], [3170, 0.22], [4430, 0.12]];
  for (let j = 0; j < len; j++) {
    const t = j / SR;
    let s = 0;
    for (const [f, a] of partials) s += a * Math.sin(TAU * f * t) * Math.exp(-t * (1.6 + f / 2600));
    const boom = Math.sin(TAU * (38 + 30 * Math.exp(-t * 10)) * t) * Math.exp(-t * 3);
    const v = gain * (0.16 * s + 0.6 * boom);
    add(i0 + j, v, v * 0.9);
  }
}
function whoosh(t0, dur, gain) {
  const i0 = Math.floor(t0 * SR);
  const len = Math.floor(dur * SR);
  let lp = 0;
  for (let j = 0; j < len; j++) {
    const x = j / len;
    const cutoff = 0.01 + 0.2 * Math.sin(Math.PI * x);
    lp += cutoff * ((rnd() * 2 - 1) - lp);
    const a = gain * Math.sin(Math.PI * x) ** 2;
    add(i0 + j, a * lp * (1 - x * 0.5), a * lp * (0.5 + x * 0.5));
  }
}
function glitch(t0, gain) {
  for (let k = 0; k < 6; k++) {
    const i0 = Math.floor((t0 + k * 0.06) * SR);
    const f = [880, 1320, 660, 1760, 990, 1480][k];
    const len = Math.floor(0.035 * SR);
    for (let j = 0; j < len; j++) {
      const sq = Math.sin(TAU * f * (j / SR)) > 0 ? 1 : -1;
      add(i0 + j, gain * sq * (k % 2 ? 0.6 : 1), gain * sq * (k % 2 ? 1 : 0.6));
    }
  }
}
function bell(t0, f, gain) {
  const i0 = Math.floor(t0 * SR);
  const len = Math.floor(5 * SR);
  for (let j = 0; j < len; j++) {
    const t = j / SR;
    const s = Math.sin(TAU * f * t) + 0.3 * Math.sin(TAU * f * 2.01 * t) + 0.12 * Math.sin(TAU * f * 3.02 * t);
    const v = gain * s * Math.exp(-t * 0.9) * Math.min(1, j / 600);
    add(i0 + j, v, v);
  }
}

metalHit(14.0, 0.9); // cut to the can
metalHit(24.0, 0.7); // question slams in
glitch(33.6, 0.05); // glitch 1
whoosh(34.3, 1.6, 0.5); // → scene 2
whoosh(74.2, 1.8, 0.45); // → scene 3
metalHit(76.0, 0.35); // spotlight opens
glitch(120.05, 0.06); // glitch 2
whoosh(119.2, 1.2, 0.5);
metalHit(134.4, 0.6); // MURDER YOUR THIRST
for (const t of [144.4, 148.3, 152.2, 156.1]) tick(t, 0.25); // montage hard cuts
whoosh(179.0, 1.6, 0.45); // → scene 5
whoosh(229.2, 1.6, 0.4); // → scene 6
bell(276.2, 220, 0.05); // questions, restrained
bell(283.0, 196, 0.045);
bell(289.8, 174.6, 0.045);
bell(333.4, 220, 0.04); // measured conclusion
metalHit(357.0, 0.55); // IT SELLS MEANING
bell(362.0, 110, 0.06); // final question

// 4) Normalize to -6 dBFS peak, soft-clip safety, write WAV
let peak = 0;
for (let i = 0; i < N; i++) peak = Math.max(peak, Math.abs(L[i]), Math.abs(R[i]));
const g = 0.5 / peak;
const buf = Buffer.alloc(44 + N * 4);
buf.write("RIFF", 0);
buf.writeUInt32LE(36 + N * 4, 4);
buf.write("WAVE", 8);
buf.write("fmt ", 12);
buf.writeUInt32LE(16, 16);
buf.writeUInt16LE(1, 20);
buf.writeUInt16LE(2, 22);
buf.writeUInt32LE(SR, 24);
buf.writeUInt32LE(SR * 4, 28);
buf.writeUInt16LE(4, 32);
buf.writeUInt16LE(16, 34);
buf.write("data", 36);
buf.writeUInt32LE(N * 4, 40);
for (let i = 0; i < N; i++) {
  buf.writeInt16LE(Math.round(32767 * Math.tanh(L[i] * g)), 44 + i * 4);
  buf.writeInt16LE(Math.round(32767 * Math.tanh(R[i] * g)), 46 + i * 4);
}
writeFileSync(new URL("../assets/music.wav", import.meta.url), buf);
console.log("wrote assets/music.wav", DUR, "s, gain", g.toFixed(3));
