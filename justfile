default: lint build

build: build-nix

# Render every doc/man/*.7.scd to result/share/man/man7/*.7 with scdoc.
build-nix:
    nix build --show-trace

lint: lint-fmt

# Read-only formatting + the eng preset's file-based linters (justfile-*,
# eng-versioning, flake-outputs/lock), via the sandboxed checks.formatting
# derivation. Does NOT modify files — the modifying counterpart is
# `codemod-fmt`.
#
# check formatting and the eng file-based linters
lint-fmt:
    #!/usr/bin/env bash
    set -euo pipefail
    system=$(nix eval --raw --impure --expr 'builtins.currentSystem')
    nix build ".#checks.${system}.formatting" --no-link --print-build-logs

lint-impure: lint-worktree

# The impure eng checks (git-remotes, sweatfile, agents-md) against the
# working tree, where .git is available. Runs conformist from the devShell
# (direnv `use flake`).
#
# run the impure eng conformist checks against the working tree
lint-worktree:
    #!/usr/bin/env bash
    set -euo pipefail
    cfg=$(nix build --no-link --print-out-paths '.#conformist-impure-config')
    conformist check --config-file "$cfg" --tree-root .

codemod-fmt: codemod-fmt-tree

# Format the tree in place (repair mode) via `nix fmt`.
codemod-fmt-tree:
    nix fmt

clean: clean-build

# Remove the built manpages output link.
clean-build:
    rm -rf result
