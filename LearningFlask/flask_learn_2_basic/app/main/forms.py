

class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    passwd = PasswordField('Password:',validators=[Length(6, 10)])
    submit = SubmitField('Submit')