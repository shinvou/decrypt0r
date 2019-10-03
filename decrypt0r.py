#!/usr/bin/env python3

import json
import requests
import sys, subprocess, os
import argparse

header = {'Accept': 'application/json'}
api_base_url = 'https://api.ipsw.me/v4/'

device_type = 'iPad4,1'
ipwndfu_path = '/Users/shinvou/Desktop/SecureRom/ipwndfu_public/'

location_of_me = os.path.dirname(os.path.realpath(__file__))

def get_device_info(device_type):
    api_url = '{0}/device/{1}?type=ipsw'.format(api_base_url, device_type)

    response = requests.get(api_url, headers=header)

    if response.status_code == 200:
        return json.loads(response.content.decode('utf-8'))
    else:
        return None

def download_file(url, file, real_filename):
    ret = subprocess.run(['partialzip', 'download', url, file, real_filename], stdout=subprocess.PIPE, stderr=subprocess.PIPE).returncode
    return ret

def decrypt_file(file):
    keybag = str(subprocess.run(['img4', '-i', file, '-b'], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL).stdout.strip(), 'utf-8').split('\n')[0]
    
    if keybag == "":
        print('      [*] We don\'t need to decrypt', file)
        new_path = 'unencrypted/' + file
        os.rename(file, new_path)
        print('      [*] Moved to', new_path)
        return
    else:
        print('      [*] Got keybag:', keybag)
        ivkey = str(subprocess.run([ipwndfu_path + 'ipwndfu', '--decrypt-gid', keybag], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL).stdout.strip(), 'utf-8').split('\n')[1]
        print('      [*] Got ivkey:', ivkey)
        new_path = 'decrypted/' + file + '.decrypted'
        subprocess.run(['img4', '-i', file, '-o', new_path, '-k', ivkey], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
        print('      [*] Decrypted file saved to', new_path)

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

    output = str(subprocess.run(['partialzip', 'list', firmware["url"]], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL).stdout.strip(), 'utf-8').split('\n')

    files_to_process = []

    for path in output:
        fixed_path = path.split(' ')[0]

        if fixed_path.endswith('im4p'):
            if "all_flash" in fixed_path or "dfu" in fixed_path:
                files_to_process.append(fixed_path)

    files_to_process = sorted(files_to_process)

    print('   [*] Found ' + str(len(files_to_process)) + ' files to download')

    for count, file in enumerate(files_to_process):
        real_filename = file.split('/').pop()

        print('   [*] Downloading {0} [{1}/{2}]'.format(file, count + 1, len(files_to_process)))
        
        while download_file(firmware['url'], file, real_filename) != 0:
            print('      [*] PartialZip failed, will try again ...')

        try:
            os.mkdir('decrypted')
            os.mkdir('unencrypted')
        except:
            pass

        print('   [*] Decrypting', file)
        decrypt_file(real_filename)

parser = argparse.ArgumentParser(description='Download and decrypt SecureRom related files')
parser.add_argument('-fw', '--firmware', help='iOS version which should be downloaded and decrypted')
args = parser.parse_args()

device_info = get_device_info(device_type)

if device_info is not None:
    firmwares = device_info['firmwares']
    print('[*] There are ' + str(len(firmwares)) + ' firmwares available for ' + device_type)
else:
    sys.exit('[!] API error')

if args.firmware is not None:
    firmware = [firmware for firmware in firmwares if firmware['version'] == args.firmware][0]
    print('[*] Processing iOS ' + firmware['version'] + ' (only)')
    process_firmware(firmware)
else:
    for count, firmware in enumerate(firmwares):
        print('[*] Processing iOS {0} [{1}/{2}]'.format(firmware['version'], count + 1, len(firmwares)))
        process_firmware(firmware)
