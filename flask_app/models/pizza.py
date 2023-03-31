from flask_app.config.mysqlconnection import connectToMySQL
import re # regex
from flask_app.models import user
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask import flash


class Pizza:
    db = "pizza_schema"
    def __init__(self, data):
        self.id = data['id']
        self.name = data['pizza_name']
        self.toppings = data['toppings']
        self.city = data['pizza_city']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.creator = None

    @classmethod
    def save(cls, data):
        query = "INSERT INTO pizzas (pizza_name, toppings, pizza_city, user_id) VALUES (%(pizza_name)s, %(toppings)s, %(pizza_city)s, %(user_id)s);"
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def get_all(cls):
        query = """SELECT * FROM pizzas
                JOIN users ON pizzas.user_id =
                users.id""";
        results = connectToMySQL(cls.db).query_db(query)
        print(results, "----------------------------------------------------")
        all_pizzas = []
        for row in results:
            pizza_row = cls(row)
            user_data = {
                'id': row['users.id'],
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'email': row['email'],
                'password': row['password'],
                'created_at': row['users.created_at'],
                'updated_at': row['users.updated_at']
            }
            user1 = user.User(user_data)
            pizza_row.creator = user1
            all_pizzas.append(pizza_row)
        return all_pizzas

    @classmethod
    def get_user_pizzas(cls,data):
        query = """SELECT * FROM pizzas
                JOIN users ON pizzas.user_id =
                users.id
                WHERE pizzas.user_id = %(id)s""";
        results = connectToMySQL(cls.db).query_db(query,data)
        all_pizzas = []
        for row in results:
            pizza_row = cls(row)
            user_data = {
                'id': row['users.id'],
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'email': row['email'],
                'password': row['password'],
                'created_at': row['users.created_at'],
                'updated_at': row['users.updated_at']
            }
            user1 = user.User(user_data)
            pizza_row.creator = user1
            all_pizzas.append(pizza_row)
        return all_pizzas


    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM pizzas WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        return cls( results[0])

    @classmethod
    def update(cls, data):
        query = "UPDATE pizzas SET pizza_name=%(pizza_name)s, toppings=%(toppings)s, pizza_city=%(pizza_city)s, updated_at=NOW(), user_id = %(user_id)s WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def destroy(cls, data):
        query = "DELETE FROM pizzas WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query,data)

    @staticmethod
    def validate_pizzas(pizza):
        is_valid = True
        if len(pizza['pizza_name']) < 2:
            is_valid = False
            flash("name must be at least 2 characters", "pizzas")
        if len(pizza['toppings']) < 2:
            is_valid = False
            flash("genre must be at least 2 characters", "pizzas")
        if len(pizza['pizza_city']) < 3:
            is_valid = False
            flash("city must be at least 2 characters", "pizzas")
        return is_valid