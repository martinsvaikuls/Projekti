#"""
import helperFunctionsDir.urls as urls
#"""
#import urls

"""
#forTesting
import Projects.ScrapingFood.helperFunctionsDir.urls as urls

"""


import sys
## ! i can shorten this mess into one function that accepts both category and name of the place urls.category+placeName

def getCategoryUrl(category, website):
    attr = ""
    print(website)
    websiteFullName = getPlaceName(website)

    match category:
        case 'b':
            attr = "urlBekelej"+str(websiteFullName)
        case 'p':
            attr = "urlMilk"+str(websiteFullName)
        case 'a':
            attr = "urlFruit"+str(websiteFullName)
        case 'm':
            attr = "urlBread"+str(websiteFullName)
        case 'g':
            attr = "urlMeat"+str(websiteFullName)
        case 'd':
            attr = "urlDrinks"+str(websiteFullName)
        case _:
            print("Somekind of error in getting url of category -> getCategoryUrl")
            print(category, websiteFullName)

            sys.exit(1)
    urlsHere = getattr(urls, attr)
    return urlsHere


def getPlaceName(website):
    print(website)
    if not website.istitle():
        match website:
            case 'm':
                website = "Maxima"
            case 'r':
                website = "Rimi"
            case 'l':
                website = "Lats"
            case 'p':
                website = "Promo"
            case 'e':
                website = "Elvi"
            case 't':
                website = "Tops"
            case _:
                print("something went wrong _doesFileExist_Match_Case -> getwebsite")
                print(website)
                sys.exit(1)
    return website


def getWebsiteFileName(websiteShort, dotName):
    fileName = ""
    website = getPlaceName(websiteShort)
    match website:
        case 'Maxima':
            fileName = urls.fileNameMaxima + dotName
        case 'Rimi':
            fileName = urls.fileNameRimi + dotName
        case 'Lats':
            fileName = urls.fileNameLats + dotName
        case 'Promo':
            fileName = urls.fileNamePromo + dotName
        case 'Elvi':
            fileName = urls.fileNameElvi + dotName
        case 'Top':
            fileName = urls.fileNameTop + dotName
        case _:
            print("something went wrong _doesFileExist_Match_Case -> getWebsiteName")
            print(website, dotName)
            sys.exit(1)
    return fileName