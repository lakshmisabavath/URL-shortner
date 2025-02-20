from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import shortuuid
from models import db, URL
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        original_url = request.form.get('url')
        if not original_url:
            return render_template('index.html', error="URL cannot be empty")

        short_code = shortuuid.ShortUUID().random(length=6)
        print(f"Generated short code: {short_code}")  # Debug print

        new_url = URL(original_url=original_url, short_code=short_code)
        db.session.add(new_url)
        db.session.commit()
        
        return render_template('success.html', short_url=f'http://127.0.0.1:5000/{short_code}')
    
    return render_template('index.html')

@app.route('/<short_code>')
def redirect_short_url(short_code):
    url_entry = URL.query.filter_by(short_code=short_code).first_or_404()
    url_entry.clicks += 1
    db.session.commit()
    return redirect(url_entry.original_url)

if __name__ == '__main__':
    app.run(debug=True)