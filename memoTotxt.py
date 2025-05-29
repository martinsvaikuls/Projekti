# ren *.memo *.zip

import os
import zipfile
from time import strftime, localtime
import urls


folderPath = r"path"


timeFindTxt = "<meta createdTime=\""
newFilePath = r""

pathToFolder = ""
innerObsPath = ""

count = 0
for filename in os.listdir(folderPath):
    file_path = os.path.join(folderPath, filename)

    try:
        ##! Opening the file and reading it 
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            try:
                with zip_ref.open("memo_content.xml", 'r') as file:
                    wholeContent = file.read().decode("utf-8")



                    timeStart = int(wholeContent.find(timeFindTxt))
                    timeEnd = int(wholeContent[timeStart+len(timeFindTxt):].find("/>"))-1+timeStart+len(timeFindTxt)-3
                    epochTime = int(wholeContent[timeStart+len(timeFindTxt):timeEnd])
 

                    textStart = int(wholeContent.find("<content>"))
                    textEnd = int(wholeContent.find("</content>"))
                    text = wholeContent[textStart:textEnd+len("</content>")]
                    text = text.replace("&lt;", "<")
                    text = text.replace("&gt;", ">")


                    ##! Making directory and saving the contents
                    year =  strftime("%Y", localtime(epochTime))
                    if not os.path.exists(urls.pathToObisdMemos+"\\"+year):
                        os.mkdir(urls.pathToObisdMemos+"\\"+year)


                    month = strftime("%m%B", localtime(epochTime))
                    if not os.path.exists(urls.pathToObisdMemos+"\\"+year+"\\"+month):
                        os.mkdir(urls.pathToObisdMemos+"\\"+year+"\\"+month)


                    newFilePath = urls.pathToObisdMemos+"\\"+year+"\\"+month+"\\"+str(epochTime)+".md"
                    with open(newFilePath, "w", encoding="utf-8") as newFile:
                        newFile.write(text)
                    newFile.close()


                
                    ##! saving media file 

                    if (text.find("img src=") is not -1):
                        mediaPath = urls.pathToObisdMemos+"\\"+year+"\\"+month+"\\attachment"+year+month+str(epochTime)
                        zip_ref.extract("media/", mediaPath)


                    print(year, end=" ")
                file.close()
            except Exception as err:
                print(err)
                print("couldnt open xml")

        zip_ref.close()
            

        
        

    except Exception as err:
        print("uh oh couldnt open: ")
        print(file_path)
        print(err)
    
    
    count+=1
    print("Memo converted to MD: "+str(count))
    #input()




