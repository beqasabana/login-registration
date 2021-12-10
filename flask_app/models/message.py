from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Message:
    def __init__(self, data):
        self.id = data['id']
        self.user_id = data['user_id']
        self.sent_to_id = data['sent_to_id']
        self.message = data['message']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls, data):
        query = "INSERT INTO messages (sender, receiver, message) VALUES(%(sender)s, %(receiver)s, %(message)s);"
        message_id = connectToMySQL('user_schema').query_db(query, data)
        return message_id