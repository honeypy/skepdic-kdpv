import os
from flask import Flask, render_template, send_file
from flask.ext.bootstrap import Bootstrap
from kdpv_maker import Worker
from announce_kdpv_maker import AnnounceWorker
from forms import UploadForm, AnnounceUploadForm
import requests
from PIL import Image
from io import BytesIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'top secret!'
bootstrap = Bootstrap(app)

@app.after_request
def add_header(r):
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

@app.route('/', methods=['GET', 'POST'])
def index():
    image = None
    form = UploadForm()
    if form.validate_on_submit():
        imagename = 'uploads/' + 'image.jpg'
        filename = os.path.join(app.static_folder, imagename)
        if form.image_file_file.data:
            form.image_file_file.data.save(filename)
        else:
            response = requests.get(form.image_file.data)
            image = Image.open(BytesIO(response.content))
            image.save(filename)
        #form.image_file.data.save(filename)
        title = form.title.data
        subtitle = form.subtitle.data
        tag = form.tag.data
        image = Worker(filename, tag, title, subtitle)
        image.process()
        return render_template('index.html', form=form, image=imagename)

    return render_template('index.html', form=form, image=image)

@app.route('/download')
def download():
    imagename = 'uploads/' + 'image.jpg'
    filename = os.path.join(app.static_folder, imagename)
    return send_file(filename,mimetype='image/jpeg')

@app.route('/announcement', methods=['GET', 'POST'])
def announcement():
    image = None
    an_form = AnnounceUploadForm()
    if an_form.validate_on_submit():
        imagename = 'uploads/' + 'image.jpg'
        background = os.path.join(app.static_folder, imagename)
        an_form.bckgrnd_file.data.save(background)
        imagename2 = 'uploads/'+'portrait.jpg'
        portrait = os.path.join(app.static_folder, imagename2)
        an_form.avatar_file.data.save(portrait)
        title = an_form.title.data
        date = an_form.date.data
        place = an_form.place.data
        themes_content = an_form.themes_content.data
        image = AnnounceWorker(background, portrait, title, date, place, themes_content)
        image.process()
        return render_template('announcement.html', form=an_form, image=imagename)

    return render_template('announcement.html', form=an_form, image=image)



if __name__ == '__main__':
    app.run(debug=True)