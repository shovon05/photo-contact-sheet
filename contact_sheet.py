import os
from PIL import Image
import pillow_heif
from tqdm import tqdm

pillow_heif.register_heif_opener()

def generate_contact_sheet(
    image_folder,
    output_pdf,
    photo_size_in=2,
    margin_in=0,
    dpi=300
):

    photo_px = int(photo_size_in * dpi)
    margin_px = int(margin_in * dpi)

    A4_W_IN = 8.27
    A4_H_IN = 11.69

    page_w = int(A4_W_IN * dpi)
    page_h = int(A4_H_IN * dpi)

    cell = photo_px + margin_px

    cols = page_w // cell
    rows = page_h // cell

    print("Grid:", cols, "x", rows)
    print("Photos per page:", cols * rows)

    valid_ext = (".jpg",".jpeg",".png",".heic")

    files = [
        f for f in os.listdir(image_folder)
        if f.lower().endswith(valid_ext)
    ]

    files.sort()

    pages = []
    page = Image.new("RGB",(page_w,page_h),"white")

    x = 0
    y = 0

    for file in tqdm(files):

        path = os.path.join(image_folder,file)

        img = Image.open(path).convert("RGB")

        if img.width > img.height:
            img = img.rotate(90, expand=True)

        scale = min(photo_px/img.width, photo_px/img.height)

        new_w = int(img.width * scale)
        new_h = int(img.height * scale)

        img = img.resize((new_w,new_h),Image.LANCZOS)

        canvas = Image.new("RGB",(photo_px,photo_px),"white")

        cx = (photo_px-new_w)//2
        cy = (photo_px-new_h)//2

        canvas.paste(img,(cx,cy))

        px = x * cell
        py = y * cell

        page.paste(canvas,(px,py))

        x += 1

        if x >= cols:
            x = 0
            y += 1

        if y >= rows:

            pages.append(page)

            page = Image.new("RGB",(page_w,page_h),"white")

            x = 0
            y = 0

    if x != 0 or y != 0:
        pages.append(page)

    print("Total pages:",len(pages))

    pages[0].save(
        output_pdf,
        save_all=True,
        append_images=pages[1:],
        resolution=dpi
    )

    print("Saved:",output_pdf)
