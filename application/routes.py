from flask import render_template, redirect, url_for, request
from application import app, db, bcrypt
from application.models import Posts, User
from application.forms import PostForm, RegistrationForm, LoginForm
from flask_login import login_user, current_user, logout_user, login_required

@app.route("/home")
@app.route("/")
def home():
    postData = Posts.query.all()
    return render_template("home.html", title = "Home", posts=postData)

@app.route("/about")
def about():
    return render_template("about.html", title = "About")

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    login_fields = [form.email, form.password, form.remember]
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')

            if next_page:
                return redirect(next_page)
            else:
                return redirect(url_for('home'))
    return render_template("login.html", title = "Login", form=form, login_fields=login_fields)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route("/register", methods=['GET','POST'])
def register():
    form = RegistrationForm()
    register_fields = [form.email, form.password, form.confirm_password]
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data)
        user = User(
            email=form.email.data,
            password=hashed_pw
        )
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('post'))
    else:
        print(form.errors)
        return render_template("register.html", title = "Register", form=form, register_fields=register_fields)

@app.route("/post", methods=["GET", "POST"])
@login_required
def post():
    form = PostForm()
    fields = [form.first_name, form.last_name, form.title, form.content]
    if form.validate_on_submit():
        postData = Posts(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            title=form.title.data,
            content=form.content.data
        )
        db.session.add(postData)
        db.session.commit()
        return redirect(url_for("home"))
    else:
        print(form.errors)
        return render_template("post.html", title="Post", form=form, fields=fields)
