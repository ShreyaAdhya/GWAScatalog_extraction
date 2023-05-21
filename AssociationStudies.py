import requests     # Manages data transfer from the GWAS Catalog REST API
import pandas as pd # Makes data handling easier
import json         # Hanling the returned data type called JSON
from collections import OrderedDict

#GWAS API URL
apiUrl = 'https://www.ebi.ac.uk/gwas/rest/api'

#set of variants' rsIDs
variants = ['rs7350481', 'rs386757812', 'rs1974718', 'rs1558860', 'rs1558861', 'rs9326246', 'rs180349', 'rs1940253872', 'rs180327','rs6589564', 'rs180326', 'rs7930786', 'rs1940284623','rs3825041', 's10790162', 'rs6589565', 'rs2160669', 'rs964184', 'rs11604424', 'rs6589566', 'rs7483863', 'rs2075290', 'rs10750096', 'rs3741298', 'rs2266788', 'rs2072560', 'rs651821', 'rs662799', 'rs7123666', 'rs6589567', 'rs4938313', 'rs6589569', 'rs1281317689', 'rs9667814', 'rs71462009', 'rs1172723086', 'rs9666150', 'rs11216140', 'rs6589570', 'rs6589571']

# Store extracted data in this list:
extractedData = []

# Iterating over all variants:
for variant in variants:

    # Accessing data for a single variant:
    requestUrl = '%s/singleNucleotidePolymorphisms/%s/associations?projection=associationBySnp' %(apiUrl, variant)
    response = requests.get(requestUrl, headers={ "Content-Type" : "application/json"})
    
    # Testing if rsID exists:
    if not response.ok:
        print("[Warning] %s is not in the GWAS Catalog!!" % variant)
        continue
    
    # Test if the returned data looks good:
    try:
        decoded = response.json()
    except:
        print("[Warning] Failed to encode data for %s" % variant)
        continue
    
    for association in decoded['_embedded']['associations']:
        trait = ",".join([trait['trait'] for trait in association['efoTraits']])
        pvalue = association['pvalue']
        
        extractedData.append(OrderedDict({'variant' : variant,
                              'trait' : trait,
                              'pvalue' : pvalue}))
							  
							  
# Format data into a table:
table = pd.DataFrame.from_dict(extractedData)
#table							  

#Convert dataframe to .csv file
table.to_csv('Set2_GWAScat_asso.csv')
