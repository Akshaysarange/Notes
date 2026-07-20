from flask import Flask, render_template, request, redirect, url_for
from models import db, Note

app = Flask(__name__)

# Database Configuration
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///notes.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize Database
db.init_app(app)

# Create Database Table
with app.app_context():
    db.create_all()


# Home Page - Show All Notes
@app.route("/")
def index():
    notes = Note.query.all()
    return render_template("index.html", notes=notes)


# Add Note
@app.route("/add", methods=["GET", "POST"])
def add_note():
    error = ""

    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]

        if title == "" or description == "":
            error = "Both fields are required."
        else:
            note = Note(title=title, description=description)
            db.session.add(note)
            db.session.commit()
            return redirect(url_for("index"))

    return render_template("add_note.html", error=error)


# Edit Note
@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_note(id):
    note = Note.query.get_or_404(id)
    error = ""

    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]

        if title == "" or description == "":
            error = "Both fields are required."
        else:
            note.title = title
            note.description = description
            db.session.commit()
            return redirect(url_for("index"))

    return render_template("edit_note.html", note=note, error=error)


# Delete Note
@app.route("/delete/<int:id>")
def delete_note(id):
    note = Note.query.get_or_404(id)
    db.session.delete(note)
    db.session.commit()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)