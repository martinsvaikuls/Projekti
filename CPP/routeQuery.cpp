#include <iostream>
#include <fstream>
#include <cstdio>

using namespace std;

const int commaCount = 4;

void route(string fileName);
void routesOnDay(string fileName);
void routesInCost(string fileName);
void errTxTOutPut();
void checkFileIntegrity(string fileName);
string userInputsString(string msg, char mode);
bool fileExists(const string& filename);
int main() {
    string fileName = "db.csv";

    //inFile.open("db.csv");
    //if (!inFile) return 0;
    checkFileIntegrity(fileName);
    cout << "started" << endl;
    string fileName2 = "db.csv";
    ifstream inFile;
    inFile.open(fileName2);
    if (!inFile) return 0;
    string txt;

    while (inFile >> txt) {
       cout << txt << endl;
    }
    inFile.close();
    while (true) {
        char usrInpt;
        cout << "please input a b c d e" << endl;
        cin >> usrInpt;

        switch (usrInpt) {
            case 'a':


                route(fileName);
                break;
            case 'b':
                routesOnDay(fileName);
                break;
            case 'c':
                routesInCost(fileName);
                break;
            case 'd':
                errTxTOutPut();
                break;
            case 'e':
                // close files?
                return 0;
                break;
            default:
                break;


        }

    }
    return 0;
}


void route(string fileName) {
    string sakumaPietura, beiguPietura;

    string msg = "Ievadiet sakuma pieturu";
    sakumaPietura = userInputsString(msg, 'r');

    msg = "Ievadiet beigu pieturu";
    beiguPietura = userInputsString(msg, 'r');


    fileName = "db.csv";
    ifstream txtFile;

    txtFile.open(fileName);
    if (!txtFile) return;

    string txt;
    bool outputRoute;
    bool readMore;

    while (txtFile >> txt) {
        outputRoute = true;
        readMore = true;
        int i = 0;
        while (txt[i] != ',') {
            if (!(sakumaPietura[i] == txt[i])) {
                //cout << "errourSakuma " << sakumaPietura[i] << " " << txt[i] << " " << i << endl;
                readMore = false;
                outputRoute = false;
                break;
            }
            i++;
        }
        i++;
        int j = 0;
        if (readMore) {
            while (txt[i] != ',') {
            if (!(beiguPietura[j] == txt[i])) {
                //cout << "errourReadMore " << beiguPietura[j] << " " << txt[i] << " " << i << endl;
                readMore = false;
                outputRoute = false;
                break;
            }
            j++;
            i++;
        }
        }

        if (outputRoute) {
            cout << txt << endl;
        }

    }
    txtFile.close();

}



void routesOnDay(string fileName) {
    string diena;

    string msg = "Ievadiet nedēļas dienu Pr, Ot, Tr, Ce, Pt, St, Sv";
    diena = userInputsString(msg, 'd');

    ifstream txtFile;
    txtFile.open("db.csv");

    txtFile.open(fileName);
    if (!txtFile) return;

    string txt;
    bool outputRoute;
    bool readMore;

    while (txtFile >> txt) {
        int commaCount = 0;
        int pointer = 0;
        bool printTxt = true;
        while (commaCount != 2) {
            if (txt[pointer] == ',') {
                commaCount++;
            }
            pointer++;
        }
        int j = 0;
        while (txt[pointer] != ',') {
            if (txt[pointer] != diena[j]) {
                printTxt = false;
            }
            pointer++;
            j++;
        }
        if (printTxt) {
            cout << txt << endl;
        }
    }
}

string userInputsString(string msg, char mode) {
    string userInput;
    int charVal;
    bool wrongInput = true;
    switch (mode) {
        case 'r':
            while (wrongInput) {
                cout << msg<< endl;
                cin >> userInput;
                for (int i = 0; i < userInput.length(); i++) {
                    charVal = int(userInput[i]);
                    if ((charVal > 64 && charVal < 91) || (charVal >96 && charVal <123)) wrongInput = false;
                }
            }
            break;
        case 'd':
            while (wrongInput) {
                cout << msg<< endl;
                cin >> userInput;
                userInput[0] = toupper(userInput[0]);
                userInput[1] = tolower(userInput[1]);
                if (userInput == "Pr")      wrongInput=false;
                else if (userInput == "Ot" )wrongInput=false;
                else if (userInput == "Tr" )wrongInput=false;
                else if (userInput == "Ce" )wrongInput=false;
                else if (userInput == "Pt" )wrongInput=false;
                else if (userInput == "St" )wrongInput=false;
                else if (userInput == "Sv" )wrongInput=false;



            }

    }


    return userInput;
}

void routesInCost(string fileName) {

}

void errTxTOutPut() {
    ifstream errFile;

    errFile.open("err.txt");
    if (!errFile) return;

    string txt;

    while (errFile >> txt) {
        cout << txt << endl;
    }
    errFile.close();
}

void checkFileIntegrity(string fileName) {
    ifstream txtFile;

    txtFile.open(fileName);
    if (!txtFile) return;


    ofstream tmpFile("tmp.csv");
    ofstream errFile("err.txt");
    string txt;
    int commaCount;
    while (txtFile >> txt) {
        commaCount = 0;
        for (int i = 0; i < txt.length(); i++) {
            if (txt[i] == ',') {
                commaCount++;
            }
        }
        if (commaCount != 4) {
            cout << "err commacount:" << commaCount << endl;
            errFile << txt << endl;
        }
        else {
            bool readString = false;
            bool properLine = true;
            int commaPointer = 1;
            int pointer = 0;
            int charVal;
            int dotCount = 0;
            int numCountAfterDot = 0;

            while (!readString) {
                int startPointer = pointer;

                switch(commaPointer) {
                    case 1: case 2: // only letters
                        while (txt[pointer] != ',') {
                            charVal = int(txt[pointer]);
                            if ( charVal >64 && charVal < 91) ;
                            else if (charVal > 96 && charVal < 123) ;
                            else {
                                cout << "err in" << commaPointer << endl;
                                cout << txt << endl;
                                properLine = false;
                                commaPointer = 6;
                                break;
                            }
                            pointer++;
                        }
                        if (pointer-startPointer <2) {
                            cout << "err in" << commaPointer << endl;
                            cout << txt << endl;
                            properLine = false;
                            commaPointer = 6;
                            break;
                        }
                        pointer++;
                        commaPointer++;
                        break;

                    case 3: // two letters max, only letters
                        while (txt[pointer] != ',') {
                            charVal = int(txt[pointer]);
                            if ( charVal >64 && charVal < 91) ;
                            else if (charVal > 96 && charVal < 123) ;
                            else {
                                cout << "err in" << commaPointer << endl;
                                cout << txt << endl;
                                properLine = false;
                                commaPointer = 6;
                                break;
                            }
                            pointer++;
                        }
                        if (pointer-startPointer != 2){
                            cout << "err in" << commaPointer << endl;
                            cout << txt << endl;
                            properLine = false;
                            commaPointer = 6;
                            break;
                        }
                        pointer++;
                        commaPointer++;
                        break;

                    case 4: // two digits Colon: two digits
                        while (txt[pointer] != ',') {
                            charVal = int(txt[pointer]);

                            if ((charVal > 47 && charVal < 58) || charVal == 58) {

                                switch(pointer-startPointer) {

                                    case 0:
                                        if (charVal > 50) {
                                            cout << "err in " << commaPointer << "case: " << pointer-startPointer << endl;
                                            cout << txt << endl;
                                            properLine = false;
                                            commaPointer = 6;
                                            pointer += 6; // 1
                                        }
                                        break;
                                    case 1: case 4:
                                        if (charVal == 58) {
                                            cout << "err in " << commaPointer << "case: " << pointer-startPointer << endl;
                                            cout << txt << endl;
                                            properLine = false;
                                            commaPointer = 6;
                                            pointer += 7; //2
                                        }
                                        break;
                                    case 2:
                                        if (charVal != 58) {
                                            cout << "err in " << commaPointer << "case: " << pointer-startPointer << endl;
                                            cout << txt << endl;
                                            properLine = false;
                                            commaPointer = 6;
                                            pointer += 8; //3
                                        }
                                        break;
                                    case 3:
                                        if (charVal > 54) {
                                            cout << "err in " << commaPointer << "case: " << pointer-startPointer << endl;
                                            cout << txt << endl;
                                            properLine = false;
                                            commaPointer = 6;
                                            pointer += 9; // 4
                                        }
                                        break;
                                }

                            }
                            else {
                                cout << charVal << " " << txt[pointer-5];
                                cout << "err in" << commaPointer << pointer-startPointer-5 << endl;
                                cout << txt << endl;
                                properLine = false;
                                commaPointer = 6;
                                break;
                            }
                            if (!properLine) {
                                break;
                            }
                            pointer++;
                        }


                        if (pointer-startPointer < 2){

                            cout << "err in" << commaPointer<< "length: " << pointer-startPointer-5 << endl;
                            cout << txt << endl;
                            properLine = false;
                            commaPointer = 6;
                            break;
                        }
                        pointer++;
                        commaPointer++;
                        break;

                    case 5:
                        while (pointer < txt.length()) {
                            charVal = int(txt[pointer]);
                            cout << charVal << " "<< txt[pointer] << endl;

                            if (dotCount == 1) {
                                numCountAfterDot++;
                                cout << numCountAfterDot << endl;
                            }
                            if (charVal == 46) {
                                dotCount++;
                                cout <<"countingDots " << dotCount << endl;
                            }


                            if ((charVal < 46 && charVal >57 ) || dotCount > 1 || charVal == 47 || numCountAfterDot > 2) {
                                cout << "err in" << commaPointer << endl;
                                cout << txt << endl;
                                properLine = false;
                                commaPointer = 6;
                                break;
                            }
                            pointer++;
                        }
                        if (pointer-startPointer < 2 || dotCount != 1){
                            cout << "dotCoutn: " << dotCount << endl;
                            cout << "err in" << commaPointer << endl;
                            cout << txt << endl;
                            properLine = false;
                            commaPointer = 6;
                            break;
                        }
                        pointer++;
                        commaPointer++;
                        break;

                    default:
                        readString = true;
                        break;

            }

            }


            cout << properLine << endl;
            if (properLine) {
                tmpFile << txt << endl;
            }
            else {
                errFile << txt << endl;
            }
        }

        //string arr[5];


    }


    txtFile.close();
    tmpFile.close();
    errFile.close();
    const char* oldname = "tmp.csv";
    const char* newname = "db.csv";

    if (fileExists(newname)) {
        // Try to remove the existing file
        if (remove(newname) != 0) {
            cout << "error deleting file" << endl;
            return;
        }
        cout << "file deleted"<< endl;
    }

    if (rename(oldname, newname) != 0)
		perror("Error renaming file");
	else
		cout << "File renamed successfully";

}

bool fileExists(const std::string& filename) {
    ifstream file(filename);
    return file.good();  // Returns true if the file exists
}

// string string string string int
