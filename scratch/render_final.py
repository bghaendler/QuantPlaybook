import fitz, os, sys
import numpy as np
base = "/Users/borjagarcia/Downloads"
files = {
 'L01': "Notes (7)/CQF_CMM_Linear_Algebra_Lecture01_Blank.pdf",
 'L04': "Notes (10)/CQF_CMM_Linear_Algebra_Lecture_04_Blank.pdf",
 'L05': "Notes (11)/CQF_CMM_Linear_Algebra_Lecture_05_Blank.pdf",
}
tag = sys.argv[1]
dpi = 110
outdir = "/Users/borjagarcia/Coursera/scratch/la_final/%s" % tag
os.makedirs(outdir, exist_ok=True)
doc = fitz.open(os.path.join(base, files[tag]))
mat = fitz.Matrix(dpi/72, dpi/72)

# render all to small grayscale arrays for diffing
small = []
for i in range(doc.page_count):
    pix = doc[i].get_pixmap(matrix=fitz.Matrix(0.25, 0.25), colorspace=fitz.csGRAY)
    a = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width).astype(np.int16)
    small.append(a)

def diff_frac(a, b):
    if a.shape != b.shape:
        return 1.0
    return np.mean(np.abs(a-b) > 30)

keep = []
n = doc.page_count
for i in range(n):
    if i == n-1:
        keep.append(i)
    else:
        d = diff_frac(small[i], small[i+1])
        # keep page i if next page changes a lot (slide boundary / reset)
        if d > 0.012:
            keep.append(i)
# Also drop a kept page if it's nearly identical to the previously kept one
final = []
for i in keep:
    if final and diff_frac(small[final[-1]], small[i]) < 0.012:
        final[-1] = i  # prefer the later (more complete) frame
    else:
        final.append(i)

mat = fitz.Matrix(dpi/72, dpi/72)
for i in final:
    pix = doc[i].get_pixmap(matrix=mat)
    pix.save(os.path.join(outdir, "p%03d.png" % (i+1)))
print(tag, "total", n, "kept", len(final), [x+1 for x in final])
