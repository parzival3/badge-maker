# Build the documents in this folder, with the fonts they expect.
#
#   nix-shell --run build          # compile every .typ here to a .pdf
#   nix-shell --run "build volunteering-at-chimalaya-nepal.typ"
#   nix-shell --run watch          # recompile on save
#   nix-shell                      # drop into a shell with typst on PATH
#
# Typst is given the repository root so documents can reach the template and
# logo in ../templates, and TYPST_FONT_PATHS supplies Inter (the brand face)
# and Noto Sans Devanagari without installing anything system-wide.

{ pkgs ? import <nixpkgs> { } }:

let
  fonts = pkgs.symlinkJoin {
    name = "chimalaya-document-fonts";
    paths = [ pkgs.inter pkgs.noto-fonts ];
  };

  # Resolved from this file's own location, so the commands work from any
  # working directory and do not depend on the checkout being a git clone.
  docs = toString ./.;
  root = toString ./..;

  build = pkgs.writeShellScriptBin "build" ''
    set -euo pipefail
    cd ${docs}
    targets=( "$@" )
    if [ ''${#targets[@]} -eq 0 ]; then targets=( *.typ ); fi
    for f in "''${targets[@]}"; do
      out="''${f%.typ}.pdf"
      echo "typst: $f -> $out"
      ${pkgs.typst}/bin/typst compile --root ${root} "$f" "$out"
    done
  '';

  watch = pkgs.writeShellScriptBin "watch" ''
    set -euo pipefail
    cd ${docs}
    f="''${1:-volunteering-at-chimalaya-nepal.typ}"
    exec ${pkgs.typst}/bin/typst watch --root ${root} "$f" "''${f%.typ}.pdf"
  '';

in
pkgs.mkShell {
  packages = [ pkgs.typst fonts build watch ];

  # Typst reads this instead of fontconfig, so the result does not depend on
  # which fonts happen to be installed on the machine.
  TYPST_FONT_PATHS = "${fonts}/share/fonts";

  shellHook = ''
    echo "typst $(${pkgs.typst}/bin/typst --version | cut -d' ' -f2) · fonts: Inter, Noto Sans Devanagari"
    echo "commands: build [file.typ]   watch [file.typ]"
  '';
}
