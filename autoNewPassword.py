### in links add all websites
import links

import selenium

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service

import time
SALTY = 1

pathToTxt = links.filePath
def main():
    print("Do you need new passwords, ")
    makeNewPass = getYorN()
    ###
    websites = dict()
    print("Do you want newPasswords for specific websites? ")
    usrAns = getYorN()

    if usrAns == "y":
        for i in range(len(links.mainWebsites)):
            print(links.mainWebsites[i] +": "+ str(i))
        ans = ""
        while ans != "q":
            ans = input("please input corresponding numbers")
            if ans.isdigit():
                ans= int(ans)
                if links.mainWebsites[ans]:
                    websites.update({ans:links.mainWebsites[i]})
    else:
        for web in links.mainWebsites:
            index = links.mainWebsites.index(web)
            websites.update({index: links.mainWebsites[index]})
    ###
    if makeNewPass == 'y':
        makePasswords(websites)

    print("do you want to see passwords? ")
    ans = getYorN()
    if ans == "y":
        openTxt()
    print("do you want to change passwords to websites ")
    ans = getYorN()
    if ans == "y":
        doWebsites(websites)
    
    

#from pywinauto import Application
import win32gui
from pywinauto.application import Application

import pywinauto
import time
import win32gui

###doesn't recognize as aplication
def openTxt():
    print("Opening TxtFile")

    app = Application(backend="uia").start('notepad.exe')
    time.sleep(1)
    fileName = links.fileName
    toPath = links.pathToFile
    application = "Untitled - Notepad"
    time.sleep(1)
    hwnd = win32gui.FindWindow(None, application)
    win32gui.MoveWindow(hwnd, 960, 0, 960, 520, True)
    pywinauto.mouse.click(coords = (977,42))
    pywinauto.mouse.click(coords = (1019,107))
    time.sleep(1)
    hwnd2 = win32gui.FindWindow(None, "Open")
    win32gui.MoveWindow(hwnd2, 960, 0, 960, 520, True)
    pywinauto.mouse.click(coords = (1576,44))
    time.sleep(0.2)
    pywinauto.keyboard.send_keys(toPath)
    pywinauto.keyboard.send_keys('+{ENTER}')
    time.sleep(0.2)
    pywinauto.mouse.click(coords = (1239,459))
    pywinauto.keyboard.send_keys(fileName)
    pywinauto.keyboard.send_keys('+{ENTER}')

def doWebsites(websites):
    service = Service()
    option = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=service, options=option)

    for web in websites:
        i = websites.get(web)       
        link = links.mainCantLogIn[i]
        if link == "None":
            continue
        driver.get(link)

        input("any Input when website has loaded in")
        ### inputs username, so the user would need to work less
        if links.mainClickUsrClass_name[i] != "None":
            usery = driver.find_element(By.CLASS_NAME, links.mainClickUsrClass_name[i])
            usery.send_keys(links.mainCantUsr[i])
        elif links.mainClickUsrID[i] != "None":
            usery = driver.find_element(By.ID, links.mainClickUsrID[i])
            usery.send_keys(links.mainCantUsr[i])
        elif links.mainClickUsrName[i] != "None":
            usery = driver.find_element(By.NAME, links.mainClickUsrName[i])
            usery.send_keys(links.mainCantUsr[i])
        elif links.mainClickUsrXpath[i] != "None":
            usery = driver.find_element(By.XPATH, links.mainClickUsrXpath[i])
            usery.send_keys(links.mainCantUsr[i])
        else:
            input("error, please input username yourself and enter anything in cmd")

        time.sleep(1)
        input("enter anything after entering passwords")

    driver.close()
    print()

def makePasswords(websites):
    ### have to do stuff here
    for web in websites:
        print(web)  
        notHapp = True
        #index = websites.get(web)
        while notHapp:
            salt = randomPass(SALTY)
            passLen = passWLength()
            thePassed = randomPass(passLen)
            thePassed = salt+thePassed
            print(thePassed)

            isHapp = input("if happ abt pass: h, any other letter not happ: ")

            if isHapp == 'h':
                ### OOOOH this is so unoptimized, but idk how to do any better
                data = "a"
                #try: 
                with open(pathToTxt, "r") as f:
                    data = f.readlines() 
                    print(data)
                    f.close()
                if len(data) < 1:
                    data.append("trash")
                didntAdd = True
                for line in data:
                    if links.mainWebsites[web] in line:
                        index = data.index(line)
                        data.pop(index)
                        data.append(str(links.mainWebsites[web]) + " " + str(thePassed)+ "\n")
                        didntAdd = False
                if didntAdd == True:
                    data.append(str(links.mainWebsites[web]) + " " + str(thePassed)+ "\n")

                with open(pathToTxt, "w") as f:
                    f.truncate()
                    f.writelines(data)
                f.close()

                notHapp = False

import random
import string

def randomPass(passLen):
    print("Creating Pass")
    password = ""
    characterList = string.ascii_letters 
    characterList = characterList + string.digits
    for i in range(passLen):
        char = random.choice(characterList)
        password = password + char
    return password

numbers = [8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30]
once = True
isRandomOnly = False
ask = True

def passWLength():
    print("Creating Salt")
    global ask
    global once
    global isRandomOnly
    if ask:
        ans = input("input y if you want to have random size passwords")
    else:
        ans = "y"
    if ans == "y":
        isRandomOnly = True
        ask = False
    if isRandomOnly == True:
        passLen = random.choice(numbers)
    elif once:
        passLen = -2
        msg = "Choose your password length from 8 to 30: "
        while (passLen<8 or passLen >30) and passLen != -1:
            print("If you want a password length same for all passwords submit -1")
            passLen = int(input(msg))
            msg = "incorrect Len: "
    else:
        msg = "Choose your password length from 8 to 30: "
        if passLen == -1:
            once = False
            while passLen < 8 or passLen > 30:
                passLen = int(input(msg))
                msg = "incorrect Len: "
    return passLen

def getYorN():
    ans = ""
    while ans != "y" and ans != "n":
        ans = input("y: yes, n: no ")
        print(ans)
    return ans

main()
