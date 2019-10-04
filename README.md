# decrypt0r
## Automatically download and decrypt SecureRom stuff (iBSS, iBEC, iBoot, etc.) for all iOS versions available

### Intro
decrypt0r automatically downloads all relevant firmware files of all available iOS versions (for one specified device type) via partialzip and decrypts them via ipwndfu.

### How do I decrypt0r?
First of all: decrypt0r assumes that you have  [img4](https://github.com/xerub/img4lib),  [partialzip](https://github.com/marcograss/partialzip) and [irecovery](https://github.com/libimobiledevice/libirecovery) installed and exported to your $PATH.

Make sure to install the requirements for this script:

>  pip install requests

Now make sure that you correctly set [ipwndfu_path](https://github.com/shinvou/decrypt0r/blob/master/decrypt0r.py#L11) to the path where you have your ipwndfu folder at.

If your device is in pwned dfu mode you can run the script. It'll automatically detect the device type.
You can also download and decrypt just a single firmware by passing the -fw flag with desired fw version.

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
- Marco Grassi for partialzip
- xerub for img4lib
- Callum Jones for ipsw.me
- axi0mX for ipwndfu
- Nikias Bassen for irecovery
