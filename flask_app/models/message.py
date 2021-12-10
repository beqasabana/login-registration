from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Message:
    def __init__(self, data):
        self.id = data['id']
        self.sender = data['sender']
        self.receiver = data['receiver']
        self.message = data['message']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls, data):
        query = "INSERT INTO messages (sender, receiver, message) VALUES(%(sender)s, %(receiver)s, %(message)s);"
        message_id = connectToMySQL('user_schema').query_db(query, data)
        return message_id

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM messages"
        all_messages_in_db = connectToMySQL('user_schema').query_db(query)
        all_messages = []
        for one_message in all_messages_in_db:
            all_messages.append(cls(one_message))
        return all_messages