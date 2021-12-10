from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.message import Message
from flask_app.models.user import User

@app.route("/send/message/to/<int:receiver>", methods=['POST'])
def send_message(receiver):
    if len(request.form['message']) == 0:
        flash("Can not send empty Message.", 'empty-message')
        return redirect('/success')
    data = {
        'sender': session['user'],
        'receiver': receiver,
        'message': request.form['message']
    }
    Message.save(data)
    return redirect('/success')