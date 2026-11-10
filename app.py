"""
app.py · TareasCECyTEM
Aplicación Flask para registrar tareas en una base de datos MySQL.
"""
import os

from flask import Flask, flash, redirect, render_template, request, url_for

from db import obtener_conexion

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "clave-solo-para-desarrollo")


@app.route("/")
def index():
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cur:
            cur.execute(
                """
                SELECT t.id, t.titulo, t.completada 
                FROM tareas t
                ORDER BY t.completada ASC, t.id DESC
                """
            )
            tareas = cur.fetchall()
    finally:
        conexion.close()

    pendientes = sum(1 for t in tareas if not t["completada"])
    return render_template(
        "index.html",
        tareas=tareas,
        pendientes=pendientes,
    )


@app.route("/agregar", methods=["POST"])
def agregar():
    titulo = request.form.get("titulo", "").strip()

    if not titulo:
        flash("Escribe un título para la tarea.", "error")
        return redirect(url_for("index"))

    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cur:
            cur.execute(
                """
                INSERT INTO tareas (titulo)
                VALUES (%s)
                """,
                (titulo,),
            )
            nuevo_id = cur.lastrowid
        conexion.commit()
    finally:
        conexion.close()

    flash(f"Tarea #{nuevo_id} guardada en la base de datos.", "ok")
    return redirect(url_for("index"))


@app.route("/completar/<int:tarea_id>", methods=["POST"])
def completar(tarea_id):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cur:
            cur.execute(
                "UPDATE tareas SET completada = 1 - completada WHERE id = %s",
                (tarea_id,),
            )
        conexion.commit()
    finally:
        conexion.close()
    return redirect(url_for("index"))


@app.route("/eliminar/<int:tarea_id>", methods=["POST"])
def eliminar(tarea_id):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cur:
            cur.execute("DELETE FROM tareas WHERE id = %s", (tarea_id,))
        conexion.commit()
    finally:
        conexion.close()
    flash(f"Tarea #{tarea_id} eliminada.", "ok")
    return redirect(url_for("index"))


@app.route("/registros")
def registros():
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cur:
            cur.execute("SELECT @@hostname AS servidor, NOW() AS consultado_en")
            info = cur.fetchone()
            cur.execute("SELECT * FROM tareas ORDER BY id DESC")
            filas = cur.fetchall()
    finally:
        conexion.close()
    return render_template("registros.html", filas=filas, info=info, buscar="")


@app.route("/salud")
def salud():
    """Evidencia de conexión: servidor, versión, base de datos y SSL."""
    try:
        conexion = obtener_conexion()
        try:
            with conexion.cursor() as cur:
                cur.execute(
                    "SELECT @@hostname AS servidor, VERSION() AS version, DATABASE() AS base"
                )
                info = cur.fetchone()
                cur.execute("SHOW SESSION STATUS LIKE 'Ssl_cipher'")
                fila = cur.fetchone()
                info["ssl"] = fila["Value"] if fila and fila["Value"] else "Sin SSL"
                cur.execute("SELECT COUNT(*) AS total FROM tareas")
                info["total_tareas"] = cur.fetchone()["total"]
        finally:
            conexion.close()
        return render_template("salud.html", ok=True, info=info)
    except Exception as error:
        return render_template("salud.html", ok=False, error=repr(error)), 500


if __name__ == "__main__":
    app.run(debug=True)