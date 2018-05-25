import re

pattern = '^(LTE|5G|GSM|WCDMA|CORE|SINGLE RAN)\d+(\s|$)';


def createUnificatePresentationNameColmun(csv):
    csv['presentation'] = list(map(lambda x: re.search(pattern, x, re.I).group(0).strip() if re.search(pattern, x, re.I) else x, csv.actionName))
    return csv