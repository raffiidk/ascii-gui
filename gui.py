
import PySimpleGUI as sg
import os.path
import re
import numpy as np
import csv
import matplotlib.image as mpi 
import matplotlib.pyplot as plt 
import os.path
from pathlib import Path
import webbrowser

sg.theme('SystemDefaultForReal')
leftSide = [
    [
        sg.Text("Image Folder"),
        sg.In(size=(10, 1), enable_events=True, key="-FOLDER-"),
        sg.FolderBrowse(),
    ],
    [
        sg.Listbox(
            values=[], enable_events=True, size=(40, 20), key="-FILE LIST-"
        )
    ],
]

rightSide = [
    [sg.Text("Image: ")],
    [sg.Text(size=(40, 1), key="-TOUT-")],
    [sg.Image(key="-IMAGE-")],
    [sg.Button("Submit Image")]
]

outputLeft = [
    [
        sg.Text("Output Text Document"),
        sg.In(size=(10, 1), enable_events=True, key="-FOLDER2-"),
        sg.FolderBrowse(),
    ],
    [
        sg.Listbox(
            values=[], enable_events=True, size=(40, 20), key="-FILE LIST2-"
        )
    ],
]

outputRight = [
    [sg.Text("Output: ")],
    [sg.Text(size=(25, 1), key="-TOUT2-")],
    [sg.Image(key="-IMAGE2-")],
    [sg.Button("Submit Output")]
]

outputFinal = [
    [sg.Text("Output text: ")],
    [sg.Text(size=(25, 1), key="-TOUT3-")],
    [sg.Image(key="-IMAGE5-")],
]

layout = [
    [
        sg.Column(outputLeft),
        sg.VSeperator(),
        sg.Column(outputRight),
        sg.VSeparator(),
        sg.Column(leftSide),
        sg.VSeparator(),
        sg.Column(rightSide),
        # sg.VSeparator(),
        # sg.Column(outputFinal)
    ]
]

window = sg.Window("IMG To ASCII Text Solution By Amethyst", layout,size=(1500, 440), margins=(0,0),font='Courier 12')

while True:

    event, values = window.read()
    if event == "Exit" or event == sg.WIN_CLOSED:
        break
    
    if event == "-FOLDER-":
        folder = values["-FOLDER-"]
        try:
            fileList = os.listdir(folder)
        except:
            fileList = []

        fnames = [
            f
            for f in fileList
            if os.path.isfile(os.path.join(folder, f))
            and f.lower().endswith((".jpg"))
        ]
        window["-FILE LIST-"].update(fnames)
    
    elif event == "-FILE LIST-":  #chosen file
        try:
            filename = os.path.join(
                values["-FOLDER-"], values["-FILE LIST-"][0]
            )
            window["-TOUT-"].update(filename)
            window["-IMAGE-"].update(filename=filename)
        except:
            pass
    
    if event == "-FOLDER2-":
        folder = values["-FOLDER2-"]
        try:
            fileList2 = os.listdir(folder)
        except:
            fileList2 = []

        fnames = [
            f
            for f in fileList2
            if os.path.isfile(os.path.join(folder, f))
            and f.lower().endswith((".txt"))
        ]
        window["-FILE LIST2-"].update(fnames)

    elif event == "-FILE LIST2-":  #chosen file
        try:
            filename1 = os.path.join(
                values["-FOLDER-"], values["-FILE LIST2-"][0]
            )
            window["-TOUT2-"].update(filename1)
            #window["-IMAGE-"].update(filename=filename)
        except:
            pass
    
    if event == "Submit Output":
        output = filename1


    if event == "Submit Image":
        print("Submit")
        image = window["-IMAGE-"]
        print(filename)
        inputf = filename

        finalist = []
        index_key = 0
        brightness = ["@","#","M","B","H","A","G","h","9","3","X","2","5","S","i","s","r",";",":",",","."," "]                           
        imgval = []
        reshape = []

        def getimg(image):
            while True:
                try:
                    photo = mpi.imread(image)
                    rows = len(photo)
                    cols = len(photo[0])
                    grey  = np.zeros((rows,cols), dtype=np.int8)
                    r = np.array(photo[:,:,0])
                    g = np.array(photo[:,:,1])
                    b = np.array(photo[:,:,2])
                    r = r*0.299
                    g = g*0.587
                    b= b*0.114
                    grey = np.round(r + g + b)
                    imgx = rows
                    imgy = cols
                except FileNotFoundError:
                    print("Please write your file with the full path")
                    break
                return grey,imgx,imgy

        def scale():
            truescale = 1
            lc = 120
            scalex = imgx//lc
            scaley = imgy//lc
            if scalex >= scaley:
                truescale = scalex
            else:
                truescale = scaley
            return truescale

        def box(x,y,scaling):

            newimg = grey

            lhs = scaling // 2

            ups = scaling // 2

            if scaling % 2 == 1:

                ds = scaling // 2

                rhs = scaling // 2

            else:

                ds = scaling // 2 - 1

                rhs = scaling // 2 - 1



            if x - ups < 0:

                ups = x

            if x + ds > imgx:

                ds = imgx - x

            if y - lhs < 0:

                lhs = y

            if y + rhs > imgy:

                rhs = imgy - y

            sumval = 0

            count = 0

            for k in range(-ups,ds):

                for l in range(-lhs,rhs):

                    count = count + 1

                    sumval = sumval + newimg[x+k][y+l]

            sumval = round(sumval / count)

            return sumval




        while True:
            try:
                with open(inputf,"r") as f:
                    f.close()
            except FileNotFoundError:
                print("Input file not found. Try using full path.")
                continue
            if inputf == output:
                print("Please put two separate paths.")
                continue
            else:
                break

        impath = inputf

        grey,imgx,imgy = getimg(inputf)
        truescale = scale()
        plt.imshow(grey)
        plt.show()
        print(imgx,imgy,truescale,"x,y,t")

        for i in range(0,imgx,truescale):
            # print(i)
            finalist.append([])
            for j in range(0,imgy,truescale):
                # print(j)
                boxval = box(i,j,truescale)
                finalist[i//truescale].append(boxval)
                index_key = finalist[i//truescale][j//truescale]//len(brightness)
                finalist[i//truescale][j//truescale] = brightness[index_key]

        with open(output, 'w', encoding='utf-8-sig') as f:
            for i in range(0,len(finalist)):
                for j in range(0,len(finalist[0])):
                    f.write(finalist[i][j])
                f.write("\n")
            print('Succcess! Check output file.') 
        
        webbrowser.open(output)


window.close()