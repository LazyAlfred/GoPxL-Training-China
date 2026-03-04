import fitz  # PyMuPDF库

doc = fitz.open("BROCHURE_GoPxL_CN_WEB-2.pdf")
for i in range(len(doc)):
    for img in doc.get_page_images(i):
        xref = img[0]
        pix = fitz.Pixmap(doc, xref)
        pix.save(f"image_p{i}_{xref}.png") # 自动保存为高清PNG