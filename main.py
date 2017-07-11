from flask import Flask, request, redirect, render_template, url_for, session, flash
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
   
    def __init__(self, title, body):
        self.title = title
        self.body = body


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

        title_error = ''
        body_error = ''

        blog_title = str(blog_title)
        blog_body = str(blog_body)
        print(blog_body)

        if len(blog_title) == 0:
            title_error = 'Please give your blog a title'
            return render_template('newpost_form.html', title_error=title_error, 
                blog_body=blog_body)

        if len(blog_body) == 0:
            body_error = 'Please give your blog some content'
            return render_template('newpost_form.html', body_error=body_error,
                blog_title=blog_title)
        
        else:
            new_blog = Blog(blog_title, blog_body)
            db.session.add(new_blog)
            db.session.commit()

            blog_id = new_blog.id
           #return redirect(url_for('blogs', id=blog_id))
            return redirect('/display?id={0}'.format(blog_id))

    else:
        return render_template('newpost_form.html')

@app.route('/display', methods = ['POST', 'GET'])
def display():
    blog_id = request.args.get('id')
    title = request.args.get('title')
    body = request.args.get('body')
    return render_template('display_blog.html', blog_id=blog_id, title=title, body=body)


if __name__ == '__main__':
    app.run()