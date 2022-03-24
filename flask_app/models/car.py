from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL

from flask_app.models import user

class Car:
    def __init__(self,data):
        self.id = data['id']
        self.color = data['color']
        self.seats = data['seats']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']

        self.user = {}

    @staticmethod
    def validate_car(form_data):
        is_valid = True
        if len(form_data['color']) < 3 or len(form_data['color']) > 25:
            flash("Car color must be between 3 and 25 characters long!")
            is_valid = False
        if len(form_data['seats']) < 1:
            flash("Please enter a valid number of seats!")
            is_valid = False
        elif int(form_data['seats']) < 2 or int(form_data['seats']) > 15:
            flash("Number of seats must be greater than 1 and less than 15!")
            is_valid = False
        return is_valid

    @classmethod
    def create_car(cls, data):
        query = "INSERT INTO cars (color, seats, user_id, created_at, updated_at) VALUES (%(color)s, %(seats)s, %(user_id)s, NOW(), NOW());"
        results = connectToMySQL('cars_db').query_db(query,data)
        return results 
    
    @classmethod
    def all_cars(cls):
        query = "SELECT * FROM cars LEFT JOIN users ON users.id = user_id;"
        results = connectToMySQL('cars_db').query_db(query)

        all_cars = []

        for row in results:
            car = cls(row)

            user_data = {
                "id" : row['users.id'],
                "first_name" : row['first_name'],
                "last_name" : row['last_name'],
                "email" : row['email'],
                "password" : row['password'],
                "created_at" : row['users.created_at'],
                "updated_at" : row['users.updated_at']
            }
            car.user = user.User(user_data)
            all_cars.append(car)

        return all_cars

    @classmethod
    def get_one_car(cls, data):
        query = "SELECT * FROM cars LEFT JOIN users ON users.id = user_id WHERE cars.id = %(car_id)s;"
        results = connectToMySQL('cars_db').query_db(query, data)

        car = cls(results[0])

        user_data = {
            "id" : results[0]['users.id'],
            "first_name" : results[0]['first_name'],
            "last_name" : results[0]['last_name'],
            "email" : results[0]['email'],
            "password" : results[0]['password'],
            "created_at" : results[0]['users.created_at'],
            "updated_at" : results[0]['users.updated_at']
        }
        car.user = user.User(user_data)
        return car

    @classmethod
    def update_car(cls,data):
        query = "UPDATE cars SET color = %(color)s, seats = %(seats)s, updated_at = NOW() WHERE id = %(car_id)s;"
        results = connectToMySQL('cars_db').query_db(query,data)
        return results 

    @classmethod
    def delete_car(cls,data):
        query = "DELETE FROM cars WHERE id = %(car_id)s;"
        results = connectToMySQL('cars_db').query_db(query,data)
        return results 
