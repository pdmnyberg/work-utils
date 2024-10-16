SHELL := /bin/bash
SRCDIR=notebooks
OUTDIR?=output
SOURCES=$(wildcard $(SRCDIR)/*.ipynb)


$(SRCDIR)/venv/bin/activate: requirements.txt
	mkdir -p $(SRCDIR) && \
	python3 -m venv $(SRCDIR)/venv && \
	(\
		source $(SRCDIR)/venv/bin/activate; \
		python -m pip install -r requirements.txt; \
	)


init: $(SRCDIR)/venv/bin/activate


$(OUTDIR)/%.py: $(SRCDIR)/%.ipynb $(SRCDIR)/venv/bin/activate
	mkdir -p $(OUTDIR)
	echo "Building: $@: $<"
	(\
		source $(SRCDIR)/venv/bin/activate; \
		jupyter nbconvert --no-prompt --to script $< --output ../$(OUTDIR)/$* \
	)


all: $(SOURCES:$(SRCDIR)/%.ipynb=$(OUTDIR)/%.py)
