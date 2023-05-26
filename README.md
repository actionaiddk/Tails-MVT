## About Tails-MVT

[**Tails-MVT**](https://github.com/ztychr/tails) is a customised version of [Tails](https://tails.net/) that has the [Mobile Verification Toolkit](https://github.com/mvt-project/mvt) preinstalled and working out of the box. Tails-MVT is meant for non-advanced users. If you have a technical background, you may want to setup [MVT](https://github.com/mvt-project/mvt) yourself and follow the official [MVT Documentation](https://docs.mvt.re/en/latest/).

#### ⚠️ **IMPORTANT** ⚠️ ####
Not finding any indications of compromise does **NOT** mean your device is not infected. It just means that the public indicators of compromise was not matched with data extracted from your phone. The indicators are derived from forensic work and publicly available. This means the the spyware authors have access to them as well, and can rule them out of future spyware.

### 1. Setup
To use [Tails-MVT](https://github.com/ztychr/tails), download the latest release under releases or build the image from source. To build [Tails-MVT](https://github.com/ztychr/tails) from source, see [Building a Tails image](https://tails.boum.org/contribute/build/).

#### 1.1 Creating an installation media
After obtaining the image, flash it to a USB drive or SD card in order to create a bootable media. To do so we recommend using [balenaEtcher](https://etcher.balena.io/). If flashing from Linux, you can use [balenaEtcher](https://etcher.balena.io/), `gnome-disk-utility` or `dd` as described in [Install Tails from Linux](https://tails.boum.org/install/linux/index.en.html). If flashing from Windows or macOS, use can use [balenaEtcher](https://etcher.balena.io/) as described in [Install Tails from Windows](https://tails.boum.org/install/windows/index.en.html) and [Install Tails from macOS](https://tails.boum.org/install/mac/index.en.html).

#### 1.2 Booting Tails-MVT
Once the image has been flashed to the media, insert it into the laptop from which the analysis shall be conducted. Press **f12** during boot (may vary from manufactorer) in order to select the USB media from boot options. You may need to disable secure boot and, or enable legacy mode in the BIOS settings. Once the image has booted, press **Start Tails**.

### 2. Analyzing Android devices

#### 2.1 Preparing the Android device
To analyse an Android device, the **developer options** and **USB debugging** need to be enabled. On the device, head to the **Settings** -> **About phone** and press the build number several times. Once the developer options are enabled, enable USB Debugging from within **Settings** -> **System** -> **Developer options** and toggle **USB debugging**.

#### 2.2 Perform analysis
To analyse your device, connect it to the laptop with a compatible cable. A cable of good quality is advised. Make the phone is turned on and unlocked Press the Windows or Super button on the keyboard and search for terminal or select it from the menu in the upper left corner: **Applications** -> **Utilities** -> **Terminal**. Once the terminal is open, type `mvt-android check-adb` and hit enter.

A prompt will appear on the Android device asking whether to trust this PC. Toggle **Always allow from this computer** and press **Allow**.

Next, a prompt will show asking whether to allow a full backup. Press **Back up my data**.
The analysis will now run and analyse the data with the indicators of compromised provided by [Mobile Verification Toolkit](https://github.com/mvt-project/mvt).

#### 2.3 Error handling
You may run into an error stating **Device is busy, maybe run `adb kill-server` and try again**. Type `killall adb` and try again. If the problem persists. Try unplugging the phone and redoing the steps again. You may also try the command `adb kill-server`, however we found that `killall adb` works in the majority of cases.

### 3. Analysing iOS devices

#### 3.1 Preparing folders
To analyse an iOS device, create a folder structure according to the one listed below. It can be done through the File Explorer found under **Applications** -> **Accessories** -> **Files** or by opening a terminal and typing `mkdir -p ios/backup ios/backup-decrypted ios/result`.

To open a terminal, press the Windows or Super button on the keyboard and search for terminal or select it from **Applications** -> **Utilities** -> **Terminal**

```
ios/
├── backup
├── backup-decrypted
└── result
```

#### 3.2 Create backup
Now connect your iOS device with a compatible cable and make sure it is unlocked. A prompt on the iOS device will show asking whether to trust this computer. Press **Trust**.

In the terminal type `idevicebackup2 -i encryption on`. You will be asked to enter a new backup password. Enter a password of your selection and make sure to remember it. If the password is already set previously, make sure you have the password ready. If the password is set but you don't know it, you may try to reset it by following the following steps described in the [MVT documentation](https://docs.mvt.re/en/latest/ios/backup/libimobiledevice/).

To create a backup, enter the following command in the terminal:

`idevicebackup2 backup --full ios/backup`

#### 3.3 Decrypt backup
To decrypt the backup, type the following command and replace <password> with the decryption password for you device backup. The <long string of numbers> will vary and you may autocomplete the command by pressing Tab on the keyboard.
  
`mvt-ios decrypt-backup -p <password> -d ios/backup-decrypted ios-analysis/backup/<long string of numbers>`

#### Perform analysis
 To check the backup, run the following command
  
 `mvt-ios check-backup --output ios/results ios/backup-decrypted`

The analysis will now run and analyse the data with the indicators of compromised provided by [Mobile V\
erification Toolkit](https://github.com/mvt-project/mvt).

### 4. Update indicators of compromise
To update the indicators of compromise, make sure the laptop is online through either WiFi or cabled connection. Once connected, a window with the title **Tor Connection** will appear. Toggle **Connect to Tor automatically** and press **Connect to Tor**. Once the connection is established, open a terminal and type `torify mvt-android download-iocs`and `torify mvt-ios download-iocs`.

Note that the indicators of compromise are reset for every reboot and will need updating again. We try to release a new image when new indicators are published to support offline complete offline analysis.
