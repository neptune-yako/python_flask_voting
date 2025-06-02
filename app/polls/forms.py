from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FieldList, SubmitField, RadioField, HiddenField
from wtforms.validators import DataRequired, Length, ValidationError

class CreatePollForm(FlaskForm):
    question = TextAreaField('投票问题', validators=[
        DataRequired(message='请输入投票问题'),
        Length(min=5, max=255, message='问题长度必须在5到255个字符之间')
    ])
    option1 = StringField('选项1', validators=[
        DataRequired(message='请至少输入两个选项'),
        Length(max=255, message='选项长度不能超过255个字符')
    ])
    option2 = StringField('选项2', validators=[
        DataRequired(message='请至少输入两个选项'),
        Length(max=255, message='选项长度不能超过255个字符')
    ])
    option3 = StringField('选项3 (可选)', validators=[
        Length(max=255, message='选项长度不能超过255个字符')
    ])
    option4 = StringField('选项4 (可选)', validators=[
        Length(max=255, message='选项长度不能超过255个字符')
    ])
    option5 = StringField('选项5 (可选)', validators=[
        Length(max=255, message='选项长度不能超过255个字符')
    ])
    submit = SubmitField('创建投票')
    
    def validate(self, extra_validators=None):
        if not super(CreatePollForm, self).validate(extra_validators):
            return False
        
        # 确保至少有两个非空选项
        options = [
            self.option1.data.strip() if self.option1.data else '',
            self.option2.data.strip() if self.option2.data else '',
            self.option3.data.strip() if self.option3.data else '',
            self.option4.data.strip() if self.option4.data else '',
            self.option5.data.strip() if self.option5.data else ''
        ]
        valid_options = [opt for opt in options if opt]
        
        if len(valid_options) < 2:
            self.option2.errors.append('请至少输入两个有效选项')
            return False
        
        return True

class EditPollForm(FlaskForm):
    question = TextAreaField('投票问题', validators=[
        DataRequired(message='请输入投票问题'),
        Length(min=5, max=255, message='问题长度必须在5到255个字符之间')
    ])
    # 使用隐藏字段存储选项ID，方便更新
    option_ids = HiddenField('选项IDs')
    
    # 动态添加选项字段，初始显示5个字段
    option1 = StringField('选项1', validators=[
        DataRequired(message='请至少输入两个选项'),
        Length(max=255, message='选项长度不能超过255个字符')
    ])
    option2 = StringField('选项2', validators=[
        DataRequired(message='请至少输入两个选项'),
        Length(max=255, message='选项长度不能超过255个字符')
    ])
    option3 = StringField('选项3 (可选)', validators=[
        Length(max=255, message='选项长度不能超过255个字符')
    ])
    option4 = StringField('选项4 (可选)', validators=[
        Length(max=255, message='选项长度不能超过255个字符')
    ])
    option5 = StringField('选项5 (可选)', validators=[
        Length(max=255, message='选项长度不能超过255个字符')
    ])
    submit = SubmitField('保存修改')
    
    def validate(self, extra_validators=None):
        if not super(EditPollForm, self).validate(extra_validators):
            return False
        
        # 确保至少有两个非空选项
        options = [
            self.option1.data.strip() if self.option1.data else '',
            self.option2.data.strip() if self.option2.data else '',
            self.option3.data.strip() if self.option3.data else '',
            self.option4.data.strip() if self.option4.data else '',
            self.option5.data.strip() if self.option5.data else ''
        ]
        valid_options = [opt for opt in options if opt]
        
        if len(valid_options) < 2:
            self.option2.errors.append('请至少输入两个有效选项')
            return False
        
        return True

class VoteForm(FlaskForm):
    option = RadioField('选择一个选项', validators=[DataRequired(message='请选择一个选项')])
    submit = SubmitField('投票')

class DeleteConfirmForm(FlaskForm):
    submit = SubmitField('确认删除') 