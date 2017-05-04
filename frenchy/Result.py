import pandas as pd
import math

class Result():
    def __init__(self, url):
        self.url = url
        tables = pd.read_html(self.url, header=0, encoding='utf8', decimal=',',
                              thousands=' ')
        self._parse([x for x in tables if not x.empty])

    def _parse(self, tables):
        rounds = math.floor(len(tables)/2)
        #results_round1 = self._parse_results(tables[3], 1)
        #results_round2 = self._parse_results(tables[1], 2)
        self.results = pd.concat([self._parse_results(t, rounds-i) for i,t in enumerate(tables[0::2])])

        #meta_round1 = self._parse_meta(tables[2], 1)
        #meta_round2 = self._parse_meta(tables[0], 2)
        #self.meta = pd.concat([meta_round1, meta_round2])
        self.meta = pd.concat([self._parse_meta(t, rounds-i) for i,t in enumerate(tables[1::2])])

    def _parse_results(self, table, round_):
        results_cols = {'Liste des candidats ': 'candidate', 'Voix': 'votes'}
        table = table.rename(columns=results_cols)
        table['candidate'] = table['candidate'].str.replace('\xa0', ' ')
        table['round'] = round_
        table = table[['round', 'candidate', 'votes']]
        table = table.set_index(['candidate', 'round'])
        return table

    def _parse_meta(self, table, round_):
        clean = lambda x: int(str(x).replace('\xa0', ''))
        table = table[['Unnamed: 0', 'Nombre']].iloc[0:5].set_index('Unnamed: 0').T
        meta_cols = {'Inscrits': 'registered', 'Votants': 'votes',
                     'Blancs ou nuls': 'blanks_or_nulls',
                     'Blancs': 'blanks',
                     'Nuls': 'nulls',
                     'Abstentions': 'abstentions'}
        table = table.rename(columns=meta_cols)
        table['round'] = round_
        table = table.set_index('round')
        table.columns.name = None
        table['registered'] = table['registered'].apply(clean)
        table['votes'] = table['votes'].apply(clean)
        table['blanks'] = table['blanks'].apply(clean)
        table['nulls'] = table['nulls'].apply(clean)
        table['abstentions'] = table['abstentions'].apply(clean)

        return table
