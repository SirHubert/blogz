from flask import Flask, request, redirect, render_template, session, flash 
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:hubert@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True 
db = SQLAlchemy(app)
app.secret_key='asdgi874'


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    post_title = db.Column(db.String(120))
    post_body = db.Column(db.String(5000))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, post_title, post_body, owner):
        self.post_title = post_title
        self.post_body = post_body
        self.owner = owner

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, username, password):
        self.username = username
        self.password = password


@app.before_request
def require_login():
    allowed_routes = ['login', 'signup', 'blog']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')

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
            return redirect ('/blog')
        else:
            return "<h1>Duplicate User</h1>"

    return render_template('signup.html')  

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username=request.form['username']
        password=request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session['username'] = username
            flash("Logged In")
            return redirect('/newpost')
        else:
            flash('User password incorrect, or user does not exist', 'error')
            return redirect('/login')


    return render_template('login.html')


@app.route('/logout', methods=['POST', 'GET'])
def logout():
    del session['username']
    return redirect('/blog')

@app.route('/', methods=['POST', 'GET'])
def index(): 
    blog_author = User.query.all()
    return render_template('index.html', blog_author=blog_author)      
    
@app.route('/newpost', methods=['POST', 'GET'])
def newpost():    
    if request.method == 'POST':            
        blog_post = request.form['blog_post']
        blog_title = request.form['blog_title']
        owner = User.query.filter_by(username=session['username']).first() 

        title_error = ''
        body_error = ''

        if len(blog_title) == 0: 
            title_error = 'Need at least 1 character for title'
        if len(blog_post) == 0:
            body_error = 'Need at least 1 character for title'
        if not title_error and not body_error:
            new_blog_post = Blog(blog_title,blog_post, owner)                
            db.session.add(new_blog_post)
            db.session.commit()
            blog_post = str(new_blog_post.id)    
            return redirect ('/individual?id='+blog_post)
        else: 
            return render_template('newpost.html', blog_title=blog_title, blog_post=blog_post, 
            body_error=body_error, title_error=title_error)
    else:
        return render_template('newpost.html')


@app.route('/blog', methods=['POST', 'GET'])
def blog():
    if request.args.get('id'):
        blog_id = request.args.get('id')
        blog = Blog.query.get(blog_id)

        return render_template('individual.html', uno_blog=blog)

    if request.args.get('user'):
        user_id = request.args.get('user')
        blogs = Blog.query.filter_by(owner_id=user_id).all()

        return render_template('singleUser.html', blogs=blogs)
    
    if request.method == 'GET':
        blogs = Blog.query.all()
        return render_template('blog.html', blogs=blogs)


    blogs = Blog.query.all()
    return render_template('blog.html', blogs=blogs)

@app.route('/individual', methods=['POST', 'GET'])
def individual_blog():
    blog_ind = request.args.get('id')
    uno_blog = Blog.query.get(blog_ind)
    return render_template('individual.html',uno_blog=uno_blog)




if __name__ == '__main__':  
    app.run()
