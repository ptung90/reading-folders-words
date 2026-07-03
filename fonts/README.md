# fonts/

Thư mục chứa font `.ttf` để nhúng vào `reading-folders.html`.

`gen_html.py` khai báo sẵn `@font-face` trỏ tới các file dưới đây. **Tên file phải khớp
chính xác** (phân biệt hoa/thường) thì tùy chọn font trong dropdown mới hoạt động.

| Tùy chọn trong dropdown (`Font`) | File cần đặt vào đây |
|---|---|
| Cursive Standard | `CursiveStandard.ttf` (weight 400) + `CursiveStandardBold.ttf` (weight 700) |

> Các tùy chọn `Chữ in (print)` và `Chữ viết (system cursive)` dùng font hệ thống,
> không cần file trong thư mục này. Đây cũng là font mặc định khi mở trang.

## Cách dùng
1. Copy file `.ttf` vào thư mục `fonts/` này, đúng tên như bảng trên.
2. Mở `reading-folders.html`, chọn font tương ứng ở toolbar → font hiển thị ngay.
3. Không cần chạy lại `gen_html.py` (khai báo `@font-face` đã có sẵn trong HTML).

> ⚠️ Lưu ý bản quyền: kiểm tra license trước khi phân phối file `.ttf` hoặc PDF bán ra ngoài.
