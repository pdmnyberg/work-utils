SRCDIR=src
OUTDIR?=output
SOURCES=$(wildcard $(SRCDIR)/*.gv.txt)


$(OUTDIR)/%.svg: $(SRCDIR)/%.gv.txt
	mkdir -p $(OUTDIR) && \
	echo "Building: $@: $^" && \
	dot -Tsvg -o$@ $<

all: $(SOURCES:$(SRCDIR)/%.gv.txt=$(OUTDIR)/%.svg)
