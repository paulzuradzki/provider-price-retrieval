### Description
This is a package for parsing provider machine readable files which are required pursuant to CMS Price Transparency regulations.

<!-- TODO: modify git URL -->
### Installation from Git
```bash
$ python -m venv venv
$ venv/bin/activate
(venv) $ python -m pip install --upgrade pip
(venv) $ python -m pip install wheel
(venv) $ python -m pip install git+https://github.com/paulzuradzki/provider-price-retrieval.git
```

### Usage
```python
>>> from mrf_parser import src_00001, src_00002

# Northwestern Memorial rates
>>> nwm_df = src_00001.to_common_format_df()

# Rush Univeristy Medical Center rates
>>> rumc_df = src_00002.to_common_format_df()

# query for foot xray rates (HCPCS/CPT 73730)
>>> print(nwm_df.query("code_desc.str.contains('XRAY FOOT')").to_markdown(index=False)) 
```
Output
| source                         |   code | code_type   | code_desc                    | rate_amt_type                                  |   rate_amt |
|:-------------------------------|-------:|:------------|:-----------------------------|:-----------------------------------------------|-----------:|
| Northwestern Memorial Hospital |  73630 | CPT®        | HB XRAY FOOT MINIMUM 3 VIEWS | gross_charge                                   |     666    |
| Northwestern Memorial Hospital |  73630 | CPT®        | HB XRAY FOOT MINIMUM 3 VIEWS | de-identified_minimum_negotiated_charge        |      32.27 |
| Northwestern Memorial Hospital |  73630 | CPT®        | HB XRAY FOOT MINIMUM 3 VIEWS | de-identified_maximum_negotiated_charge        |     408.26 |
| Northwestern Memorial Hospital |  73630 | CPT®        | HB XRAY FOOT MINIMUM 3 VIEWS | discounted_cash_price                          |     466    |
| Northwestern Memorial Hospital |  73630 | CPT®        | HB XRAY FOOT MINIMUM 3 VIEWS | negotiated_charge:_nmh_aetna__3004_            |     234.43 |
| Northwestern Memorial Hospital |  73630 | CPT®        | HB XRAY FOOT MINIMUM 3 VIEWS | negotiated_charge:_nmh_cigna_hmo_and_oap__336_ |     378.29 |
| Northwestern Memorial Hospital |  73630 | CPT®        | HB XRAY FOOT MINIMUM 3 VIEWS | negotiated_charge:_nmh_cigna_local_plus__331_  |     203.13 |
| Northwestern Memorial Hospital |  73630 | CPT®        | HB XRAY FOOT MINIMUM 3 VIEWS | negotiated_charge:_nmh_cigna__363_             |     253.08 |
| Northwestern Memorial Hospital |  73630 | CPT®        | HB XRAY FOOT MINIMUM 3 VIEWS | negotiated_charge:_nmh_cigna_ppo__338_         |     408.26 |
| Northwestern Memorial Hospital |  73630 | CPT®        | HB XRAY FOOT MINIMUM 3 VIEWS | negotiated_charge:_nmh_humana__553_            |     263.87 |
| Northwestern Memorial Hospital |  73630 | CPT®        | HB XRAY FOOT MINIMUM 3 VIEWS | negotiated_charge:_nmh_uhc__419_               |     249    |
| Northwestern Memorial Hospital |  73630 | CPT®        | HB XRAY FOOT MINIMUM 3 VIEWS | negotiated_charge:_nmh_uhc_core__329_          |     231    |
| Northwestern Memorial Hospital |  73630 | CPT®        | HB XRAY FOOT MINIMUM 3 VIEWS | negotiated_charge:_nmhc_cigna_one__627_        |      32.27 |
| Northwestern Memorial Hospital |  73630 | CPT®        | HB XRAY FOOT MINIMUM 3 VIEWS | negotiated_charge:_nmhc_imagine_health__653_   |     233.1  |
| Northwestern Memorial Hospital |  73630 | CPT®        | HB XRAY FOOT MINIMUM 3 VIEWS | negotiated_charge:_health_alliance             |     249.75 |
| Northwestern Memorial Hospital |  73630 | CPT®        | HB XRAY FOOT MINIMUM 3 VIEWS | negotiated_charge:_bcbs_ppo                    |     245.55 |
| Northwestern Memorial Hospital |  73630 | CPT®        | HB XRAY FOOT MINIMUM 3 VIEWS | negotiated_charge:_bcbs_hmo                    |     168.9  |
| Northwestern Memorial Hospital |  73630 | CPT®        | HB XRAY FOOT MINIMUM 3 VIEWS | negotiated_charge:_bcbs_blue_choice            |     168.9  |

```python
# Northwestern facilities (excluding Palos)
>>> nwm_df['source'].value_counts(normalize=True)
```
```
Northwestern Memorial Hospital                             0.188022
Northwestern Medicine Lake Forest Hospital                 0.162225
Northwestern Medicine Central DuPage Hospital              0.123137
Northwestern Medicine Kishwaukee Hospital                  0.118233
Northwestern Medicine Delnor Hospital                      0.098263
Northwestern Medicine McHenry Hospital                     0.092865
Northwestern Medicine Valley West Hospital                 0.087151
Northwestern Medicine Huntley Hospital                     0.070112
Northwestern Medicine Woodstock Hospital                   0.038272
Northwestern Medicine Marianjoy Rehabilitation Hospital    0.021720
```

### Todos
* need metadata for tagging provider sources
    * last refresh date, effective dates
    * address, lat/long coordinates
* add multithreading for multi-file downloads
* add column validation
    * E.g., in `code` column, we want DRG to consistently appear as "001" vs. "MS-001"
    * `code_type` labels should also be consistent.
* add progress bars for longer/looped downloads