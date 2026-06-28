import fitz, os, sys, hashlib
base = "/Users/borjagarcia/Downloads"
files = {
 'L01': "Notes (7)/CQF_CMM_Linear_Algebra_Lecture01_Blank.pdf",
 'L03a': "Notes (9)/CQF_CMM_Linear_Algebra_Lecture_03_Blank.pdf",
 'L03b': "Notes (9)/CQF_CMM_Linear_Algebra_Lecture_03_Blank 02.pdf",
 'L04': "Notes (10)/CQF_CMM_Linear_Algebra_Lecture_04_Blank.pdf",
 'L05': "Notes (11)/CQF_CMM_Linear_Algebra_Lecture_05_Blank.pdf",
}
tag = sys.argv[1]
dpi = int(sys.argv[2]) if len(sys.argv) > 2 else 120
outdir = "/Users/borjagarcia/Coursera/scratch/la_img/%s" % tag
os.makedirs(outdir, exist_ok=True)
doc = fitz.open(os.path.join(base, files[tag]))
mat = fitz.Matrix(dpi/72, dpi/72)
prev = None
kept = []
for i in range(doc.page_count):
    pix = doc[i].get_pixmap(matrix=mat)
    # full-page hash to skip exact duplicates
    h = hashlib.md5(pix.tobytes("ppm")).hexdigest()
    if h == prev:
        continue
    prev = h
    p = os.path.join(outdir, "p%03d.png" % (i+1))
    pix.save(p)
    kept.append(i+1)
print(tag, "pages", doc.page_count, "rendered(unique-consecutive)", len(kept))
print("kept:", kept)
