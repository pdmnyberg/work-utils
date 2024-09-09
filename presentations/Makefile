SRCDIR=src
OUTDIR?=output
RSCDIR=resources
COMMON_STYLE=$(SRCDIR)/meerkatsstyle.tex
SOURCES=$(wildcard $(SRCDIR)/*.md)

$(RSCDIR)/git-log.png:
	curl \
		"https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Git-logo.svg/1024px-Git-logo.svg.png" \
		-o "$@"

$(RSCDIR)/long-road.jpg:
	curl \
		"https://images.unsplash.com/photo-1583778957124-763fd4826122?q=80&w=500&h=2000&fmt=jpeg&fit=crop" \
		-o "$@"

$(RSCDIR)/road-sign.jpg:
	curl \
		"https://images.unsplash.com/photo-1530518618982-f7f23af0e533?q=80&w=500&h=2000&fmt=jpeg&fit=crop" \
		-o "$@"

$(RSCDIR)/crisp.jpg:
	curl \
		"https://images.unsplash.com/photo-1604565011092-c0fa4416f80f?q=80&w=500&h=2000&fmt=jpeg&fit=crop" \
		-o "$@"

$(OUTDIR)/%.pdf: \
	$(SRCDIR)/%.md \
	$(SRCDIR)/meerkatsstyle.tex \

	mkdir -p $(OUTDIR) && \
	HEADEREXT="$(SRCDIR)/overrides/$*.md.tex" && \
	echo "Building: $@: $^" && \
	pandoc --pdf-engine=xelatex \
		-t beamer \
		--include-in-header="$(COMMON_STYLE)" \
		`[ -f "$$HEADEREXT" ] && echo "--include-in-header=$$HEADEREXT"` \
		-o $@ \
		$<

$(RSCDIR)/all-images: \
	$(RSCDIR)/git-log.png \
	$(RSCDIR)/long-road.jpg \
	$(RSCDIR)/road-sign.jpg \
	$(RSCDIR)/crisp.jpg
	touch $@

all: \
	$(RSCDIR)/all-images \
	$(SOURCES:$(SRCDIR)/%.md=$(OUTDIR)/%.pdf)
