{
  description = "XDG specifications with manpages for the Base Directory Specification";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-25.11";
    nixpkgs-master.url = "github:NixOS/nixpkgs/d233902339c02a9c334e7e593de68855ad26c4cb";
    utils.url = "https://flakehub.com/f/numtide/flake-utils/0.1.102";
  };

  outputs =
    {
      self,
      nixpkgs,
      nixpkgs-master,
      utils,
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
      in
      {
        packages.default = pkgs.runCommand "xdg-manpages" { nativeBuildInputs = [ pkgs.scdoc ]; } ''
          mkdir -p $out/share/man/man7
          ${builtins.concatStringsSep "\n" (
            map (
              name: "scdoc < ${./doc/man + "/${name}.7.scd"} > $out/share/man/man7/${name}.7"
            ) manpages
          )}
        '';

        devShells.default = pkgs.mkShell {
          packages = [
            pkgs.scdoc
            pkgs-master.just
            pkgs.mandoc
          ];
        };
      }
    );
}
