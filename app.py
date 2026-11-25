import hmac
import os
import secrets
import sqlite3
from pathlib import Path

from flask import Flask, abort, flash, redirect, render_template, request, session, url_for


BASE_DIR = Path(__file__).resolve().parent


def create_app():
    app = Flask(__name__, instance_path=str(BASE_DIR / "instance"))
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-only-change-this-secret")
    app.config["DATABASE"] = str(Path(app.instance_path) / "contacts.sqlite3")

    Path(app.instance_path).mkdir(parents=True, exist_ok=True)

    def get_db():
        db = sqlite3.connect(app.config["DATABASE"])
        db.row_factory = sqlite3.Row
        return db

    def check_csrf():
        token = session.get("csrf_token", "")
        submitted = request.form.get("csrf_token", "")
        if not token or not hmac.compare_digest(token, submitted):
            abort(400, description="El formulario ha caducado. Recarga la página e inténtalo de nuevo.")

    @app.context_processor
    def inject_csrf_token():
        if "csrf_token" not in session:
            session["csrf_token"] = secrets.token_urlsafe(32)
        return {"csrf_token": session["csrf_token"]}

    def initialize_database():
        with get_db() as db:
            db.execute(
                """CREATE TABLE IF NOT EXISTS contacts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT NOT NULL DEFAULT '',
                    notes TEXT NOT NULL DEFAULT '',
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                )"""
            )

    @app.get("/")
    def index():
        with get_db() as db:
            contacts = db.execute(
                "SELECT id, name, email, notes, created_at FROM contacts ORDER BY id DESC"
            ).fetchall()
        return render_template("index.html", contacts=contacts)

    @app.route("/nuevo", methods=["GET", "POST"])
    def create_contact():
        if request.method == "POST":
            check_csrf()
            name = request.form.get("name", "").strip()
            email = request.form.get("email", "").strip()
            notes = request.form.get("notes", "").strip()
            if not name:
                flash("El nombre es obligatorio.", "error")
                return render_template("form.html", contact=None, values=request.form), 400

            with get_db() as db:
                db.execute(
                    "INSERT INTO contacts (name, email, notes) VALUES (?, ?, ?)",
                    (name, email, notes),
                )
            flash("Registro creado correctamente.", "success")
            return redirect(url_for("index"))

        return render_template("form.html", contact=None, values={})

    @app.route("/editar/<int:contact_id>", methods=["GET", "POST"])
    def edit_contact(contact_id):
        with get_db() as db:
            contact = db.execute(
                "SELECT id, name, email, notes FROM contacts WHERE id = ?", (contact_id,)
            ).fetchone()
            if contact is None:
                abort(404)

            if request.method == "POST":
                check_csrf()
                name = request.form.get("name", "").strip()
                email = request.form.get("email", "").strip()
                notes = request.form.get("notes", "").strip()
                if not name:
                    flash("El nombre es obligatorio.", "error")
                    return render_template("form.html", contact=contact, values=request.form), 400

                db.execute(
                    "UPDATE contacts SET name = ?, email = ?, notes = ? WHERE id = ?",
                    (name, email, notes, contact_id),
                )
            else:
                return render_template("form.html", contact=contact, values=dict(contact))

        flash("Registro actualizado correctamente.", "success")
        return redirect(url_for("index"))

    @app.post("/eliminar/<int:contact_id>")
    def delete_contact(contact_id):
        check_csrf()
        with get_db() as db:
            db.execute("DELETE FROM contacts WHERE id = ?", (contact_id,))
        flash("Registro eliminado.", "success")
        return redirect(url_for("index"))

    initialize_database()
    return app


app = create_app()


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
