# xdg's conformist overlay, merged with conformist.lib.presets.{eng,eng-impure}
# in flake.nix (conformist.lib.evalModule — the pure lane imports presets.eng
# + this file; the impure lane imports presets.eng-impure alone). presets.eng
# enables the eng-convention linters (eng-versioning, flake-outputs/lock, the
# justfile-* roster); presets.eng-impure carries the git-state lane
# (git-remotes, git-default-branch, sweatfile, agents-md, gomod2nix). xdg is a
# Nix + scdoc/DocBook prose repo (no Go, no Rust), so nixfmt plus the
# statix/deadnix Nix linters are the relevant roster here — both are safe to
# enable as of conformist commit be54c5b (see igloo's conformist.nix /
# igloo#87, igloo#88 for the upstream crashes that predated that fix). Here
# live nixfmt, statix, deadnix, the eng-versioning key, and repo-specific
# excludes.
_: {
  programs.nixfmt.enable = true;

  linters = {
    statix.enable = true;
    deadnix.enable = true;
    # xdg has neither go.mod nor Cargo.toml at the tree root, so
    # eng-versioning(7) can't derive the key; pin it explicitly, matching the
    # fleet convention (doppelgang/circus/igloo all pin explicitly). xdg has
    # no version.env yet — nothing here versions independently of the repo
    # itself — so this check is currently inert; see the adoption commit
    # message for details.
    eng-versioning.key = "XDG_VERSION";
  };

  settings.excludes = [
    "*.md"
    "flake.lock"
    "LICENSE*"
    "result"
    "result-*"
  ];
}
