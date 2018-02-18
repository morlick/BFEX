from scrapper import *

# this should be done with a real service but
# I do not know how that will work yet
data = json.load(open(r'../../../../faculty.json'))

for item in data:
    name_from_json = item['name']
    name_from_json = re.sub('[.]', '', name_from_json)
    name_list = re.findall('[A-Z][^A-Z]*', name_from_json)
    formated_name = "-".join(name_list).lower()

    # concatenate names into url
    url = base_url + formated_name

    ret = ScraperFactory.create_scraper(ScraperFactory, url, PROFILE)
    try:
        print(ret[0].meta_data)
    except:
        pass