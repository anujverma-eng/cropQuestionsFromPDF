import fitz,re
from PIL import Image
import time
import psutil


def extractquestion(page_no,qn_no,fileName):
    doc = fitz.open(fileName)
    page = doc.load_page(page_no)
    blocks=page.get_text('dict',flags=0)['blocks']
    start,end=False,False
    useful_block_line_span=[]

    for blockIdx,block in enumerate(blocks):
        for lineIdx,line in enumerate(block["lines"]):
            for wordIdx,word in enumerate(line['spans']):
                # print(word['text'])
                if re.match(fr'{qn_no}\.',word['text']):
                    # print("Start Status",word['text'])
                    start=True
                if re.match(fr'{qn_no+1}\.',word['text']):
                    # print("End Status",word['text'])
                    end=True
                if end:break
                if start:
                    useful_block_line_span.append((blockIdx,lineIdx,wordIdx))
        if end:break
    point = [blocks[blk]['lines'][line]['spans'][span]['bbox']for blk,line,span in useful_block_line_span]
    fileSaveError="NO"
    try:
        x0=min([i[0]for i in point])+10
        y0=min([i[1]for i in point])
        x1=max([i[2]for i in point])+10
        y1=max([i[3]for i in point])
    except:
        print("")
        print("************** Error ***************")
        print("")
        print(f"Error in Question ={qn_no}")
        fileSaveError=qn_no


    try:
        if (fileSaveError=="NO" ):
            mat = fitz.Matrix(2.0,2.0)
            page.get_pixmap(clip=(x0,y0,x1,y1),matrix=mat).save(f'{qn_no}.png')
            img = Image.open(f'{qn_no}.png')
            img.show()
            print(f'{qn_no}.png saved')
            for proc in psutil.process_iter():
                if proc.name() == "Microsoft.Photos.exe":
                    # time.sleep(0.02)
                    proc.kill()
        else:
            mat = fitz.Matrix(2.0,2.0)
            page.get_pixmap(clip=(x0,y0,x1,y1),matrix=mat).save(f'{qn_no}_ERROR.png')
    except:
        print("")
        print("*********** Warning !! ********************")
        print(f"Unable to Save Image for Question {qn_no}")
        print("")

print("************  Welcome to the CropQ !! ************  :) anujverma-eng")
print("Happy cropping !!")
print("")
q_done=1
fileName=input("Enter name of PDF file = ")
pages = int(input("Enter total number of pages (Having Questions Only) = "))
for page in range(pages):
    questions = int(input(f"Enter the Number of questions in Page - {page+1} = "))+1

    for q in range(q_done,questions):
        extractquestion(page, q,fileName)
        q_=q
    q_done=q_
print("Thank you for Using !!")
print("           -- Anuj Verma")
time.sleep(10)
print("Good Bye!!")