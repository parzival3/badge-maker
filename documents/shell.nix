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

  # nix-shell exports SOURCE_DATE_EPOCH=315532800 (1 Jan 1980) for reproducible
  # builds, and typst honours it: every PDF came out stamped 1980, and
  # datetime.today() returned 1980 inside documents. Use the real clock.
  realClock = ''export SOURCE_DATE_EPOCH="$(date +%s)"'';

  build = pkgs.writeShellScriptBin "build" ''
    set -euo pipefail
    ${realClock}

    # -o takes a directory (PDFs are named after the source) or a single
    # output file. Without it, each PDF lands beside its .typ.
    dest=""
    while [ $# -gt 0 ]; do
      case "$1" in
        -o|--output) dest="$2"; shift 2 ;;
        -h|--help)
          echo "usage: build [-o DIR|FILE.pdf] [file.typ ...]"; exit 0 ;;
        *) break ;;
      esac
    done

    cd ${docs}
    targets=( "$@" )
    if [ ''${#targets[@]} -eq 0 ]; then targets=( *.typ ); fi

    if [ -n "$dest" ] && [ ''${#targets[@]} -gt 1 ] && [ "''${dest%.pdf}" != "$dest" ]; then
      echo "build: -o FILE.pdf needs exactly one input, got ''${#targets[@]}" >&2
      exit 1
    fi

    for f in "''${targets[@]}"; do
      if [ -z "$dest" ]; then
        out="''${f%.typ}.pdf"
      elif [ "''${dest%.pdf}" != "$dest" ]; then
        out="$dest"
      else
        mkdir -p "$dest"
        out="$dest/''${f%.typ}.pdf"
      fi
      echo "typst: $f -> $out"
      ${pkgs.typst}/bin/typst compile --root ${root} "$f" "$out"
    done
  '';

  watch = pkgs.writeShellScriptBin "watch" ''
    set -euo pipefail
    ${realClock}
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
    ${realClock}
    echo "typst $(${pkgs.typst}/bin/typst --version | cut -d' ' -f2) · fonts: Inter, Noto Sans Devanagari"
    echo "commands: build [-o DIR|FILE.pdf] [file.typ]   watch [file.typ]"
  '';
}
