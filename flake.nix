{
  description = "XDG specifications with manpages for the Base Directory Specification";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-25.11";
    nixpkgs-master.url = "github:NixOS/nixpkgs/567a49d1913ce81ac6e9582e3553dd90a955875f";
    utils.url = "https://flakehub.com/f/numtide/flake-utils/0.1.102";

    # igloo's overlay provides pkgs.gomod2nix (and its buildGoApplication
    # family) — a package plain nixpkgs does not carry. The eng-impure preset
    # (below) unconditionally enables the gomod2nix linter regardless of
    # whether a repo has a go.mod (the linter's own check self-gates on
    # go.mod at RUNTIME; igloo is needed just so the module can EVALUATE).
    # Used only to source pkgs for the conformist evals below — the rest of
    # this flake stays on plain nixpkgs.
    igloo.url = "https://code.linenisgreat.com/igloo/archive/master.tar.gz";
    igloo.inputs.nixpkgs-master.follows = "nixpkgs-master";

    # conformist provides the linter/formatter multiplexer, its Nix module
    # library (conformist.lib), and the eng-convention presets. Consumed from
    # the forge (linenisgreat/conformist) via the tarball form, matching the
    # doppelgang/circus fleet convention.
    conformist = {
      url = "https://code.linenisgreat.com/conformist/archive/master.tar.gz";
      inputs = {
        igloo.follows = "igloo";
        nixpkgs-master.follows = "nixpkgs-master";
        utils.follows = "utils";
      };
    };
  };

  outputs =
    {
      self,
      nixpkgs,
      nixpkgs-master,
      utils,
      igloo,
      conformist,
    }:
    utils.lib.eachDefaultSystem (
      system:
      let
        pkgs = import nixpkgs { inherit system; };
        pkgs-master = import nixpkgs-master { inherit system; };

        manpages = [
          "basedir-spec"
          "xdg_cache_home"
          "xdg_config_dirs"
          "xdg_config_home"
          "xdg_data_dirs"
          "xdg_data_home"
          "xdg_log_dirs"
          "xdg_log_home"
          "xdg_runtime_dir"
          "xdg_state_home"
        ];

        conformistPkg = conformist.packages.${system}.default;

        # igloo's flake path (legacyPackages), not the `import igloo {}`
        # shim: legacyPackages honors the nixpkgs-master follows above; the
        # shim reads igloo's own committed flake.lock and would silently
        # ignore it (igloo#37, conformist's own flake.nix does the same).
        pkgsIgloo = igloo.legacyPackages.${system};

        # Pure lane: the eng preset + this repo's overlay (./conformist.nix).
        # Drives `nix fmt` and the sandboxed `checks.formatting`.
        conformistEval = conformist.lib.evalModule pkgsIgloo {
          imports = [
            conformist.lib.presets.eng
            ./conformist.nix
          ];
          package = conformistPkg;
        };

        # Impure lane: the git-state checks (git-remotes, sweatfile,
        # agents-md, gomod2nix) run against the working tree via
        # `just lint-worktree`, where .git is available.
        conformistImpureEval = conformist.lib.evalModule pkgsIgloo {
          imports = [ conformist.lib.presets.eng-impure ];
          package = conformistPkg;
          projectRootFile = "flake.nix";
        };
      in
      {
        packages.default = pkgs.runCommand "xdg-manpages" { nativeBuildInputs = [ pkgs.scdoc ]; } ''
          mkdir -p $out/share/man/man7
          ${builtins.concatStringsSep "\n" (
            map (name: "scdoc < ${./doc/man + "/${name}.7.scd"} > $out/share/man/man7/${name}.7") manpages
          )}
        '';

        # The generated config for the impure lane's `just lint-worktree`.
        packages.conformist-impure-config = conformistImpureEval.config.build.configFile;

        # `nix fmt` runs conformist wrapped with the generated config
        # (conformistEval above).
        formatter = conformistEval.config.build.wrapper;

        checks.formatting = conformistEval.config.build.check self;

        devShells.default = pkgs.mkShell {
          packages = [
            pkgs.scdoc
            pkgs-master.just
            pkgs.mandoc
            conformistPkg
          ];
        };
      }
    );
}
