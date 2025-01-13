# İçeri Aktarma
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
# SQLite ile bağlantı kurma
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Diary.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# DB oluşturma
db = SQLAlchemy(app)

# Görev #1. DB tablosu oluşturma

class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    subtitle = db.Column(db.String(100), nullable=False)
    text = db.Column(db.String(100), nullable=False)

# Create the tables in the database
with app.app_context():
    db.create_all()

@app.route('/card/<int:id>')
def card(id):
    card = Card.query.get(id)
    if card is None:
        return 'Card not found'
    return render_template('card.html', card=card)
@app.route('/')
def index():
    cards = Card.query.all()
    return render_template('index.html', cards=cards)

@app.route('/create')
def create():
    return render_template('create_card.html')

@app.route('/form_create', methods=['POST'])
def form_create():
    title = request.form.get('title')
    subtitle = request.form.get('subtitle')
    text = request.form.get('text')

    new_card = Card(title=title, subtitle=subtitle, text=text)
    db.session.add(new_card)
    db.session.commit()

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)