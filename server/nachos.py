import os
import time
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from server.auth import login_required
from server.db import get_db
from nest import test_lab

bp = Blueprint('nachos', __name__)

@bp.route('/')
@login_required
def index():
    db = get_db()
    scores = db.execute(
        'select lab, score from score where num = ? order by lab', 
        (g.user['num'],)
    ).fetchall()
    scores_copy = []
    for score in scores:
        scores_copy.append({'lab':str(score['lab']), 'score':str(score['score'])})
    return render_template('nachos/index.html', scores=scores_copy)

@bp.route('/commit/<int:lab>', methods=['POST'])
@login_required
def commit(lab):
    zip_file = request.files['nachos.zip']
    def is_zip_file(filename):
        return '.' in filename and filename.split('.')[-1] == 'zip'
    if not is_zip_file(zip_file.filename):
        return render_template('nachos/result.html', 
            lab=lab, score=0, log='Uploaded file is not a .zip file')
    filename = str(g.user['num'])+'_lab'+str(lab)+'_'+str(int(time.time()))+'.zip'
    zip_file.save(filename)
    score, log = test_lab(lab, filename)
    db = get_db()
    entry = db.execute('select * from score where num = ? and lab = ?',
        (g.user['num'], lab)).fetchall()[0]
    last_score = entry['score']
    if score > last_score:
        db.execute('update score set score = ? where num = ? and lab = ?',
            (score, g.user['num'], lab))
        db.commit()
    return render_template('nachos/result.html', lab=lab, score=score, log=log)
