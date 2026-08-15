const preview = document.getElementById('preview');
const btnStart = document.getElementById('btn-start');
const btnStop = document.getElementById('btn-stop');
const camStatus = document.getElementById('cam-status');
const manualBarcode = document.getElementById('manual-barcode');
const btnLookup = document.getElementById('btn-lookup');
const resultDiv = document.getElementById('result');

let stream = null;
let scanInterval = null;

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
        resultDiv.innerHTML = `
          <div class="alert alert-success">
            <strong>${p.name}</strong><br>
            <span class="text-muted">${p.brand || ''} ${p.category ? '· ' + p.category : ''}</span><br>
            <span class="small font-monospace">${p.barcode}</span><br>
            <a href="/products/${encodeURIComponent(p.barcode)}" class="btn btn-sm btn-success mt-2">View Details</a>
          </div>`;
      } else {
        resultDiv.innerHTML = `
          <div class="alert alert-warning">
            Barcode <code>${barcode}</code> not found in database.<br>
            <a href="/products/add?barcode=${encodeURIComponent(barcode)}" class="btn btn-sm btn-outline-success mt-2">Add this product</a>
          </div>`;
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
