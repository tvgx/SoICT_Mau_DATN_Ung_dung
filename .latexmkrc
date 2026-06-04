# .latexmkrc — Cấu hình latexmk
# Tất cả file tự động sinh ra sẽ được đặt vào thư mục build/
$out_dir = 'build';

# Dùng pdflatex
$pdf_mode = 1;
$pdflatex = 'pdflatex -interaction=nonstopmode -synctex=1 %O %S';

# Dùng bibtex
$bibtex_use = 1;

# Sau khi build xong, copy PDF ra thư mục gốc để dễ xem
$success_cmd = 'cp build/main.pdf main.pdf';
