from flask import Flask, request, redirect, render_template, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:hello123@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'y337kGcys&zP3B'

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

@app.before_request
def require_login():
    allowed_routes = ['blogs', 'login', 'signup', 'index']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()


        if user and user.password == password:
            session['username'] = username
            flash("Logged in")
            return redirect('/newpost')
        else:
            flash('User password incorrect, or user does not exist', 'error')          

    return render_template('login.html')

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']
     
        existing_user = User.query.filter_by(username=username).first()
        if not existing_user:
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username
            return redirect('/newpost')
        else:
            return "<h1>Username already exists</h1>"

    return render_template('signup.html')


@app.route('/logout')
def logout():
    del session['username']
    return redirect('/blog')

@app.route('/', methods=['POST', 'GET'])
def index():
    owners = User.query.all()
    
    return render_template('index.html', owners=owners)

#@app.route('/', methods=['POST', 'GET'])
#def index():

    #owner = User.query.filter_by(username=session['username']).first()

    #if request.method == 'POST':
        #task_name = request.form['task']
        #new_owner = Task(task_name, owner)
        #db.session.add(new_task)
        #db.session.commit()

    #tasks = Task.query.filter_by(completed=False,owner=owner).all()
    #completed_tasks = Task.query.filter_by(completed=True,owner=owner).all()
    #return render_template('todos.html',title="Get It Done!", 
        #tasks=tasks, completed_tasks=completed_tasks)

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
        owner = User.query.filter_by(username=session['username']).first()

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
        title=blog.title, body=blog.body, owner=blog.owner)

@app.route('/userblogs', methods=['POST', 'GET'])
def userblogs():
    
    user_id = request.args.get('id')
    user = User.query.filter_by(id=user_id).first()
    #blogs = Blog.query.filter(Blog.owner_id == user).all()
    #owner = User.query.filter_by(username=session['username']).first()
    return render_template('singleUser.html', user=user)


if __name__ == '__main__':
    app.run()