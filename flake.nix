{
  description = "Flake to manage python workspace";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/master";
    flake-utils.url = "github:numtide/flake-utils";
    mach-nix.url = "github:DavHau/mach-nix?ref=3.3.0";
  };

  outputs = { self, nixpkgs, flake-utils, mach-nix }:
    flake-utils.lib.eachDefaultSystem (system:
    let
      python = "python310";
      pkgs = nixpkgs.legacyPackages.${system};
      mach-nix-wrapper = import mach-nix { inherit pkgs python; };
      requirements = ''
        click
        colorama
        contourpy
        cycle
        Flask
        fonttool
        greenlet
        itsdangerous
        Jinja2
        joblib
        kiwisolver
        MarkupSafe
        matplotlib
        numpy
        packaging
        pandas
        Pillow
        pyparsing
        python-dateutil
        pytz
        scikit-learn
        scipy
        seaborn
        six
        SQLAlchemy
        threadpoolctl
        Werkzeug
      '';
      pythonBuild = mach-nix-wrapper.mkPython { inherit requirements; };
    in {
      devShell = pkgs.mkShell {
        buildInputs = [
          (pkgs.${python}.withPackages
            (ps: with ps; [ pip black pyflakes isort ]))
          pkgs.nodePackages.pyright
          pkgs.glpk
          pythonBuild
        ];
      };
    });
}