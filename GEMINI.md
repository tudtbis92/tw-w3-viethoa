# Quy trình Việt hoá Total War: Warhammer III

Tài liệu này quy định quy trình làm việc bắt buộc cho Agent khi thực hiện dự án Việt hoá game Total War: Warhammer III.

## 1. Cấu trúc thư mục dự án
- `text_origin/`: Chứa các file text (.xml hoặc .tsv) được trích xuất từ pack gốc của game.
- `text_translated/`: Chứa các file text đã được dịch sang tiếng Việt.
- `build/`: Thư mục tạm để đóng gói pack mod.

## 2. Quy trình trích xuất (Extraction)
- Sử dụng `rpfm_cli` để trích xuất toàn bộ text từ `data.pack` (hoặc các pack ngôn ngữ gốc như `local_en.pack`).
- Đặt các file đã trích xuất vào thư mục `text_origin/`.
- Tên file và cấu trúc thư mục bên trong `text_origin/` phải được giữ nguyên để đảm bảo tính tương thích khi đóng gói lại.

## 3. Quy trình dịch và Kiểm tra (Translation & Validation)
- Khi dịch một file từ `text_origin/`, kết quả phải được lưu vào đường dẫn tương ứng trong `text_translated/`.
- **Xử lý file lớn:** Đối với các file có số lượng key lớn, Agent **bắt buộc** thực hiện quy trình sau:
    1. Đọc nội dung file gốc với kích thước **200 key/lần**.
    2. Dịch từng phần.
    3. Ghi kết quả dịch của mỗi phần vào một file tạm (chunk).
    4. Sử dụng script `append_safe.py` để nối nội dung từ file chunk vào file kết quả cuối cùng trong `text_translated/`.
    5. Cập nhật `PROGRESS.md` sau mỗi đợt dịch.
    6. Lặp lại cho đến khi kết thúc file.
- **Encoding (Mã hóa):** Khi ghi file (sử dụng `write_file`, `replace` hoặc các lệnh shell), **bắt buộc** phải sử dụng mã hóa **UTF-8** (đảm bảo hiển thị đúng tiếng Việt có dấu). Tuyệt đối tránh sử dụng các encoding mặc định của hệ thống hoặc không xác định, điều này sẽ gây ra lỗi hiển thị (Mojibake).
- **Bắt buộc:** Sau khi dịch xong mỗi file table, Agent phải thực hiện kiểm tra số lượng key (hoặc số dòng dữ liệu).
- Số lượng key trong file tại `text_translated/` **phải khớp hoàn toàn** với số lượng key trong file gốc tại `text_origin/`.
- Nếu phát hiện sai lệch, phải dừng lại và sửa đổi trước khi tiếp tục file tiếp theo.

## 4. Đóng gói (Packing)
- Sử dụng `rpfm_cli` để tạo một pack mới tên là `text_translated.pack`.
- Pack này sẽ chứa các file đã được dịch từ thư mục `text_translated/`.

## 6. Quy trình Resume và Theo dõi tiến độ
- Mọi tiến độ dịch thuật phải được ghi nhận vào file `PROGRESS.md` tại thư mục gốc của dự án.
- **Trước khi bắt đầu bất kỳ session mới nào**, Agent phải:
    1. Đọc file `PROGRESS.md` để xác định table nào đang được dịch dở dang.
    2. Đọc file `MEMORY.md` để nắm bắt các lưu ý quan trọng từ session trước.
- Cấu trúc file `PROGRESS.md` bao gồm: Tên file, Tổng số key, Số key đã dịch, Trạng thái (In Progress/Done), và % hoàn thành.
- **Tính liên tục và An toàn:** 
    - Agent phải cập nhật `PROGRESS.md` **ngay lập tức** sau khi dịch xong mỗi file hoặc khi thực hiện một khối lượng dịch thuật đáng kể (ví dụ: mỗi 50-100 dòng).
    - Trong trường hợp gặp lỗi hoặc sắp kết thúc session, Agent **bắt buộc** phải ghi lại trạng thái chính xác (đang dừng ở dòng nào, table nào) vào `PROGRESS.md` để đảm bảo không mất context khi resume.
