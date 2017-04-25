from .Result import Result
from bs4 import BeautifulSoup
import requests
import pandas as pd

def get_departement_results(base_url):
    s = BeautifulSoup(requests.get(base_url).content)
    departements = [(x['value'], x.text,) for x in s.select('select option[value]') if x['value']!='#']
    results = {}
    for url,name in departements:
        r = get(base_url.replace('index.html', url))
        r.meta['departement']=name
        r.results['departement']=name
        results[name] = r
    return {'results': pd.concat([x.results for x in results.values()]),
            'meta': pd.concat([x.meta for x in results.values()]),
            }

def get(url):
    return Result(url)
