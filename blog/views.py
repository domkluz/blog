from flask import render_template, request, redirect, url_for
from flask import flash
from flask_login import login_user, login_required, logout_user
from werkzeug.security import check_password_hash
from . import app
from .database import session, Entry, User
from flask_login import current_user


@app.route("/", methods = ["GET"])
@app.route("/page/<int:page>")
def entries(page=1, login="login"):
    #ZERO-INDEXED PAGE
    PAGINATE_BY = 15
    PAGINATE_B = 10
    PAGINATE_C = 5
    page_index= page -1
    count = session.query(Entry).count()
    start = page_index * PAGINATE_BY
    end = start + PAGINATE_BY
    
    total_pages = (count -1) // PAGINATE_BY + 1
    has_next = page_index < total_pages -1 
    has_prev = page_index >0 
    
    entries = session.query(Entry)
    entries = entries.order_by(Entry.datetime.desc()) # this is referring to descending order.
    entries = entries[start:end]
    
    if current_user.is_authenticated == True:
        login="logout"
    
    
    
    return render_template("entries.html",
                            entries = entries,
                            has_next = has_next,
                            has_prev = has_prev,
                            page=page,
                            total_pages=total_pages,
                            PAGINATE_BY=PAGINATE_BY,
                            PAGINATE_B=PAGINATE_B,
                            PAGINATE_C=PAGINATE_C,
                            login=login)


@app.route("/", methods = ["POST"])
@app.route("/page/<int:page>")
def entries_view(page=1,login="login"):
    PAGINATE_BY = int(request.form['drop-down']) # using the name attribute from select
    page_index= page -1
    
    if PAGINATE_BY == 5:
        PAGINATE_B=10
        PAGINATE_C=15
    elif PAGINATE_BY ==10:
        PAGINATE_B=5
        PAGINATE_C=15
    else:
        PAGINATE_B = 10
        PAGINATE_C = 5
        
      
    count = session.query(Entry).count()
    start = page_index * PAGINATE_BY
    end = start + PAGINATE_BY
    
    total_pages = (count -1) // PAGINATE_BY + 1
    has_next = page_index < total_pages -1 
    has_prev = page_index >0 
    
    entries = session.query(Entry)
    entries = entries.order_by(Entry.datetime.desc()) # this is referring to descending order.
    entries = entries[start:end]
    
    current_user=current_user
    
    return render_template("entries.html",
                            entries = entries,
                            has_next = has_next,
                            has_prev = has_prev,
                            page=page,
                            total_pages=total_pages,
                            PAGINATE_BY=PAGINATE_BY,
                            PAGINATE_B=PAGINATE_B,
                            PAGINATE_C=PAGINATE_C,
                            current_user=current_user)


@app.route("/entry/add", methods = ["GET"])
@login_required
def add_entry_get():
    return render_template("add_entry.html")
    
@app.route("/entry/add", methods = ["POST"])
@login_required
def add_entry_post():
    entry = Entry(title = request.form["title"], content = request.form["content"], author = current_user)
    session.add(entry)
    session.commit()
    return redirect (url_for("entries"))


@app.route("/entry/<article_id>")
def view_entry(article_id=1):
    entries = session.query(Entry).filter(Entry.id == article_id).first()
    
    return render_template("single_entry.html",entries = entries)


@app.route("/entry/<article_id>/edit", methods = ["GET"])
@login_required
def edit_entry_get(article_id=1):
    entry_edit = session.query(Entry).filter(Entry.id == article_id).first()
    #content_edit = session.query(Entry.content).filter(Entry.id== article_id).first()
    return render_template("edit_entry.html",entry_edit=entry_edit)
    
    
@app.route("/entry/<article_id>/edit",methods = ["POST"])
@login_required
def edit_entry_post(article_id=1):
    entry_update = session.query(Entry).filter(Entry.id==article_id).first()
    entry_update.title = request.form["title"]
    entry_update.content = request.form["content"]
    session.commit()
    return redirect (url_for("entries"))


@app.route("/entry/<article_id>/delete", methods = ["GET"])
@login_required
def delete_entry_get(article_id=1):
    return render_template("confirm2.html", article_id=article_id)

@app.route("/entry/<article_id>/delete/entries", methods = ["POST"])
@login_required
def delete_entry_post(article_id=1):
    if request.form["delete"]=="yes":
        entry_delete = session.query(Entry).filter(Entry.id==article_id).first()
        session.delete(entry_delete)
        session.commit()
        return redirect (url_for("entries"))
    else:
        return redirect (url_for("entries"))


# at one point this was an alternative way to have a confirmation button.
#@app.route("/entry/<article_id>/delete", methods = ["POST"])
#@login_required
#def delete_entry_post(article_id=1):
    #if request.form["confirm_delete"]=="delete":
        #entry_delete = session.query(Entry).filter(Entry.id==article_id).first()
        #session.delete(entry_delete)
        #session.commit()
        #return redirect (url_for("entries"))
    #else:
        #return redirect (url_for("entries"))


@app.route("/login", methods = ["GET"])
def login_get():
    return render_template("login.html")


@app.route("/login", methods = ["POST"])
def login_post():
    email = request.form["email"]
    password = request.form["password"]
    user = session.query(User).filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        flash("Incorrect username or password", "danger")
        return redirect(url_for("login_get"))
    
    login_user(user)
    return redirect(request.args.get("next") or url_for('entries'))

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("entries"))