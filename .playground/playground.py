import os, requests
from lxml import html
from pprint import pprint
import re, json
from tak import dict as wiki

lang = "pl"


def cleanhtml(html):
    CLEANR = re.compile('<.*?>')
    cleantext = re.sub(CLEANR, "", html)
    return cleantext

with open("temp.txt", "w+") as haha:
    haha.write(json.dumps(wiki, ensure_ascii=False))
    haha.seek(0)
    read = haha.read()
    cleaned = cleanhtml(read)
    output = json.loads(cleaned)
    print(type(output), output["pl"])





# def recurse(thing):
#     if isinstance(thing, dict):
#
#         for key, value in thing.items():
#             noHTML = re.compile('<.*?>')
#
#             try:
#                 cleaned = re.sub(noHTML, '', value)
#                 thing[value] = cleaned
#                 print(f'Dict: {key}, {value}')
#
#             except TypeError as e:
#                 pass
#
#             if isinstance(value, dict):
#                 recurse(value)
#
#             elif isinstance(value, list):
#                 recurse(value)
#
#     elif isinstance(thing, list):
#
#         for value in thing:
#             noHTML = re.compile('<.*?>')
#
#             try:
#                 cleaned = re.sub(noHTML, '', value)
#                 thing[value] = cleaned
#                 print(f'List: {value}')
#
#             except TypeError as e:
#                 pass
#
#             if isinstance(value, dict):
#                 recurse(value)
#
#             elif isinstance(value, list):
#                 recurse(value)
#
# for k in wiki.keys():
#     if k == lang:
#         recurse(wiki[lang])
#     else:
#         pass




# from google.cloud import translate_v2, translate_v3
# import six
#
# googlebot = translate_v2.Client()
# betterbot = translate_v3.TranslationServiceClient()
#
# text = "lub w dość niskiej temperaturze."
# target = "de"
#
# if isinstance(text, six.binary_type):
#     text = text.decode("utf-8")
#
# result = googlebot.translate(text, target_language=target)
# print(result)

