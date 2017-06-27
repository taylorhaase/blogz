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
    completed = db.Column(db.Boolean)

    def __init__(self, name):
        self.name = name
        self.completed = False


@app.route('/blog', methods=['POST', 'GET'])
def index():

    if request.method == 'POST':
        blog_name = request.form['blog']
        new_blog = Blog(blog_name)
        db.session.add(new_blog)
        db.session.commit()

    blogs = Blog.query.filter_by(posted=False).all()
    posted_blogs = Blog.query.filter_by(completed=True).all()
    return render_template('blog.html',title="Build a Blog", 
        blogs=blogs, posted_blogs=posted_blogs)


@app.route('/newpost', methods=['POST'])
def add_post():

    post_id = int(request.form['post-id'])
    blog = Blog.query.get(post_id)
    blog.posted_blogs = True
    db.session.add(blog)
    db.session.commit()

    return redirect('/blog')


if __name__ == '__main__':
    app.run()