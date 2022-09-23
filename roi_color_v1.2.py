import fitz,re
from PIL import Image
import time
import cv2
import numpy as np
import psutil
import os
from colorama import init
from colorama import Fore, Back, Style

init()

# ! Draw ROI Function
def drawROI(fileName,page,page_no):
    page.get_pixmap().save(f'Page({page_no+1}).png')
    pageImg = cv2.imread(f'Page({page_no+1}).png')
    print(Style.DIM+Fore.WHITE+"")
    try:
        x,y,w,h = cv2.selectROI(pageImg)
        cv2.destroyAllWindows()
        return x,y,w,h
    except Exception as e:
        print("")
        print(e)
        print("You need to crop Image Manually, Unable to Open ROI Selector !!")
        print(Style.BRIGHT)
        return 0,0,0,0

# ! Extract Questions Function
def extractquestion(page_no,qn_no,fileName,ssName,zoom,imgName):
    try:
        try:
            doc = fitz.open(fileName)
            page = doc.load_page(page_no)
            try:
                r1 = page.search_for("SECTION - B", quads = True)
                page.add_redact_annot(r1[0])
                page.apply_redactions()
                r2 = page.search_for("SECTION - C", quads = True)
                page.add_redact_annot(r2[0])
                page.apply_redactions()
                r3 = page.search_for("SECTION - D", quads = True)
                page.add_redact_annot(r3[0])
                page.apply_redactions()
                r4 = page.search_for("SECTION - E", quads = True)
                page.add_redact_annot(r4[0])
                page.apply_redactions()
                r5 = page.search_for("SECTION - F", quads = True)
                page.add_redact_annot(r5[0])
                page.apply_redactions()
                r6 = page.search_for("SECTION - G", quads = True)
                page.add_redact_annot(r6[0])
                page.apply_redactions()
                r7 = page.search_for("SECTION - H", quads = True)
                page.add_redact_annot(r7[0])
                page.apply_redactions()
                r8 = page.search_for("SECTION - I", quads = True)
                page.add_redact_annot(r8[0])
                page.apply_redactions()
                r9 = page.search_for("SECTION - J", quads = True)
                page.add_redact_annot(r9[0])
                page.apply_redactions()
            except:
                allOk=True
        except:
            print(Fore.RED+Style.BRIGHT+"")
            print("************** Error ***************")
            print("File name is not correct || OR || File doesn't exist !!")
            print("************** Kindly Restart app with Right File !! ***************")
            print(("Kindly Don't Proceed further !"))
            print(Style.RESET_ALL+"")
            return
        blocks=page.get_text('dict',flags=0)['blocks']
        start,end=False,False
        useful_block_line_span=[]

        for blockIdx,block in enumerate(blocks):
            for lineIdx,line in enumerate(block["lines"]):
                for wordIdx,word in enumerate(line['spans']):
                    if re.match(fr'{qn_no}\.',word['text']):
                        start=True
                    if (re.match(fr'{qn_no+1}\.',word['text'])):
                        end=True
                    if end:break
                    if start:
                        useful_block_line_span.append((blockIdx,lineIdx,wordIdx))
            if end:break
        point = [blocks[blk]['lines'][line]['spans'][span]['bbox']for blk,line,span in useful_block_line_span]
        fileSaveError="NO"
        try:
            x0=min([i[0]for i in point])+15
            y0=min([i[1]for i in point])
            x1=max([i[2]for i in point])+5
            y1=max([i[3]for i in point])
            if (x1-x0 > 370 or y1-y0>300):
                print(Fore.CYAN+Style.BRIGHT+"")
                # print("************************************ Warning !! ************************************")
                print(f"Crop Image for Question: {qn_no} || USE ROI & Select the Image.")
                # print("************************************************************************************")
                print("")
                x,y,w,h = drawROI(fileName, page, page_no)
                if(x==0 and y==0 and w==0 and h==0):
                    return
                time.sleep(0.1)
                x0=x
                y0=y
                x1=x+w
                y1=y+h
                print(Style.RESET_ALL+"")
        except:
            try:
                print(Fore.CYAN+Style.BRIGHT+"")
                # print("************************************ Warning !! ************************************")
                print(f"Crop Image for Question: {qn_no} || USE ROI & Select the Image.")
                # print("************************************************************************************")
                x,y,w,h = drawROI(fileName, page, page_no)
                x0=x
                y0=y
                x1=x+w
                y1=y+h
                print(Style.RESET_ALL+"")
            except:
                print(Fore.RED+Style.BRIGHT+"")
                print("Some Major Error in question "+qn_no+" Kindly crop it Manually !")
                print(Style.RESET_ALL+"")
                fileSaveError="Yes"


        try:
            if (fileSaveError=="NO" ):
                mat = fitz.Matrix(zoom,zoom)
                if(imgName=="Y"):
                    page.get_pixmap(clip=(x0,y0,x1,y1),matrix=mat).save(f'{ssName}{qn_no:03}.png')
                else:
                    page.get_pixmap(clip=(x0,y0,x1,y1),matrix=mat).save(f'{qn_no}.png')
                # if(showMe=="Y"):
                try:
                    if(imgName=="Y"):
                        img = Image.open(f'{ssName}{qn_no:03}.png')
                    else:
                        img = Image.open(f'{qn_no}.png')
                    img.show()
                    for proc in psutil.process_iter():
                        if proc.name() == "Microsoft.Photos.exe":
                            # time.sleep(0.02)
                            proc.kill()
                except:
                    print(Fore.RED+Style.BRIGHT+"Unable to show Image!")
                return
            else:
                mat = fitz.Matrix(2.0,2.0)
                if(imgName=="Y"):
                    page.get_pixmap(clip=(x0,y0,x1,y1),matrix=mat).save(f'{ssName}{qn_no:03}_ERROR.png')
                else:
                    page.get_pixmap(clip=(x0,y0,x1,y1),matrix=mat).save(f'{qn_no}.png')
                return
        except:
            print(Fore.RED+Style.BRIGHT+"")
            print("***************************** Warning !! *********************************")
            print(f"Unable to Save Image for Question {qn_no}  || You need to crop it Manually")
            print("")
            print(Style.RESET_ALL+"")
            return
    except Exception as e:
        print(Fore.RED+Style.BRIGHT+"")
        print(str(e))
        print("************************ OOP's !! There is some error, Kindly connect with :within FN) *******************************")
        print("------------------ Anuj Verma || 78886-65915   || anuj@pw.live  || anujverma123ok@gmail.com -----------------")
        print(Style.RESET_ALL+"")
        return


# ! Default RUNNER
def defaultRunner():
    q_done=1
    fileName=input("Enter name of PDF file = ")
    imgName = input("Do you want to save images with custom name (Y/N) ")
    ssName=""
    if(imgName=="Y" or imgName=="y"):
        ssName = input("Enter name of ScreenShots you want to save = ")
    
    print("")

    # showMe = input("Do you want to see Images ? (Enter 'Y' for Yes & 'N' for No) = ")
    try:
        zoom = int(input("Enter the Zoom Factor = "))
    except:
        print("Enter the Numeric value Between (1 to 50), Enter value 10 for 200% Zoom")
    print("")
    pages = int(input("Enter total number of pages (Having Questions Only) = "))
    for page in range(pages):
        print(Fore.GREEN+Style.BRIGHT+"")
        questions = int(input(f"Enter the Number of questions in Page - {page+1} = "))+1

        for q in range(q_done,questions):
            extractquestion(page, q,fileName,ssName,zoom,imgName)
            q_=q
        q_done=q_+1
    return

# ! CUSTOM PAGE INPUT FUNCTION
def CustomPageInput():
    fileName=input("Enter name of PDF file = ")
    imgName = input("Do you want to save images with custom name (Y/N) ")
    ssName=""
    if(imgName=="Y" or imgName=="y"):
        imgName="Y"
        ssName = input("Enter name of ScreenShots you want to save = ")
    
    print("")
    try:
        zoom = int(input("Enter the Zoom Factor = "))
    except:
        print("Enter the Numeric value Between (1 to 50), Enter value 10 for 200% Zoom")
    print("")
    pageStart = int(input("Enter the Page Number from questions STARTS : "))-1
    pageEnd = int(input("Enter the Page Number from questions   ENDS : "))
    for page in range(pageStart,pageEnd):
        print(Fore.GREEN+Style.BRIGHT+"")
        questStart = int(input(f"Enter the Question Number START in Page - {page+1} = "))
        questEnd = int(input(f"Enter the Question Number ENDS in Page - {page+1} = "))+1
        for q in range(questStart,questEnd):
            # print(f"page = {page} & Q = {q}")
            extractquestion(page, q,fileName,ssName,zoom,imgName)
            q_=q
    return



# ! Main Function Starts from here!!

try:
    print("")
    print(Fore.YELLOW+Style.BRIGHT+"************  Welcome to the Crop Tool || Physics Wallah Private Limited ||!! ************  :) anujverma-eng")
    print("Happy cropping !!")
    print(Style.RESET_ALL)
    print("")
    print(Style.BRIGHT+Fore.WHITE+Back.BLUE+"")
    print("-------- Choose your Program to run for : --------")
    print("    1. Default Runner                             ")
    print("    2. Custom Page input                          ")
    # print(Style.RESET_ALL)
    print(Fore.BLUE+Style.BRIGHT+Back.RESET+"")
    runner = int(input("Enter you Runner: "))
    print(Fore.GREEN+Style.BRIGHT+Back.RESET+"")
    print("")
    if(runner==1):
        print("YOU HAVE CHOOSE DEFAULT RUNNER")
        defaultRunner()
    elif(runner==2):
        print("YOU HAVE CHOOSE CUSTOM PAGE RUNNER")
        CustomPageInput()
    else:
        print("YOU HAVE CHOOSE DEFAULT RUNNER")
        defaultRunner()

    print("")
    print(Fore.BLUE+Style.BRIGHT+"")
    print("Thank you for Using !!")
    print("           -- Anuj Verma")
    time.sleep(180)
    print("Good Bye!!")
except:
    print(Fore.RED+Style.BRIGHT+"")
    print("************************ OOP's !! There is some error, Kindly connect with :Starting FN) *******************************")
    print("--------------------------- Share the Screen shot of the command prompt with --------------------------------")
    print("------------------ Anuj Verma || 78886-65915   || anuj@pw.live  || anujverma123ok@gmail.com -----------------")
    print("")