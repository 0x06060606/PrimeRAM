import os
import sys
import pathlib
import ccl_abx

def ccl_abx_decode(filepath):
    input_path = pathlib.Path(filepath)
    with input_path.open("rb") as f:
        reader = ccl_abx.AbxReader(f)
        doc = reader.read()
    output_path = input_path.with_suffix(".xml")
    with output_path.open("wb") as f:
        f.write(doc, encoding="utf-8")
    return output_path

def carve_files(data, epoch):
    Memory = {
        'LoadingAnimation': [
            '\\',
            '|',
            '/',
            '-',
        ],
    }
    def check_validity(data, magic):
        if data[0:len(Magic[magic]['start'])] != Magic[magic]['start']:
            return False
        if data[-len(Magic[magic]['end']):] != Magic[magic]['end']:
            return False
        return True
    Magic = {
        'PNG': {
            'start': b'\x89\x50\x4E\x47\x0D\x0A\x1A\x0A',
            'end': b'\x49\x45\x4E\x44\xAE\x42\x60\x82',
            'extension': 'png',
            'type': 'image',
            'check': check_validity,
            'skip': False
        },
        'TSYS': {
            'start': b'\x54\x53\x59\x53\x2A\x00\x00\x00',
            'end': b'\x00\x00\x00\x00\x00\x00\x00\x00',
            'extension': 'tsys',
            'type': 'system',
            'check': check_validity,
            'skip': False
        },
        'DATABASE': {
            'start': b'\x53\x51\x4C\x69\x74\x65\x20\x66',
            'end': b'\x00\x00\x00\x00\x00\x00\x00\x00',
            'extension': 'db',
            'type': 'database',
            'check': check_validity,
            'skip': False
        },
        'Android Binary XML': {
            'start': b'\x41\x42\x58\x00\x10\x32\xff\xff',
            'end': b'\x33\x00\x00\x11\x00\x00\x00\x00',
            'extension': 'xml.abx',
            'type': 'xml',
            'check': check_validity,
            'skip': False,
            'post': ccl_abx_decode
        },
        'Android ProtoBuf': {
            'start': b'\x0A\x0D\x0A\x0B\x41\x6E\x64\x72',
            'end': b'\x00\x00\x00\x00\x00\x00\x00\x00',
            'extension': 'protobuf',
            'type': 'protobuf',
            'check': check_validity,
            'skip': False
        },
        'LevelDB': {
            'start': b'\x91\x11\x0c\x00\x0d\x01\x00\x01',
            'end': b'\x57\xfb\x80\x8b\x24\x75\x47\xdb',
            'extension': 'ldb',
            'type': 'database',
            'check': check_validity,
            'skip': False
        },
    }
    file_size = len(data)
    print(' ' * 100, end='\r')
    print(f"  | Carving RAM |  ", end='\r')
    for magic in Magic:
        if Magic[magic].get('skip', False):
            continue
        else:
            print(f"  | Carving {magic} from RAM |  ", end='\r')
        try:
            start = 0
            end = 0
            print(' ' * 100, end='\r')
            while True:
                Start_MB = (start) / 1024 / 1024
                End_MB = file_size / 1024 / 1024
                print(f"  | Carving {magic} from {Start_MB:.2f}MB to {End_MB:.2f}MB | Found {len(Memory.get(Magic[magic]['type'], []))} {magic} files |  ", end='\r')
                start = data.find(Magic[magic]['start'], start)
                if start == -1:
                    break
                end = data.find(Magic[magic]['end'], start)
                if end == -1:
                    break
                file_data = data[start:end+8]
                folder = epoch + '/' + Magic[magic]['type']
                if not os.path.exists(folder):
                    os.makedirs(folder)
                if Magic[magic]['check'](file_data, magic):
                    file_name = f"{folder}/{start}-{end+8}.{Magic[magic]['extension']}"
                    Memory[folder] = Memory.get(folder, []) + [file_name]
                    with open(file_name, 'wb') as file2:
                        file2.write(file_data)
                    if Magic[magic].get('post', False):
                        Magic[magic]['post'](file_name)
                    start = end + 8
                else:
                    start += 1
        except KeyboardInterrupt:
            print(' ' * 100, end='\r')
            print(f"  | Skipping {magic} |  ", end='\r')
            continue
    print(' ' * 100, end='\r')
    try:
        with open(f'{epoch}/{epoch}.bin', 'wb') as file:
            file.write(str(Memory).encode('utf-8'))
        Files_Found = 0
        for folder in Memory:
            Files_Found += len(Memory[folder])
        print(f"  | Finished Carving RAM | Found {Files_Found} files |  ", end='\r')
    except FileNotFoundError:
        print(f"  | Finished Carving RAM | Nothing Found |  ", end='\r')

def extract_strings(data, epoch):
    file_size = len(data)
    pos = 0
    print(' ' * 100, end='\r')
    strings = []
    print(' ' * 100, end='\r')
    for i in range(len(data)):
        try:
            if data[i] >= 32 and data[i] <= 126:
                string = ''
                for j in range(4):
                    if data[i+j] >= 32 and data[i+j] <= 126:
                        string += chr(data[i+j])
                    else:
                        break
                if len(string) > 3:
                    strings.append(string)
            pos = i
            Start_MB = (pos) / 1024 / 1024
            End_MB = file_size / 1024 / 1024
            print(f"  | Extracting Strings from RAM | Found {len(strings)} strings | {Start_MB:.2f}MB to {End_MB:.2f}MB |  ", end='\r')
        except IndexError:
            break
    with open(f'{epoch}/strings.txt', 'w') as file:
        for string in strings:
            file.write(string + '\n')
    print(' ' * 100, end='\r')
    print(f"  | Finished Extracting Strings from RAM | Found {len(strings)} strings |  ")

if __name__ == '__main__':
    with open('RAMS21Ultra.bin', 'rb') as file:
        import random
        print(' ' * 100, end='\r')
        print(f"  | Loading RAM Analysis |  ", end='\r')
        data = file.read()
    import time
    epoch = str(int(time.time()))
    carve_files(data, epoch)
    #extract_strings(data, epoch)
    print(' ' * 100, end='\r')
    print(f"  | Finished RAM Analysis |  ", end='\r\n')