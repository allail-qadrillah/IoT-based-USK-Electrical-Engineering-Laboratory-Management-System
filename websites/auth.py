from flask import Blueprint, render_template, request, redirect, url_for

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template('public/login.html')

@auth.route('/signup')
def signup():
    return render_template('public/signup.html')

@auth.route('/logout')
def logout():
    # return redirect(url_for('main.index'))
    return 'logout'