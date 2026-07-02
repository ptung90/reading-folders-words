# fonts/

Thư mục chứa font `.ttf` để nhúng vào `reading-folders.html`.

`gen_html.py` khai báo sẵn `@font-face` trỏ tới các file dưới đây. **Tên file phải khớp
chính xác** (phân biệt hoa/thường) thì tùy chọn font trong dropdown mới hoạt động; nếu
thiếu file, font đó sẽ tự fallback về cursive mặc định của hệ thống.

| Tùy chọn trong dropdown (`Font`) | File cần đặt vào đây |
|---|---|
| Jarman | `Jarman.ttf` |
| Jardotty (dotted) | `Jardotty.ttf` |
| LMS Spelling Bee (dotted) | `LMSSpellingBee.ttf` |
| KG Primary Dots | `KGPrimaryDots.ttf` |
| KG Primary Dots Lined | `KGPrimaryDotsLined.ttf` |
| DotNess | `DotNess.ttf` |
| DashNess | `DashNess.ttf` |
| Cursive Standard | `CursiveStandard.ttf` (weight 400) + `CursiveStandardBold.ttf` (weight 700) |

> Các tùy chọn `Chữ in (print)` và `Chữ viết (system cursive)` dùng font hệ thống,
> không cần file trong thư mục này.

## Cách dùng
1. Tải file `.ttf`, đổi tên cho khớp bảng trên rồi copy vào thư mục `fonts/` này.
2. Mở `reading-folders.html`, chọn font tương ứng ở toolbar → font hiển thị ngay.
3. Không cần chạy lại `gen_html.py` (khai báo `@font-face` đã có sẵn trong HTML).

> ⚠️ Lưu ý bản quyền: nhiều font chỉ **free cho personal/classroom use**. Kiểm tra license
> trước khi phân phối file `.ttf` hoặc PDF bán ra ngoài (xem thêm phần font trong `CLAUDE.md`).
