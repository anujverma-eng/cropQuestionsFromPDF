import fitz,re
from PIL import Image
def extractquestion(page_no,qn_no,fileName):
    doc = fitz.open(fileName)
    page = doc.load_page(page_no)
    blocks=page.get_text('dict',flags=0)['blocks']
    start,end=False,False
    useful_block_line_span=[]

    for blockidx,block in enumerate(blocks):
        for lineidx,line in enumerate(block["lines"]):
            for wordidx,word in enumerate(line['spans']):
                # print(word['text'])
                if re.match(fr'{qn_no}\.',word['text']):
                    # print("Start Status",word['text'])
                    start=True
                if re.match(fr'{qn_no+1}\.',word['text']):
                    # print("End Status",word['text'])
                    end=True
                if end:break
                if start:
                    useful_block_line_span.append((blockidx,lineidx,wordidx))
        if end:break
    point = [blocks[blk]['lines'][line]['spans'][span]['bbox']for blk,line,span in useful_block_line_span]
    # print(point)
    # print(50*'*')
    fileSaveError="NO"
    try:
        x0=min([i[0]for i in point])
        y0=min([i[1]for i in point])
        x1=max([i[2]for i in point])
        y1=max([i[3]for i in point])
        # print(x1-x0,y1-y0)
    except:
        print(f"Error in Question ={qn_no}")
        fileSaveError=qn_no


    try:
        if (fileSaveError=="NO" ):
            mat = fitz.Matrix(2.0,2.0)
            page.get_pixmap(clip=(x0,y0,x1,y1),matrix=mat).save(f'{fileName}_Q{qn_no}.png')
        else:
            mat = fitz.Matrix(2.0,2.0)
            page.get_pixmap(clip=(x0,y0,x1,y1),matrix=mat).save(f'{fileName}_Q{qn_no}_ERROR.png')
    except:
        print(f"Unable to Save Image for Question {qn_no}")
    # display(Image.open("question.png"))

# extractquestion(1,13)
q_done=1
fileName=input("Enter name of file = ")
pages = int(input("Enter total number of pages "))
for page in range(pages):
    questions = int(input(f"Enter the Number of questions in Page - {page+1} = "))+1

    for q in range(q_done,questions):
        extractquestion(page, q,fileName)
        q_=q
    q_done=q_
    # print(q_done)
    # print(i)3