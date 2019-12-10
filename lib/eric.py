import lib.basefun as basefun
from ckanapi import RemoteCKAN

#######################################################################

# Validate that two orgas are identical, otherwise stop!
def stopIfTwoOrgasAreNotIdent(repo1, repo2):
    if areTwoOrgasIdentical(repo1, repo2) != True:
        print("ERROR: Organisational structures NOT identical!")
        exit()

# Check whether two organisational structures are identical
def areTwoOrgasIdentical(repo1, repo2):
    OrgaList1 = repo1.call_action('organization_list')
    OrgaList2 = repo2.call_action('organization_list')
    if set(OrgaList1) == set(OrgaList2):
        return True
    else:
        return False

#######################################################################

# Identify packages that appear in repo 1 but not in 2
def identifyUnpublPkgs(repo1, repo2):
    pkgsRepo1 = repo1.call_action('package_list')
    pkgsRepo2 = repo2.call_action('package_list')
    result = arePkgsInPkgList(pkgsRepo1, pkgsRepo2, pick=False)
    return result

# Check whether packages appear in a list of packages
# Options allow to pick only true or false responses,
# e.g. func(Pkgs, List, pick=True) returns only true.
def arePkgsInPkgList(pkgs, pkgList, **kwargs):
    picked = kwargs.get('pick', None)
    dictionary = dict(); packageList = []
    for i in range(len(pkgs)):
        result = isPkgInPkgList(pkgs[i],pkgList)
        if picked == True and result == True:
            packageList.append(pkgs[i])
        elif picked == False and result == False:
            packageList.append(pkgs[i])
        else:
            dictionary.update({pkgs[i]:result})
    if picked == True or picked == False:
        return packageList
    else:
        return dictionary

# Check whether package is in list of packages
def isPkgInPkgList(pkg, pkgList):
    pkg = {pkg}; pkgList = set(pkgList)
    return pkg.issubset(pkgList)

#######################################################################

# Get organization name for package
def getOrgaNameForPkg(pkg, repo):
    response = repo.call_action('package_show', {'id': pkg})
    organization = response['organization']
    return organization['name']

# Get organization names for list of packages
def getOrgaNamesForPkgList(pkgList, repo):
    dictionary = dict()
    for i in range(len(pkgList)):
        ograName = getOrgaNameForPkg(pkgList[i], repo)
        dictionary.update({pkgList[i]:ograName})
    return dictionary

# Get data managers for list of packages
def getDataManagersForPkgList(pkgList, repo):
    dictionary = dict()
    for i in range(len(pkgList)):
        ograName = getOrgaNameForPkg(pkgList[i], repo)
        response = repo.call_action('organization_show', {'id': ograName})
        dataManager = response['datamanager']
        dictionary.update({pkgList[i]:dataManager})
    return dictionary

# Get maintainers for list of packages
def getMaintainersForPkgList(pkgList, repo):
    dictionary = dict()
    for i in range(len(pkgList)):
        response = repo.call_action('package_show', {'id': pkgList[i]})
        maintainer = response['maintainer']
        dictionary.update({pkgList[i]:maintainer})
    return dictionary

#######################################################################

# Collect all information needed to compose email to data manager
def prepareEmailToDataManager(repo, dictDataManagerPkgs, dictPkgsMaintainers):
    result = list()
    for user in dictDataManagerPkgs.keys():
        
        entry = dict()
        entry.update({'From':'rdm@eawag.ch'})

        manager = getUserFieldData(repo, user, 'display_name')
        name = manager.split(", ")
        firstname = name[1].split(" ")
        greeting = 'Dear ' + firstname [0] + ','
        entry.update({'To':manager})

        packageList = dictDataManagerPkgs[user]
        maintainers = set()
        for package in packageList:
            maintainer = dictPkgsMaintainers[package]
            maintainer = getUserFieldData(repo, maintainer, 'display_name')
            maintainers.add(maintainer)
        maintainers.discard(manager)
        if maintainers == set():
            maintainers = {}
        entry.update({'CC':list(maintainers)})
        
        entry.update({'BCC':'rdm@eawag.ch'})
        entry.update({'Subject':'Publish your research data to ERIC open!'})


        content = greeting + ' ... tbd ... ' + \
            'the following packages could be opened: ' + str(packageList)
        entry.update({'Content':content})

        result.append(entry)
    return result

def getUserFieldData(repo, user, field):
    response = repo.call_action('user_show', {'id': user})
    result = response[field]
    return result

def getPackageFieldData(repo, package, field):
    response = repo.call_action('package_show', {'id': package})
    result = response[field]
    return result

#######################################################################