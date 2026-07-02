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
| `reading-folders-data.json` | **Nguồn dữ liệu duy nhất** (single source of truth) — 526 từ |
| `gen_html.py` | Sinh `reading-folders.html` từ JSON (nhúng data inline). Chạy: `python gen_html.py` |
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
        { "grapheme": "ai",  "words": ["b[ai]t", "r[ai]l"] },
        { "grapheme": "a-e", "words": ["c[a]k[e]", "s[a]l[e]"] }  // split digraph
      ]
    }
  ]
}
```

### Quy ước marker âm đích — QUAN TRỌNG
Âm đích (grapheme) được bọc trong **dấu ngoặc vuông `[...]`** ngay trong chuỗi từ:
- `b[ai]t` → render `b` + `<span class="sound">ai</span>` + `t`
- `c[a]k[e]` → split digraph `a-e` (magic-e) → tô đỏ **cả** `a` và `e`

Regex render trong HTML:
```js
word.split(/\[([^\]]+)\]/).map((s,i)=> i%2 ? `<span class="sound">${s}</span>` : s).join('')
word.replace(/[\[\]]/g,'')   // lấy từ gốc (bỏ marker)
```

### Nguyên tắc khi biên tập data
- Chỉ giữ từ mà **grapheme của card thực sự xuất hiện** → mọi marker luôn hợp lệ.
- Bỏ từ PDF xếp nhầm cột (vd `evoke/remote` dưới `e-e`, `deceive` dưới `ie`).
- Từ **lowercase** + **dedup** trong từng card.

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
