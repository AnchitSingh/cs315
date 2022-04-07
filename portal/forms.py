from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField,TextAreaField,IntegerField,DateField,SelectField,DecimalField
from wtforms.fields import IntegerRangeField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from portal.models import user
from flask_wtf.file import FileField, FileAllowed, FileRequired


class RegistrationForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',validators=[DataRequired(), EqualTo('password')])
    confirm_password = PasswordField('Confirm Password',validators=[DataRequired(), EqualTo('password')])
    admin_code = StringField('Code')
    submit = SubmitField('Sign Up')
    
    def validate_username(self, username):
        user1 = user.query.filter_by(username=username.data).first()
        if user1:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user1 = user.query.filter_by(email=email.data).first()
        if user1:
            raise ValidationError('That email is taken. Please choose a different one.')




class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=40)])
    firstname = StringField('First Name',
                           validators=[Length(min=2, max=40)])
    lastname = StringField('Last Name',
                           validators=[DataRequired(), Length(min=2, max=40)])
    # phone_no = IntegerField('Phone Number')
    address = TextAreaField('Address')
    email = StringField('Email',validators=[DataRequired(), Email()])
    picture = FileField('Update Picture',validators=[FileAllowed(['jpg','png','jpeg','gif'])])
    submit = SubmitField('Update')
    
    def validate_username(self, username):
        if username.data != current_user.username:
            user1 = user.query.filter_by(username=username.data).first()
            if user1:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user1 = user.query.filter_by(email=email.data).first()
            if user1:
                raise ValidationError('That email is taken. Please choose a different one.')

class CreateDatabase(FlaskForm):
    file = FileField('Upload File')
    submit = SubmitField('Upload')
    


class UploadFile(FlaskForm):
    filename = StringField('File Name',validators=[DataRequired(), Length(min=2, max=40)])
    info = TextAreaField('Info')
    file = FileField('Upload File',validators=[FileAllowed(['pdf'])])
    submit1 = SubmitField('Upload')
    
class CreateFile(FlaskForm):
    filename = StringField('File Name',validators=[DataRequired(), Length(min=2, max=40)])
    info = TextAreaField('Info')
    submit2 = SubmitField('Start Editing')
    



class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')



# class AddCS(FlaskForm):
#     class_number = SelectField('Number',choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')],validators=[DataRequired()])
#     subject_name = SelectField('Name',choices=[('english', 'English'), ('math', 'Math'), ('science', 'Science'), ('hindi', 'Hindi')],validators=[DataRequired()])
#     teacher_id = StringField()
#     submit1 = SubmitField('Submit')

# class changeCS(FlaskForm):
#     old_class_number = SelectField('Number',choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')],validators=[DataRequired()])
#     old_subject_name = SelectField('Name',choices=[('english', 'English'), ('math', 'Math'), ('science', 'Science'), ('hindi', 'Hindi')],validators=[DataRequired()])
#     new_class_number = SelectField('Number',choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')],validators=[DataRequired()])
#     new_subject_name = SelectField('Name',choices=[('english', 'English'), ('math', 'Math'), ('science', 'Science'), ('hindi', 'Hindi')],validators=[DataRequired()])
#     teacher_id = StringField()
#     submit2 = SubmitField('Change')

# class removeCS(FlaskForm):
#     class_number = SelectField('Number',choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')],validators=[DataRequired()])
#     subject_name = SelectField('Name',choices=[('english', 'English'), ('math', 'Math'), ('science', 'Science'), ('hindi', 'Hindi')],validators=[DataRequired()])
#     teacher_id = StringField()
#     submit3 = SubmitField('Remove')


# class CreateClass(FlaskForm):
#     class_number = SelectField('Number',choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')],validators=[DataRequired()])
#     subject_name = SelectField('Name',choices=[('english', 'English'), ('math', 'Math'), ('science', 'Science'), ('hindi', 'Hindi')],validators=[DataRequired()])
#     submit = SubmitField('Add')


# class AddMarks(FlaskForm):
#     marks = DecimalField('Marks',validators=[DataRequired()])
#     comment = TextAreaField('Comment')
#     student_id = IntegerField('Id')
#     assignment_id = IntegerField('Id')
#     submit = SubmitField('Add')



# class UploadVideo(FlaskForm):
#     file_name = StringField('File Name',validators=[DataRequired(), Length(min=2, max=40)])
#     info = TextAreaField('Info')
#     file = FileField('Upload File',validators=[FileAllowed(['mp4','mkv','webm'])])
#     submit = SubmitField('Add')



# class CreateAssignment(FlaskForm):
#     class_no = SelectField('Class',choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')],validators=[DataRequired()])
#     subject = SelectField('Subject',choices=[('english', 'English'), ('math', 'Math'), ('hindi', 'Hindi'), ('science', 'Science')],validators=[DataRequired()])
#     teacher_id = IntegerField(validators=[DataRequired()])
#     assign_no = IntegerField('Assignment No.',validators=[DataRequired()])
#     max_marks = IntegerField('Max Marks',validators=[DataRequired()])
#     submit = SubmitField('Create')


class CreateAccount(FlaskForm):
    username = StringField('Username',validators=[DataRequired()])
    email = StringField('Username',validators=[DataRequired(),Email()])
    submit = SubmitField('Invite')
    def validate_username(self, username):
        user1 = user.query.filter_by(username=username.data).first()
        if user1:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user1 = user.query.filter_by(email=email.data).first()
        if user1:
            raise ValidationError('That email is taken. Please choose a different one.')




class RequestResetForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(),Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user1 = user.query.filter_by(email=email.data).first()
        if user1 is None:
            raise ValidationError('There is no account with that email. You must register first')



class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')



# class InviteForm(FlaskForm):
#     firstname = StringField('First Name',validators=[DataRequired(), Length(min=2, max=40)])
#     password = PasswordField('Password', validators=[DataRequired()])
#     picture = FileField('Update Picture',validators=[FileAllowed(['jpg','png','jpeg','gif'])])
#     confirm_password = PasswordField('Confirm Password',validators=[DataRequired(), EqualTo('password')])
#     submit = SubmitField('Update Account')


# class PostForm(FlaskForm):
#     title=StringField('Title',validators=[DataRequired()])
#     content=TextAreaField('Content',validators=[DataRequired()])
#     submit=SubmitField('Post')
