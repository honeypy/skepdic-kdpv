from PIL import Image
from PIL import ImageOps
from PIL import ImageFont, ImageDraw

class AnnounceWorker:
    def __init__(self, background, portrait, title, date, place, themes_content):
        self.background = background
        self.portrait = portrait
        self.title = title.replace('\r','') #исправляем неведомый баг
        self.date = date.replace('\r','')
        self.place = place.replace('\r','')
        self.themes = 'ОСНОВНЫЕ ТЕМЫ:'
        self.themes_content = themes_content.replace('\r','')
        self.width = 1200
        self.height = 650
        self.right_padding = 40
        self.title_font = ImageFont.truetype('static/fonts/CoreSansM65Bold.ttf', 55)
        self.date_font = ImageFont.truetype('static/fonts/CoreSansM65Bold.ttf', 70)
        self.place_font = ImageFont.truetype('static/fonts/CoreSansM65Bold.ttf', 40)
        self.themes_font = ImageFont.truetype('static/fonts/CoreSansM65Bold.ttf', 45)
        self.themes_content_font = ImageFont.truetype('static/fonts/CoreSansM55Medium.ttf', 40)
        self.im = Image.open(self.background).convert('RGBA')

    def process(self):
        self.adjust()
        self.darken()
        self.draw_avatar()
        self.draw_name()
        self.draw_date()
        self.draw_place()
        self.draw_themes()
        self.draw_themes_content()
        self.im.save('static/uploads/image.jpg')

    def darken(self):
        self.im = self.im.point(lambda p: p * 0.45)

    def adjust(self):
        # подгоняем размер
        self.im = ImageOps.fit(self.im, (self.width, self.height), method=3, bleed=0.0, centering=(0.5, 0.5))

    def draw_name(self):
        # пишем заголовок
        self.draw = ImageDraw.Draw(self.im)
        title = max(self.title.split('\n'))
        print(title)
        title_width = self.title_font.getsize(title)[0]
        self.start_point = (self.width-title_width)-self.right_padding
        self.right_border = title_width+self.start_point
        self.text_location = (self.start_point,45)
        self.draw.multiline_text(self.text_location, text=self.title, font=self.title_font, spacing=20, align='right')
        self.lower = self.draw.multiline_textsize(self.title, font=self.title_font, spacing=20)[1]

    def draw_date(self):
        date_width = self.date_font.getsize(self.date)[0]
        date_x = self.width-date_width-self.right_padding
        self.date_location = (date_x, self.lower+50)
        self.draw.text(self.date_location, text=self.date, font=self.date_font)

    def draw_place(self):
        place = self.place.split('\n')[0]
        place_width = self.place_font.getsize(place)[0]
        place_x = self.width-place_width-self.right_padding
        self.place_location = (place_x, self.lower+130)
        self.draw.text(self.place_location, text=self.place,font=self.place_font,align='right')

    def draw_themes(self):
        themes_width = self.themes_font.getsize(self.themes)[0]
        themes_x = self.width-themes_width-self.right_padding
        self.themes_location = (themes_x, self.lower+230)
        self.draw.text(self.themes_location, text=self.themes, font=self.themes_font)

    def draw_themes_content(self):
        themes_content = max(self.themes_content.split('\n'))
        print(themes_content)
        themes_content_width = self.themes_content_font.getsize(themes_content)[0]
        themes_x = self.width-themes_content_width-self.right_padding
        self.themes_content_location = (themes_x, self.lower+270)
        self.draw.multiline_text(self.themes_content_location, text=self.themes_content, font=self.themes_content_font, align='right')

    def draw_avatar(self):
        im = Image.open(self.portrait)
        width = im.width
        height = im.height

        new_width_start = (width-height)/2
        new_width_end = new_width_start+height
        box = (new_width_start,0,new_width_end,height)
        im = im.crop(box)
        width = im.width
        height = im.height

        size = (width * 4, height * 4)
        size2 = (size[0]-20, size[1]-20)

        #создаем маску
        mask = Image.new('L', size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0) + size, fill=255)

        #рисуем белую границу
        border = Image.new('L', size, 0)
        d = ImageDraw.Draw(border)
        d.ellipse((0, 0) + size, fill=255)
        d.ellipse((20,20) + size2, fill=0)

        output = ImageOps.fit(im, mask.size, centering=(0.5, 0.5))
        output.putalpha(mask)
        output.paste(border, mask=border)
        output.thumbnail((400, 400), Image.ANTIALIAS)
        box = (80, 210)
        self.im.paste(output, box, mask=output)
