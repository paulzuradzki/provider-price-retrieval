### Description
This is a package for parsing provider machine readable files which are required pursuant to CMS Price Transparency regulations.

<!-- TODO: modify git URL -->
### Installation
```bash
$ python -m venv venv
$ venv/bin/activate
(venv) $ python -m pip install --upgrade pip
(venv) $ python -m pip install git+https://github.com/user/your_package.git
```

### Usage 
```python
from mrf_parser import src_00001, src_00002

# Northwestern Memorial rates
nwm_df = src_00001.to_common_format_df()

# Rush Univeristy Medical Center rates
rumc_df = src_00002.to_common_format_df()
```
### Structure
```
.
├── ReadMe.md      
├── client.py      
├── docs
├── mrf_parser     
│   ├── __init__.py
│   └── sources
│       ├── common.py
│       ├── src_00001.py
│       └── src_00002.py
├── notebooks
├── requirements.txt
└── tests
```

### Todos
* need metadata for tagging provider sources
    * last refresh date, effective dates
    * address, lat/long coordinates