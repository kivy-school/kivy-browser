// pyshader.wasm in the page: PyShader source + options -> Kivy .glsl
const WASM = new URL("../pyshader/pyshader.wasm", import.meta.url);
const encoder = new TextEncoder(), decoder = new TextDecoder();

export class CompileError extends Error {
  constructor(text) {
    const m = /^(?:(.+?), )?line (\d+): ([\s\S]*)$/.exec(text.trim());
    super(m ? m[3] : text.trim());
    this.file = m?.[1] ?? null;
    this.line = m ? Number(m[2]) : Number(/ at line (\d+)/.exec(text)?.[1]) || null;
  }
}

function wasi(memory) {
  const view = () => new DataView(memory().buffer);
  const imports = {
    args_sizes_get: (c, s) => { view().setUint32(c, 0, true); view().setUint32(s, 0, true); return 0; },
    environ_sizes_get: (c, s) => { view().setUint32(c, 0, true); view().setUint32(s, 0, true); return 0; },
    args_get: () => 0,
    environ_get: () => 0,
    clock_res_get: (id, out) => { view().setBigUint64(out, 1000n, true); return 0; },
    clock_time_get: (id, p, out) => { view().setBigUint64(out, BigInt(Date.now()) * 1000000n, true); return 0; },
    fd_prestat_get: () => 8,
    fd_prestat_dir_name: () => 8,
    fd_fdstat_get: (fd, out) => {
      if (fd > 2) return 8;
      const v = view();
      v.setUint8(out, 2);
      v.setUint16(out + 2, 0, true);
      v.setBigUint64(out + 8, 0n, true);
      v.setBigUint64(out + 16, 0n, true);
      return 0;
    },
    fd_close: () => 0,
    sched_yield: () => 0,
    fd_write: (fd, iovs, n, written) => {
      const v = view();
      let total = 0;
      for (let i = 0; i < n; i++) total += v.getUint32(iovs + i * 8 + 4, true);
      v.setUint32(written, total, true);
      return 0;
    },
    random_get: (ptr, len) => { crypto.getRandomValues(new Uint8Array(memory().buffer, ptr, len)); return 0; },
    proc_exit: (code) => { throw new Error(`pyshader.wasm exited (${code})`); },
  };
  return new Proxy(imports, { get: (t, k) => t[k] ?? (() => 52) });
}

let exportsPromise;
function load() {
  exportsPromise ??= (async () => {
    let ex;
    const { instance } = await WebAssembly.instantiateStreaming(fetch(WASM), {
      wasi_snapshot_preview1: wasi(() => ex.memory),
    });
    ex = instance.exports;
    ex._initialize();
    return ex;
  })();
  return exportsPromise;
}

function put(ex, bytes) {
  if (!bytes.length) return 0;
  const ptr = ex.pyshader_alloc(bytes.length);
  new Uint8Array(ex.memory.buffer, ptr, bytes.length).set(bytes);
  return ptr;
}

export async function compile(source, options) {
  const ex = await load();
  ex.pyshader_clear_modules();
  const src = encoder.encode(source), opt = encoder.encode(options);
  const s = put(ex, src), o = put(ex, opt);
  const failed = ex.pyshader_compile(s, src.length, o, opt.length);
  if (s) ex.pyshader_dealloc(s, src.length);
  if (o) ex.pyshader_dealloc(o, opt.length);
  const len = ex.pyshader_result_len();
  const text = len ? decoder.decode(new Uint8Array(ex.memory.buffer, ex.pyshader_result_ptr(), len)) : "";
  ex.pyshader_result_free();
  if (failed) throw new CompileError(text);
  return text;
}
