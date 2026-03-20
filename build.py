"""
Cach dung:
  python build.py "path/to/letter.docx" "https://script.google.com/macros/s/.../exec"

Sau khi chay xong, deploy len GitHub Pages:
  git add index.html && git commit -m "update letter" && git push
"""

import base64, sys, os

if len(sys.argv) < 3:
    print('Cach dung: python build.py <file.docx> <apps_script_url>')
    print('  file.docx        - File Word noi dung thu')
    print('  apps_script_url  - URL cua Google Apps Script')
    sys.exit(1)

docx_path = sys.argv[1]
apps_url = sys.argv[2]

if not os.path.exists(docx_path):
    print(f'Khong tim thay file: {docx_path}')
    sys.exit(1)

with open(docx_path, 'rb') as f:
    b64 = base64.b64encode(f.read()).decode()

HTML = r"""<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Letter of Recommendation - Signature</title>
<script src="https://cdnjs.cloudflare.com/ajax/libs/mammoth/1.8.0/mammoth.browser.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/signature_pad/4.1.7/signature_pad.umd.min.js"></script>
<style>
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: Arial, sans-serif; background: #f0f2f5; padding: 20px; color: #222; }
.container { max-width: 820px; margin: 0 auto; }
.section-title {
  font-size: 12px; font-weight: 700; color: #555; text-transform: uppercase;
  letter-spacing: 0.8px; margin-bottom: 10px; padding-bottom: 6px;
  border-bottom: 2px solid #d0d0d0; margin-top: 28px;
}
.section-title:first-child { margin-top: 0; }
.doc-card {
  background: #fff; border-radius: 10px; box-shadow: 0 2px 12px rgba(0,0,0,0.10);
  padding: 48px 56px; font-family: "Times New Roman", Times, serif;
  font-size: 12pt; line-height: 1.7;
}
.doc-card p { text-align: justify; margin-bottom: 14px; }
.doc-card h1, .doc-card h2, .doc-card h3 { margin-bottom: 16px; }
.doc-loading { text-align: center; color: #999; padding: 40px; font-style: italic; }
.form-card {
  background: #fff; border-radius: 10px; box-shadow: 0 2px 12px rgba(0,0,0,0.10);
  padding: 24px 28px;
}
.sig-wrapper {
  position: relative; border: 2px dashed #bbb; border-radius: 8px;
  background: #fafafa; margin-bottom: 10px; overflow: hidden;
}
#signature-canvas { display: block; width: 100%; height: 200px; cursor: crosshair; touch-action: none; }
.sig-placeholder {
  position: absolute; top: 50%; left: 50%; transform: translate(-50%,-50%);
  color: #bbb; font-size: 14px; pointer-events: none; text-align: center;
  user-select: none; line-height: 1.5;
}
.sig-actions { margin-bottom: 4px; }
.btn-clear {
  background: #f3f3f3; border: 1px solid #ccc; border-radius: 6px;
  padding: 6px 14px; font-size: 13px; cursor: pointer; color: #555;
}
.btn-clear:hover { background: #e8e8e8; }
.input-group { margin-bottom: 18px; }
.input-group:last-child { margin-bottom: 0; }
.input-label { display: block; font-size: 13px; font-weight: 600; color: #444; margin-bottom: 6px; }
.input-field {
  width: 100%; padding: 10px 14px; font-size: 14px;
  border: 1.5px solid #d0d0d0; border-radius: 8px; outline: none;
  transition: border-color 0.2s; font-family: Arial, sans-serif;
}
.input-field:focus { border-color: #2563eb; }
.btn-submit {
  display: block; width: 100%; padding: 14px; margin-top: 20px;
  background: linear-gradient(135deg, #2563eb, #1d4ed8);
  color: #fff; font-size: 16px; font-weight: 700; border: none;
  border-radius: 10px; cursor: pointer; letter-spacing: 0.5px;
  transition: opacity 0.2s, transform 0.1s;
}
.btn-submit:hover { opacity: 0.92; transform: translateY(-1px); }
.btn-submit:active { transform: translateY(0); }
.btn-submit:disabled { opacity: 0.6; cursor: not-allowed; transform: none; }
.error-msg { color: #dc2626; font-size: 12px; margin-top: 6px; display: none; }
.success-msg {
  text-align: center; margin-top: 20px; padding: 20px; background: #dcfce7;
  border-radius: 10px; display: none;
}
.success-msg h3 { color: #16a34a; margin-bottom: 8px; }
.success-msg p { color: #166534; font-size: 14px; }
@media (max-width: 600px) {
  .doc-card { padding: 24px 16px; font-size: 11pt; }
  .form-card { padding: 18px 16px; }
}
</style>
</head>
<body>
<div class="container">

<div class="section-title">N&#7897;i dung th&#432;</div>
<div class="doc-card" id="doc-content">
  <div class="doc-loading">&#272;ang t&#7843;i n&#7897;i dung th&#432;...</div>
</div>

<div class="section-title">Ch&#7919; k&#253;</div>
<div class="form-card">
  <div class="sig-wrapper">
    <canvas id="signature-canvas"></canvas>
    <div class="sig-placeholder" id="sig-placeholder">
      K&#253; t&#234;n t&#7841;i &#273;&#226;y<br>
      <small style="font-size:12px;">(d&#249;ng chu&#7897;t ho&#7863;c ng&#243;n tay tr&#234;n m&#224;n h&#236;nh c&#7843;m &#7913;ng)</small>
    </div>
  </div>
  <div class="sig-actions">
    <button class="btn-clear" onclick="clearSignature()">&#10005; X&#243;a ch&#7919; k&#253;</button>
  </div>
  <div class="error-msg" id="sig-error">Vui l&#242;ng k&#253; t&#234;n.</div>
</div>

<div class="section-title">Th&#244;ng tin ng&#432;&#7901;i k&#253;</div>
<div class="form-card">
  <div class="input-group">
    <label class="input-label" for="manager-name">H&#7885; v&#224; t&#234;n</label>
    <input class="input-field" type="text" id="manager-name" placeholder="Nh&#7853;p h&#7885; v&#224; t&#234;n &#273;&#7847;y &#273;&#7911;...">
    <div class="error-msg" id="name-error">Vui l&#242;ng nh&#7853;p h&#7885; v&#224; t&#234;n.</div>
  </div>
  <div class="input-group">
    <label class="input-label" for="email-input">Email</label>
    <input class="input-field" type="email" id="email-input" placeholder="email@example.com">
    <div class="error-msg" id="email-error">Vui l&#242;ng nh&#7853;p email h&#7907;p l&#7879;.</div>
  </div>
  <div class="input-group">
    <label class="input-label" for="phone-input">S&#7889; &#273;i&#7879;n tho&#7841;i</label>
    <input class="input-field" type="tel" id="phone-input" placeholder="+84 ...">
    <div class="error-msg" id="phone-error">Vui l&#242;ng nh&#7853;p s&#7889; &#273;i&#7879;n tho&#7841;i.</div>
  </div>
</div>

<button class="btn-submit" id="btn-submit" onclick="handleSubmit()">
  G&#7917;i th&#244;ng tin
</button>

<div class="success-msg" id="success-msg">
  <h3>&#10003; G&#7917;i th&#224;nh c&#244;ng!</h3>
  <p>Ch&#7919; k&#253; v&#224; th&#244;ng tin c&#7911;a b&#7841;n &#273;&#227; &#273;&#432;&#7907;c l&#432;u l&#7841;i.<br>C&#7843;m &#417;n b&#7841;n!</p>
</div>

</div>
<script>
// === Config ===
var TEMPLATE_B64 = '__TEMPLATE_B64__';
var APPS_SCRIPT_URL = '__APPS_SCRIPT_URL__';

// === Render DOCX via mammoth.js ===
function base64ToArrayBuffer(b64) {
  var bstr = atob(b64);
  var u8 = new Uint8Array(bstr.length);
  for (var i = 0; i < bstr.length; i++) u8[i] = bstr.charCodeAt(i);
  return u8.buffer;
}

mammoth.convertToHtml({arrayBuffer: base64ToArrayBuffer(TEMPLATE_B64)})
  .then(function(result) {
    document.getElementById('doc-content').innerHTML = result.value;
  })
  .catch(function(err) {
    document.getElementById('doc-content').innerHTML =
      '<p style="color:red;">Loi tai noi dung: ' + err.message + '</p>';
  });

// === Signature Pad ===
var canvas = document.getElementById('signature-canvas');
var signaturePad = new SignaturePad(canvas, {
  backgroundColor: 'rgba(255,255,255,0)',
  penColor: '#000033',
  minWidth: 1,
  maxWidth: 2.5
});
function resizeCanvas() {
  var ratio = Math.max(window.devicePixelRatio || 1, 1);
  var rect = canvas.getBoundingClientRect();
  canvas.width = rect.width * ratio;
  canvas.height = rect.height * ratio;
  canvas.getContext('2d').scale(ratio, ratio);
  signaturePad.clear();
}
window.addEventListener('resize', resizeCanvas);
resizeCanvas();
signaturePad.addEventListener('beginStroke', function() {
  document.getElementById('sig-placeholder').style.display = 'none';
});
function clearSignature() {
  signaturePad.clear();
  document.getElementById('sig-placeholder').style.display = '';
}

// === Validation ===
function validate() {
  var ok = true;
  function check(fail, id) {
    var el = document.getElementById(id);
    if (fail) { el.style.display = 'block'; ok = false; }
    else { el.style.display = 'none'; }
  }
  check(signaturePad.isEmpty(), 'sig-error');
  check(!document.getElementById('manager-name').value.trim(), 'name-error');
  var em = document.getElementById('email-input').value.trim();
  check(!em || em.indexOf('@') === -1, 'email-error');
  check(!document.getElementById('phone-input').value.trim(), 'phone-error');
  return ok;
}

// === Submit ===
async function handleSubmit() {
  if (!validate()) return;
  if (!APPS_SCRIPT_URL) {
    alert('Chua cau hinh Apps Script URL. Vui long lien he nguoi tao trang.');
    return;
  }
  var btn = document.getElementById('btn-submit');
  btn.disabled = true;
  btn.textContent = 'Dang gui...';
  try {
    var data = {
      name: document.getElementById('manager-name').value.trim(),
      email: document.getElementById('email-input').value.trim(),
      phone: document.getElementById('phone-input').value.trim(),
      signature: signaturePad.toDataURL('image/png')
    };
    await fetch(APPS_SCRIPT_URL, {
      method: 'POST',
      mode: 'no-cors',
      headers: { 'Content-Type': 'text/plain;charset=utf-8' },
      body: JSON.stringify(data)
    });
    // Hide form, show success
    document.querySelectorAll('.form-card, .section-title, .btn-submit').forEach(function(el) {
      el.style.display = 'none';
    });
    document.getElementById('success-msg').style.display = 'block';
  } catch (err) {
    alert('Loi: ' + err.message);
    console.error(err);
    btn.disabled = false;
    btn.innerHTML = 'Gui thong tin';
  }
}
</script>
</body>
</html>"""

html = HTML.replace('__TEMPLATE_B64__', b64).replace('__APPS_SCRIPT_URL__', apps_url)

# Write index.html in the same directory as build.py
script_dir = os.path.dirname(os.path.abspath(__file__))
output = os.path.join(script_dir, 'index.html')

with open(output, 'w', encoding='utf-8') as f:
    f.write(html)

print(f'Da tao index.html ({len(html):,} bytes)')
print(f'Deploy: git add index.html && git commit -m "update" && git push')
