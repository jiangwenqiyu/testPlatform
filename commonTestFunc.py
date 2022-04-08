import requests
import re

pat = '#(\d+)\.(.*?)\.(.*?)#'
t = '#1.res.cacacac#   #2.res.cacacac#'
a = re.findall(pat, t)
print(a)
