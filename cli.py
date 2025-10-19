import click
from flask import Flask
from models import db, User

app = Flask(__name__)
app.config.from_pyfile('.env')
db.init_app(app)

@click.group()
def cli():
    pass

@cli.command("init_db")
def init_db():
    with app.app_context():
        db.create_all()
        click.echo("Database initialized.")

@cli.command("create_admin")
def create_admin():
    with app.app_context():
        username = input("Admin username: ")
        email = input("Admin email: ")
        password = input("Admin password: ")
        user = User(username=username, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        click.echo("Admin user created.")

if __name__ == "__main__":
    cli()