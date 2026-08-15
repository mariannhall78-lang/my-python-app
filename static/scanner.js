const preview = document.getElementById('preview');
const btnStart = document.getElementById('btn-start');
const btnStop = document.getElementById('btn-stop');
const camStatus = document.getElementById('cam-status');
const manualBarcode = document.getElementById('manual-barcode');
const btnLookup = document.getElementById('btn-lookup');
const resultDiv = document.getElementById('result');

let stream = null;
let scanInterval = null;

function escHtml(str) {
  return String(str ?? '').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
}

async function lookupBarcode(barcode) {
  barcode = barcode.trim();
  if (!barcode) return;
  resultDiv.innerHTML = '<div class="text-muted small">Looking up…</div>';
  try {
    const res = await fetch(`/api/barcode/${encodeURIComponent(barcode)}`);
    if (res.ok) {
      const data = await res.json();
      if (data.found) {
        const p = data.product;
        const detail = document.createElement('div');
        detail.className = 'alert alert-success';
        detail.innerHTML = `<strong>${escHtml(p.name)}</strong><br>
          <span class="text-muted">${escHtml(p.brand || '')} ${p.category ? '· ' + escHtml(p.category) : ''}</span><br>
          <span class="small font-monospace">${escHtml(p.barcode)}</span>`;
        const link = document.createElement('a');
        link.href = `/products/${encodeURIComponent(p.barcode)}`;
        link.className = 'btn btn-sm btn-success mt-2';
        link.textContent = 'View Details';
        detail.appendChild(link);
        resultDiv.replaceChildren(detail);
      } else {
        const warn = document.createElement('div');
        warn.className = 'alert alert-warning';
        warn.innerHTML = `Barcode <code>${escHtml(barcode)}</code> not found in database.`;
        const link = document.createElement('a');
        link.href = `/products/add?barcode=${encodeURIComponent(barcode)}`;
        link.className = 'btn btn-sm btn-outline-success mt-2';
        link.textContent = 'Add this product';
        warn.appendChild(link);
        resultDiv.replaceChildren(warn);
      }
    }
  } catch (e) {
    resultDiv.innerHTML = '<div class="alert alert-danger">Error looking up barcode.</div>';
  }
}

btnLookup.addEventListener('click', () => lookupBarcode(manualBarcode.value));
manualBarcode.addEventListener('keydown', e => { if (e.key === 'Enter') lookupBarcode(manualBarcode.value); });

btnStart.addEventListener('click', async () => {
  if (!('BarcodeDetector' in window)) {
    camStatus.textContent = 'BarcodeDetector API not supported in this browser. Use manual lookup.';
    return;
  }
  try {
    stream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: 'environment' } });
    preview.srcObject = stream;
    btnStart.disabled = true;
    btnStop.disabled = false;
    camStatus.textContent = 'Scanning…';
    const detector = new BarcodeDetector({ formats: ['ean_13', 'ean_8', 'upc_a', 'upc_e', 'code_128', 'qr_code'] });
    scanInterval = setInterval(async () => {
      try {
        const barcodes = await detector.detect(preview);
        if (barcodes.length > 0) {
          const value = barcodes[0].rawValue;
          camStatus.textContent = `Detected: ${value}`;
          manualBarcode.value = value;
          await lookupBarcode(value);
        }
      } catch (_) {}
    }, 800);
  } catch (e) {
    camStatus.textContent = `Camera error: ${e.message}`;
  }
});

btnStop.addEventListener('click', () => {
  if (scanInterval) { clearInterval(scanInterval); scanInterval = null; }
  if (stream) { stream.getTracks().forEach(t => t.stop()); stream = null; }
  preview.srcObject = null;
  btnStart.disabled = false;
  btnStop.disabled = true;
  camStatus.textContent = 'Camera stopped.';
});
