import sys

frozen: bool = getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS")
if frozen:
    import nslog  # noqa: F401

import os  # noqa: E402
import subprocess  # noqa: E402

if frozen:
    here = sys._MEIPASS  # type: ignore
else:
    here = os.path.dirname(os.path.abspath(__file__))


def main():
    bin: str
    env: dict[str, str] = os.environ.copy()
    if frozen:
        if os.path.isfile(f"{here}/mednafen"):
            print("mednafen included in bundle, using bundled version", flush=True)
            env["PATH"] = here + os.pathsep + env["PATH"]
        else:
            print(
                "mednafen not included in bundle, searching for system version",
                flush=True,
            )
            path_guesses: list[str] = [
                f"{os.path.expanduser('~')}/.local/bin",
                "/usr/local/bin",
                "/opt/homebrew/bin",
                "/opt/homebrew/opt/mednafen/bin",
                "/usr/local/opt/mednafen/bin",
                "/opt/local/bin",
                "/opt/local/sbin",
            ]
            env["PATH"] = os.pathsep.join(path_guesses) + os.pathsep + env["PATH"]
    if frozen:
        bin = f"{here}/mednaffe"
    else:
        bin = f"{here}/src/mednaffe"

    try:
        subprocess.run((bin,), env=env, capture_output=True)
    except subprocess.CalledProcessError as e:
        print("could not run mednaffe: " + e.stdout.decode())


if __name__ == "__main__":
    main()
