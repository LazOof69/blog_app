from flask import Flask, render_template, redirect, url_for, flash, request
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from config import Config
from models import db, User, Post, Comment
from flask_migrate import Migrate
app = Flask(__name__)
app.config.from_object(Config)
app.config['SECRET_KEY'] = 'mysecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
migrate = Migrate(app, db)
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# 路由
@app.route('/')
def home():
    if current_user.is_authenticated:
        print(f"Authenticated user: {current_user.username}")
        posts = Post.query.filter(
            (Post.is_public == True) | (Post.user_id == current_user.id)
        ).all()
    else:
        print("Anonymous user accessing home page.")
        posts = Post.query.filter_by(is_public=True).all()
    print(f"Number of posts displayed: {len(posts)}")
    return render_template('home.html', posts=posts)



@app.route('/post/<int:post_id>')
def post_detail(post_id):
    post = Post.query.get_or_404(post_id)
    if not post.is_public and post.user_id != current_user.id:
        flash('You do not have permission to view this post.', 'danger')
        return redirect(url_for('home'))
    return render_template('post_detail.html', post=post)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')
        user = User(username=username, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        flash('Account created successfully!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/post/<int:post_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    # 查询帖子
    post = Post.query.get_or_404(post_id)

    # 确认用户是该帖子的作者
    if post.user_id != current_user.id:
        flash('You are not authorized to edit this post.', 'danger')
        return redirect(url_for('home'))

    if request.method == 'POST':
        # 更新帖子内容
        post.title = request.form['title']
        post.content = request.form['content']
        post.is_public = request.form['is_public'] == 'True'

        # 保存到数据库
        db.session.commit()
        flash('Post updated successfully!', 'success')
        return redirect(url_for('post_detail', post_id=post.id))

    # 渲染编辑页面
    return render_template('edit_post.html', post=post)


@app.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.user_id != current_user.id:
        flash('You are not authorized to delete this post.', 'danger')
        return redirect(url_for('home'))
    db.session.delete(post)
    db.session.commit()
    flash('Post deleted successfully!', 'success')
    return redirect(url_for('home'))

@app.route('/post/<int:post_id>/comment', methods=['POST'])
@login_required
def add_comment(post_id):
    post = Post.query.get_or_404(post_id)
    if not post.is_public and post.user_id != current_user.id:
        flash('You do not have permission to comment on this post.', 'danger')
        return redirect(url_for('home'))
    content = request.form['content']
    comment = Comment(content=content, post_id=post_id, user_id=current_user.id)
    db.session.add(comment)
    db.session.commit()
    flash('Comment added successfully!', 'success')
    return redirect(url_for('post_detail', post_id=post_id))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login failed. Check your email and password.', 'danger')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('home'))

@app.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        is_public = request.form['is_public'] == 'True'
        post = Post(title=title, content=content, is_public=is_public, user_id=current_user.id)
        db.session.add(post)
        db.session.commit()
        flash('Post created successfully!', 'success')
        return redirect(url_for('home'))
    return render_template('new_post.html')


if __name__ == '__main__':
    app.run(debug=True)
