REPORT=thesis
LATEX=pdflatex
BIBTEX=bibtex --min-crossrefs=1000
REF=thesis.bib

TEX=$(REPORT).tex \
	$(wildcard *.tex) \
	$(wildcard sections/*.tex) \
	$(REF)

PS2PDF=ps2pdf14 -dPDFSETTINGS=/prepress -dEPSCrop
GNUPLOT=gnuplot

SRCS = $(TEX)

all: $(REPORT).pdf

$(REPORT).pdf: $(SRCS) $(REF) $(PDF)
	$(LATEX) $(REPORT)
	$(BIBTEX) $(REPORT)
	perl -p -i -e "s/%\s+//" $(REPORT).bbl
	$(LATEX) $(REPORT)
	$(LATEX) $(REPORT)

spell:
	make clean
	for i in $(SRCS) ; do ispell $$i; done

open:
	open $(REPORT).pdf

tidy:
	-rm -f *.dvi *.aux *.log *.blg *.bbl

clean:
	-rm -f *~ *.toc *.glo  *.idx  *.lof  *.lol *.lot *.out *.dvi *.aux *.log *.blg *.bbl $(REPORT).pdf $(REPORT).ps \
  $(PDF)

.PHONY: clean tidy ps pdf
