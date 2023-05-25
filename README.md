## About tails-mvt

[**Tails-MVT**](https://github.com/ztychr/tails) is a customized version of [Tails](https://tails.net/) that has the [Mobile Verification Toolkit](https://github.com/mvt-project/mvt) preinstalled and working out of the box.

### Setup
To use [Tails-MVT](https://github.com/ztychr/tails), download the latest release under releases, or build the image from source. To build [tails-mvt](https://github.com/ztychr/tails) from source, see [Building a Tails image](https://tails.boum.org/contribute/build/).

#### Creating an installation media
After obtaining the image, flash it to a USB drive or SD card in order to create a bootable media. To do so, use your preferred image flashing utility. If flashing from Linux, you can use [balenaEtcher](https://etcher.balena.io/), `gnome-disk-utility` or `dd` as described in [Install Tails from Linux](https://tails.boum.org/install/linux/index.en.html). If flashing from Windows or macOS, you can use [balenaEtcher](https://etcher.balena.io/) as described in [Install Tails from Windows](https://tails.boum.org/install/windows/index.en.html) and [Install Tails from Windows](https://tails.boum.org/install/mac/index.en.html).

#### Booting tails
Once the media has been flashed, insert it into the laptop from which the analysis shall be conducted. Press f12 (may vary from manufactorer) in order to select the USB media as a boot option. You may need to disable secure boot and enable Legacy mode in the BIOS settings. Once the image has booted, press **Start Tails**.

### Analysing Android devices

#### Preparing the Android device
To analyze an Android device, the developer options and USB debugging need to be enabled. On the device, head to the **Settings** -> **About phone** and press the build number several times. Once the developer options are enabled, enable USB Debugging from within **Settings** -> **System** -> **Developer options** and toggle **USB debugging**. Once the Desktop is showing, proceed to the next step.

#### Perform analysis
To analyse your device, connect it to the laptop with compatible cable of good quality. Make sure it is unlocked before starting the analysis. Press the Windows or Super button on the keyboard and search for terminal or selt it from **Applications** -> **Utilities** -> **Terminal**. Once the terminal is open, `mvt-android check-adb`. 

A prompt will appear on the Android device asking whether to trust this PC. Toggle **Always allow from this computer** and press **Allow**.

Next, a prompt will show asking whether to allow a full backup. Press **Back up my data**.
The analysis will now run and match the indicators of compromised provided by [Mobile Verification Toolkit](https://github.com/mvt-project/mvt).

**IMPORTANT**
Not finding any indications of compromise does **NOT** mean the device is not infected. It just means that the public indicators of compromise was not matched with stored data on your phone. The indicators are derived from forensic work and publicly available. This means the the spyware authors have access to them as well, and can rule them out of future infections.

#### Debugging
You may run into an error stating **Device is busy, maybe run `adb kill-server` and try again**. Type `killall adb` and try again. If the problem persists. Try unplugging the phone and try again. You may also try the command `adb kill-server`, however we found that `killall adb` works in the majority of cases.

### Analysing iOS devices
