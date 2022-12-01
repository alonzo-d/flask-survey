from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True

debug = DebugToolbarExtension(app)

responses = []

@app.get('/')
def show_survey_start():
    """Generate survey start page with title, instructions, and a start button
    and show the page"""
    return render_template('survey_start.html', title=survey.title, instructions=survey.instructions)

@app.post('/begin')
def begin_survey():
    """Start the survey by redirecting to the first question"""
    return redirect('/questions/0')

@app.get('/questions/<int:q_num>')
def show_question(q_num):
    """Generate and show form for current question"""
    return render_template('question.html', question=survey.questions[q_num])