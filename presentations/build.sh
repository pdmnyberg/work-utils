#!/bin/bash
CURDIR=`dirname "${BASH_SOURCE[0]}"`
SRCDIR="src"
OUTDIR="output"

pushd "$CURDIR"  # Entering presentations working directory

mkdir -p "$OUTDIR"

curl \
    https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Git-logo.svg/1024px-Git-logo.svg.png \
    -o "resources/git-logo.png"

for filepath in $SRCDIR/*.md; do
    FILENAME=$(basename "$filepath") &&
    OUTFILE="$OUTDIR/$FILENAME.pdf" &&
    HEADEREXT="$SRCDIR/overrides/$FILENAME.tex" &&
    echo "Building: $OUTFILE" &&
    pandoc \
        -t beamer \
        --include-in-header="$SRCDIR/meerkatsstyle.tex" \
        `[[ -f "$HEADEREXT" ]] && echo "--include-in-header=$HEADEREXT"` \
        -o "$OUTFILE" \
        "$filepath" 
done

popd  # Exiting presentations working directory