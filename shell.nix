{ pkgs ? import <nixpkgs> { } }:
let
  whatthepatch = p: p.callPackage ./release.nix { };
  pythonEnv = pkgs.python3.withPackages
    (p: [ p.pytest p.flake8 p.black p.build p.docutils (whatthepatch p) ]);
in pkgs.mkShell { packages = [ pythonEnv ]; }
