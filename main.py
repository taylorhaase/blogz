from flask import Flask, request, redirect, render_template, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:hello123@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(1000))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
   
    def __init__(self, title, body, owner):
        self.title = title
        self.body = body
        self.owner = owner

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))
    password = db.Column(db.String(20))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, username, password):
        self.username = username
        self.password = password


@app.route('/', methods=['POST', 'GET'])
def index():
    return redirect('/blog')

@app.route('/blog', methods=['POST', 'GET'])
def blogs():
    
    blogs = Blog.query.all()
    blog_id = request.args.get('id')
    return render_template('blog.html',blogs=blogs, id=blog_id)
    

@app.route('/newpost', methods=['POST', 'GET'])
def newpost():
    if request.method == 'POST':

        blog_title = request.form['title']
        blog_body = request.form['body']
                #added 'owner'
        owner = request.form['owner']

        title_error = ''
        body_error = ''

        blog_title = str(blog_title.strip())
        blog_body = str(blog_body.strip())

        if len(blog_title) == 0:
            title_error = 'Please give your blog a title'
            return render_template('newpost_form.html', title_error=title_error, 
                blog_body=blog_body)

        if len(blog_body) == 0:
            body_error = 'Please give your blog some content'
            return render_template('newpost_form.html', body_error=body_error,
                blog_title=blog_title)
        
        else:
                                #added owner to new_blog
            new_blog = Blog(blog_title, blog_body, owner)
            db.session.add(new_blog)
            db.session.commit()

            blog_id = new_blog.id

            return redirect('/display?id=' + str(blog_id))
    else:
        return render_template('newpost_form.html')

@app.route('/display', methods = ['POST', 'GET'])
def display():
    blog_id = request.args.get('id')
    blog = Blog.query.filter(Blog.id == blog_id).first()
    
    return render_template('display_blog.html', blog_id=blog_id, 
        title=blog.title, body=blog.body)


if __name__ == '__main__':
    app.run()