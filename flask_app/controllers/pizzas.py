from flask import render_template,redirect,session,request,flash
from flask_app import app
from flask_app.models.pizza import Pizza
from flask_app.models.user import User


@app.route('/new/pizza')
def new_pizza():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":session['user_id']
    }
    return render_template('new_pizza.html',user=User.get_by_id(data))


@app.route('/create/pizza',methods=['POST'])
def create_pizza():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Pizza.validate_pizzas(request.form):
        return redirect('/new/pizza')
    data = {
        "pizza_name": request.form["pizza_name"],
        "toppings": request.form["toppings"],
        "pizza_city": request.form["pizza_city"],
        "user_id": session["user_id"]
    }
    Pizza.save(data)
    return redirect('/dashboard')

@app.route('/edit/pizza/<int:id>')
def edit_pizza(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    user_data = {
        "id":session['user_id']
    }
    return render_template("edit_pizza.html",pizza=Pizza.get_one(data),user=User.get_by_id(user_data))

@app.route('/update/pizza',methods=['POST'])
def update_pizza():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Pizza.validate_pizzas(request.form):
        return redirect(f"/edit/pizza/{request.form['id']}")
    data = {
        "pizza_name": request.form["pizza_name"],
        "toppings": request.form["toppings"],
        "pizza_city": request.form["pizza_city"],
        "id": request.form['id'],
        "user_id": session['user_id']
    }
    Pizza.update(data)
    return redirect('/dashboard')

@app.route('/mypizzas')
def show_pizzas():
    if 'user_id' not in session:
        return redirect('/logout')
    user_data = {
        "id":session['user_id']
    }
    return render_template("mypizzas.html", user_pizzas = Pizza.get_user_pizzas(user_data), user=User.get_by_id(user_data))

@app.route('/destroy/pizza/<int:id>')
def destroy_pizza(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    Pizza.destroy(data)
    return redirect('/dashboard')