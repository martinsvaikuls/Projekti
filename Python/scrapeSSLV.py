from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service

import time
import os
import csv
import datetime



URL = "https://www.ss.lv/lv/electronics/computers/pc/"

cancelCookieXPATH = "/html/body/div[6]/div/div/table/tbody/tr/td[2]/button"

fileNameXPATH = "/html/body/div[4]/div/table/tbody/tr/td/div[1]/table/tbody/tr/td/div/div[1]/h2"

inputFromCostID = "f_o_8_min"
inputToCostID = "f_o_8_max"
searchCostRangeXPATH = "/html/body/div[4]/div/table/tbody/tr/td/div[1]/table/tbody/tr/td/form/table[1]/tbody/tr/td[2]/input"
sortCostXPATH = "/html/body/div[4]/div/table/tbody/tr/td/div[1]/table/tbody/tr/td/form/table[2]/tbody/tr[1]/td[5]/noindex/a"

mainBodyXPATH =      "/html/body/div[4]/div/table/tbody/tr/td/div[1]/table/tbody/tr/td/form/table[2]/tbody"
headerXPATH = "/html/body/div[4]/div/table/tbody/tr/td/div[1]/table/tbody/tr/td/form/table[2]/tbody/tr[1]"
infoScrapeXPATH = ""
infoScrapeXPATHone = "/html/body/div[4]/div/table/tbody/tr/td/div[1]/table/tbody/tr/td/form/table[2]/tbody/tr[2]"
infoScrapeXPATHtwo = "/html/body/div[4]/div/table/tbody/tr/td/div[1]/table/tbody/tr/td/form/table[2]/tbody/tr[3]"
endOfPageID = "tr_bnr_712"


nextPageXPATH = "/html/body/div[4]/div/table/tbody/tr/td/div[1]/table/tbody/tr/td/form/div[2]/a[10]"
                



def main():
    
    driver = driverInitialization()
    driver.get(URL)

    print("Cenas amplitūda?")
    costFrom = "a"
    userInput = input("Cena no: ")
    if userInput != "-":
        try:
            costFrom = int(userInput)
        except:
            while type(costFrom) is not int and costFrom != "-":

                print("Ievadiet skaitlisku vērtību")
                print("Vai - (domuzīmi) ja nevēlaties cenas amplitūdu")
                userInput = input("Cena no: ")
                if userInput != "-":
                    try:
                        costFrom = int(userInput)
                    except:
                        pass
                else:
                    costFrom = userInput
    else:
        costFrom = userInput


    costTo  = "a"
    userInput = input("Cena līdz: ")
    if userInput != "-":
        try:
            costTo = int(userInput)
        except:
            while type(costTo) is not int and costTo != "-":

                print("Ievadiet skaitlisku vērtību")
                print("Vai - (domuzīmi) ja nevēlaties cenas amplitūdu")
                userInput = input("Cena līdz: ")
                if userInput != "-":
                    try:
                        costTo = int(userInput)
                    except:
                        pass
                else:
                    costTo = userInput
    else:
        costTo = userInput

    driver.find_element(By.XPATH, cancelCookieXPATH).click()

    if (costFrom != "-"):
        driver.find_element(By.ID, inputFromCostID).send_keys(costFrom)

    if (costTo != "-"):
        driver.find_element(By.ID, inputToCostID).send_keys(costTo)

    if (costFrom != "-" or costTo != "-"):
        driver.find_element(By.XPATH, searchCostRangeXPATH).click()
        time.sleep(3)

    driver.find_element(By.XPATH, sortCostXPATH).click()


    fileName = driver.find_element(By.XPATH, fileNameXPATH).text
    fileName = (fileName.split("/")[-1]).strip()

    todayDate = datetime.date.today()
    csvFilePath = os.path.dirname(os.path.abspath(__file__)) + "\\" + fileName + str(todayDate)+ ".csv"
    createHeaderForCSVFIle = False

    if not os.path.isfile(csvFilePath):
        createHeaderForCSVFIle = True

    endOfInfo = False
    with open(csvFilePath, "a", encoding="utf8", newline="") as file:
        writeInCsv = csv.writer(file, delimiter=";")
        if createHeaderForCSVFIle:
            headerInfo = driver.find_element(By.XPATH, headerXPATH)
            headerCount = 2
            readAllHeaderInfo = False
            headerList = list()
            while not readAllHeaderInfo:
                try:
                    headerList.append((headerInfo.find_element(By.XPATH, "./td["+str(headerCount)+"]").text).strip().replace("\n", " "))
                except:
                    readAllHeaderInfo = True
                headerCount += 1

        while not endOfInfo:
            endOfPage = False
            count = 2
            items = driver.find_element(By.XPATH, mainBodyXPATH)
            while not endOfPage:

                try:

                    itemList = list()
                    elementIndex = 3
                    endOfElements = False

                    infoScrapeXPATHone = "/html/body/div[4]/div/table/tbody/tr/td/div[1]/table/tbody/tr/td/form/table[2]/tbody/tr["+str(count)+"]"
                    elementPack = driver.find_element(By.XPATH, infoScrapeXPATHone)
                    

                    while not endOfElements:
                        try:
                            elementInfo = elementPack.find_element(By.XPATH, "./td["+str(elementIndex)+"]").text
                            elementInfo = elementInfo.split("\n")

                            for e in elementInfo:
                                itemList.append(e)

                            elementIndex += 1

                        except:
                            
                            endOfElements = True

                    print(itemList[0])
                    writeInCsv.writerow(itemList)
                    
                except:
                    endOfPage = True

                count +=1
            
            try:
                input("pls enter any key")
                driver.find_element(By.XPATH, nextPageXPATH).click()
                time.sleep(3)
            except:
                print("Could not go to next Page")
                endOfInfo = True


    file.close()
    driver.close()

def driverInitialization():
    service = Service()
    option = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=service, options=option)
    return driver

main()
