# xdg

A personal fork of the freedesktop.org [XDG Base Directory
Specification](https://specifications.freedesktop.org/basedir-spec/latest/),
trimmed down to the parts that are actively maintained here:

- `doc/man/` — `scdoc` sources for `man 7` pages covering the base directory
  variables (`XDG_CONFIG_HOME`, `XDG_DATA_HOME`, …), including the proposed
  `XDG_LOG_HOME` / `XDG_LOG_DIRS`.
- `basedir/basedir-spec.xml` — the DocBook spec, extended with the
  `XDG_LOG_HOME` / `XDG_LOG_DIRS` additions.
- `docs/plans/` — design notes behind those additions.

The upstream website builder, the other freedesktop specifications, and the
`fhs` / `mpris` submodules have been removed; this repository is not used to
build <https://specifications.freedesktop.org/>.

## Building the manpages

```bash
nix build      # or: just build
```

The default flake package renders every `doc/man/*.7.scd` to
`result/share/man/man7/*.7` with `scdoc`.

## Licenses

See `LICENSE.CC-BY-SA-4.0` and `LICENSE.LGPL-3.0`.
