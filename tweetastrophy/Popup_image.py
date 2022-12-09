from PIL import Image, ImageFont, ImageDraw
import base64
from io import BytesIO


def create_popup(text, image_path):

    img = Image.open(image_path, 'r')


    text_list = text.split()
    count = 0
    new_list = []
    for word in text_list:
        if count < 30:
            count += len(word)
            new_list.append(word)
        else:
            new_list.append(word + ' /n')
            count = 0
    new_text = ' '.join(i for i in new_list)
    title_font = ImageFont.truetype('tweetastrophy/Roboto-Italic.ttf', 26)
    small_font = ImageFont.truetype('tweetastrophy/Roboto-Italic.ttf', 18)


    image_editable = ImageDraw.Draw(img)
    x = 210
    y = 280
    y_lim = 400
    # x_lim = 655
    for i in new_text.split('/n'):
        image_editable.text((x,y), i.strip(), (1, 1, 1),font=title_font)
        y=y+40
        if y >= y_lim:
            image_editable.text((200,430), '. . . . click here continue reading', (1, 1, 1),font=small_font)
            break

    size = 512, 512

    img.thumbnail(size, Image.Resampling.LANCZOS)

    buf = BytesIO()
    img.save(buf, 'jpeg')
    buf.seek(0)
    image_bytes = buf.read()

    encoded = base64.b64encode(image_bytes)

    return encoded
