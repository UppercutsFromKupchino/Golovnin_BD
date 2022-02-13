from flask_login import UserMixin
from app import db
from app import login_manager
from flask import flash, redirect, url_for


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    __tablename__ = '_user'
    __table_args__ = {'extend_existing': True}

    id_of_user = db.Column(db.Integer(), primary_key=True)

    def get_id(self):
        return self.id_of_user

    @staticmethod
    def get_user_for_login(login_user):
        try:
            query = db.session.query(User).filter(User.login_of_user == login_user).first()
            return query
        except:
            flash('Ошибка взаимодействия с базой данных! Попробуйте позже!')
            return redirect(url_for('login'))

    @staticmethod
    def add_user(login, password, fio, role):
        user_to_add = User(password_of_user=password, login_of_user=login, fio_of_user=fio, id_of_role=role)
        try:
            db.session.add(user_to_add)
            db.session.commit()
            flash('Пользователь успешнно зарегистрирован')
        except:
            flash('Ошибка взаимодействия с базой данных! Попробуйте позже!')
            return redirect(url_for('register'))


class EmitentOfStock(db.Model):
    __tablename__ = 'emitent_of_stock'
    __table_args__ = {'extend_existing': True}

    @staticmethod
    def get_all_emitents():
        try:
            query = db.session.query(EmitentOfStock).all()
            return query
        except:
            flash('Ошибка взаимодействия с базой данных! Попробуйте позже!')
            return redirect(url_for('emitents'))

    @staticmethod
    def add_emitent(name_emitent):
        emitent_to_add = EmitentOfStock(name_of_emitent=name_emitent)
        try:
            db.session.add(emitent_to_add)
            db.session.commit()
            flash('Эмитент успешно добавлен')
        except:
            flash('Ошибка взаимодействия с базой данных! Попробуйте позже!')
            return redirect(url_for('emitents'))

    @staticmethod
    def get_id_of_emitent_by_name(name):
        try:
            query = db.session.query(EmitentOfStock).filter(EmitentOfStock.name_of_emitent == name).one()
            return query
        except:
            flash('Ошибка взаимодействия с базой данных! Попробуйте позже!')
            return redirect(url_for('stock'))


class RoleOfUser(db.Model):
    __tablename__ = 'role_of_user'
    __table_args__ = {'extend_existing': True}

    @staticmethod
    def get_role_by_id(id_role):
        try:
            query = db.session.query(RoleOfUser).filter(RoleOfUser.id_of_role == id_role).one()
            return query
        except:
            flash('Ошибка взаимодействия с базой данных! Попробуйте позже!')
            return redirect(url_for('login'))

    @staticmethod
    def get_all_roles():
        try:
            query = db.session.query(RoleOfUser).all()
            return query
        except:
            flash('Ошибка взаимодействия с базой данных! Попробуйте позже!')
            return redirect(url_for('register'))

    @staticmethod
    def get_id_of_role_by_name(role):
        try:
            query = db.session.query(RoleOfUser).filter(RoleOfUser.name_of_role == role).one()
            return query
        except:
            flash('Ошибка взаимодействия с базой данных! Попробуйте позже!')
            return redirect(url_for('register'))


class Stock(db.Model):
    __tablename__ = 'stock'
    __table_args__ = {'extend_existing': True}

    @staticmethod
    def add_stock(emitent, price, ticker, pe, _yield):
        stock_to_add = Stock(id_of_emitent=emitent, price_of_stock=price, ticker=ticker, pe=pe,
                             _yield=_yield)
        try:
            db.session.add(stock_to_add)
            db.session.commit()
            flash('Акция успешно добавлена')
        except:
            flash('Ошибка взаимодействия с базой данных! Попробуйте позже!')
            return redirect(url_for('stocks'))

    @staticmethod
    def get_all_stocks():
        try:
            query = db.session.query(Stock, EmitentOfStock)
            query = query.join(EmitentOfStock)
            return query.all()
        except:
            flash('Ошибка взаимодействия с базой данных! Попробуйте позже!')
            return redirect(url_for('stocks'))

    @staticmethod
    def delete_stock(id_stock):
        try:
            Stock.query.filter(Stock.id_of_stock == id_stock).delete()
            db.session.commit()
            flash('Акция успешно удалена')
        except:
            flash('Ошибка взаимодействия с базой данных! Попробуйте позже!')
            return redirect(url_for('stocks'))


class StockBought(db.Model):
    __tablename__ = 'stock_bought'
    __table_args__ = {'extend_existing': True}

    @staticmethod
    def buy_stock(id_stock, id_user, date, quantity):
        stock_to_buy = StockBought(id_of_stock=id_stock, id_of_user=id_user, datetime_of_stock=date,
                                   quantity_of_stocks=quantity)
        try:
            db.session.add(stock_to_buy)
            db.session.commit()
            flash('Акция успешно добавлена в портфель')
        except:
            flash('Ошибка взаимодействия с базой данных! Попробуйте позже!')
            return redirect(url_for('stocks'))

    @staticmethod
    def get_stocks_of_user(id_user):
        try:
            query = db.session.query(StockBought, Stock, EmitentOfStock)
            query = query.join(Stock, Stock.id_of_stock == StockBought.id_of_stock)
            query = query.join(EmitentOfStock, Stock.id_of_emitent == EmitentOfStock.id_of_emitent)
            query = query.filter(StockBought.id_of_user == id_user).all()
            return query
        except:
            flash('Ошибка взаимодействия с базой данных! Попробуйте позже!')
            return redirect(url_for('stocks_user'))
