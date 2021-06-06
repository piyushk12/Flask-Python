
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import random


# intialise SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///coustomer.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Coustomer(db.Model):
    coustID = db.Column(db.Integer, primary_key=True)
    coustName = db.Column(db.String(50), nullable=False)
    coustEmail = db.Column(db.String(60), nullable=False)
    coustRandom = db.Column(db.Integer, nullable=True)
    dateOfJoin = db.Column(db.DATETIME, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.coustID}-{self.coustName}"


@app.route('/', methods=['GET', 'POST'])
def addCoustomer():
    if(request.method == "POST"):
        name = request.form['title']
        email = request.form['desc']
        randNum = random.randint(1, 1001)
        #id = int(request.form['desc1'])
        coust = Coustomer(coustName=name, coustEmail=email,
                          coustRandom=randNum)
        db.session.add(coust)
        db.session.commit()
    allCoustomer = Coustomer.query.all()

    return render_template('index.html', allCoustomer=allCoustomer)


@app.route('/show')
def printDb():
    allCoustomer = Coustomer.query.all()
    print(allCoustomer)
    return 'Okk'


@app.route('/update/<int:coustID>')
def update(coustID):
    coustomer = Coustomer.query.filter_by(coustID=coustID).first()
    coustomer.coustRandom = random.randint(1, 1001)
    db.session.commit()
    return redirect("/")


@app.route('/delete/<int:coustID>')
def delete(coustID):
    coustomer = Coustomer.query.filter_by(coustID=coustID).first()
    db.session.delete(coustomer)
    db.session.commit()
    return redirect("/")


if __name__ == '__main__':
    app.run(debug=True)
