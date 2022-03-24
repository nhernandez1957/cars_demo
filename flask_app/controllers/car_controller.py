from flask_app import app
from flask import render_template, redirect, session, request, flash

from flask_app.models.user import User
from flask_app.models.car import Car

#================================
# Create New Car Routes
#================================
@app.route('/new/car')
def new_car():
    if "user_id" not in session:
        flash("Please Login or Register before accessing site!")
        return redirect('/')

    user_id = session['user_id']
    return render_template("new_car.html", user_id = user_id)

@app.route('/create/car', methods=['POST'])
def create_car():
    if not Car.validate_car(request.form):
        return redirect('/new/car')

    data = {
        "color" : request.form['color'],
        "seats" : request.form['seats'],
        "user_id" : request.form['user_id']
    }
    Car.create_car(data)
    return redirect('/dashboard')

#================================
# Show Car Route
#================================
@app.route('/show/<int:car_id>')
def show_car(car_id):
    if "user_id" not in session:
        flash("Please Login or Register before accessing site!")
        return redirect('/')

    data = {
        "car_id" : car_id
    }
    car = Car.get_one_car(data)
    logged_in_id = session['user_id']
    return render_template("show_car.html", car = car, logged_in_id = logged_in_id)

#================================
# Edit Car Routes
#================================
@app.route('/edit/<int:car_id>')
def edit_car(car_id):
    if "user_id" not in session:
        flash("Please Login or Register before accessing site!")
        return redirect('/')

    data = {
        "car_id" : car_id
    }
    car = Car.get_one_car(data)
    return render_template("edit_car.html", car = car)

@app.route('/update/<int:car_id>', methods=['POST'])
def update_car(car_id):
    if not Car.validate_car(request.form):
        return redirect(f"/edit/{car_id}")
    
    data = {
        "car_id" : car_id,
        "color" : request.form['color'],
        "seats" : request.form['seats']
    }
    Car.update_car(data)
    return redirect("/dashboard")

#================================
# Delete Car Route
#================================
@app.route('/delete/<int:car_id>')
def delete_car(car_id):
    data = {
        "car_id" : car_id
    }
    Car.delete_car(data)
    return redirect("/dashboard")