#!/usr/bin/env python3

import json
import requests
import sys, subprocess, os, shutil
import argparse
from remotezip import RemoteZip

header = {'Accept': 'application/json'}
api_base_url = 'https://api.ipsw.me/v4/'

ipwndfu_path = '/Users/shinvou/Desktop/SecureRom/ipwndfu_public/'

location_of_me = os.path.dirname(os.path.realpath(__file__))

def get_device_type():
    output = str(subprocess.run(['irecovery', '-m', '-v'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT).stdout.strip(), 'utf-8').split('\n')
    
    if 'DFU Mode' not in output:
        sys.exit('[!] No device in DFU mode found')
    
    device_type = output[4].split()[2][:-1]

    print('[*] Found ' + device_type + ' in DFU mode')

    return device_type

def get_device_info(device_type):
    api_url = '{0}/device/{1}?type=ipsw'.format(api_base_url, device_type)

    response = requests.get(api_url, headers=header)

    if response.status_code == 200:
        return json.loads(response.content.decode('utf-8'))
    else:
        sys.exit('[!] API error')

def list_files(url):
    files_to_process = []

    with RemoteZip(url) as zip:
        for zip_info in zip.infolist():
            path = zip_info.filename

            if 'sep' in path:
                continue

            if 'kernelcache' in path:
                files_to_process.append(path)
            
            if path.endswith('im4p'):
                files_to_process.append(path)
    
    files_to_process.sort()

    return files_to_process

def download_file(url, file, real_filename):
    with RemoteZip(url) as zip:
        zip.extract(file)
    
    os.rename(file, real_filename)

    if os.path.isdir(file.split('/')[0]):
        shutil.rmtree(file.split('/')[0])

def decrypt_file(file, decryption_info):
    keybag = str(subprocess.run(['img4', '-i', file, '-b'], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL).stdout.strip(), 'utf-8').split('\n')[0]
    
    if not keybag:
        print('      [*] We don\'t need to decrypt', file)
        new_path = 'unencrypted/' + file

        if 'kernelcache' in new_path:
            new_path += '.im4p'

        os.rename(file, new_path)
        print('      [*] Moved to', new_path)
        return
    else:
        print('      [*] Got keybag:', keybag)
        ivkey = str(subprocess.run([ipwndfu_path + 'ipwndfu', '--decrypt-gid', keybag], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL).stdout.strip(), 'utf-8').split('\n')[1]
        print('      [*] Got ivkey:', ivkey)
        new_path = 'decrypted/' + os.path.splitext(os.path.basename(file))[0] + '.decrypted'
        subprocess.run(['img4', '-i', file, '-o', new_path, '-k', ivkey], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
        print('      [*] Decrypted file saved to', new_path)

        decryption_info[file] = { 'keybag' : keybag, 'iv' : ivkey[:32], 'key' : ivkey[-64:], 'ivkey' : ivkey}

def process_firmware(firmware):
    os.chdir(location_of_me)

    dirname = firmware['version'] + '_' + firmware['buildid']

    if os.path.isdir(dirname) and len(os.listdir(dirname)) != 0:
        return
    
    try:
        os.mkdir(dirname)
    except:
        pass
    
    os.chdir(dirname)

    while True:
        try:
            files_to_process = list_files(firmware['url'])
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            print('   [!] remotezip failed listing files, will try again ...')
        else:
            print('   [*] Found ' + str(len(files_to_process)) + ' files to download')
            break
    
    decryption_info = {}

    for count, file in enumerate(files_to_process):
        real_filename = file.split('/').pop()

        print('   [*] Downloading {0} [{1}/{2}]'.format(file, count + 1, len(files_to_process)))

        while True:
            try:
                download_file(firmware['url'], file, real_filename)
            except (KeyboardInterrupt, SystemExit):
                raise
            except:
                print('      [!] remotezip failed downloading file, will try again ...')
            else:
                print('      [*] Successfully downloaded ' + real_filename)
                break

        try:
            os.mkdir('decrypted')
            os.mkdir('unencrypted')
        except:
            pass

        print('   [*] Decrypting', file)
        decrypt_file(real_filename, decryption_info)
    
    os.chdir(location_of_me)

    with open(dirname + '.json', 'w') as outfile:
        json.dump(decryption_info, outfile, indent=4)
        print('   [*] Saved decryption information to ' + dirname + '.json')

parser = argparse.ArgumentParser(description='Download and decrypt SecureRom related files')
parser.add_argument('-fw', '--firmware', help='iOS version to download and decrypt')
args = parser.parse_args()

device_type = get_device_type()
device_info = get_device_info(device_type)
device_firmwares = device_info['firmwares']

print('[*] There are ' + str(len(device_firmwares)) + ' firmwares available for ' + device_type)

if args.firmware is not None:
    for firmware in device_firmwares:
        if firmware['version'] == args.firmware:
            print('[*] Processing iOS ' + firmware['version'] + ' (only)')
            process_firmware(firmware)
else:
    for count, firmware in enumerate(device_firmwares):
        print('[*] Processing iOS {0} [{1}/{2}]'.format(firmware['version'], count + 1, len(device_firmwares)))
        process_firmware(firmware)
