from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:hello123@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(1000))

    def __init__(self, name, title, body):
        self.name = name
        self.title = title
        self.body = body


@app.route('/', methods=['POST', 'GET'])
def index():
    return redirect('/blog')

@app.route('/blog', methods=['POST', 'GET'])
def blogs():
    return render_template('blog.html')

    blogs = Blog.query.all()
    

@app.route('/newpost', methods=['POST', 'GET'])
def newpost():
    return render_template('newpost_form.html')

    if request.method == 'POST':
        blog_title = request.form['title']
        blog_body = request.form['body']
        new_blog = Blog(blog_title, blog_body)
        db.session.add(new_blog)

        db.session.commit()

        return render_template('blog.html', title="Build a Blog", 
        blogs=blogs)


@app.route('/validate-blog', methods =['POST', 'GET'])
def entry_error():
    title = request.form['title']
    newpost = request.form['newpost']

    title_error = ''
    blog_error = ''

    newpost = str(newpost)
    if len(newpost) == 0:
        blog_error = "Please give your blog some content"


    title = str(title)
    if len(title) == 0:
        title_error = "Please give your blog a title"

    if not blog_error and not title_error:
        return redirect('/blog')

    else:
        return render_template("newpost_form.html", title_error=title_error, blog_error=blog_error, 
        title=title, newpost=newpost)


if __name__ == '__main__':
    app.run()