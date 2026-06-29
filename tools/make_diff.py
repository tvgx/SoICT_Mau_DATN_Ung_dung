#!/usr/bin/env python3
"""Sinh main_diff.tex theo dõi thay đổi giữa HEAD (snapshot) và bản hiện tại.

Cách làm: dự án dùng subfiles nên latexdiff --flatten không xử lý được
(nó coi \subfile như \input và gặp \begin{document} lồng nhau). Thay vào đó
ta diff TỪNG subfile riêng (mỗi subfile vẫn compile được), đặt bản diff cạnh
bản gốc với đuôi .diff.tex, rồi tạo main_diff.tex trỏ tới các bản diff và
chèn khối preamble của latexdiff (định nghĩa \DIFadd, \DIFdel...) vào preamble
chính (vì subfiles bỏ qua preamble của file con).
"""
import os, re, subprocess, sys, tempfile

ROOT = "/home/lordfeeder/workspaces/SoICT_Mau_DATN_Ung_dung"
OLD = "/tmp/old_snap"
LATEXDIFF = ["perl", os.path.join(ROOT, "tools/latexdiff")]
ENV = dict(os.environ, PERL5LIB=os.path.join(ROOT, "tools/lib"))

def _norm_copy(src, want_end):
    """Tạo bản copy tạm có \\end{document} (latexdiff cần cặp begin/end).
    Trả về (đường dẫn tạm, file gốc có \\end{document} hay không)."""
    txt = open(src, encoding="utf-8").read()
    has_end = "\\end{document}" in txt
    if want_end and not has_end:
        if not txt.endswith("\n"):
            txt += "\n"
        txt += "\\end{document}\n"
    tmp = tempfile.NamedTemporaryFile("w", suffix=".tex", delete=False, encoding="utf-8")
    tmp.write(txt)
    tmp.close()
    return tmp.name, has_end

def run_latexdiff(old_file, new_file, out_file):
    # Một số subfile (vd Chuong/1) thiếu \end{document}; subfiles vẫn build được
    # nhưng latexdiff đòi cặp begin/end. Vá tạm rồi gỡ lại ở output.
    new_orig_has_end = "\\end{document}" in open(new_file, encoding="utf-8").read()
    norm_old, _ = _norm_copy(old_file, want_end=True)
    norm_new, _ = _norm_copy(new_file, want_end=True)
    r = subprocess.run(LATEXDIFF + ["--encoding=utf8", norm_old, norm_new],
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=ENV)
    for t in (norm_old, norm_new):
        try: os.unlink(t)
        except OSError: pass
    if r.returncode != 0:
        sys.stderr.write(f"[latexdiff FAIL] {new_file}\n{r.stderr.decode()[-400:]}\n")
        return False
    out = r.stdout.decode("utf-8")
    if not new_orig_has_end:
        # gỡ \end{document} ta đã thêm để bản diff khớp cấu trúc gốc của subfile
        idx = out.rfind("\\end{document}")
        if idx != -1:
            out = out[:idx] + out[idx + len("\\end{document}"):]
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(out)
    return True

def resolve(path):
    """Thêm .tex nếu thiếu, trả về đường dẫn tương đối từ ROOT."""
    return path if path.endswith(".tex") else path + ".tex"

def main():
    main_tex = open(os.path.join(ROOT, "main.tex"), encoding="utf-8").read()

    # Tìm các dòng \subfile{...} đang active (không bị comment ở đầu dòng)
    subfile_re = re.compile(r'^(?P<indent>[^%\n]*?)\\subfile\{(?P<arg>[^}]+)\}', re.M)
    targets = []
    for m in subfile_re.finditer(main_tex):
        targets.append(m.group("arg").strip())

    print("Subfiles active:", targets)

    empty = tempfile.NamedTemporaryFile("w", suffix=".tex", delete=False)
    empty.write("\\documentclass[main.tex]{subfiles}\n\\begin{document}\n\\end{document}\n")
    empty.close()

    replacements = {}     # arg -> arg_diff (để thay trong main_diff.tex)
    preamble_block = None

    for arg in targets:
        rel = resolve(arg)
        new_file = os.path.join(ROOT, rel)
        old_file = os.path.join(OLD, rel)
        if not os.path.exists(new_file):
            print(f"  SKIP (no new file): {rel}")
            continue
        old_src = old_file if os.path.exists(old_file) else empty.name
        diff_rel = rel[:-4] + ".diff.tex"
        diff_file = os.path.join(ROOT, diff_rel)
        ok = run_latexdiff(old_src, new_file, diff_file)
        if not ok:
            continue
        nadd = sum(1 for _ in open(diff_file, encoding="utf-8", errors="ignore") if "DIFadd" in _)
        print(f"  DIFF {rel}  (old={'HEAD' if old_src!=empty.name else 'NEW-FILE'})")
        # arg dùng trong main_diff: bỏ .tex nếu arg gốc không có .tex
        new_arg = diff_rel[:-4] if not arg.endswith(".tex") else diff_rel
        replacements[arg] = new_arg
        if preamble_block is None:
            txt = open(diff_file, encoding="utf-8").read()
            mm = re.search(r'%DIF PREAMBLE EXTENSION ADDED BY LATEXDIFF.*?%DIF END PREAMBLE EXTENSION ADDED BY LATEXDIFF',
                           txt, re.S)
            if mm:
                preamble_block = mm.group(0)

    # Tạo main_diff.tex
    out = main_tex
    for arg, new_arg in replacements.items():
        out = out.replace("\\subfile{" + arg + "}", "\\subfile{" + new_arg + "}")
    if preamble_block:
        out = out.replace("\\begin{document}",
                          preamble_block + "\n\\begin{document}", 1)
    with open(os.path.join(ROOT, "main_diff.tex"), "w", encoding="utf-8") as f:
        f.write(out)
    print(f"\nWrote main_diff.tex  ({len(replacements)} subfiles diffed)")

if __name__ == "__main__":
    main()
