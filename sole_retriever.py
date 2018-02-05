"""Retrieve sneakers releases from SoleCollector"""
import sys
import os
import json
import time
from urllib import urlopen
from collections import OrderedDict
try:
    from tqdm import tqdm
except ImportError:
    print 'Install tqdm module:\n \tpip install tqdm\n Otherwise it MIGHT go into space.'
    def tqdm(*args, **kwargs):
        """No requirements"""
        if args:
            return args[0]
        return kwargs.get('iterable', None)

BASE_URL = 'https://solecollector.com/api/sneaker-api'

def main_menu():
    """main menu"""
    os.system('clear')
    print '\nSup boi.'
    print '\nDo you want to steal shoes from Solecollector?\n'
    print '1. Start'
    print '2. Quit'
    choice = raw_input(" >>  ")

    if choice.lower() == '1':
        load_brands()
        releases_url()
    elif choice.lower() == '2':
        sys.exit()
    else:
        print "Invalid selection, please try again.\n"
        main_menu()

def load_brands():
    """Load json with brands info (id, release count etc.)"""
    os.system('clear')
    try:
        print ''
        print 'Loading...'
        sys.stdout.write("\033[F")
        brands_data = urlopen('%s/brands?get=99' % BASE_URL).read()
        load_brands.data = json.loads(brands_data)
        print 'Loading : ok'
        time.sleep(2)
    except ValueError:
        print 'Could not connect...'
        print 'Trying again.'
        time.sleep(2)
        load_brands()
        releases_url()


def releases_url():
    """Generating pairs with urls of every brand"""
    os.system('clear')
    releases_url.data = []
    releases_url.count = 0
    for i in load_brands.data:
        skip = 0
        releases_count = i['releases_count']
        releases_url.count = releases_url.count + releases_count
        url = '%s/releases?parent_id=%s&get=100&skip=%s' % (BASE_URL, i['id'], skip)
        pair = i['name'], url
        releases_url.data.append(pair)
        skip = 100
        while releases_count > skip:
            url = '%s/releases?parent_id=%s&get=100&skip=%s' % (BASE_URL, i['id'], skip)
            pair = i['name'], url
            releases_url.data.append(pair)
            skip = skip + 100
    print '\nGenerated %s links from %s brands' % (len(releases_url.data), len(load_brands.data))
    print 'Total of %s release\'s details avalivable to download!\n' % releases_url.count
    print 'Continue:\n'
    print '1. Download'
    print '2. Save links to JSON'
    print '3. Save brands details to JSON \n'
    print '0. Back'
    choice = raw_input(" >>  ")
    if choice.lower() == '1':
        download_releases()
    elif choice.lower() == '2':
        make_json(releases_url.data)
    elif choice.lower() == '3':
        make_json(load_brands.data)
    else:
        print "Invalid selection, please try again.\n"
        main_menu()

def save_option():
    """menu after downloading"""
    os.system('clear')
    print '\nRetrieved %s / %s items.' %(len(download_releases.all), releases_url.count)
    print 'Save data to JSON file?\n'
    print '1. Yes'
    print '2. No'
    print '3. Exit'
    choice = raw_input(" >>  ")
    if choice.lower() == '1':
        make_json(download_releases.sneakers)
    elif choice.lower() == '2':
        main_menu()
    elif choice.lower() == '3':
        sys.exit()
    else:
        print "Invalid selection, returning to menu.\n"
        main_menu()

def download_releases():
    """downloading details of all releases"""
    os.system('clear')
    print '\nDownloading all releases, this might take a while.'
    print '\n\tPress Ctrl + C to cancel.'
    release_id = 0
    download_releases.all = {}
    download_releases.sneakers = {}
    releases_data_pb = tqdm(releases_url.data, position=1)
    try:
        for i in releases_data_pb:
            releases_data_pb.set_description(' Items: %s ' % release_id)
            release_data = urlopen(i[1]).read()
            release = json.loads(release_data)
            release_pb = tqdm(release, smoothing=0.3, position=3)
            for j in release_pb:
                release_pb.set_description(' Brand: %s ' % i[0])
                download_releases.all.update(
                    {release_id: {'brand' : i[0],
                                  'release_date' : j['release_date'],
                                  'image_url' : j['hero_image_url'],
                                  'description' : j['description'],
                                  'release_date_pretty' : j['release_date_pretty'],
                                  'original_price' : j['original_price'],
                                  'slug' : j['alias'],
                                  'model_name' : j['name'],
                                 }})
                release_id = release_id + 1
    except (KeyboardInterrupt, ValueError):
        srtSneak = OrderedDict(sorted(download_releases.all.items(), key=lambda i: i[1]['release_date'], reverse=True))
        download_releases.sneakers.update({'sneakers' : srtSneak, 'brands' : load_brands.data})
        save_option()
    srtSneak = OrderedDict(sorted(download_releases.all.items(), key=lambda i: i[1]['release_date'], reverse=True))
    download_releases.sneakers.update({'sneakers' : srtSneak, 'brands' : load_brands.data})
    save_option()


def make_json(data):
    """save do json file"""
    os.system('clear')
    if data == releases_url.data:
        print '\nSaving Links to JSON file'
        with open('links.json', 'w') as db_file:
            db_file.write(json.dumps(data, indent=4, sort_keys=True))
        print 'Saved. Returning'
        time.sleep(3)
        releases_url()
    elif data == load_brands.data:
        print '\nSaving brands details to JSON file'
        with open('brands.json', 'w') as db_file:
            db_file.write(json.dumps(data, indent=4, sort_keys=True))
        print 'Saved. Returning'
        time.sleep(3)
        releases_url()
    elif data == download_releases.sneakers:
        print '\nSaving to JSON file'
        with open('releases.json', 'w') as db_file:
            db_file.write(json.dumps(data, indent=4))
        print 'Saved. Returning to menu'
        time.sleep(3)
        main_menu()

main_menu()
