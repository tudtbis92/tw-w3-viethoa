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
- **Quy trình dịch (Bắt buộc cho mọi file):** Mọi file translation **bắt buộc** phải xử lý theo các bước sau:
    1. Chạy script `split_tsv.py <path_to_origin_tsv>` để chia file gốc thành các file chunk lưu trực tiếp trong thư mục `chunks/` theo định dạng `filename_chunk_x.tsv` (mỗi file 200 key).
    2. Spawn sub-agent dịch song song các file chunk. Kết quả dịch của mỗi chunk phải được lưu thành `filename_chunk_translated_x.tsv` trong cùng thư mục `chunks/`.
    3. Cập nhật `PROGRESS.md` sau khi hoàn thành mỗi chunk.
    4. **Kiểm tra tính toàn vẹn (Bắt buộc):** Trước khi chạy script merge, Agent **phải** kiểm tra số lượng dòng (key) của từng file `filename_chunk_translated_x.tsv` so với file gốc `filename_chunk_x.tsv`. Hai file phải có số dòng khớp hoàn toàn. Nếu phát hiện sai lệch (do sub-agent dịch thiếu hoặc thừa dòng), phải yêu cầu dịch lại chunk đó trước khi tiếp tục.
    5. Sau khi đã xác nhận toàn bộ các chunk đều khớp, chạy script `merge_chunks.py <filename>` để nối các file chunk đã dịch thành file kết quả cuối cùng trong `text_translated/`. Script này cũng sẽ thực hiện xóa bỏ các file chunk (gốc và dịch) sau khi hoàn tất.
    6. Thực hiện so sánh số lượng key giữa file kết quả và file gốc để đảm bảo tính toàn vẹn.
- **Encoding (Mã hóa):** Khi ghi file (sử dụng `write_file`, `replace` hoặc các lệnh shell), **bắt buộc** phải sử dụng mã hóa **UTF-8** (đảm bảo hiển thị đúng tiếng Việt có dấu). Tuyệt đối tránh sử dụng các encoding mặc định của hệ thống hoặc không xác định, điều này sẽ gây ra lỗi hiển thị (Mojibake).
- **Bắt buộc:** Sau khi dịch xong mỗi file table, Agent phải thực hiện kiểm tra số lượng key (hoặc số dòng dữ liệu).
- Số lượng key trong file tại `text_translated/` **phải khớp hoàn toàn** với số lượng key trong file gốc tại `text_origin/`.
- Nếu phát hiện sai lệch, phải dừng lại và sửa đổi trước khi tiếp tục file tiếp theo.

## 4. Quy tắc đặc biệt khi dịch

### Key "placeholder" — KHÔNG ĐƯỢC DỊCH
- Các key có nội dung text là `placeholder`, `PLACEHOLDER`, `Placeholder`, hoặc các biến thể viết tắt như `ph`, `PH`, `[ph]`, `[PH]`, cũng như từ `deprecated` trong file gốc là **text tạm thời của CA chưa được điền nội dung thực hoặc đã bị loại bỏ**.
- **Bắt buộc:** Giữ nguyên nguyên văn giá trị gốc (giữ đúng case: lowercase/uppercase/titlecase/brackets như file origin).
- **Tuyệt đối không** dịch thành "vùng giữ chỗ", "lỗi thời" hay bất kỳ nội dung tiếng Việt nào.
- Nếu text chứa placeholder kèm theo mô tả khác (ví dụ: `[ph] empire fort`), hãy giữ nguyên phần placeholder và dịch phần nội dung thực nếu cần, hoặc tốt nhất là giữ nguyên cả câu nếu nó rõ ràng là text nháp của developer.
- Phạm vi ảnh hưởng: Hàng ngàn key trải rộng nhiều file trong toàn dự án.

## 5. Đóng gói (Packing)
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
