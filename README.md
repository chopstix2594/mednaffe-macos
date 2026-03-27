## Mednaffe
Mednaffe is a front-end (GUI) for [mednafen emulator](https://mednafen.github.io/ "mednafen emulator")

Its main features are:

 * It is written in C language.
 * Available for Linux, Windows, and macOS.
 * The only dependency is GTK 3.
   * The macOS App adds Python 3 as a dependency, along with the following pip libraries:
    * PyInstaller
    * std-nslog
    * Pillow
    * darkdetect
 * GPLv3 licensed.

#### Downloads - Version 0.9.3
 * You can download Mednaffe [here](https://github.com/AmatCoder/mednaffe/releases/latest "Downloads").
 * You can read the changelog [here](https://github.com/AmatCoder/mednaffe/blob/master/ChangeLog "ChangeLog").
 * [Flatpak](https://flathub.org/apps/details/com.github.AmatCoder.mednaffe) is available for Linux users.
 * [App](https://github.com/chopstix2594/mednaffe-macos/releases/latest) is available for macOS users; two versions are available:
    * A version which includes Mednafen itself (1.32.1 at time of writing)
    * A version which runs a system installation of Mednafen, which can be installed from [Homebrew](https://brew.sh) or [MacPorts](https://www.macports.org/) or built from the source.
      * More specifically, the following paths will be searched for Mednafen's executable:
        * `$HOME/.local/bin` - create a symlink here if your installation is not in any of the following paths
        * `/usr/local/bin`
        * `/opt/homebrew/bin`
        * `/opt/homebrew/opt/mednafen/bin`
        * `/usr/local/opt/mednafen/bin`
        * `/opt/local/bin`
        * `/opt/local/sbin`
   * macOS's gatekeeper may block the app from running; allow the app in System Settings -> Privacy & Security or run `xattr -d com.apple.quarantine <APP>` on the app in a terminal if this is the case.

*Note: Mednaffe only works with 1.22.1 or higher versions of mednafen emulator.*

#### Screenshots

###### Linux/GTK 3

![Mednaffe on Linux/GTK 3](https://github.com/AmatCoder/mednaffe/blob/wiki/mednaffe-0.9.0-linux.png "Mednaffe on Linux/GTK 3")

![Mednaffe on Linux/GTK 3](https://github.com/AmatCoder/mednaffe/blob/wiki/mednaffe-0.9.0-linux2.png "Mednaffe on Linux/GTK 3")

###### Windows

![Mednaffe on Windows 7](https://github.com/AmatCoder/mednaffe/blob/wiki/mednaffe-0.9.0-windows.png "Mednaffe on Windows 7")

![Mednaffe on Windows 7](https://github.com/AmatCoder/mednaffe/blob/wiki/mednaffe-0.9.0-windows2.png "Mednaffe on Windows 7")

###### macOS

![Mednaffe on macOS 26 Tahoe](https://github.com/chopstix2594/mednaffe-macos/blob/wiki/mednaffe-0.9.3-macos.png "Mednaffe on macOS 26 Tahoe")
![Mednaffe on macOS 26 Tahoe](https://github.com/chopstix2594/mednaffe-macos/blob/wiki/mednaffe-0.9.3-macos2.png "Mednaffe on macOS 26 Tahoe")
