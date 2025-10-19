import click
from app import app, db
from models import User

@click.group()
def cli():
    pass

@cli.command()
def init_db():
    """إنشاء قاعدة البيانات"""
    db.create_all()
    click.echo("Database initialized.")

@cli.command()
@click.argument('username')
@click.argument('email')
@click.argument('password')
def create_admin(username, email, password):
    """إنشاء مستخدم admin"""
    from werkzeug.security import generate_password_hash
    admin = User(username=username, email=email, password=generate_password_hash(password))
    db.session.add(admin)
    db.session.commit()
    click.echo(f"Admin {username} created.")

if __name__ == '__main__':
    cli()
