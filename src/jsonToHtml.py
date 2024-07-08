#!/bin/env python

"""
To run conversion:
(base) ml-9953350:src durack1$ python jsonToHtml.py 6.5.0

"""
"""2023
PJD 29 Nov 2023 - copied from https://github.com/WCRP-CMIP/CMIP6_CVs/blob/138a089499cd2a9418186fb27cd184063f2d34da/src/jsonToHtml.py
PJD 29 Nov 2023 - first prototype completes
PJD  2 Jul 2024 - update with x.y.z versioning
PJD  2 Jul 2024 - update to deal with new source_id formats and information
PJD  3 Jul 2024 - augment _status with active download link
PJD  6 Jul 2024 - add README.md/CITATION.cff version tagging
"""

# This script takes the json file and turns it into a nice jquery/data-tabled html doc
import argparse
import datetime
import json
import os
import re
import sys
from urllib.request import urlopen

# from collections import defaultdict

# %% Create generic header
header = """<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="en" xml:lang="en">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
<meta name="author" content="Paul J. Durack" />
<meta name="description" content="Controlled vocabulary for input4MIPs" />
<meta name="keywords" content="HTML, CSS, JavaScript" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<link rel="stylesheet" type="text/css" charset="utf-8" href="https://pcmdi.github.io/assets/dataTables/jquery.dataTables.min.css" />
<script type="text/javascript" charset="utf-8" src="https://pcmdi.github.io/assets/jquery/jquery.slim.min.js"></script>
<script type="text/javascript" charset="utf-8" src="https://pcmdi.github.io/assets/dataTables/jquery.dataTables.min.js"></script>
<!-- Global site tag (gtag.js) - Google Analytics -->
<script type="text/javascript" src="https://pcmdi.github.io/assets/google/googleAnalyticsTag.js" ></script>
<script type="text/javascript">
//<![CDATA[
$(document).ready( function () {
    $('#table_id').DataTable();
    } );
//]]>
</script>\n"""

# %% Argparse extract
# Matching version format 6.5.1
# verTest = re.compile(r'[6][.][2][.][0-9]+[.][0-9]+')
verTest = re.compile(r"[6][.][5][.][0-9]")
parser = argparse.ArgumentParser()
parser.add_argument(
    "ver",
    metavar="str",
    type=str,
    help="For e.g. '6.5.1' as a command line argument will ensure version information is written to the html output",
)
argDict = parser.parse_args()
if re.search(verTest, argDict.ver):
    version = argDict.ver  # 1 = make files
    print("** HTML Write mode - ", version, " will be written **")
else:
    print("** Version: ", version, " invalid, exiting")
    sys.exit()

# %% Set global arguments
destDir = "../docs/"

# %% Process source_id
infile = "../input4MIPs_source_id.json"
f = open(infile)
dic = json.load(f)
dic1 = dic.get("source_id")  # Fudge to extract duplicate level
dic = dic1
del dic1
print(dic.keys())
# exp_dict2 = exp_dict.get("version")
# print(exp_dict2)
# print(dict.keys())

# deal with existing file
fout = "".join([destDir, infile[:-4].replace("../", ""), "html"])
if os.path.exists(fout):
    os.remove(fout)
print("processing", fout)
fo = open(fout, "w")

# print >> fo, ''.join([header, """
fo.write(
    "".join(
        [
            header,
            "<title>input4MIPs source_id values</title>\n</head>\n<body>",
            "<p><h1>PCMDI input4MIPs_CVs version: ",
            version,
            "</h1></p>",
            '<table id="table_id" class="display compact" style="width:100%">\n',
        ]
    )
)

"""
../input4MIPs_source_id.json
"ACCESS1-3-rcp85-1-0":{
            "_status":"Published",
            "contact":"ISMIP6 Steering Team (ismip6@gmail.com)",
            "dataset_category":"surfaceFluxes",
            "datetime_start":"1950-07-01",
            "datetime_stop":null,
            "frequency":"yrC",
            "further_info_url":"http://www.climate-cryosphere.org/wiki/index.php?title=ISMIP6_wiki_page",
            "grid_label":"grg",
            "institution_id":"NASA-GSFC",
            "license":"CC BY 4.0",
            "mip_era":"CMIP6",
            "nominal_resolution":"10 km",
            "realm":"landIce",
            "region":"",
            "source":"ACCESS1-3-rcp85-1-0 derived dataset computed from CMIP5 ACCESS1-3 historical and rcp85 simulations for ISMIP6",
            "source_id":"ACCESS1-3-rcp85-1-0",
            "source_version":"1.0",
            "target_mip":"ISMIP6",
            "title":"ISMIP6 (CMIP6) - ACCESS1-3-rcp85-1-0 derived data prepared for input4MIPs",
            "|dataProviderExtra":{
                "source_variables":[
                    "acabf",
                    "evspsbl",
                    "mrros",
                    "pr",
                    "sftflf",
                    "so",
                    "ts"
                ]
            },
            "|dataProviderFile":{
                "Conventions":"CF-1.6",
                "creation_date":"2020-09-04T15:13:47Z",
                "tracking_id":null
            },
            "|esgfIndex":{
                "_timestamp":"2021-04-22T19:05:37.327Z",
                "data_node":"esgf-data2.llnl.gov",
                "latest":true,
                "replica":false,
                "version":"20210422",
                "xlink":"http://cera-www.dkrz.de/WDCC/meta/CMIP6/input4MIPs.CMIP6.ISMIP6.NASA-GSFC.ACCESS1-3-rcp85-1-0.ocean.yrC.thetao.grg.v20210422.json|Citation|citation"
            }
        },

"""
dictOrderK = [  # html target
    "institution_id",
    "mip_era",
    "target_mip",
    "_status",
    "datetime_start",
    "datetime_stop",
    "dataset_category",
    "realm",
    "contact",
    "latest",
    "source_version",
    "version",
    "_timestamp",
]
url = "<a href='https://aims2.llnl.gov/search?project=input4MIPs&versionType=all&activeFacets=%7B%22source_id%22%3A%22!SRC!%22%7D' target='_blank'>Published</a>"

first_row = False
print("start loop")
for src in dic.keys():
    print("enter src:", src)
    src_dic = dic[src]
    # Create table columns
    if not first_row:
        ids = dictOrderK  # Overwrite ordering
        for hf in ["thead", "tfoot"]:
            fo.write("<%s>\n<tr>\n<th>source_id</th>\n" % hf)
            for i in ids:
                i = i.replace("_", " ")  # Remove '_' from table titles
                fo.write("<th>%s</th>\n" % i)
            fo.write("</tr>\n</%s>\n" % hf)
    first_row = True
    fo.write("<tr>\n<td>%s</td>\n" % src)
    # Fill columns with values
    for k in ids:
        print("k:", k)
        # catch _status
        if k == "_status":
            if src_dic["_status"] == "Published":
                st = url.replace("!SRC!", src)
        # deal with |esgfIndex entries
        elif k in ["_timestamp", "latest", "version"]:
            print("enter if k")
            st = str(src_dic["|esgfIndex"][k])
            print("st:", st)
        else:
            st = src_dic[k]
        print("st:", st)
        # Deal with embeds
        if isinstance(st, (list, tuple)):
            st = " ".join(st)
        if (st is None) or (type(st) is bool):
            pass
            # print(st, type(st))
        elif "@" in st:
            st = st.replace("@", " at ")
        fo.write("<td>%s</td>\n" % st)
    fo.write("</tr>\n")
fo.write("</table>")
fo.write("""\n</body>\n</html>\n""")
fo.close()

# %% update version info

# update Readme.md
target_url = "https://raw.githubusercontent.com/PCMDI/input4MIPs_CVs/main/README.md"
txt = urlopen(target_url).read().decode("utf-8")
txt = re.sub("[0-9].[0-9].[0-9]", version, txt)
# delete existing file and write back to repo
readmeH = "../README.md"
os.remove(readmeH)
fH = open(readmeH, "w")
fH.write(txt)
fH.close()
print("README.md updated")
del (target_url, txt, readmeH, fH)

# update CITATION.cff
target_url = "https://raw.githubusercontent.com/PCMDI/input4MIPs_CVs/main/CITATION.cff"
txt = urlopen(target_url).read().decode("utf-8")
# replace versionId
txt = re.sub("[0-9].[0-9].[0-9]", version, txt)
# replace date-released
timeNow = datetime.datetime.now().strftime("%Y-%m-%d")
txt = re.sub("[0-9]{4}-[0-9]{2}-[0-9]{2}", timeNow, txt)
# delete existing file and write back to repo
citationH = "../CITATION.cff"
os.remove(citationH)
fH = open(citationH, "w")
fH.write(txt)
fH.close()
print("CITATION.cff updated")
del (target_url, txt, citationH, fH)
