import time, json
import lib.eric as eric
from ckanapi import RemoteCKAN

starttime = time.time()

private = RemoteCKAN('https://data.eawag.ch')
public = RemoteCKAN('https://opendata.eawag.ch')

eric.stopIfTwoOrgasAreNotIdent(private, public)

unpubPkgs = eric.identifyUnpublPkgs(private, public)

dictPkgsDataMan = eric.getDataManagersForPkgList(unpubPkgs, private)
dictDataManagerPkgs = eric.basefun.invDict(dictPkgsDataMan)
dictPkgsMaintainers = eric.getMaintainersForPkgList(unpubPkgs, private)

result = eric.prepareEmailToDataManager(private, dictDataManagerPkgs, dictPkgsMaintainers)
print(result)

with open('result.json', 'w') as outfile:
    json.dump(result, outfile)

elapsedtime = time.time() - starttime
print(elapsedtime)