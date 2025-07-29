from src.core.services import register_entry, add_score, list_entries
from src.data.database import SessionLocal
from flask import Flask, render_template, request, redirect, url_for
import sys
import os

# Dynamically add the project root to sys.path (reuse from CLI if needed)
project_root = os.path.abspath(os.path.join(
    os.path.dirname(__file__), '..', '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)


app = Flask(__name__, template_folder='templates')


@app.route('/')
def index():
    return render_template('base.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        rider_name = request.form['rider_name']
        rider_age = int(request.form['rider_age'])
        horse_name = request.form['horse_name']
        horse_age = int(request.form['horse_age'])
        event_name = request.form['event_name']

        with SessionLocal() as session:
            entry = register_entry(
                session, rider_name, rider_age, horse_name, horse_age, event_name)
        return redirect(url_for('list_entries_web'))
    return render_template('register.html')


@app.route('/score', methods=['GET', 'POST'])
def score():
    if request.method == 'POST':
        entry_id = int(request.form['entry_id'])
        score = int(request.form['score'])

        with SessionLocal() as session:
            entry = add_score(session, entry_id, score)
            if not entry:
                return "Entry not found", 404
        return redirect(url_for('list_entries_web'))
    return render_template('score.html')


@app.route('/list')
def list_entries_web():
    with SessionLocal() as session:
        entries = list_entries(session)
    return render_template('list.html', entries=entries)


if __name__ == '__main__':
    app.run(debug=True)
