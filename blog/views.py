from flask import render_template, request, redirect, url_for

from . import app
from .database import session, Entry


PAGINATE_BY = 5

@app.route("/")
@app.route("/page/<int:page>")
def entries(page=1):
    #ZERO-INDEXED PAGE
    page_index= page -1
    
    count = session.query(Entry).count()
    start = page_index * PAGINATE_BY
    end = start + PAGINATE_BY
    
    total_pages = (count -1) // PAGINATE_BY + 1
    has_next = page_index < total_pages -1 # this is a true or flase statement
    has_prev = page_index >0 #this is a true or flase statement
    
    entries = session.query(Entry)
    entries = entries.order_by(Entry.datetime.desc()) # this is referring to descending order.
    entries = entries[start:end]
    
    return render_template("entries.html",
                            entries = entries,
                            has_next = has_next,
                            has_prev = has_prev,
                            page=page,
                            total_pages=total_pages)
    

@app.route("/entry/add", methods = ["GET"])
def add_entry_get():
    return render_template("add_entry.html")
    
@app.route("/entry/add", methods = ["POST"])
def add_entry_post():
    entry = Entry(title = request.form["title"], content = request.form["content"])
    session.add(entry)
    session.commit()
    return redirect (url_for("entries"))


@app.route("/entry/<article_id>")
def view_entry(article_id=1):
    entries = session.query(Entry).filter(Entry.id == article_id).first()
    
    return render_template("single_entry.html",entries = entries)


@app.route("/entry/<article_id>/edit", methods = ["GET"])
def edit_entry_get(article_id=1):
    entry_edit = session.query(Entry).filter(Entry.id == article_id).first()
    #content_edit = session.query(Entry.content).filter(Entry.id== article_id).first()
    return render_template("edit_entry.html",entry_edit=entry_edit)
    
    
@app.route("/entry/<article_id>/edit",methods = ["POST"])
def edit_entry_post(article_id=1):
    entry_update = session.query(Entry).filter(Entry.id==article_id).first()
    entry_update.title = request.form["title"]
    entry_update.content = request.form["content"]
    session.commit()
    return redirect (url_for("entries"))


@app.route("/entry/<article_id>/confirm")
def confirm(article_id=1):
    return render_template("confirm.html", article_id=article_id)


@app.route("/entry/<article_id>/delete")
def delete_entry(article_id=1):
    entry_delete = session.query(Entry).filter(Entry.id==article_id).first()
    session.delete(entry_delete)
    session.commit()
    return redirect (url_for("entries"))
    