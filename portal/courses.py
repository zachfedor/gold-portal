import functools

import os

import sys

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from . import db

from portal.db import get_db

bp = Blueprint('courses', __name__, url_prefix='/courses')

@bp.route('/courses')
def index():
    db = get_db()
    #posts = db.execute(
    #    'SELECT p.id, title, body, created, author_id, username'
    #    ' FROM post p JOIN user u ON p.author_id = u.id'
    #    ' ORDER BY created DESC'
    #).fetchall()
    return render_template('/courses/courses.html')

@bp.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == "GET":
        return render_template('/courses/create.html')

    elif request.method == "POST":
        course = request.form.get('course', False)
        course_id = request.form['course_id']
        course_description = request.form['course_description']
        error = None

        if course:
            with db.get_db() as con:
                with con.cursor() as cur:
                    cur.execute("INSERT INTO courses (course, course_id, course_description) VALUES (%s, %s, %s)",(course, course_id, course_description))

            # Save to database
            #con = db.get_db()
            #cur = con.cursor()
            #cur.execute("INSERT INTO courses (course, course_id, course_description) VALUES (%s, %s, %s)",(course, course_id, course_description)

            #)
            #con.commit()
            #con.close()
        flash('Success!', 'success')
        flash('Your new course is created!', 'success')

        return render_template('/courses/create.html', course=course)
    return render_template('/courses/create.html', course=course)

@bp.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == "GET":
        return render_template('/courses/update.html')

    elif request.method == "POST":
        course = request.form['course']
        course_id = request.form['course_id']
        course_description = request.form['course_description']
        error = None

        if course:

            # Save to database
            con = db.get_db()
            cur = con.cursor()
            cur.execute(
                    "SELECT * FROM courses WHERE course_id = %s",
                    (course_id,)
            )
            result=cur.fetchone()
            if result != None:
                cur.execute(
                        "UPDATE courses SET course = %s, course_description = %s WHERE course_id = %s",
                        (course, course_description, course_id)
                )
                flash('Success!', 'success')
                flash('Your new course is edited!', 'success')

            elif result == None:
                flash('That course does not exist')

            con.commit()
            con.close()

        return render_template('/courses/update.html', course=course)
    return render_template('/courses/update.html', course=course)
