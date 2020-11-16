import functools
from flask import Blueprint, g, redirect, session, url_for, request, make_response, jsonify
from flaskr.db import get_db
bp = Blueprint('auth',__name__,url_prefix='/auth')


@bp.route('/register',methods=('GET','POST'))
def register():
    if request.method == 'POST':
        return 'POST Success'
    if request.method == 'GET':
        res = get_db().execute('select * from users')
        print(type(res))
        # return make_response(jsonify(res))
        return jsonify({'result': [dict(row) for row in res]})
