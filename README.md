# decrypt0r
## Automatically download and decrypt SecureRom stuff (iBSS, iBEC, iBoot, etc.) for all iOS versions available

### Intro
decrypt0r automatically downloads all relevant firmware files for all available iOS versions (for the connected device) via remotezip and decrypts them via ipwndfu and img4.

### How do I decrypt0r?
First of all: decrypt0r assumes that you have [img4](https://github.com/xerub/img4lib) and [irecovery](https://github.com/libimobiledevice/libirecovery) installed and exported to your $PATH.

Also make sure to install the requirements for this script:

>  pip3 install -r requirements.txt

Further you need to set [ipwndfu_path](https://github.com/shinvou/decrypt0r/blob/master/decrypt0r.py#L12) to your ipwndfu folder path.

If your device is in pwned dfu mode you are ready to go.

>  python3 decrypt0r.py

You'll find the decrypted files in the associated folder for each firmware. You'll also find a json file containing decryption info (keybag, iv, key, ivkey) for each decrypted file.

If you want to download and decrypt a specific iOS version you can use the following command:

> python3 decrypt0r.py -fw 12.0

*NOTE: If this tool fails, just re-run it. I implemented some sanity checks so that not every firmware gets decrypted again.*

### How do I get?
You should know that.

### How do I compile?
/

### License?
Pretty much the BSD license, just don't repackage it and call it your own please!

Also if you do make some changes, feel free to make a pull request and help make things more awesome!

### Contact Info?
If you have any support requests please feel free to email me at shinvou[at]gmail[dot]com.

Otherwise, feel free to follow me on twitter: [@biscoditch](https:///www.twitter.com/biscoditch)!

### Special Thanks
- xerub for img4lib
- Callum Jones for ipsw.me
- axi0mX for ipwndfu
- Nikias Bassen for irecovery
