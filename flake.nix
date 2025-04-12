{
  description = "A simple bot made for the Minearchy Discord server";

  inputs = {
    systems.url = "github:nix-systems/default";
    nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
  };

  outputs = { systems, nixpkgs, ... }: let
      inherit (nixpkgs) lib;

    eachSystem = lib.genAttrs (import systems);
  in {
    packages = eachSystem (system: let
      pkgs = import nixpkgs { inherit system; };

      pypkgs = pkgs.python313Packages;
    in rec {
      default = minearchy-bot;

      minearchy-bot = pypkgs.buildPythonApplication {
        pname   = "minearchy-bot";
        version = "0.0.1";

        src    = ./.;
        format = "pyproject";

        build-system = [ pypkgs.setuptools ];

        dependencies = [
          pypkgs.discordpy
          # TODO: pypkgs.jishaku
          pypkgs.mcstatus
        ];

        meta.mainProgram = "minearchy-bot";
      };

      minearchy-bot-container = pkgs.dockerTools.buildImage {
        name = "minearchy-bot";
        tag  = "latest";

        copyToRoot = pkgs.buildEnv {
          name = "image-root";
          
          pathsToLink = [ "/bin" ];
          paths       = [
            pkgs.uutils-coreutils-noprefix
            minearchy-bot
          ];
        };

        config.Env        = [ "PATH=/bin" ];
        config.WorkingDir = "/minearchy-bot";
        config.Cmd        = lib.getExe minearchy-bot;
      };
    });
  };
}
