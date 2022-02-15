from mrf_parser import src_00001, src_00002, src_00003
import logging

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

logging.info('retrieving Northwestern Memorial rates...')
nwm_df = src_00001.to_common_format_df()

logging.info('retrieving Rush Univeristy Medical Center rates...')
rumc_df = src_00002.to_common_format_df()

logging.info('retrieving Advocate Health Care rates...')
ahc_df = src_00003.to_common_format_df()

############
# queries
############

# query for foot xray rates (HCPCS/CPT 73730)
print(nwm_df.query("code_desc.str.contains('XRAY FOOT')").to_markdown(index=False)) 
