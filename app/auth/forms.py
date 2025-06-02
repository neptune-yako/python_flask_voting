from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from app.models import User

class LoginForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(message='请输入用户名')])
    password = PasswordField('密码', validators=[DataRequired(message='请输入密码')])
    submit = SubmitField('登录')

class RegistrationForm(FlaskForm):
    username = StringField('用户名', validators=[
        DataRequired(message='请输入用户名'), 
        Length(min=3, max=20, message='用户名长度必须在3到20个字符之间')
    ])
    password = PasswordField('密码', validators=[
        DataRequired(message='请输入密码'),
        Length(min=6, message='密码长度至少为6个字符')
    ])
    confirm_password = PasswordField('确认密码', validators=[
        DataRequired(message='请确认密码'),
        EqualTo('password', message='两次输入的密码不匹配')
    ])
    submit = SubmitField('注册')
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('该用户名已被使用，请选择其他用户名。') 