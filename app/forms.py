from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, IntegerField, HiddenField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    login = StringField(validators=[DataRequired()])
    password = PasswordField(validators=[DataRequired()])
    submit = SubmitField("Авторизуйтесь")


class RegisterForm(FlaskForm):
    login = StringField(validators=[DataRequired()])
    password = PasswordField(validators=[DataRequired()])
    fio = StringField()
    select_role = SelectField(choices=[])
    submit = SubmitField("Зарегистрируйтесь")


class AddEmitentForm(FlaskForm):
    name_of_emitent = StringField(validators=[DataRequired()])
    submit = SubmitField("Добавить эмитента")


class AddStockForm(FlaskForm):
    select_emitent = SelectField(choices=[])
    price = IntegerField(validators=[DataRequired()])
    ticker = StringField(validators=[DataRequired()])
    pe = IntegerField(validators=[DataRequired()])
    yield_field = IntegerField(validators=[DataRequired()])
    submit_add = SubmitField("Добавить акцию")


class DeleteStockForm(FlaskForm):
    id_of_stock = HiddenField()
    submit_delete = SubmitField("Удалить акцию")


class BuyStockForm(FlaskForm):
    id_of_stock_buy = HiddenField()
    quantity = IntegerField(validators=[DataRequired()])
    submit_buy = SubmitField("Купить акцию")
