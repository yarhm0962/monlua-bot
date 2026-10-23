'use strict';

const { execFileSync } = require('child_process');

let _cachedPython = null;

function getPythonBin() {
  if (_cachedPython) return _cachedPython;
  if (process.env.PYTHON_BIN) {
    _cachedPython = process.env.PYTHON_BIN;
    return _cachedPython;
  }
  // The symbolic lifter is CPU-bound pure Python. Prefer PyPy when it is
  // installed: its JIT substantially reduces large Luraph v15.1 lift times.
  // Keep the explicit PYTHON_BIN override authoritative, and fall back to
  // the platform's normal Python if PyPy is unavailable.
  const candidates = process.platform === 'win32'
    ? ['pypy3', 'pypy', 'python', 'py', 'python3']
    : ['pypy3', 'pypy', 'python3', 'python'];

  for (const cmd of candidates) {
    try {
      execFileSync(cmd, ['--version'], { stdio: 'ignore' });
      _cachedPython = cmd;
      return cmd;
    } catch {}
  }
  throw new Error('Python not found. Please install Python 3.10+ or set the PYTHON_BIN environment variable.');
}

module.exports = { getPythonBin };
