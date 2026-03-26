# Stdlib imports
import argparse
import os
import shutil
import subprocess
import sys

# Library imports
from PyInstaller import __main__ as pyi

homebrew_prefix_or_none: str | None = os.environ.get("HOMEBREW_PREFIX")
assert homebrew_prefix_or_none is not None, (
    "HOMEBREW_PREFIX environment variable not set"
)
homebrew_prefix: str = homebrew_prefix_or_none
assert homebrew_prefix in os.environ["PATH"]

mednafen_or_none: str | None = shutil.which("mednafen")


def configure():
    try:
        subprocess.run(("./configure",))
    except subprocess.CalledProcessError as e:
        print(f"configure failed: {e}")
        sys.exit(1)


def build():
    try:
        subprocess.run(("make", f"-j{os.cpu_count()}"))
    except subprocess.CalledProcessError as e:
        print(f"make failed: {e}")
        sys.exit(1)


def bundle(include_mednafen: bool = False):
    mednaffe: str = "./src/mednaffe"
    assert os.path.isfile(mednaffe), "mednaffe binary is present"
    pyi_args: list[str] = [
        "./launch-macappbundle.py",
        "--name",
        "Mednaffe",
        "--icon",
        "share/icons/hicolor/128x128/apps/mednaffe.png",
        "--onedir",
        "--windowed",
        "--add-binary",
        f"{mednaffe}{os.pathsep}.",
        "--noconfirm",
    ]
    if include_mednafen:
        assert mednafen_or_none is not None, "mednafen binary is present"
        mednafen: str = mednafen_or_none
        pyi_args += [
            "--add-binary",
            f"{mednafen}{os.pathsep}.",
        ]
    pyi.run(pyi_args)


def main():
    parser = argparse.ArgumentParser(description="deploy mednaffe as macOS app bundle")
    parser.add_argument(
        "--build",
        "-B",
        action="store_true",
        help="automatically (re)compile mednaffe before bundle creation",
    )
    parser.add_argument(
        "--include-mednafen",
        action="store_true",
        help="include mednafen binary directly in the bundle",
    )
    in_args: argparse.Namespace = parser.parse_args()

    if in_args.build:
        configure()
        build()

    bundle(in_args.include_mednafen)


if __name__ == "__main__":
    main()
