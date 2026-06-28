import fitz, os, sys
from PIL import Image
base = "/Users/borjagarcia/Downloads"
files = {
 'L01': "Notes (7)/CQF_CMM_Linear_Algebra_Lecture01_Blank.pdf",
 'L04': "Notes (10)/CQF_CMM_Linear_Algebra_Lecture_04_Blank.pdf",
 'L05': "Notes (11)/CQF_CMM_Linear_Algebra_Lecture_05_Blank.pdf",
}
tag = sys.argv[1]
cols, rows = 3, 4   # 12 slides per sheet
thumb_w = 520
doc = fitz.open(os.path.join(base, files[tag]))
outdir = "/Users/borjagarcia/Coursera/scratch/la_contact"
os.makedirs(outdir, exist_ok=True)
imgs = []
for i in range(doc.page_count):
    pix = doc[i].get_pixmap(matrix=fitz.Matrix(thumb_w/ (doc[i].rect.width), thumb_w/(doc[i].rect.width)))
    im = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    imgs.append((i+1, im))
per = cols*rows
sheets = (len(imgs)+per-1)//per
from PIL import ImageDraw
for s in range(sheets):
    chunk = imgs[s*per:(s+1)*per]
    if not chunk: break
    tw = chunk[0][1].width
    th = chunk[0][1].height
    pad = 26
    W = cols*tw + (cols+1)*8
    H = rows*(th+pad) + 8
    sheet = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(sheet)
    for idx,(pno,im) in enumerate(chunk):
        r = idx//cols; c = idx%cols
        x = 8 + c*(tw+8); y = 8 + r*(th+pad)
        d.text((x+2, y), "%s p%d"%(tag,pno), fill="red")
        sheet.paste(im, (x, y+pad-4))
    p = os.path.join(outdir, "%s_sheet%02d.png" % (tag, s+1))
    sheet.save(p)
    print("wrote", p, "pages", chunk[0][0], "-", chunk[-1][0])
