from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, BooleanField
from wtforms.validators import DataRequired


class JobForm(FlaskForm):
    team_leader = StringField('Team leader', validators=[DataRequired()])
    job = StringField('Job', validators=[DataRequired()])
    work_size = IntegerField('Work size', validators=[DataRequired()])
    collaborators = StringField('Collaborators', validators=[DataRequired()])
    start_date = StringField('Start date', validators=[DataRequired()])
    end_date = StringField('End date', validators=[DataRequired()])
    is_finished = BooleanField('Is finished')
    submit = SubmitField('Add job')
