from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
from flask_app.controllers import users
from flask_app.models import message


EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.messages_sent = []
        self.messages_received = []

    def get_received_messages(self):
        query = "SELECT * FROM users LEFT JOIN messages ON users.id = messages.receiver_id WHERE users.id = %(id)s;"
        data = {
            'id': self.id
        }
        results = connectToMySQL('user_schema').query_db(query, data)
        for one_result in results:
            data = {
                'id': one_result['messages.id'],
                'sender_id': one_result['sender_id'],
                'receiver_id': one_result['receiver_id'],
                'message': one_result['message'],
                'created_at': one_result['messages.created_at'],
                'updated_at': one_result['messages.updated_at']
            }
            self.messages_received.append(message.Message(data))
        return

    @classmethod
    def save(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES(%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        user_id = connectToMySQL('user_schema').query_db(query, data)
        return user_id

    @classmethod
    def get_user_by_id(cls, data):
        query = "SELECT * FROM users WHERE users.id = %(id)s;"
        user = connectToMySQL('user_schema').query_db(query, data)
        return cls(user[0])

    @classmethod
    def get_user_by_email(cls, data):
        query = "SELECT * FROM users WHERE users.email = %(email)s;"
        user = connectToMySQL('user_schema').query_db(query, data)
        if user:
            return cls(user[0])
        return False

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users"
        users_in_db = connectToMySQL('user_schema').query_db(query)
        users_cls = []
        for user in users_in_db:
            users_cls.append(cls(user))
        return users_cls

    @staticmethod
    def validate_email(form):
        is_valid = True
        if not EMAIL_REGEX.match(form['email']):
            flash("Invalid Email Address!", 'registration-error')
            is_valid = False
            return is_valid
        all_users_in_db = User.get_all()
        for one_user in all_users_in_db:
            if one_user.email == form['email']:
                flash("Email address already exists use different email address.", 'registration-error')
                is_valid = False
        return is_valid

    @staticmethod
    def validate_registation(form):
        is_valid = True
        if len(form['first_name']) < 2:
            is_valid = False
            flash("First Name must be at least 2 Characters.", 'registration-error')
        if len(form['last_name']) < 2:
            is_valid = False
            flash("Last Name must be at least 2 Characters.", 'registration-error')
        is_valid = User.validate_email(form)
        if len(form['password']) < 6:
            flash("Password is too short. Password should be at least 6 characters.", 'registration-error')
            is_valid = False
            return is_valid
        if form['password'] != form['password-conf']:
            flash("Password does not match.", 'registration-error')
            is_valid = False
        return is_valid

    @staticmethod
    def validate_login(form):
        is_valid = True
        data = {
            'email': form['email']
        }
        user = User.get_user_by_email(data)
        if not user:
            is_valid = False
            flash("Invalid Email Address or Password.", 'login-error')
            return is_valid
        if not users.bcrypt.check_password_hash(user.password, form['password']):
            is_valid = False
            flash("Invalid Email Address or Password.", 'login-error')
            return is_valid
        return user.id