from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.utils import ImageReader
from PIL import Image
import io


def draw_ruler(pdf, font_size=12):
    pdf.setFont("Helvetica", font_size)
    y = 770
    pdf.drawString(100, y, "x100")
    pdf.drawString(200, y, "x200")
    pdf.drawString(300, y, "x300")
    pdf.drawString(400, y, "x400")
    pdf.drawString(500, y, "x500")

    pdf.drawString(10, 100, "y100")
    pdf.drawString(10, 200, "y200")
    pdf.drawString(10, 300, "y300")
    pdf.drawString(10, 400, "y400")
    pdf.drawString(10, 500, "y500")
    pdf.drawString(10, 600, "y600")
    pdf.drawString(10, 700, "y700")
    pdf.drawString(10, 800, "y800")


def init_pdf(filename="reports/SayBananaReport.pdf"):
    pdf = canvas.Canvas(filename, pagesize=letter)
    return pdf


def set_title(pdf, title="Say Banana Report", fontisize=22, height=725):
    pdf.setFont("Helvetica", fontisize)
    page_width = letter[0]
    title_width = pdfmetrics.stringWidth(title, "Helvetica", fontisize)
    x = (page_width - title_width) / 2
    pdf.drawString(x, height, title)


def set_image(pdf, image, x, y, max_width=None, max_height=None):
    """
    Add and scale down an image to fit within specified maximum width or height on a PDF page,
    while maintaining its aspect ratio. Supports both file path and PIL Image object.

    :param pdf: The canvas object to add the image to.
    :param image: The path to the image or a PIL Image object.
    :param x: The x-coordinate of the lower-left corner of the image.
    :param y: The y-coordinate of the lower-left corner of the image.
    :param max_width: (Optional) The maximum width the image should be scaled to.
    :param max_height: (Optional) The maximum height the image should be scaled to.
    """
    if isinstance(image, str):
        # If the input is a file path
        img = ImageReader(image)
        iw, ih = img.getSize()
    elif isinstance(image, Image.Image):
        # If the input is a PIL Image object
        iw, ih = image.size
        buf = io.BytesIO()
        image.save(buf, format="PNG")
        buf.seek(0)
        img = ImageReader(buf)
    else:
        raise ValueError(
            "Invalid image input. Must be a file path or a PIL Image object."
        )

    aspect_ratio = iw / float(ih)

    # Determine the scaling factor based on the aspect ratio
    if max_width and max_height:
        scale_factor = min(max_width / iw, max_height / ih)
    elif max_width:
        scale_factor = max_width / iw
    elif max_height:
        scale_factor = max_height / ih
    else:
        scale_factor = 1  # No scaling if max dimensions are not provided

    # Calculate the new dimensions
    new_width = iw * scale_factor
    new_height = ih * scale_factor

    # Draw the image on the canvas with the new dimensions
    pdf.drawImage(img, x, y, new_width, new_height, mask="auto")

    # Close the buffer if it was created
    if isinstance(image, Image.Image):
        buf.close()


def set_text(pdf, text, font_size=12, x=None, y=100, font_name="Helvetica"):

    pdf.setFont(font_name, font_size)
    if x is None:
        # If x is not provided, center the text
        page_width = letter[0]
        text_width = pdfmetrics.stringWidth(text, font_name, font_size)
        x = (page_width - text_width) / 2
    pdf.drawString(x, y, text)
