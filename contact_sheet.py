import os
from PIL import Image
import pillow_heif
from tqdm import tqdm
import img2pdf

pillow_heif.register_heif_opener()


def generate_contact_sheet(
    image_folder,
    output_pdf,
    photo_size_in=2,
    margin_in=0.015,
    dpi=300
):
    """
    Advanced masonry packing contact sheet generator.

    Args:
        image_folder (str): Path to input images
        output_pdf (str): Output PDF path
        photo_size_in (float): Max photo height (inches)
        margin_in (float): Margin between photos (inches)
        dpi (int): DPI for output
    """

    # ======================
    # SETTINGS
    # ======================

    PAGE_W = int(8.27 * dpi)
    PAGE_H = int(11.69 * dpi)

    MAX_HEIGHT = int(photo_size_in * dpi)
    MARGIN = int(margin_in * dpi)

    TEMP_DIR = os.path.join("/content", "pages")
    os.makedirs(TEMP_DIR, exist_ok=True)

    valid_ext = (".jpg", ".jpeg", ".png", ".heic")

    files = [
        os.path.join(image_folder, f)
        for f in os.listdir(image_folder)
        if f.lower().endswith(valid_ext)
    ]

    files.sort()

    print("Total images:", len(files))

    # ======================
    # UTIL FUNCTIONS
    # ======================

    def smart_rotate(img):
        if img.width > img.height:
            r = img.rotate(90, expand=True)
            if r.height > img.height:
                return r
        return img

    def compute_row_height(row):
        ratio_sum = sum(i.width / i.height for i in row)
        return int((PAGE_W - (len(row) - 1) * MARGIN) / ratio_sum)

    def draw_row(page, row, y, h):
        x = 0
        for img in row:
            scale = h / img.height
            w = int(img.width * scale)
            resized = img.resize((w, h), Image.LANCZOS)
            page.paste(resized, (x, y))
            x += w + MARGIN
        return h

    def save_page(page_id, page):
        path = os.path.join(TEMP_DIR, f"page_{page_id}.jpg")
        page.save(path, quality=95)
        return path

    # ======================
    # MAIN PACKING ENGINE
    # ======================

    page = Image.new("RGB", (PAGE_W, PAGE_H), "white")
    cursor_y = 0
    row = []
    page_id = 0
    page_paths = []

    i = 0
    total = len(files)

    while i < total:

        img = Image.open(files[i]).convert("RGB")
        img = smart_rotate(img)

        row.append(img)

        # lookahead optimization
        next_imgs = row.copy()

        if i + 1 < total:
            nxt = Image.open(files[i + 1]).convert("RGB")
            nxt = smart_rotate(nxt)
            next_imgs.append(nxt)

        h_now = compute_row_height(row)
        h_next = compute_row_height(next_imgs) if len(next_imgs) > 1 else h_now

        if h_next < MAX_HEIGHT:

            row_h = min(h_now, MAX_HEIGHT)

            draw_row(page, row, cursor_y, row_h)

            cursor_y += row_h + MARGIN
            row = []

            # new page condition
            if cursor_y + MAX_HEIGHT > PAGE_H:

                page_paths.append(save_page(page_id, page))

                page_id += 1
                page = Image.new("RGB", (PAGE_W, PAGE_H), "white")
                cursor_y = 0

        i += 1

    # last row
    if row:
        remaining = PAGE_H - cursor_y
        draw_row(page, row, cursor_y, min(MAX_HEIGHT, remaining))

    page_paths.append(save_page(page_id, page))

    print("Total pages:", len(page_paths))

    # ======================
    # BUILD FINAL PDF
    # ======================

    with open(output_pdf, "wb") as f:
        f.write(img2pdf.convert(page_paths))

    print("Saved:", output_pdf)
