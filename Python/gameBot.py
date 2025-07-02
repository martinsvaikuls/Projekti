import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
import time
import sys


def main():
    loginUsr = ""
    passwordUsr = ""
    loginUsr = input("username: ")
    passwordUsr = input("password: ")

    ## ! For some unknown reason you can't use google chrome, as it spams the console
    gecko_driver = 'D:\\Programmas\\geckodriver'
    #service = Service()
    url = "https://mmoquest.com/"
    service = webdriver.FirefoxService()
    options = webdriver.FirefoxOptions()
    driver = webdriver.Firefox(service=service, options=options)
    

    driver.get(url)
    #logger = logging.getLogger('selenium')
    input()

    time.sleep(1)
    
    login = driver.find_element(By.CLASS_NAME, "login.button_auth_Input")
    login.send_keys(loginUsr)

    passWord = driver.find_element(By.CLASS_NAME, "password.button_auth_Input")
    passWord.send_keys(passwordUsr)
    
    try:
        driver.find_element(By.XPATH, "/html/body/mobitva/div/center/table[1]/tbody/tr/td").click()
        time.sleep(2)
    except:
        print()
    finally:
        while True:
            choice = ""
            choice = input("Player vs enviroment: pve \nPlayer vs player(bot): pvp \nor quit: quit ")

            match choice:
                case "pve":
                    battle(driver,1)
                case "pvp":
                    battle(driver,3)
                case "quit":
                    break
        
    

    


    driver.close()



def battle(driver, battleType):
    battlePath = "/html/body/mobitva/div/table[1]/tbody/tr/td["+str(battleType)+"]"
    driver.find_element(By.XPATH, battlePath).click()

    enemyNum = input("which enemy you want? (1-10) ")
    print()
    ## !
    correctAns = ["a","m","exit"]
    question = input("do you want to have \nautomatic battle: a \nyour decided moves: m\nif neither: exit\n")
    while question not in correctAns:
        question = input("do you want to have \nautomatic battle: a \nyour decided moves: m\nif neither: exit\n")
    print()
    attackCombo = []
    ## !
    match question:
        case "a":
            print("automatic battles only")
        case "m":
            correctAns = ["up","st","dw","bl","ubl"]
            print("you will have to enter your combos.\nAfter your combos automatic battle will start\nCode Does Not Buy Potions For You!")
            print()
            question = input("""
hit up: up
hit straight: st
hit down: dw
                                 
block: bl
unblock: ubl
                                 
potion 1: 1
potion 2: 2
potion 3: 3
potion 4: 4
potion 5: 5 
potion 6: 6
potion 7: 7             
                                  
start bot running now: exit
Reminder: drink or block at the start of your turn\n""")
            if question.lower() in correctAns:
                attackCombo.append(question.lower())
            while question != "exit":
                question = input("""
hit up: up
hit straight: st
hit down: dw
                                 
block: bl
unblock: ubl
                                 
potion 1: 1
potion 2: 2
potion 3: 3
potion 4: 4
potion 5: 5 
potion 6: 6
potion 7: 7             
                                  
start bot running now: exit
Reminder: drink or block at the start of your turn\n""")
                if question.lower() in correctAns:
                    attackCombo.append(question.lower())
        case "exit":
            print("code is stopped and exits")
            sys.exit(0)
        case _:
            print("something went wrong int deciding ")
            sys.exit(0)
    ## !
    battleCount = input("battle count: ")

    ## !
    TRIES = 5
    for i in range(int(battleCount)):
        ## !
        time.sleep(3)
        print()
        print(i+1)

        battleChoiceZone(driver,battleType, TRIES)
        

        ### ^
        time.sleep(1)
        enemyChoiceZone(driver, enemyNum, battleType, TRIES)

        ongoingBattle(driver,attackCombo)


        


def battleChoiceZone(driver, battleType, tries):
    try:    
        if driver.find_element(By.XPATH, '/html/body/mobitva/div/table[3]/tbody/tr/td').text == "Назад":
            return
        driver.find_element(By.XPATH, "/html/body/mobitva/div/table[1]/tbody/tr/td["+str(battleType)+"]").click()
            
    except: 
        if tries < 1:
            print("could not resolve issue with pvp/pve element, closing code")
            sys.exit(1)

        print("Can't find pvp/pve, retry in 3 seconds will try this many times: " + str(tries))
        time.sleep(3)
        battleChoiceZone(driver, battleType, tries-1)

def enemyChoiceZone(driver, enemyNum, battleType,tries):
    try:
        enemy = ''
        match battleType:
            
            case 1:
                enemy = '/html/body/mobitva/div/div/table/tbody/tr[2]/td[2]/div['+str(enemyNum)+']/table/tbody/tr/td[4]'
            case 3:
                enemy = '/html/body/mobitva/div/div/center/div['+str(enemyNum)+']'
            case _:
                print("error clsing down code")
                sys.exit(1)
        
        driver.find_element(By.XPATH, enemy).click()

    except: 
        if tries < 1:
            print("could not resolve issue with pvp/pve element, closing code")
            sys.exit(1)
        print("Can't find enemy in pvp/pve, retry in 3 seconds will try this many times: " + str(tries))
        time.sleep(3)
        battleChoiceZone(driver, enemyNum, tries-1)

MULY_AUTOBATTLE = -0.0822
MULX_AUTOBATTLE = 0

MULY_LAYER_ATTC = 0.1507
MULX_UPATTC = -0.6042
MULX_STRATTC = 0
MULX_DWNATTC = 0.6042

MULY_SHIELD = 0.4247
MULX_SHIELD_POT4 = -0.7083

MULY_POTLAYER1 = 0.4247
MULY_POTLAYER2 = 0.7808

MULX_POT1_5 = -0.25
MULX_POT2_6 = 0.2083
MULX_POT3_7 = 0.6667



def ongoingBattle(driver, attackCombos):
    tries = 15
    while driver.find_element(By.XPATH, "/html/div[8]/div[1]/div/table[3]/tbody/tr/td").text != "Команды":
        if(tries < 0 ):
            print("could not load battle, check internet")
            sys.exit(1)
        print("loading battle..." + str(tries))
        time.sleep(1)
        tries= tries-1
    startTime = time.time()
    index = 0

    canvas = driver.find_element(By.XPATH, "/html/div[8]/div[1]/div/div/canvas")
    ignoreAutoBattle = False
    ## ! canvas mesurments are here because if someone decides to change window size between battle then it will destroy itself, though I could warn, because this will not help
    canvas_height = driver.execute_script("return arguments[0].height", canvas)/2
    canvas_width = driver.execute_script("return arguments[0].width", canvas)/2
    print(attackCombos)
    
    while driver.find_element(By.XPATH, "/html/div[8]/div[1]/div/table[3]/tbody/tr/td").text == "Команды": 
        
        time.sleep(0.3)
        if doesBattleUIExit(driver, canvas_height, canvas_width):
            time.sleep(0.6)

            if index < len(attackCombos):
                match attackCombos[index]:
                    case "up":
                        print("up", end=" ")
                        action_chains = ActionChains(driver)
                        moveY = canvas_height*MULY_LAYER_ATTC
                        moveX = canvas_width*MULX_UPATTC
                        action_chains.move_to_element(canvas).move_by_offset(moveX, moveY).click().perform()
                    case "st":
                        print("st", end=" ")
                        action_chains = ActionChains(driver)
                        moveY = canvas_height*MULY_LAYER_ATTC
                        moveX = canvas_width*MULX_STRATTC
                        action_chains.move_to_element(canvas).move_by_offset(moveX, moveY).click().perform()
                    
                    case "dw":
                        print("dw", end=" ")
                        action_chains = ActionChains(driver)
                        moveY = canvas_height*MULY_LAYER_ATTC
                        moveX = canvas_width*MULX_DWNATTC
                        action_chains.move_to_element(canvas).move_by_offset(moveX, moveY).click().perform()
                        
                    case "bl":
                        print("bl", end=" ")
                        action_chains = ActionChains(driver)
                        moveY = canvas_height*MULY_SHIELD
                        moveX = canvas_width*MULX_SHIELD_POT4
                        action_chains.move_to_element(canvas).move_by_offset(moveX, moveY).click().perform()
                        
                    case "ubl":
                        action_chains = ActionChains(driver)
                        moveY = canvas_height*MULY_SHIELD
                        moveX = canvas_width*MULX_SHIELD_POT4
                        action_chains.move_to_element(canvas).move_by_offset(moveX, moveY).click().perform()
                        
                    case "1":
                        action_chains = ActionChains(driver)
                        moveY = canvas_height*MULY_POTLAYER1
                        moveX = canvas_width*MULX_POT1_5
                        action_chains.move_to_element(canvas).move_by_offset(moveX, moveY).click().perform()
                        
                    case "2":
                        action_chains = ActionChains(driver)
                        moveY = canvas_height*MULY_POTLAYER1
                        moveX = canvas_width*MULX_POT2_6
                        action_chains.move_to_element(canvas).move_by_offset(moveX, moveY).click().perform()
                        
                    case "3":
                        action_chains = ActionChains(driver)
                        moveY = canvas_height*MULY_POTLAYER1
                        moveX = canvas_width*MULX_POT3_7
                        action_chains.move_to_element(canvas).move_by_offset(moveX, moveY).click().perform()
                        
                    case "4":
                        action_chains = ActionChains(driver)
                        moveY = canvas_height*MULY_POTLAYER2
                        moveX = canvas_width*MULX_SHIELD_POT4
                        action_chains.move_to_element(canvas).move_by_offset(moveX, moveY).click().perform()
                        
                    case "5":
                        action_chains = ActionChains(driver)
                        moveY = canvas_height*MULY_POTLAYER2
                        moveX = canvas_width*MULX_POT1_5
                        action_chains.move_to_element(canvas).move_by_offset(moveX, moveY).click().perform()
                        
                    case "6":
                        action_chains = ActionChains(driver)
                        moveY = canvas_height*MULY_POTLAYER2
                        moveX = canvas_width*MULX_POT2_6
                        action_chains.move_to_element(canvas).move_by_offset(moveX, moveY).click().perform()
                        
                    case "7":
                        action_chains = ActionChains(driver)
                        moveY = canvas_height*MULY_POTLAYER2
                        moveX = canvas_width*MULX_POT3_7
                        action_chains.move_to_element(canvas).move_by_offset(moveX, moveY).click().perform()
                        
                    case _:
                        print("something went wrong in execution of attack combos, bot is closing down")
                        driver.close()
                        sys.exit(3)
                index = index+1
            elif not ignoreAutoBattle:
                action_chains = ActionChains(driver)
                moveY = canvas_height*MULY_AUTOBATTLE
                moveX = canvas_width*MULX_AUTOBATTLE
                action_chains.move_to_element(canvas).move_by_offset(moveX, moveY).click().perform()
                ignoreAutoBattle = True

            #match:
            
        if time.time() - startTime > 600:
            print("out of safety code is shutting down")
            driver.close()
            sys.exit(2)
    time.sleep(1)
    driver.find_element(By.XPATH, "/html/body/mobitva/div/div/center/div").click()


def doesBattleUIExit(driver, heigth, width):
    try:
        canvas = driver.find_element(By.XPATH, "/html/div[8]/div[1]/div/div/canvas")

        moveY= heigth*MULY_LAYER_ATTC
        moveX = width*MULX_UPATTC
        action_chains = ActionChains(driver)
        action_chains.move_to_element(canvas).move_by_offset(moveX, moveY).perform()
        if "pointer" in canvas.get_attribute("style"):
            return True
        else:
            return False
    except:
        print("battle does not exist or is done")
        return False

def safeExit(driver, msg):
    pass

main()
