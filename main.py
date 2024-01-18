from requests import get
from json import loads, dumps, dump, load
from json.decoder import JSONDecodeError
import re
from time import sleep
import sys

from datetime import datetime

link_pattern = 'https://opendatabot.ua/l/{}'

api_land_koatuu = 'https://auctions.nodered.5nix.com/api/land-koatuu/{}'

def land_koatuu_dump(number: int):
    with open(f'cadastres/{number}.json', 'w') as file:
        request = get(api_land_koatuu.format(number), {'limit': 0})

        items = []

        if request.ok:
            try:
                json = request.json()

                items = json\
                    .get('_embedded', {})\
                    .get('items', 0)
            except JSONDecodeError:
                return False
            
        data = {
            'land': number, 
            'items': items
        }

        dump(data, file, indent=4)

        return True

def land_koatuu_load(number: int):
    try:
        with open(f'cadastres/{number}.json', 'r') as file:
            return load(file)
    except FileNotFoundError:
        return False
    
def l(cadastre, tries=1):
    request = get(link_pattern.format(cadastre))
    
    if not request.ok:
        print('request failed, code with code', request.status_code)

        if tries <= 3:
            print(f'retrying after 5 minutes')

            sleep(60 * 5)

            return l(cadastre, tries=tries + 1)
        
        print('failed retryind, code is ', request.status_code)
        print('sorry, unable to continue')

        sys.exit()

        return []

    content = request.content;

    match = re.search("window.__INITIAL_STATE__='(?P<json>.*)'", content.decode())

    landData = {}

    if match:
        json = match.group('json')

        try:
            json = json \
                .replace('\\\"', '"') \
                .replace('\\\'', '’')
            
            landData = loads(json) \
                    .get('pageData', {}) \
                    .get('landData', {})
        except JSONDecodeError as e:
            with open(f'skipped/test-{cadastre}.txt', 'a') as file:
                file.write('\n' + '=' * 50 + '\n')
                file.write(e.msg)
                file.write(json)
                file.write('\n' + '=' * 50 + '\n')

    return landData

# hms = lambda: datetime.now().strftime("%H:%M:%S")

# delta = lambda d: f'{int(d) // 3600}:{int(d) % 3600 // 60}:{int(d) % 3600 % 60}'

# koatuu_list = land_koatuu_load(1825255101)

# koatuu_land = koatuu_list.get('land')
# koatuu_items = koatuu_list.get('items', [])

# if not koatuu_list:
#     print('no list')
#     exit()

# print(f'list loaded:\n land {koatuu_land}\n items {len(koatuu_items)}')

# coords_list = {}
# s, f, t = 0, 0, len(koatuu_items)
# r = t

# cooldown = 30

# start_time = datetime.now()

# print('starting on', hms(), '\n\n')

# with open('coordinates/1825255101.json', 'w') as file:
#     file.write('[')

# for item in koatuu_items:
#     if not cooldown:
#         print(f'{hms()} - cooling down for 100 seconds ...')
#         sleep(100)
#         cooldown = 30

#     cooldown -= 1

#     print(f'{hms()} - loading {item}')
#     landData = l(item)
#     print(f'{hms()} - loaded {item}')

#     sleep(2)

#     if not landData:
#         f += 1
#         # coords_list[item] = []
#         print(f'{hms()} - skipped {item}\n')
#         continue
    
#     r -= 1

#     with open('coordinates/1825255101.json', 'a') as file:
#         file.write('\n')
#         dump(landData, file, indent=4, ensure_ascii=False)

#         if r:
#             file.write(',')

#         s += 1

#         print(f'{hms()} - succeed {item} ({s}/{t} - {f}) \n')

#         continue

#     print(f'{hms()} - skipped {item}\n')

# with open('coordinates/1825255101.json', 'a') as file:
#     file.write('\n]')

# print('end on', hms())
# print('time spend', delta((datetime.now() - start_time).total_seconds()))
# print('dumped! bye !')


# skips = ['1825255101:05:003:0162', '1825255101:05:007:0200', '1825255100:01:000:0255', '1825255101:05:007:0201', '1825255101:05:003:0161', '1825255101:05:005:0145', '1825255101:05:008:0330', '1825255101:05:002:0168']

# for item in skips:
#     with open('coordinates/1825255101-add.json', 'a') as file:
#         x = l(item)
#         print(x)
#         dump(x, file, indent=4, ensure_ascii=False)
#         if item != skips[-1]:
#             file.write(',\n')

# from json import load, dump

# items = None

# with open('coordinates/1825255101.json', 'r') as file:
#     items = load(file)

# r = {}

# for item in items:
#     if 'geom' not in item.keys():
#         print(item['landId'])
#         continue
#     coordinates = item['geom']['coordinates'][0]
#     landId = item['landId']

#     for coord in coordinates:
#         coord[0], coord[1] = coord[1], coord[0]

#     r[landId] = coordinates

# with open('testdata/coordinates-1.txt', 'w') as file:
#     dump(r, file, ensure_ascii=False)