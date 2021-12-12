from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user

class Message:
    def __init__(self, data):
        self.id = data['id']
        self.sender = user.User.get_user_by_id({
            'id': data['sender_id']
        })
        self.receiver = user.User.get_user_by_id({
            'id': data['receiver_id']
        })
        self.message = data['message']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls, data):
        query = "INSERT INTO messages (sender_id, receiver_id, message) VALUES(%(sender)s, %(receiver)s, %(message)s);"
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

    @classmethod
    def delete(cls, data):
        query = "DELETE FROM messages WHERE id = %(id)s"
        connectToMySQL('user_schema').query_db(query, data)
        return 