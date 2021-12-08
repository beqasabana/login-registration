from flask_app.config.mysqlconnection import connectToMySQL

class User:
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls,data):
        query = "INSERT INTO users_schema (first_name, last_name, email, password) VALUES(%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        user_id = connectToMySQL('users_schema').query_db(query, data)
        return user_id

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users"
        users_in_db = connectToMySQL('users_schema').query_db(query)
        users_cls = []
        for user in users_in_db:
            users_cls.append(cls(user))
        return users_cls