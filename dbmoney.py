#!flask/bin/python
from flask import Flask, jsonify, abort, request, make_response, url_for, redirect, render_template, session
import sqlite3
import json
import db_lib as db  # library of custom database functions
from datetime import datetime
from flask.ext.httpauth import HTTPBasicAuth
import os

#curl -i -X DELETE http://localhost/dbmoney/api/v1.0/transactions/100
#curl -i  -X POST -d "{\"date\":\"01/16/2016\", \"type\":\"Credit Card: Dawn\", \"payee\":\"Post Alley Cafe\", \"category\":\"Food: Dining Out\", \"trans_id\":\"89\", \"amount\":\"6.39\", \"notes\":\"\"}" -H "Content-Type: application/json" http://localhost/dbmoney/api/v1.0/transactions/add

app = Flask(__name__, static_url_path="")
auth = HTTPBasicAuth()

@app.route('/add')
def add():
    return render_template('add.html')

@app.route('/list')
def get_print():
    return render_template('list.html')

@app.route('/dbmoney/api/v1.0/transactions/last', methods=['GET'])
def get_last():
    last_id = db.get_last_transaction('transactions')
    return jsonify({'next_id': last_id[0][0] + 1})

@app.route('/dbmoney/api/v1.0/categories', methods=['GET'])
def get_categories():
    my_categories = db.get_categories('categories')
    return jsonify({"categories": my_categories})

@app.route('/dbmoney/api/v1.0/payees', methods=['GET'])
def get_payees():
    my_payees = db.get_payees('transactions')
    return jsonify({"payees": my_payees})
	
@app.route('/dbmoney/api/v1.0/transactions/list', methods=['GET'])
def get_transactions():
    transactions = db.get('transactions')
    return jsonify({'transactions': transactions})

@app.route('/dbmoney/api/v1.0/transactions/add', methods=['POST'])
def add_transaction():
    print(request.json)
    if not request.json or not 'item' or not 'type' in request.json:
        abort(400)
    transaction = {
        'date': request.json['date'],
        'type': request.json['type'],
        'payee': request.json['payee'],
        'category': request.json['category'],
        'notes': request.json['notes'],
        'trans_id': int(request.json['trans_id']),
        'amount': request.json['amount']
    }
	
    db.add_transaction(transaction)
    return jsonify({'transaction': transaction}), 201

@app.route('/dbmoney/api/v1.0/transactions/<int:id>', methods = ['DELETE'])
def delete_transaction(id):
    db.delete_transaction(id)
    return jsonify({'id': id, 'state': 'deleted'}), 201

if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(debug=True, host='0.0.0.0', port=80)