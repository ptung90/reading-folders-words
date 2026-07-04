# -*- coding: utf-8 -*-
# Build reading-folders.html (+ index.html for GitHub Pages) from reading-folders-data.json.
# Run:  python gen_html.py
import json, io, os

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "reading-folders-data.json")
OUT = os.path.join(HERE, "reading-folders.html")
OUT_INDEX = os.path.join(HERE, "index.html")

data = json.load(io.open(SRC, encoding="utf-8"))
data_js = json.dumps(data, ensure_ascii=False)

html = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Reading Folders — Printable Cards</title>
<style>
  :root{
    --red:#d32f2f;
    --blue:#1565c0;
    --ink:#1a1a1a;
    --cut:#b0b0b0;
    --cols:3;
    --rows:3;
    --word-fs:42px;
    --page-w:297mm;
    --page-h:210mm;
  }
  *{ box-sizing:border-box; -webkit-print-color-adjust:exact; print-color-adjust:exact; }
  html,body{ margin:0; padding:0; }
  body{ font-family:"Segoe UI",Arial,sans-serif; color:var(--ink); background:#eceef1; }

  /* ---- downloaded preview font ---- */
  @font-face{ font-family:"Cursive Standard"; src:url("fonts/CursiveStandard.ttf") format("truetype"); font-weight:400; }
  @font-face{ font-family:"Cursive Standard"; src:url("fonts/CursiveStandardBold.ttf") format("truetype"); font-weight:700; }

  /* ---- word content fonts (togglable) ---- */
  .wcard .w,.grouphead .g,.gcard .head .g,.gcard .words{
    font-family:"Century Gothic","Trebuchet MS",Arial,sans-serif;  /* print / manuscript */
  }
  body.cursive .wcard .w,
  body.cursive .grouphead .g,
  body.cursive .gcard .head .g,
  body.cursive .gcard .words{
    font-family:"Segoe Script","Bradley Hand","Lucida Handwriting","Comic Sans MS",cursive;
  }
  body.cursive .gcard .words{ font-size:15px; line-height:1.95; }
  body.cursive .grouphead .g,body.cursive .gcard .head .g{ font-size:30px; }

  body.font-cursive-standard .gcard .words{ font-size:16px; line-height:1.9; }
  body.font-cursive-standard .grouphead .g, body.font-cursive-standard .gcard .head .g{ font-size:32px; }

  body.font-cursive-standard .wcard .w{ font-family:"Cursive Standard",cursive; }
  body.font-cursive-standard .grouphead .g,body.font-cursive-standard .gcard .head .g,body.font-cursive-standard .gcard .words{ font-family:"Cursive Standard",cursive; }

  /* ---------- Toolbar (screen only) ---------- */
  .toolbar{
    position:sticky; top:0; z-index:10; background:#fff; border-bottom:1px solid #d5d9df;
    padding:12px 18px; display:flex; flex-wrap:wrap; gap:16px; align-items:flex-end;
    box-shadow:0 1px 6px rgba(0,0,0,.08);
  }
  .toolbar h1{ font-size:16px; margin:0 12px 0 0; align-self:center; }
  .tb-group{ display:flex; flex-direction:column; gap:4px; font-size:12px; }
  .tb-group b{ font-size:11px; text-transform:uppercase; letter-spacing:.5px; color:#667; }
  .tb-group label{ font-weight:400; margin-right:8px; white-space:nowrap; }
  .folders-filter{ max-width:520px; flex-wrap:wrap; display:flex; gap:2px 10px; }
  button.print{
    margin-left:auto; background:var(--blue); color:#fff; border:0; border-radius:6px;
    padding:10px 18px; font-size:14px; font-weight:600; cursor:pointer;
  }
  button.print:hover{ filter:brightness(1.08); }
  .hint{ font-size:12px; color:#667; padding:8px 18px 0; }

  /* ---------- Print sheet ---------- */
  .sheet{ background:#fff; margin:16px auto; padding:0; width:var(--page-w); min-height:var(--page-h);
          box-shadow:0 2px 12px rgba(0,0,0,.12); }
  .section-title{ font-size:15px; font-weight:700; color:var(--blue); margin:0 0 8px;
                  border-bottom:2px solid var(--blue); padding-bottom:4px; }

  /* group header inside word-card grid */
  .grouphead{ grid-column:1/-1; display:flex; align-items:baseline; gap:10px;
              margin:10px 0 2px; padding-bottom:2px; border-bottom:1px solid #e2e2e2; }
  .grouphead .g{ font-size:20px; font-weight:800; color:var(--red); }
  .grouphead .k{ font-size:11px; color:#889; text-transform:uppercase; letter-spacing:.5px; }

  /* ---------- Word cards (cut grid) ---------- */
  .wordgrid{ display:grid; grid-template-columns:repeat(var(--cols),calc((var(--page-w) - 2px) / var(--cols)));
             border-top:1px dashed var(--cut); border-left:1px dashed var(--cut); }
  .wcard{ width:calc((var(--page-w) - 2px) / var(--cols)); height:calc((var(--page-h) - 2px) / var(--rows)); border-right:1px dashed var(--cut); border-bottom:1px dashed var(--cut);
          display:flex; align-items:center; justify-content:center; padding:6px 16px;
          break-inside:avoid; }
  /* screen-only page badge so the print pagination is visible in preview */
  .pagenum{ font-family:"Segoe UI",Arial,sans-serif; font-size:11px; color:#889;
            padding:6px 10px 4px; letter-spacing:.3px; }
  .wcard .w{ font-size:var(--word-fs); font-weight:700; letter-spacing:.5px; }

  /* ---------- Grapheme list cards ---------- */
  .gcardgrid{ display:grid; grid-template-columns:repeat(2,1fr); gap:8mm; }
  .gcard{ border:1.5px solid #444; border-radius:7px; padding:10px 12px 12px; break-inside:avoid; }
  .gcard .head{ display:flex; align-items:baseline; gap:8px; border-bottom:1.5px solid #eee;
                margin-bottom:6px; padding-bottom:5px; }
  .gcard .head .g{ font-size:26px; font-weight:800; color:var(--red); line-height:1; }
  .gcard .head .k{ font-size:11px; color:var(--blue); text-transform:uppercase; letter-spacing:.6px; }
  .gcard .head .n{ margin-left:auto; font-size:10px; color:#aab; }
  .gcard .words{ columns:2; column-gap:14px; font-size:13px; line-height:1.65; }
  .gcard .words .w{ break-inside:avoid; }

  /* the highlighted grapheme */
  .sound{ color:var(--red); }

  /* ---------- Font weight override ---------- */
  body.fw-normal .wcard .w,
  body.fw-normal .grouphead .g,
  body.fw-normal .gcard .head .g,
  body.fw-normal .gcard .words{ font-weight:400 !important; }
  body.fw-bold .wcard .w,
  body.fw-bold .grouphead .g,
  body.fw-bold .gcard .head .g,
  body.fw-bold .gcard .words{ font-weight:700 !important; }

  /* ---------- Fake italic (synthetic oblique) ---------- */
  body.fake-italic .wcard .w,
  body.fake-italic .grouphead .g,
  body.fake-italic .gcard .head .g,
  body.fake-italic .gcard .words{ font-style:italic !important; }

  /* ---------- Black & white mode ---------- */
  body.bw .sound{ color:#000; font-weight:800; text-decoration:underline; text-underline-offset:2px; }
  body.bw .grouphead .g, body.bw .gcard .head .g{ color:#000; }
  body.bw .gcard .head .k{ color:#000; }
  body.bw .section-title{ color:#000; border-color:#000; }

  .hidden{ display:none !important; }

  @page{ size:A4 landscape; margin:0; }
  @media print{
    body{ background:#fff; }
    .toolbar,.hint{ display:none !important; }
    /* clean cut-grid: hide screen-only labels/badges on paper */
    .section-title,.grouphead,.pagenum{ display:none !important; }
    .sheet{ margin:0; padding:0; width:auto; min-height:0; box-shadow:none; }
    .sheet + .sheet{ break-before:page; }
  }
</style>
</head>
<body>

<div class="toolbar">
  <h1>Reading Folders</h1>
  <div class="tb-group">
    <b>View</b>
    <div>
      <label><input type="radio" name="view" value="both" checked> Cả hai</label>
      <label><input type="radio" name="view" value="words"> Thẻ từ</label>
      <label><input type="radio" name="view" value="graphemes"> Thẻ grapheme</label>
    </div>
  </div>
  <div class="tb-group">
    <b>Khổ giấy</b>
    <div>
      <label><input type="radio" name="orientation" value="landscape" checked> Ngang</label>
      <label><input type="radio" name="orientation" value="portrait"> Dọc</label>
    </div>
  </div>
  <div class="tb-group">
    <b>Lưới thẻ (cột × hàng)</b>
    <div style="display:flex;gap:8px;">
      <label>Cột <input type="number" id="colsInput" value="3" min="1" max="10" step="1" style="width:52px;padding:5px 6px;border:1px solid #c5cbd3;border-radius:5px;font-size:13px;"></label>
      <label>Hàng <input type="number" id="rowsInput" value="3" min="1" max="10" step="1" style="width:52px;padding:5px 6px;border:1px solid #c5cbd3;border-radius:5px;font-size:13px;"></label>
    </div>
  </div>
  <div class="tb-group">
    <b>Font</b>
    <select id="fontSel" style="padding:5px 8px;border:1px solid #c5cbd3;border-radius:5px;font-size:13px;">
      <option value="print">Chữ in (print)</option>
      <option value="cursive">Chữ viết (system cursive)</option>
      <option value="cursive-standard" selected>Cursive Standard</option>
    </select>
  </div>
  <div class="tb-group">
    <b>Cỡ chữ</b>
    <select id="fontSizeSel" style="padding:5px 8px;border:1px solid #c5cbd3;border-radius:5px;font-size:13px;">
      <option value="auto">Tự động (theo font)</option>
      <option value="28">28px</option>
      <option value="32">32px</option>
      <option value="36">36px</option>
      <option value="40">40px</option>
      <option value="44">44px</option>
      <option value="48">48px</option>
      <option value="52">52px</option>
      <option value="56">56px</option>
      <option value="60">60px</option>
      <option value="64">64px</option>
      <option value="72">72px</option>
      <option value="80">80px</option>
      <option value="90">90px</option>
      <option value="100">100px</option>
    </select>
  </div>
  <div class="tb-group">
    <b>Độ đậm</b>
    <select id="weightSel" style="padding:5px 8px;border:1px solid #c5cbd3;border-radius:5px;font-size:13px;">
      <option value="auto">Mặc định</option>
      <option value="normal">Normal (400)</option>
      <option value="bold">Bold (700)</option>
    </select>
  </div>
  <div class="tb-group">
    <b>Kiểu</b>
    <label><input type="checkbox" id="italicChk"> Nghiêng (italic giả)</label>
  </div>
  <div class="tb-group">
    <b>Màu</b>
    <div>
      <label><input type="radio" name="color" value="red" checked> Đỏ (Montessori)</label>
      <label><input type="radio" name="color" value="bw"> Đen trắng</label>
    </div>
  </div>
  <div class="tb-group">
    <b>Folders</b>
    <div class="folders-filter" id="folderFilter"></div>
  </div>
  <button class="print" onclick="window.print()">🖨️ In / Lưu PDF</button>
</div>
<div class="hint">Mẹo in PDF: nhấn nút trên (hoặc Ctrl/Cmd+P) → chọn <b>Save as PDF</b> → khổ <b>A4</b> → bật <b>Background graphics</b> để giữ màu đỏ và viền cắt.</div>

<div id="app"></div>

<script>
const DATA = __DATA__;

// "b[ai]t" -> "b<span class='sound'>ai</span>t"
function renderWord(w){
  return w.split(/\[([^\]]+)\]/).map((seg,i)=> i%2 ? '<span class="sound">'+seg+'</span>' : seg).join('');
}
function esc(s){ return s.replace(/&/g,'&amp;').replace(/</g,'&lt;'); }

// "surv[ei]llance|30" -> { text:"surv[ei]llance", fs:30 }; trailing |<px> = manual font size
function parseWord(raw){
  const m = raw.match(/\|(\d+)\s*$/);
  return m ? { text: raw.slice(0, m.index), fs: parseInt(m[1],10) } : { text: raw, fs: null };
}

const app = document.getElementById('app');
const filterBox = document.getElementById('folderFilter');

// build folder filter checkboxes (only folders that have any words)
const nonEmpty = DATA.folders.filter(f => f.cards.some(c=>c.words.length));
nonEmpty.forEach(f=>{
  const id='f_'+f.keySound;
  const lbl=document.createElement('label');
  lbl.innerHTML='<input type="checkbox" value="'+f.keySound+'" checked> '+f.keySound;
  filterBox.appendChild(lbl);
});

function selectedFolders(){
  return [...filterBox.querySelectorAll('input:checked')].map(i=>i.value);
}
function currentView(){ return document.querySelector('input[name=view]:checked').value; }

// auto-fit: shrink any word wider than its card (single proportional pass); skip manually-sized words
const MIN_FIT_FS = 12;
const FIT_MARGIN = 0.90;                     // shrink to 90% of the card width -> more breathing room from the edge
function fitWords(){
  app.querySelectorAll('.wcard .w').forEach(span=>{
    if(span.dataset.fixed) return;          // manual |px — leave exactly as set
    span.style.fontSize = '';               // reset to global --word-fs before measuring
    const card = span.parentElement;
    const cs = getComputedStyle(card);
    const avail = card.clientWidth - parseFloat(cs.paddingLeft) - parseFloat(cs.paddingRight);
    if(span.scrollWidth > avail){
      const cur = parseFloat(getComputedStyle(span).fontSize);
      span.style.fontSize = Math.max(MIN_FIT_FS, Math.floor(cur * avail / span.scrollWidth * FIT_MARGIN)) + 'px';
    }
  });
}

function render(){
  const sel = new Set(selectedFolders());
  const view = currentView();
  const folders = DATA.folders.filter(f=> sel.has(f.keySound) && f.cards.some(c=>c.words.length));
  let out='';

  // ---- Section 1: word cards (flattened, packed, split into A4 pages) ----
  if(view==='both' || view==='words'){
    const cols = parseInt(colsInput.value, 10) || 3;
    const rows = parseInt(rowsInput.value, 10) || 3;
    const perPage = Math.max(1, cols * rows);
    // flatten every word across all selected folders/graphemes — no grouping
    const allWords = [];
    folders.forEach(f=> f.cards.filter(c=>c.words.length).forEach(c=> c.words.forEach(w=> allWords.push(w))));
    const pageCount = Math.ceil(allWords.length / perPage);
    for(let p=0; p<pageCount; p++){
      const pageWords = allWords.slice(p*perPage, (p+1)*perPage);
      out += '<div class="sheet"><div class="pagenum">Trang '+(p+1)+'/'+pageCount+' · '+pageWords.length+' thẻ</div><div class="wordgrid">';
      pageWords.forEach(w=>{
        const pw = parseWord(w);
        const attr = pw.fs ? ' style="font-size:'+pw.fs+'px" data-fixed="1"' : '';
        out += '<div class="wcard"><span class="w"'+attr+'>'+renderWord(esc(pw.text))+'</span></div>';
      });
      out += '</div></div>';
    }
  }

  // ---- Section 2: grapheme list cards ----
  if(view==='both' || view==='graphemes'){
    out += '<div class="sheet"><div class="section-title">Thẻ theo grapheme — Grapheme cards</div><div class="gcardgrid">';
    folders.forEach(f=>{
      f.cards.filter(c=>c.words.length).forEach(c=>{
        out += '<div class="gcard"><div class="head"><span class="g">'+esc(c.grapheme)+'</span>'
             + '<span class="k">folder '+esc(f.keySound)+'</span>'
             + '<span class="n">'+c.words.length+' words</span></div><div class="words">';
        c.words.forEach(w=>{ out += '<div class="w">'+renderWord(esc(parseWord(w).text))+'</div>'; });
        out += '</div></div>';
      });
    });
    out += '</div></div>';
  }

  app.innerHTML = out;
  fitWords();
}

filterBox.addEventListener('change', render);
document.querySelectorAll('input[name=view]').forEach(r=>r.addEventListener('change', render));
document.querySelectorAll('input[name=color]').forEach(r=>r.addEventListener('change', e=>{
  document.body.classList.toggle('bw', e.target.value==='bw');
  fitWords();
}));

// font toggle, also settable via ?font=xxx for headless export
const fontSel = document.getElementById('fontSel');
const FONT_CLASSES = ['cursive','font-cursive-standard'];
function applyFont(v){
  document.body.classList.remove(...FONT_CLASSES);
  if(v && v!=='print') document.body.classList.add(v==='cursive' ? 'cursive' : 'font-'+v);
}
fontSel.addEventListener('change', e=>{ applyFont(e.target.value); applyFontSize(); });
const _f = new URLSearchParams(location.search).get('font');
if(_f) fontSel.value = _f;
applyFont(fontSel.value);

// card grid columns/rows per page (card size = page size / cols,rows), also settable via ?cols=&rows=
const colsInput = document.getElementById('colsInput');
const rowsInput = document.getElementById('rowsInput');
function applyGrid(){
  const cols = parseInt(colsInput.value, 10) || 3;
  const rows = parseInt(rowsInput.value, 10) || 3;
  document.documentElement.style.setProperty('--cols', cols);
  document.documentElement.style.setProperty('--rows', rows);
}
function onGridChange(){ applyGrid(); render(); }
colsInput.addEventListener('input', onGridChange);
rowsInput.addEventListener('input', onGridChange);
const _cols = new URLSearchParams(location.search).get('cols');
const _rows = new URLSearchParams(location.search).get('rows');
if(_cols) colsInput.value = _cols;
if(_rows) rowsInput.value = _rows;
applyGrid();

// paper orientation, also settable via ?orientation=portrait|landscape
const orientationRadios = document.querySelectorAll('input[name=orientation]');
const pageStyleTag = document.createElement('style');
document.head.appendChild(pageStyleTag);
function applyOrientation(v){
  const landscape = v !== 'portrait';
  document.documentElement.style.setProperty('--page-w', landscape ? '297mm' : '210mm');
  document.documentElement.style.setProperty('--page-h', landscape ? '210mm' : '297mm');
  pageStyleTag.textContent = '@page{ size:A4 '+(landscape ? 'landscape' : 'portrait')+'; margin:0; }';
}
orientationRadios.forEach(r=>r.addEventListener('change', e=>{ applyOrientation(e.target.value); fitWords(); }));
const _o = new URLSearchParams(location.search).get('orientation');
if(_o){ const match=[...orientationRadios].find(r=>r.value===_o); if(match) match.checked=true; }
applyOrientation(document.querySelector('input[name=orientation]:checked').value);

// word font size (px), "auto" follows each font's built-in default; also settable via ?fontsize=xxx
const fontSizeSel = document.getElementById('fontSizeSel');
const DEFAULT_FS = { print:42, cursive:48, 'cursive-standard':50 };
function applyFontSize(){
  const v = fontSizeSel.value;
  const px = v==='auto' ? (DEFAULT_FS[fontSel.value] || 42) : parseInt(v,10);
  document.documentElement.style.setProperty('--word-fs', px+'px');
  fitWords();
}
fontSizeSel.addEventListener('change', applyFontSize);
const _fs = new URLSearchParams(location.search).get('fontsize');
if(_fs) fontSizeSel.value = _fs;
applyFontSize();

// font-weight override, also settable via ?weight=xxx
const weightSel = document.getElementById('weightSel');
function applyWeight(v){
  document.body.classList.remove('fw-normal','fw-bold');
  if(v==='normal') document.body.classList.add('fw-normal');
  if(v==='bold') document.body.classList.add('fw-bold');
}
weightSel.addEventListener('change', e=>{ applyWeight(e.target.value); fitWords(); });
const _w = new URLSearchParams(location.search).get('weight');
if(_w){ weightSel.value = _w; applyWeight(_w); }

// fake italic toggle, also settable via ?italic=1
const italicChk = document.getElementById('italicChk');
italicChk.addEventListener('change', e=>{
  document.body.classList.toggle('fake-italic', e.target.checked);
  fitWords();
});
if(new URLSearchParams(location.search).get('italic')==='1'){ italicChk.checked = true; document.body.classList.add('fake-italic'); }

render();
</script>
</body>
</html>
"""

html = html.replace("__DATA__", data_js)
io.open(OUT, "w", encoding="utf-8").write(html)
io.open(OUT_INDEX, "w", encoding="utf-8").write(html)
print("Wrote", OUT, "and", OUT_INDEX, "-", len(html), "bytes each")
