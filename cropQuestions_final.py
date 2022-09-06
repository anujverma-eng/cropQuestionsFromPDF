import fitz,re
from PIL import Image
import time
import psutil


def extractquestion(page_no,qn_no,fileName,ssName,zoom):
    try:
        doc = fitz.open(fileName)
    except:
        print("")
        print("************** Error ***************")
        print("File name is not correct || OR || File doesn't exist !!")
        print("************** Kindly Restart app with Right File !! ***************")
        print(("Kindly Don't Proceed further !"))
        print("")
        return
    # area = fitz.paper_size("A4")
    # print(area)
    page = doc.load_page(page_no)
    blocks=page.get_text('dict',flags=0)['blocks']
    start,end=False,False
    useful_block_line_span=[]

    for blockIdx,block in enumerate(blocks):
        for lineIdx,line in enumerate(block["lines"]):
            for wordIdx,word in enumerate(line['spans']):
                # print(word['text'])
                if re.match(fr'{qn_no}\.',word['text']):
                    start=True
                if re.match(fr'{qn_no+1}\.',word['text']):
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
        # print(qn_no," = ",x1-x0,y1-y0)
        if (x1-x0 > 370 or y1-y0>300):
            print("")
            print("************************************ Warning !! ************************************")
            print(f"Unable to save Image for Question: {qn_no}  || You need to crop it Manually")
            print("************************************************************************************")
            print("")
            fileSaveError="Yes"
            return
    except:
        fileSaveError=qn_no
        print("")
        print("************** Error ***************")
        print(f"Error in Question ={qn_no}")
        print("")


    try:
        if (fileSaveError=="NO" ):
            mat = fitz.Matrix(zoom,zoom)
            page.get_pixmap(clip=(x0,y0,x1,y1),matrix=mat).save(f'{ssName}{qn_no:03}.png')
            # if(showMe=="Y"):
            try:
                img = Image.open(f'{ssName}{qn_no:03}.png')
                img.show()
                for proc in psutil.process_iter():
                    if proc.name() == "Microsoft.Photos.exe":
                        # time.sleep(0.02)
                        proc.kill()
            except:
                print("Unable to show Image!")
                
        else:
            mat = fitz.Matrix(2.0,2.0)
            page.get_pixmap(clip=(x0,y0,x1,y1),matrix=mat).save(f'{ssName}{qn_no:03}_ERROR.png')
    except:
        print("")
        print("***************************** Warning !! *********************************")
        print(f"Unable to Save Image for Question {qn_no}  || You need to crop it Manually")
        print("")

print("************  Welcome to the CropQ !! ************  :) anujverma-eng")
print("Happy cropping !!")
print("")
q_done=1
fileName=input("Enter name of PDF file = ")
ssName = input("Enter name of ScreenShots you want to save = ")
print("")
# showMe = input("Do you want to see Images ? (Enter 'Y' for Yes & 'N' for No) = ")
zoom = int(input("Enter the Zoom Factor = "))
print("")
pages = int(input("Enter total number of pages (Having Questions Only) = "))
for page in range(pages):
    questions = int(input(f"Enter the Number of questions in Page - {page+1} = "))+1

    for q in range(q_done,questions):
        extractquestion(page, q,fileName,ssName,zoom)
        q_=q
    q_done=q_
print("")
print("")
print("Thank you for Using !!")
print("           -- Anuj Verma")
time.sleep(180)
print("Good Bye!!")