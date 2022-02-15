"""
Rush University Medical Center and Affiliate Facilities

Data notes
* 3 provider links, standard-ish format
* Excel docs with IP and OP tab
* IP tab => skip first row
* OP tab => skip first row sometimes... (edge case)

Steps
* retrieve IP and OP Excel data sets and combine
* convert from wide to tall (melt payer rate columns) and rename columns
* combine IP and OP to common foramt

"""
import pandas as pd

def to_common_format_df():

    # set up target URLs
    rush_lookup = {
        "Rush University Medical Center": "https://www.rush.edu/sites/default/files/media-documents/rumc-standard-charges-2022.xlsx",
        "Rush Copley Medical Center": "https://www.rush.edu/sites/default/files/media-documents/rcmc-standard-charges-2022.xlsx",
        "Rush Oak Park Hospital": "https://www.rush.edu/sites/default/files/media-documents/roph-standard-charges-2022.xlsx",
    }

    df_ip = pd.DataFrame()
    df_op = pd.DataFrame()

    for label, url in rush_lookup.items():
        _df_ip = (pd.read_excel(url, sheet_name='IP')
                    .pipe(tweak_df, facility_type='IP', label=label)
                    .assign(source=label)
                )

        _df_op = (pd.read_excel(url, sheet_name='OP')
                    .pipe(tweak_df, facility_type='OP')
                    .dropna(subset=['code_id'])
                    .assign(source=label)
                )
        
        df_ip = pd.concat([df_ip, _df_ip])
        df_op = pd.concat([df_op, _df_op])
        
    # unpivot payer from wide to tall for IP and OP data sets
    non_rate_cols = ['code_type', 'drg_code', 'code_description', 'source']
    rate_cols = set(df_ip.columns) - set(non_rate_cols)
    melted_ip = (df_ip
                .rename(columns={'drg_code': 'code', 'code_description': 'code_desc'})
                .melt(id_vars=['code_type', 'code', 'code_desc', 'source'], value_vars=rate_cols, var_name='rate_amt_type', value_name='rate_amt')
            )


    non_rate_cols = ['code_type', 'code_cpt/hcpcs', 'ndc', 'code_description', 'source']
    rate_cols = set(df_op.columns) - set(non_rate_cols)
    melted_op = (df_op
        .rename(columns={'code_cpt/hcpcs': 'code', 'code_description': 'code_desc'})        
        .assign(code=df_op['code_cpt/hcpcs'].combine_first(df_op['ndc']))               # same as SQL coalesce
        .drop(columns=['ndc'])        
        .melt(id_vars=['code_type', 'code', 'code_desc', 'source'], value_vars=rate_cols, var_name='rate_amt_type', value_name='rate_amt')        
    )

    melted = (pd.concat([melted_ip, melted_op], axis='rows')
                .loc[:, ['source', 'code', 'code_type', 'code_desc', 'rate_amt_type', 'rate_amt']]
                .dropna(subset=['rate_amt'])
            )

    return melted

def tweak_df(df, facility_type=None, label=None): 
    """Skips first row."""
    if facility_type=='OP' or label=='Rush University Medical Center':
        # same effect as skipping first row
        df.columns = df.iloc[0, :]
        df = df.drop(index=0).reset_index(drop=True)
    df.columns = [str(col).lower().replace(' ', '_') for col in df.columns]    
    return df
