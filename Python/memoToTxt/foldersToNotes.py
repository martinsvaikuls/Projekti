import os
import zipfile
from time import strftime, localtime
import urls

folderPath = r"D:\testingSavingMemos"
for filename in os.listdir(folderPath):
    print(filename)
    file_path = folderPath+"\\"+filename

    for filename2 in os.listdir(file_path):
        file_path2 = file_path+"\\"+filename2
        #print(file_path2)
        #print(filename2)
        with open(file_path2+"\\"+filename2+".md", "w", encoding="utf-8") as newFile:
            for text in os.listdir(file_path2):
                newFile.write("[["+text+"]]\n")

        newFile.close()
        print(filename2)

    with open(file_path+"\\"+filename+".md", "w", encoding="utf-8") as newFile:
        for text in os.listdir(file_path):
            newFile.write("[["+text+"]]\n")
    newFile.close()
    
    