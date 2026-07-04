# Tomoe — Reading Folders (Montessori phonics printables)

Bộ thẻ đọc Montessori ("Reading Folders") dạng HTML → in ra PDF. Dữ liệu gốc trích từ
`Reading Folders words.pdf` (ở thư mục cha `..\`). Toàn bộ nằm trong folder này.

## Mục tiêu
Tạo thẻ đọc phonics theo **nhóm âm (sound families)**: mỗi *folder* là 1 key sound
(vd `ai`), bên trong có nhiều *card* theo grapheme (`ai`, `ay`, `ei`, `a-e`), mỗi card
có danh sách từ với **âm đích tô đỏ** (chuẩn màu Montessori). In trên khổ **A4**, lưới
nhiều thẻ/trang có viền đứt để cắt.

## Files

| File | Vai trò |
|---|---|
| `reading-folders-data-full.json` | **Nguồn dữ liệu chính** (single source of truth) — 772 từ, bản đầy đủ từ PDF (1) |
| `reading-folders-data.json` | Bản gốc cũ (526 từ) — giữ để tham chiếu, KHÔNG còn build từ file này |
| `gen_html.py` | Sinh `reading-folders.html` + `index.html` từ `reading-folders-data-full.json` (nhúng data inline). Chạy: `python gen_html.py` |
| `reading-folders.html` | Trang in — mở bằng trình duyệt, có toolbar chọn tùy chọn rồi Ctrl/Cmd+P |
| `reading-folders-print.pdf` | PDF bản **chữ in** (Century Gothic) |
| `reading-folders-cursive.pdf` | PDF bản **chữ viết** (cursive) |

> ⚠️ Sửa nội dung từ ngữ **chỉ sửa trong JSON**, rồi chạy lại `gen_html.py` để build lại HTML.
> HTML nhúng data inline nên KHÔNG sửa tay trong HTML (sẽ bị ghi đè).

## Cấu trúc JSON

```jsonc
{
  "folders": [
    {
      "keySound": "ai",                       // chữ xanh lá ngoài bìa folder
      "graphemes": ["ai","ay","ei","a-e"],    // danh sách grapheme (để dựng tab)
      "cards": [
        { "grapheme": "ai",  "words": ["bait", "rail"] },   // TỪ THƯỜNG, không dấu ngoặc
        { "grapheme": "a-e", "words": ["cake", "sale"] }    // split digraph a-e
      ]
    }
  ]
}
```

### Quy ước âm đích — QUAN TRỌNG (đã đổi sang tự-tô)
Data lưu **từ thường, KHÔNG có dấu `[...]`**. App **tự tô đỏ** grapheme của từng card lúc render
(`markWord()` trong `gen_html.py`), theo quy tắc:
- Grapheme liền (ai, ee, oo, ge, tion…) → tô **lần xuất hiện đầu tiên**: `bait` (card `ai`) → `b`+<span>ai</span>+`t`.
- Split digraph `X-e` (a-e, e-e, i-e, o-e, u-e) → regex `X([^aeiou]+)e$` → tô **cả nguyên âm + e cuối**: `cake` → `c`+a+`k`+e.
- Từ không chứa grapheme của card → hiện trơn, không tô (không lỗi). `markWord` idempotent (strip `[]` cũ) + tự lowercase.

> Nhờ vậy người dùng chỉ cần gõ **từ thường** vào đúng card → không phải học dấu ngoặc.
> `markWord` là bản port JS của thuật toán trong file build cũ; strip-brackets-rồi-mark = giữ nguyên kết quả.

### Import / Export (cho người không rành kỹ thuật tự sửa)
Toolbar có nhóm nút **📂 Nhập · 💾 Xuất · ↺** (JSON):
- **Xuất** → tải `reading-folders-data.json` (từ thường) về máy để sửa.
- **Nhập** → chọn file JSON đã sửa → nạp + lưu vào `localStorage['rf-data']` (nhớ qua các lần mở).
- **↺** → xoá localStorage, về `DEFAULT_DATA` (bản build sẵn).
- `DATA` là `let`, ưu tiên localStorage nếu có; validate tối thiểu `Array.isArray(obj.folders)`.

> Đã cân nhắc CSV/Excel nhưng bỏ (Excel Trust Center hay chặn mở Text/CSV trên máy công ty). Sửa JSON bằng JSONedit / JSON Editor Online.

### Ghi đè cỡ chữ cho 1 từ — hậu tố `|px` (tuỳ chọn)
Thêm `|<số>` cuối từ để ép cỡ chữ riêng **trên thẻ từ**: `circumstance|28` → 28px, `data-fixed` nên **auto-fit không đụng**.
`parseWord()` tách `|px` trước khi `markWord()` tô. Thẻ grapheme bỏ qua cỡ.

**Auto-fit (mặc định):** `fitWords()` tự co từ nào rộng hơn ô cho vừa (giảm đều font-size, sàn 12px) —
chỉ tác động từ **chưa** có `|px`. Chạy sau mỗi render + khi đổi font/cỡ/đậm/nghiêng/lưới/hướng.

### Nguyên tắc khi biên tập data
- Gõ **từ thường** vào đúng card (grapheme của card phải thật sự xuất hiện trong từ thì mới được tô).
- Từ **lowercase** + **dedup** trong từng card.
- Muốn ép cỡ 1 từ dài: hậu tố `|px` (vd `circumstance|28`).

## Phạm vi dữ liệu (theo đúng PDF gốc)
14 folder: `ai, ee, ie, oa, ue, or, er, ou, oy, s, j, f, e, shun`.

- **Có từ:** `ee` (148), `ie` (139), `ai` (89), `j` (79), `ue` (39), `s` (25), `or` (7)
- **Rỗng** (PDF không có từ dùng được): `oa, er, ou, oy, f, e, shun` — vẫn giữ khung
  folder/card để sau này điền từ vào là HTML/PDF tự cập nhật.
- `s` tách `ce`/`ci` thành 2 card riêng; `j` tách `ge`/`gi` — cho dễ dựng UI.

## HTML — tính năng toolbar (chỉ hiện trên màn hình, ẩn khi in)
- **View:** Cả hai / chỉ Thẻ từ / chỉ Thẻ grapheme
- **Font:** Chữ in (print) / Chữ viết (cursive) — cũng set được qua URL `?font=cursive`
- **Màu:** Đỏ (Montessori) / Đen trắng (âm đích gạch chân — tiết kiệm mực laser)
- **Folders:** tick chọn folder muốn in
- Nút **In / Lưu PDF**

Hai loại thẻ:
1. **Thẻ từ (word cards):** lưới 3 cột/A4, viền đứt để cắt, mỗi thẻ 1 từ + tag grapheme góc.
2. **Thẻ grapheme:** 2 thẻ/hàng, mỗi thẻ = 1 grapheme + folder + số từ + list 2 cột.

### Font hiện dùng
- Print: `"Century Gothic","Trebuchet MS",Arial,sans-serif` (a/g một tầng, hợp Montessori)
- Cursive: `"Segoe Script","Bradley Hand","Lucida Handwriting","Comic Sans MS",cursive`
  (dựa vào font hệ thống — máy khác không có Segoe Script sẽ về cursive mặc định)

## Xuất PDF (headless Chrome)
```bash
CHROME="/c/Program Files/Google/Chrome/Application/chrome.exe"
BASE="file:///G:/My%20Drive/01_PROJECTS/Tomoe/CODE/reading-folders.html"
"$CHROME" --headless=new --disable-gpu --no-pdf-header-footer \
  --print-to-pdf="reading-folders-print.pdf"   "$BASE?font=print"
"$CHROME" --headless=new --disable-gpu --no-pdf-header-footer \
  --print-to-pdf="reading-folders-cursive.pdf" "$BASE?font=cursive"
```
Hoặc in tay: mở HTML → Ctrl/Cmd+P → **Save as PDF**, khổ **A4**, bật **Background graphics**
(giữ màu đỏ + viền cắt).

## Font Montessori cursive free (để nhúng thật chuẩn — TODO tùy chọn)
Muốn 2 bản PDF ra đúng font ở **mọi máy**: tải `.ttf` rồi nhúng base64 `@font-face` vào HTML.

Ứng viên (đa số **personal/classroom use**, bán tài liệu phải mua license):
- **ABCursive** (TPT, trả phí) — khớp đúng movable alphabet Montessori, có bản nét đứt + dòng kẻ. Chuẩn nhất.
- **ABC Cursive Dotted Line** (Best Font) — cursive có dòng tập viết, free.
- **LMS Spelling Bee**, **Jardotty/Jarman Dotted** (FontSpace) — cursive trẻ em, free.
- **KG Primary Dots / DotNess / DashNess**, mục *Script > School fonts* (DaFont).
- Nguồn nên tránh (repack/ads): onlinewebfonts, fontpalace, freefontdl, fonts101.

## Quy trình sửa đổi (cheat-sheet)
1. Sửa từ ngữ → `reading-folders-data.json`
2. `python gen_html.py` → build lại `reading-folders.html`
3. Xem lại trong trình duyệt (hoặc chạy lệnh headless Chrome ở trên) → xuất PDF
