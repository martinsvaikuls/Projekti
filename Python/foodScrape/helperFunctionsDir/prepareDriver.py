from selenium.webdriver.common.by import By 

import time


def prepareMaxima(driver):
    HALF_SCREEN_SORTING_FOOD_BOX = "b-category-children--pseudoselect.b-pseudoselect--title"
                             #"b-category-children--pseudoselect b-pseudoselect--title"
                             
    #HALF_SCREEN_OPEN_SORTING_BOX = "b-category-children b-pseudoselect--items.b-show-pseudoselect-list"
    HALF_SCREEN_OPEN_SORTING_BOX = "/html/body/div[3]/div/div[3]/div/div[3]/div[1]/div[2]"
    FULL_SCREEN_SORTING_BOX = "b-category-children--wrap.b-pseudoselect.b-pseudoselect--padding.b-category-page--navigation"
                            
    OPEN_SORTING_PREF_BOX = "b-orderby.form-control"
    SORTING_PREF = "//option[@value='comparativePriceAsc']"

    #"b-orderby form-control" when half screen for clicking on dropdown 

    try:
        try:
            # as of right now i don't know the reason for this 2024/8/14 because next one just overwrites this one anyways always
            driver.find_element(By.CLASS_NAME, HALF_SCREEN_SORTING_FOOD_BOX).click()
            time.sleep(0.5)
            price = driver.find_element(By.CLASS_NAME, HALF_SCREEN_OPEN_SORTING_BOX)
            
        except:
            print("prepareDriver -> prepareMaxima -> lowest level exception")
            price = driver.find_element(By.CLASS_NAME, FULL_SCREEN_SORTING_BOX) ##! not tested in 8/20/2024
        
        
        ##bad
        ##! but why?? 14/02/2024
        ##! yeah these upper comments don't help at all 4/8/2024
        
        price.find_element(By.CLASS_NAME, OPEN_SORTING_PREF_BOX).click()
        time.sleep(0.5)

        price.find_element(By.XPATH, SORTING_PREF).click()
        time.sleep(8)
        
        return driver
    except:
        print("prepareMaxima -> cant sort like normal human")
    
    return driver


def prepareRimi(driver):
    ##!Getting rid of ad
    try:
        time.sleep(1)
        COOKIES_ID = "CybotCookiebotDialogBodyLevelButtonLevelOptinDeclineAll"
        CLOSE_AD_CLASS = "modal__close"
        
        driver.find_element(By.ID, COOKIES_ID).click()
        time.sleep(3)
        driver.find_element(By.CLASS_NAME, CLOSE_AD_CLASS).click()
    except:
        print("prepareDriver -> prepareRimi did not find ad")
    ### ^


    ##!Sort by price per kg
    try: 
        ##!Getting it to be sorted in proper way
        OPEN_SORTING_BOX_CLASS = "link-button.-with-right-icon.section-header__sort.js-distill"
        SORTING_BOX_CONTENTS_CLASS = "distill-dropdown.js-sort-content"
        SORTING_BY_LOWEST_XPATH = ".//ul/li[5]/label"

        driver.find_element(By.CLASS_NAME, OPEN_SORTING_BOX_CLASS).click()
        time.sleep(0.2)
        sort = driver.find_element(By.CLASS_NAME, SORTING_BOX_CONTENTS_CLASS)
        sort.find_element(By.XPATH, SORTING_BY_LOWEST_XPATH).click()
        
    except:
        print("prepareRimi -> Unable to sort by kg, will sort by popularity")

    try:
        ##!Getting 80 items
        OPEN_PROD_COUNT_CLASS = "link-button.-with-right-icon.section-header__pages.js-distill"
        PROD_COUNT_CONTENTS_CLASS = "distill-dropdown.js-page-size-content"
        PROD_80_COUNT = ".//ul/li[4]/label"

        driver.find_element(By.CLASS_NAME, OPEN_PROD_COUNT_CLASS).click()
        time.sleep(0.2)
        dropdown = driver.find_element(By.CLASS_NAME, PROD_COUNT_CONTENTS_CLASS)
        dropdown.find_element(By.XPATH, PROD_80_COUNT).click()
    except:
        print("prepareRimi -> unable to get 80 items")

    try:
        ##!Accepting New changes
        ACCEPT_CHANGES_CLASS = "button.-small.gtm"

        driver.find_element(By.CLASS_NAME, ACCEPT_CHANGES_CLASS).click()
        time.sleep(0.2)
    except:
        print("prepareRimi -> could not save changes")


    time.sleep(4)
    return driver
    

def preparePromo(driver):
    pass


def prepareLats(driver):
    
    try:
        OPEN_SORTING_BOX_CLASS = "jq-selectbox__select"
        SORTING_BOX_CONTENTS_CLASS = "jq-selectbox__dropdown"
        SORTING_BY_LOWEST_XPATH = ".//ul/li[4]"
        driver.find_element(By.CLASS_NAME, OPEN_SORTING_BOX_CLASS).click()
        time.sleep(0.2)
        sort = driver.find_element(By.CLASS_NAME, SORTING_BOX_CONTENTS_CLASS)
        sort.find_element(By.XPATH, SORTING_BY_LOWEST_XPATH).click()
    except:
        print("prepareLats -> Unable to sort by kg, will sort by popularity")

    return driver


def prepareElvi(driver):
    return driver # literally does not have any way to prepare the browser


def prepareTop(driver):
    ACCEPT_COOKIES_CLASS = "cookie-accept-all.button.btn.btn-primary"
    PERSONAL_COOKIES_CLASS = "cookie-adjust.button.btn.btn-secondary"
    ACCEPT_FEW_COOKIES_CLASS = "cookie-accept.button.btn.btn-secondary"
    
    
    return driver