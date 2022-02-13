from app import app
from flask import session, render_template, url_for, redirect, flash
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.forms import LoginForm, RegisterForm, AddEmitentForm, AddStockForm, DeleteStockForm, BuyStockForm
from app.models import User, RoleOfUser, EmitentOfStock, Stock, StockBought
import datetime


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/login', methods=['GET', 'POST'])
def login():

    login_form = LoginForm()

    if login_form.submit.data:

        user = User.get_user_for_login(login_form.login.data)

        if user:

            if check_password_hash(user.password_of_user, login_form.password.data):

                login_user(user)
                session['role'] = RoleOfUser.get_role_by_id(user.id_of_role).name_of_role
                return redirect(url_for('index'))

            else:
                flash('Пароль неверный')
        else:
            flash('Такого пользователя не существует')

    return render_template("login.html", login_form=login_form)


@app.route('/register', methods=['GET', 'POST'])
def register():

    register_form = RegisterForm()
    all_roles = RoleOfUser.get_all_roles()
    register_form.select_role.choices = [i.name_of_role for i in all_roles]

    if register_form.submit.data:

        id_of_users_role = RoleOfUser.get_id_of_role_by_name(register_form.select_role.data)

        _hashed_password = generate_password_hash(register_form.password.data)

        User.add_user(register_form.login.data, _hashed_password, register_form.fio.data,
                      id_of_users_role.id_of_role)

        return redirect(url_for('login'))

    return render_template("register.html", register_form=register_form)


@app.route('/emitents', methods=['GET', 'POST'])
@login_required
def emitents():

    list_of_emitents = EmitentOfStock.get_all_emitents()

    if session['role'] == 'admin':

        add_emitent_form = AddEmitentForm()

        if add_emitent_form.submit.data:

            EmitentOfStock.add_emitent(add_emitent_form.name_of_emitent.data)
            return redirect(url_for('emitents'))

        return render_template("emitents.html", list_of_emitents=list_of_emitents, add_emitent_form=add_emitent_form)

    if session['role'] == 'user':

        return render_template("emitents.html", list_of_emitents=list_of_emitents)


@app.route('/stocks', methods=['GET', 'POST'])
@login_required
def stocks():
    if session['role'] == 'admin':

        add_stock_form = AddStockForm()
        delete_stock_form = DeleteStockForm()
        choices = EmitentOfStock.get_all_emitents()
        add_stock_form.select_emitent.choices = [i.name_of_emitent for i in choices]

        all_stocks = Stock.get_all_stocks()

        if add_stock_form.submit_add.data:

            id_of_stock = EmitentOfStock.get_id_of_emitent_by_name(add_stock_form.select_emitent.data)
            Stock.add_stock(id_of_stock.id_of_emitent, add_stock_form.price.data, add_stock_form.ticker.data,
                            add_stock_form.pe.data, add_stock_form.yield_field.data)
            return redirect(url_for('stocks'))

        if delete_stock_form.submit_delete.data:

            Stock.delete_stock(delete_stock_form.id_of_stock.data)
            return redirect(url_for('stocks'))

        return render_template("stocks.html", add_stock_form=add_stock_form, all_stocks=all_stocks,
                               delete_stock_form=delete_stock_form)

    if session['role'] == 'user':

        buy_stock_form = BuyStockForm()

        if buy_stock_form.submit_buy.data:

            current_datetime = datetime.datetime.now()

            StockBought.buy_stock(buy_stock_form.id_of_stock_buy.data, current_user.get_id(), current_datetime,
                                  buy_stock_form.quantity.data)
            return redirect((url_for('stocks')))

        return render_template("stocks.html", all_stocks=all_stocks, buy_stock_form=buy_stock_form)


@app.route('/stocks_user')
@login_required
def stocks_user():

    stocks_of_user = StockBought.get_stocks_of_user(current_user.get_id())
    stocks_of_user_len = len(stocks_of_user)
    income_list = []
    for i in range(stocks_of_user_len):
        income = ((1 + (stocks_of_user[i][1]._yield / 100)) * stocks_of_user[i][1].price_of_stock) * \
                 stocks_of_user[i][0].quantity_of_stocks
        income_list.append(income)

    return render_template("stocks_user.html", stocks_of_user=stocks_of_user, income_list=income_list,
                           stocks_of_user_len=stocks_of_user_len)


@app.route('/logout')
def logout():
    logout_user()
    session.clear()
    return redirect(url_for('index'))
