import fitz, os
base = "/Users/borjagarcia/Downloads"
files = [
 ('L01', "Notes (7)/CQF_CMM_Linear_Algebra_Lecture01_Blank.pdf"),
 ('L03a', "Notes (9)/CQF_CMM_Linear_Algebra_Lecture_03_Blank.pdf"),
 ('L03b', "Notes (9)/CQF_CMM_Linear_Algebra_Lecture_03_Blank 02.pdf"),
 ('L04', "Notes (10)/CQF_CMM_Linear_Algebra_Lecture_04_Blank.pdf"),
 ('L05', "Notes (11)/CQF_CMM_Linear_Algebra_Lecture_05_Blank.pdf"),
]
out = []
for tag, f in files:
    path = os.path.join(base, f)
    doc = fitz.open(path)
    out.append("\n\n############ %s  (%d pages)  %s ############" % (tag, doc.page_count, f))
    seen = set()
    for i in range(doc.page_count):
        t = doc[i].get_text().strip()
        if t in seen:
            continue
        seen.add(t)
        out.append("==== %s p%d ====" % (tag, i+1))
        out.append(t)
open("/Users/borjagarcia/Coursera/scratch/la_dump.txt", "w").write("\n".join(out))
print("done; chars", sum(len(x) for x in out))
