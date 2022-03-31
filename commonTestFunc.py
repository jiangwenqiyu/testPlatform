import re

url = '#1.status#'
pat = '#\d+\..*#'
a = re.findall(pat, url)
print(a)




