from flask import Flask, request, redirect, render_template, session, flash 
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:hubert@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True 
db = SQLAlchemy(app)
app.secret_keys='asdgi874'


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    post_title = db.Column(db.String(120))
    post_body = db.Column(db.String(5000))

    def __init__(self, post_title, post_body):
        self.post_title = post_title
        self.post_body = post_body
        
    
@app.route('/newpost', methods=['POST', 'GET'])
def newpost():    
    if request.method == 'POST':            
        blog_post = request.form['blog_post']
        blog_title = request.form['blog_title']

        title_error = ''
        body_error = ''

        if len(blog_title) == 0: 
            title_error = 'Need at least 1 character for title'
        if len(blog_post) == 0:
            body_error = 'Need at least 1 character for title'
        if not title_error and not body_error:
            new_blog_post = Blog(blog_title,blog_post)                
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
    blogs = Blog.query.all()
    return render_template('blog.html', blogs=blogs)

@app.route('/individual', methods=['POST', 'GET'])
def individual_blog():
    blog_ind = request.args.get('id')
    uno_blog = Blog.query.get(blog_ind)
    return render_template('individual.html',uno_blog=uno_blog)



if __name__ == '__main__':  
    app.run()
