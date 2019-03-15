LA  = pdflatex -shell-escape 
BIB = biber
PY  = python3

default: report

report:
	$(PY) PrintDia.py
	$(LA) report.tex
	$(BIB) report
	$(LA) report.tex
