# decrypt0r
## Automatically download and decrypt SecureRom stuff (iBSS, iBEC, iBoot, etc.) for all iOS versions available

### Intro
decrypt0r automatically downloads all relevant firmware files of all available iOS versions (for one specified device type) via partialzip and decrypts them via ipwndfu.

### How do I decrypt0r?
First of all: decrypt0r assumes that you have  [img4](https://github.com/xerub/img4lib/) and  [partialzip](https://github.com/marcograss/partialzip) installed and exported to your $PATH.

Make sure to install the requirements for this script:

>  pip install requests

Now make sure that you correctly set [ipwndfu_path](https://github.com/shinvou/decrypt0r/blob/master/decrypt0r.py#L11) to the path where you have your ipwndfu folder and that you set [device_type](https://github.com/shinvou/decrypt0r/blob/master/decrypt0r.py#L10) to the device you'll be using this script for.

If your device is in pwned dfu mode you can run the script.

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
