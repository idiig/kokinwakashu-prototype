{
  description = "kokinwakashu-prototype — Kokinwakashu TEI reference data";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
      in
      {
        devShells.default = pkgs.mkShell {
          buildInputs = with pkgs; [
            python3
            uv
            libxml2   # xmllint for validation
          ];

          shellHook = ''
            if [ -f pyproject.toml ]; then
              uv sync --quiet
            fi
          '';
        };
      });
}
