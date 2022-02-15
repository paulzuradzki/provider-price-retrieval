"""
Advocate Health Care (Illinois)

Source URL: https://www.advocatehealth.com/about-us/financial-assistance-for-patients/hospital-pricing-information
"""

import pandas as pd
import xml.etree.ElementTree as ET

def to_common_format_df():

    # read_xml() is new in pandas 1.3.0
    df = pd.read_xml('https://www.advocatehealth.com/assets/documents/hospital-pricing-information/362169147_advocate-christ-medical-center_standardcharges.xml')
    non_rate_cols = ['facility', 'type', 'chargecode_drg_cpt', 'description', 'rev', 'cpt']
    rate_cols = set(df.pipe(tweak_df).columns) - set(non_rate_cols)

    # re-shape data from wide (payer rates as columns) to tall
    df = (df.pipe(tweak_df)
            .melt(id_vars=['source', 'code_type', 'code', 'code_desc'], 
                  value_vars=rate_cols, 
                  var_name='rate_amt_type',
                  value_name='rate_amt')
         )    
    
    return df

def tweak_df(df):
    """Edits to dataframe:
        * edit columns names to lower-case and fill spaces with underscores
        * coalesce 'rev', 'chargecode_drg_cpt', and 'cpt' columns into one 'code' column
        * rename and drop columns
    """
    df.columns = [col.lower().replace(' ', '_') for col in df.columns]
    df = (df.assign(code=df['rev'].combine_first(df['chargecode_drg_cpt']).combine_first(df['cpt']))
            .rename(columns={'description': 'code_desc', 'type': 'code_type', 'facility': 'source'})
            .drop(columns=['chargecode_drg_cpt', 'rev', 'cpt'])
         )
    return df

if __name__ == "__main__":
    """
    Sample usage as submodule:
    $ python -im mrf_parser.sources.src_00003
    >>> df = to_common_format_df()
    """
    pass