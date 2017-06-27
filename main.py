from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:hello123@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))

    def __init__(self, name):
        self.name = name

@app.route('/')
def index():
    return redirect('/blog')


@app.route('/blog', methods=['POST', 'GET'])
def blog():

    if request.method == 'POST':
        blog_name = request.form['blog']
        new_blog = Blog(blog_name)
        db.session.add(new_blog)
        db.session.commit()

    blogs = Blog.query.all()
    return render_template('blog.html',title="Build a Blog", 
        blogs=blogs)


@app.route('/newpost', methods=['POST','GET'])
def newpost():

    if request.method == 'POST':

        blog_id = int(request.form['newpost'])
        newpost = Blog.query.get(blog_id)
        db.session.add(newpost)
        db.session.commit()

    return render_template('newpost_form.html', title="Add a Blog Entry")



if __name__ == '__main__':
    app.run()