from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///user_info.db"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Ananyachanda12@localhost:5433/postgres'


db = SQLAlchemy(app)



class user_info(db.Model):
    slno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    floatingInput=db.Column(db.Float, nullable=False)
    date_created = db.Column(db.DateTime, default= datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.SLNo} - {self.title}"
    
@app.route('/', methods = ['GET', 'POST'])
def hello_world():
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        floatingInput= request.form['floatingInput']
        all_user =user_info(title = title, desc = desc, floatingInput=floatingInput)
        db.session.add(all_user)
        db.session.commit()

    all_user = user_info.query.all()
    return render_template('index.html', all_user = all_user)

@app.route('/show')
def products():
    all_user = user_info.query.all()
    print(all_user)
    return 'This is products page'

@app.route('/update/<int:slno>', methods=['GET', 'POST'])
def update(slno):
    if request.method=='POST':
        title = request.form['title']
        desc = request.form['desc']
        user_info = user_info.query.filter_by(slno=slno).first()
        user_info.title = title
        user_info.desc = desc
        db.session.add(user_info)
        db.session.commit()
        return redirect("/")
        
    user_info = user_info.query.filter_by(slno=slno).first()
    return render_template('update.html', user_info=user_info)

@app.route('/delete/<int:slno>')
def delete(slno):
    user_info = user_info.query.filter_by(slno=slno).first()
    db.session.delete(user_info)
    db.session.commit()
    return redirect("/")

if __name__=="__main__":
    app.run(debug=True, port=8000)


