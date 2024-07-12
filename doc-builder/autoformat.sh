#!/usr/bin/env bash
set -e

BASEDIR=$(dirname "$0")
cd $BASEDIR

echo "=== ISort ==="
python -m isort \
	--py 39 \
	--profile="black" \
	--skip-gitignore \
	--ls \
	--ac \
	.

echo "=== Black ==="
python -m black  \
	-S \
        -l 100 \
        -t py311 \
        .
