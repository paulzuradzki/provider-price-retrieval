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
from mrf_parser import src_00001, src_00002

# Northwestern Memorial rates
nwm_df = src_00001.to_common_format_df()

# Rush Univeristy Medical Center rates
rumc_df = src_00002.to_common_format_df()
```

### Todos
* need metadata for tagging provider sources
    * last refresh date, effective dates
    * address, lat/long coordinates
* add multithreading for multi-file downloads
* add column validation
    * E.g., in `code` column, we want DRG to consistently appear as "001" vs. "MS-001"
    * `code_type` labels should also be consistent.