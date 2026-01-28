# Script to compile LaTeX document
# Adds MiKTeX to PATH and runs pdflatex

# Add MiKTeX to PATH
$env:Path += ";$env:LOCALAPPDATA\Programs\MiKTeX\miktex\bin\x64"

Write-Host "Compiling LaTeX document..." -ForegroundColor Green

# First pass - generate aux files
pdflatex -interaction=nonstopmode main.tex

# Compile bibliography if .bib file exists
if (Test-Path "Danh_sach_tai_lieu_tham_khao.bib") {
    Write-Host "`nProcessing bibliography..." -ForegroundColor Yellow
    bibtex main
}

# Second pass - resolve references
Write-Host "`nSecond pass..." -ForegroundColor Yellow
pdflatex -interaction=nonstopmode main.tex

# Third pass - finalize
Write-Host "`nFinal pass..." -ForegroundColor Yellow  
pdflatex -interaction=nonstopmode main.tex

Write-Host "`n✓ Compilation complete! PDF file: main.pdf" -ForegroundColor Green

# Open PDF if successful
if (Test-Path "main.pdf") {
    Write-Host "Opening PDF..." -ForegroundColor Cyan
    Start-Process "main.pdf"
}
