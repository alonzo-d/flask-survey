from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True

debug = DebugToolbarExtension(app)

@app.get('/')
def show_survey_start():
    """Generate survey start page with title, instructions, and a start button
    and show the page"""
    return render_template('survey_start.html', survey=survey)

@app.post('/begin')
def begin_survey():
    """Start the survey by redirecting to the first question"""
    session['responses'] = []
    return redirect('/questions/0')

@app.get('/questions/<int:q_num>')
def show_question(q_num):
    """Generate and show form for current question"""
    if len(session['responses']) == len(survey.questions):
        flash('You are trying to access an invalid question!')
        return redirect('/thanks')

    if q_num != len(session['responses']):
        flash('You are trying to access an invalid question!')
        return redirect(f'/questions/{len(session["responses"])}')

    return render_template('question.html', question=survey.questions[q_num])

@app.post('/answer')
def handle_answer():
    """ stores answer and redirects to next question """
    responses = session['responses']
    responses.append(request.form.get('answer', ''))
    session['responses'] = responses
    if len(session['responses']) == len(survey.questions):
        return redirect('/thanks')

    return redirect(f'/questions/{len(session["responses"])}')

@app.get('/thanks')
def show_thanks_page():
    """Generate and show a thank you page"""
    qs_and_as = {survey.questions[idx].prompt: session['responses'][idx] for idx in range(len(survey.questions))}
    return render_template('completion.html', qs_and_as=qs_and_as)