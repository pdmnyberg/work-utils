#!/bin/bash
CURDIR=`dirname "${BASH_SOURCE[0]}"`
SRCDIR="src"
OUTDIR="output"

pushd "$CURDIR"  # Entering presentations working directory

mkdir -p "$OUTDIR"

curl \
    "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Git-logo.svg/1024px-Git-logo.svg.png" \
    -o "resources/git-logo.png"
curl \
    "https://images.unsplash.com/photo-1583778957124-763fd4826122?q=80&w=500&h=2000&fmt=jpeg&fit=crop" \
    -o "resources/long-road.jpg"

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