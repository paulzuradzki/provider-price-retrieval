"""
Northwestern Memorial Health Systems
"""
from pprint import pprint
import re

from bs4 import BeautifulSoup
import pandas as pd
import requests

def to_common_format_df():
    url = 'https://www.nm.org/patients-and-visitors/billing-and-insurance/chargemaster'
    soup = BeautifulSoup(requests.get(url).text, 'html.parser')

    ### gather negotiated rate URLs
    rate_elements = soup.select('.panel-content')[1].find_all('a')
    rate_lookup = {}
    for e in rate_elements:
        if 'Palos Hospital' in e.text:
            # TODO: make edge case for Palos non-standardized file
            continue
        rate_lookup[e.text] = url + e['href']

    rates = pd.DataFrame()
    for label, url in rate_lookup.items():
        rates = pd.concat([rates, url_to_df(url=url, label=label)])
        
    rates = rates.reset_index(drop=True)
    rates[['code_type', 'code']] = pd.DataFrame(rates['billing_code'].apply(parse_billing_code_col).values.tolist())

    rates = (rates
                .assign(rate_amt=rates['rate_amt'].str.replace('$', '', regex=False).astype(float))
                .loc[:, ['source', 'code', 'code_type', 'service_description', 'rate_amt_type', 'rate_amt']]
                .rename(columns={'service_description': 'code_desc'})
                .drop_duplicates()
                .dropna(subset=['rate_amt'])
            )    

    return rates

#############################################
### retrieve and consolidate negotiated rates
#############################################

def cleanup_cols(df):
    """We will pipe this func on each dataframe in loop before consolidating df's."""
    df.columns = [col.lower().replace(' ', '_') for col in df.columns]
    return df

def parse_billing_code_col(s):
    l = s.split()
    if 'MS-DRG' in s:
        code_type, code = l[0], l[4]
    elif re.search('CPT|HCPCS', s):
        code_type, code = l[0], l[1]
    else:
        code_type, code = 'Other', None
    return code_type, code

def url_to_df(url=None, label=None):
    _rates = (pd.read_csv(url, encoding='latin1', sep='|')
                .assign(source=label)
                .pipe(cleanup_cols)
             )
    
    charge_cols = [col for col in _rates.columns if re.search('discount|charge', col) is not None]
    non_charge_cols = set(_rates.columns) - set(charge_cols)   
    _rates = _rates.melt(id_vars=non_charge_cols, value_vars=charge_cols, var_name='rate_amt_type', value_name='rate_amt')
    return _rates