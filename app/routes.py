from flask import Flask, request, redirect, url_for, render_template
from app import app, db
from app.models import Book, Author, Rental
from app.forms import BookForm


@app.route("/books/", methods=["GET", "POST"])
def book_list():
    form = BookForm()
    error = ""
    if request.method == "POST":
        if form.validate_on_submit():
            all_authors_names = []
            all_authors_results = Author.query.all()
            for author in all_authors_results:
                all_authors_names.append(author.name)
            if form.data["author"] in all_authors_names:
                pass
            else:
                new_author = Author(name=form.data["author"])
                db.session.add(new_author)
                db.session.commit()
            author_from_form = Author.query.filter_by(name=form.data['author']).first()
            rental = Rental.query.filter_by(status=form.data['status']).first()
            new_book = Book(tittle=form.data["tittle"], quantity=form.data['quantity'], author_id=author_from_form.id,
                            rental_id=rental.id)
            db.session.add(new_book)
            db.session.commit()
        return redirect((url_for("book_list")))
    return render_template("book.html", form=form, books=Book.query.all(), error=error)


#@app.route("books/edit/{{ int:id }}", method=["GET"])
#def book_edit(id):
    #book = Book.query.get(id)
   # form = BookForm(data=book)
   # if request.method == "POST":
        #if form.validate_on_submit():
            #new_book = Book(tittle=form.data["tittle"], quantity=form.data['quantity'], author_name=form.data["author"],
                            #rental_status=form.data["status"])
         #   db.session.add(new_book)
        #    db.session.commit()
     #   return redirect((url_for("book_list")))
#    return render_template("book_id.html", form=form, id=id)


if __name__ == "__main__":
    app.run(debug=True)

