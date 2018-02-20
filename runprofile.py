from bfex.components.scraper.scraper import *
from bfex.components.scraper.scraperfactory import *
from bfex.components.scraper.scrapertype import *
from bfex.common.utils import generate_names_from_json

# this should be done with a real service but
# I do not know how that will work yet
data = json.load(open(r'../faculty.json'))

for item in data:
    formated_name = generate_names_from_json(item)
    # concatenate names into url
    url = base_url + formated_name

    scrapp = ScraperFactory.create_scraper(url, ScraperType.PROFILE)
    try:
        print(formated_name)
        print(scrapp[0].meta_data)
    except:
        pass