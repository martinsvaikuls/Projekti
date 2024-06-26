import pywinauto
import time

time.sleep(1)
pywinauto.mouse.click(coords = (1769, 200))
timeStart = time.time()
timeToScroll = 1.4
stop = ""
quit = ""
while quit != "quit":
    print("do not touch device")
    while time.time() - timeStart < timeToScroll:
        pywinauto.keyboard.send_keys("{UP down}")

    pywinauto.keyboard.send_keys("{VK_LWIN down}"
                                    "{VK_SHIFT down}"
                                    "{s down}")
    pywinauto.mouse.press(coords = (1376, 97))
    pywinauto.mouse.release(coords = (1906, 979))
    pywinauto.keyboard.send_keys("{VK_SHIFT up}"
                                    "{VK_LWIN up}"
                                    "{s up}")
    pywinauto.mouse.click(coords = (301, 337))
    pywinauto.keyboard.send_keys("{VK_CONTROL down}"
                                "{v down}")

    pywinauto.keyboard.send_keys("{VK_CONTROL up}"
                                "{v up}")

    pywinauto.keyboard.send_keys("{VK_CONTROL down}"
                                "{a down}"
                                )

    pywinauto.keyboard.send_keys("{VK_CONTROL up}"
                                "{a up}"
                                )
    pywinauto.keyboard.send_keys("{BACKSPACE}")
    print("free window time to stop script")
    #for i in range(5):


"""
print screen info
1376 97
1906 979

"""
