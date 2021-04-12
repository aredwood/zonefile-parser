import json

sample_json = [{'rtype': 'SOA', 'name': 'mywebsite.com.', 'rclass': 'IN', 'rdata': {'mname': 'mywebsite.com.', 'rname': 'root.mywebsite.com.', 'serial': '2034847964', 'refresh': '7200', 'retry': '3600', 'expire': '86400', 'minimum': '3600'}, 'ttl': '3600'},
{'rtype': 'A', 'name': 'mywebsite.com.', 'rclass': 'IN', 'rdata': {'value': '105.33.55.52'}, 'ttl': '7200'},
{'rtype': 'MX', 'name': 'mywebsite.com.', 'rclass': 'IN', 'rdata': {'priority': '10', 'host': 'alt3.aspmx.l.google.com.'}, 'ttl': '1'},
{'rtype': 'MX', 'name': 'mywebsite.com.', 'rclass': 'IN', 'rdata': {'priority': '5', 'host': 'alt2.aspmx.l.google.com.'}, 'ttl': '1'},
{'rtype': 'TXT', 'name': 'mywebsite.com.', 'rclass': 'IN', 'rdata': {'value': 'v=spf1 include:_spf.google.com ~all'}, 'ttl': '1'}]

for each in sample_json:
    rdata_list = list(each['rdata'].values()) 
    # Just testing the format before I write it to a zone text file
    print(f"{each['name']} {each['rtype']} {' '.join(rdata_list)}")
