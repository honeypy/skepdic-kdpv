from PIL import Image
from PIL import ImageOps
from PIL import ImageFont, ImageDraw
import os

class Worker:
    def __init__(self, filename, tag, title, subtitle):
        self.filename = filename
        self.tag_white = tag
        self.tag_red = '@skepdic'
        self.title = title.replace('\r','')
        self.subtitle = subtitle.replace('\r','')
        self.width = 1200
        self.height = 650
        self.white_tag_font = ImageFont.truetype('static/fonts/NeoSansW1G-Italic.otf', 30)
        self.red_tag_font = ImageFont.truetype('static/fonts/NeoSansW1G-BoldItalic.otf', 30)
        self.mainttext_font = ImageFont.truetype('static/fonts/Zantroke.otf', 60)
        self.subtitle_font = ImageFont.truetype('static/fonts/NeoSansW1G-Light.otf', 50)
        self.im = Image.open(self.filename).convert('RGBA')

    def process(self):
        self.adjust()
        self.darken()
        self.draw_logo()
        self.draw_tag()
        self.draw_title()
        self.draw_subtitle()

    def adjust(self):
        # подгоняем размер
        self.im = ImageOps.fit(self.im, (self.width, self.height), method=3, bleed=0.0, centering=(0.5, 0.5))

    def darken(self):
        self.im = self.im.point(lambda p: p*0.45)

    def draw_logo(self):
        #импортируем, преобразуем и вставляем лого
        self.logo = Image.open('static/logo.png').convert('RGBA')
        self.logo = ImageOps.fit(self.logo, (210, 85), method=1, bleed=0.0, centering=(0.5, 0.5))
        self.logo_location = (91, 47)
        self.im.paste(self.logo, self.logo_location)

    def draw_tag(self):
        # рисуем тэг
        self.draw = ImageDraw.Draw(self.im)
        white_tag_location = (315,80)
        self.draw.text(white_tag_location, self.tag_white, font=self.white_tag_font)
        width = self.white_tag_font.getsize(self.tag_white)[0]
        red_tag_location = (white_tag_location[0]+width, white_tag_location[1])
        self.draw.text(red_tag_location, self.tag_red, font=self.red_tag_font, fill='#ef2525')

    def draw_title(self):
        #пишем заголовок
        self.draw = ImageDraw.Draw(self.im)
        self.logo_height = self.logo.size[1]
        self.text_location = (self.logo_location[0]-5, self.logo_location[1] + self.logo_height + 45)
        self.draw.multiline_text(self.text_location, text=self.title, font=self.mainttext_font, spacing=25, fill='#ef2525')


    def draw_subtitle(self):
        self.draw = ImageDraw.Draw(self.im)
        text_height = self.draw.multiline_textsize(text=self.title, font=self.mainttext_font, spacing=40)[1]
        vertical = self.text_location[1]+text_height+10
        self.subtitle_location=(self.logo_location[0]-5, vertical)
        self.draw.multiline_text(self.subtitle_location, self.subtitle, font=self.subtitle_font, spacing=30)
        self.im.save(self.filename, 'JPEG', quality=100, subsmapling=0)

