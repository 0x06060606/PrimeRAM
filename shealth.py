import re
import pandas as pd
import time
from tqdm import tqdm
import mmap

Results = {}
Patterns = {
    'sqlitecipher_key': re.compile(r"x'[a-f0-9]{96}'"),
    # Add more patterns here
}

def read_file_with_progress(filename):
    chunk_size = 1024 * 1024 * 10  # 10 MB chunk size
    file_content = bytearray()
    with open(filename, 'rb') as file:
        file_size = file.seek(0, 2)
        file.seek(0)
        with tqdm(total=file_size, unit='B', unit_scale=True, desc="Reading RAM File") as pbar:
            while True:
                chunk = file.read(chunk_size)
                if not chunk:
                    break
                file_content.extend(chunk)
                pbar.update(len(chunk))
    print(' ' * 100, end='\r')
    print(' [#] Please Wait... [May Take Some Time] ', end='\r')
    return bytes(file_content).decode(errors='ignore')

data = read_file_with_progress('RAMS21Ultra.bin')
print(' ' * 100, end='\r')
print(' [#] Parsing RAM Dump... [...]', end='\r')
for key, pattern in Patterns.items():
    print(' ' * 100, end='\r')
    print(f' [#] Parsing RAM Dump... [{key}: {len(Results.get(key, []))}] ', end='\r')
    for match in pattern.findall(data):
        print(' ' * 100, end='\r')
        print(f' [#] Parsing RAM Dump... [{key}: {len(Results.get(key, []))}] ', end='\r')
        if key not in Results:
            Results[key] = []
        Results[key].append(match)
print(f' [#] Parsing RAM Dump... [Done] ', end='\r')
df = pd.DataFrame(Results)
ExportName = str(str(int(time.time())) + '.csv')
df.to_csv(ExportName, index=False)
print(' ' * 100, end='\r')
print(f' [#] Results Exported to {ExportName} ')

