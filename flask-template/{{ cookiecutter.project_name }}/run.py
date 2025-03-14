from app import create_app
{% if cookiecutter.use_db == "y" %}
from app.extensions import db
{% endif %}

app = create_app()

{% if cookiecutter.use_db == "y" %}
@app.cli.command("create-db")
def create_database():
    with app.app_context():
        db.create_all()
{% endif %}

if __name__ == '__main__':
    app.run(debug=True)
