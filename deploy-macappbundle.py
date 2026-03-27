# Stdlib imports
import argparse
import os
import subprocess
import sys
from platform import machine as platform_machine
from shutil import which

# Library imports
from PyInstaller import __main__ as pyi

if sys.platform != "darwin":
    print("Deploying the macOS App is only possible on macOS; exiting...")
    sys.exit(1)

homebrew_prefix_or_none: str | None = os.environ.get("HOMEBREW_PREFIX")
assert homebrew_prefix_or_none is not None, (
    "HOMEBREW_PREFIX environment variable not set"
)
homebrew_prefix: str = homebrew_prefix_or_none
assert homebrew_prefix in os.environ["PATH"]

mednafen_or_none: str | None = which("mednafen")


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
    assert os.path.isfile(mednaffe), "mednaffe binary is not present"
    pyi_args: list[str] = [
        "./launch-macappbundle.py",
        "--icon",
        "share/icons/hicolor/128x128/apps/mednaffe.png",
        "--onedir",
        "--windowed",
        "--add-binary",
        f"{mednaffe}{os.pathsep}.",
        "--noconfirm",
    ]
    if include_mednafen:
        assert mednafen_or_none is not None, "mednafen binary is not present"
        mednafen: str = mednafen_or_none
        pyi_args += [
            "--name",
            "Mednaffe+Mednafen",
            "--add-binary",
            f"{mednafen}{os.pathsep}.",
        ]
    else:
        pyi_args += [
            "--name",
            "Mednaffe",
        ]
    pyi.run(pyi_args)


def compress(include_mednafen: bool = False):
    ver: str = ""
    with open("configure", "r") as f:
        ver_line: str = ""
        for line in f.readlines():
            if "PACKAGE_VERSION" in line:
                ver_line = line
                break
        if ver_line:
            print(ver_line)
            ver = ver_line.split("=")[1].replace("'", "").strip()
    machine: str = platform_machine().replace("arm64", "aarch64")
    pkgname: str = f"mednaffe-{ver}-macos1-macOS-{machine}.tar.xz"
    appname: str = "Mednaffe.app"
    if include_mednafen:
        mednafen_info: list[str] = (
            subprocess.run(("mednafen",), check=False, capture_output=True)
            .stdout.decode()
            .splitlines()
        )
        mednafen_version: str = (
            mednafen_info[0].replace("Starting Mednafen", "").strip()
        )
        pkgname = pkgname.replace(
            f"mednaffe-{ver}-macos1",
            f"mednaffe-{ver}-macos1+mednafen-{mednafen_version}",
        )
        appname = "Mednaffe+Mednafen.app"
    os.chdir("dist")
    env: dict[str, str] = os.environ.copy()
    env["XZ_OPT"] = f"-T{os.cpu_count()}"
    try:
        subprocess.run(("tar", "-cJvf", pkgname, appname), env=env)
    except subprocess.CalledProcessError as e:
        print(f"could not create compressed package: {e}")
        sys.exit(1)
    os.chdir("..")


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
    parser.add_argument(
        "--compress",
        action="store_true",
        help="create package archive",
    )
    in_args: argparse.Namespace = parser.parse_args()

    if in_args.build:
        configure()
        build()

    bundle(in_args.include_mednafen)

    if in_args.compress:
        compress(in_args.include_mednafen)


if __name__ == "__main__":
    main()
