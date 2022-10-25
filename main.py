import re
import sys
from pathlib import Path

import requests  # for using API
import xml.etree.ElementTree as ET  # for parsing XML

api_username = sys.argv[1:][0]  # account for USPS API access

request_url = 'http://production.shippingapis.com/ShippingAPI.dll?' + \
              'API=ZipCodeLookup&XML=<ZipCodeLookupRequest USERID="{}">'.format(api_username) + \
              '{}</ZipCodeLookupRequest>'

xml_frag = '<Address ID="1"><Address1></Address1><Address2>{}</Address2><City>{}</City><State>{}</State></Address>'

out_path = Path.cwd() / "out.tsv"
in_path = Path.cwd() / "test-data.tsv"
# in_path = Path.cwd() / "MKE-Call-Center-10-5-22.tsv"
address_regex = '^(.*?),'
zip_regex = '([0-9]{5})-?[0-9]{,4}$'


# Given a street address (e.g., 123 Main St), query API for ZIP code
def fill_zip_code(street_address):
    r = requests.get(request_url.format(xml_frag.format(street_address, "Milwaukee", "WI")))  # call API

    root = ET.fromstring(r.content)  # parse XML
    zip5 = root.find('Address/Zip5')
    if zip5 is not None:
        return zip5.text
    else:
        return None


# Given the address portion of the data line (e.g., 7988 N 94TH ST, MILWAUKEE, WI)
# extract the street address as the portion of the string before the first comma
def get_street_address(address):
    match = re.search(address_regex, address)
    if match is not None:
        return match.group(1)
    else:
        return None


# Given an array of strings, output them to the console and the output
# file as a single tab-delimited string.
def output(line_num, parts, out_file):
    parts.insert(0, str(line_num))
    print("\t".join(parts))
    try:
        out_file.write("\t".join(parts))
    except:
        print("Exception on line " + line_num)


if __name__ == '__main__':
    with out_path.open(mode="a", encoding='utf-8') as out_file:
        with in_path.open(encoding='utf-8') as call_center_data:
            line_num = 0  # track last list number processed
            for line in call_center_data.readlines():
                line_num += 1
                if line_num < 51409:  # pick up after error
                    continue
                parts = str.split(line, "\t")
                address = parts[0]

                # address is totally absent
                if address is None or len(address.strip()) == 0:
                    continue

                # trim whitespace
                address = address.strip()

                # look for zip in address
                match = re.search(zip_regex, address)
                if match is not None:
                    # zip found
                    zip = match.group(1)
                    if zip == "00000":
                        # try to call api
                        street = get_street_address(address)
                        if street is not None:
                            zip = fill_zip_code(street)
                            # api failed to deliver
                            if zip is None:
                                continue
                        else:
                            continue
                    # reprint the line with zip first, comma delimited
                    parts.insert(0, zip)
                    output(line_num, parts, out_file)
                else:
                    # zip not found, extract street address
                    # test if comma separates street from city
                    if "," in address:
                        street = get_street_address(address)
                    else:
                        street = address  # no comma, must be just street
                    if street is not None:
                        zip = fill_zip_code(street)
                        # api failed to deliver
                        if zip is None:
                            continue
                        else:
                            # reprint the line with zip first, comma delimited
                            parts.insert(0, zip)
                            output(line_num, parts, out_file)
