from mrf_parser import src_00001, src_00002

# Northwestern Memorial rates
nwm_df = src_00001.to_common_format_df()

# Rush Univeristy Medical Center rates
rumc_df = src_00002.to_common_format_df()

from mrf_parser import src_00001, src_00002

# Northwestern Memorial rates
nwm_df = src_00001.to_common_format_df()

# Rush Univeristy Medical Center rates
rumc_df = src_00002.to_common_format_df()

# query for foot xray rates (HCPCS/CPT 73730)
print(nwm_df.query("code_desc.str.contains('XRAY FOOT')").to_markdown(index=False)) 