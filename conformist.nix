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
{ lib, ... }:
{
  programs.nixfmt.enable = true;

  linters = {
    statix.enable = true;
    deadnix.enable = true;
    # xdg is versionless by design: zero tags, no version literals, and eng
    # consumes it as a rev-pinned master tarball — nothing here versions
    # independently of the repo itself. conformist v0.1.19 fixed the
    # eng-versioning trigger gate (conformist#92) so the linter now FAILS a
    # flake-bearing repo with no version.env instead of silently skipping;
    # under the fleet policy ("adopt version.env where a version exists"),
    # xdg is the versionless case and opts out explicitly. Tracked at xdg#2
    # — re-enable by adopting version.env if a release process ever lands.
    eng-versioning.enable = lib.mkForce false;
  };

  settings.excludes = [
    "*.md"
    "flake.lock"
    "LICENSE*"
    "result"
    "result-*"
  ];
}
