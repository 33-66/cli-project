import click
from models import User, Task, Category
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Create the database engine and session once
engine = create_engine('sqlite:///to_do.db')
Session = sessionmaker(bind=engine)

def get_user_by_id(session, user_id):
     user = session.get(User,user_id)
     if not user:
         click.echo(f"User with ID {user_id} not found.")
         return None
     return user

@click.group()
def cli():
    """"
    This is a  command line interface for managing tasks and  categories
    """
    pass

@click.command()
# @click.argument('username')
def add_user():
    """
     Add a new user to the system
    Args:
        username (str): username
    """
    # prompt for username
    username = click.prompt("Input your username please", type=str)
    with Session() as session:
        user = User(name=username)
        session.add(user)
        session.commit()
        click.echo(f'User {username} added successfully')

@click.command()
def add_task():
    """"
    Add a new task to the system
    """
    with Session() as session:
        # prompt for user ID
        user_id = click.prompt("Enter user ID", type=int)
        user = get_user_by_id(session, user_id)
        if not user:
            return
        # show  available  categories
        categories = session.query(Category).all()
        click.echo("Available  categories")
        for  each_category in categories:
            click.echo(f"\t{each_category.name}")
        # prompt for task title
        title = click.prompt("Enter task title", type=str)
        # prompt for category
        category_name = click.prompt("Enter category name", type=str)

        category_obj = session.query(Category).filter_by(name=category_name).first()
        if not category_obj:
            click.echo(f"Category {category_name} not found.")
            return
        # create and add task
        task = Task(title=title, user=user, category=category_obj)
        session.add(task)
        click.echo(f'Task {title} added successfully for user {user.name}.')

@click.command()
def add_category():
    """
    Add  a new category to the system
    """
    with Session() as session:
        # prompt for category name
        category_name = click.prompt("Enter category name ", type=str)

        #  check if category  is there
        existing_category = session.query(Category).filter_by(name=category_name).first()
        if existing_category:
            click.echo(f"Category {category_name} already there")
        else:
            # create and add category
            category = Category(name=category_name)
            session.add(category)
            session.commit()  # Commit changes to the database
            click.echo(f"Category {category_name} has been created ")
@click.command()
def show_categories():
    """
    Show all available categories
    """
    with Session() as session:
        categories = session.query(Category).all()
        if not categories:
            click.echo("No categories available")
        else:
            click.echo("Available Categories")
            for cateogry in categories:
                click.echo(f'{cateogry.name} Tasks')

cli.add_command(add_user)
cli.add_command(add_task)
cli.add_command(add_category)
cli.add_command(show_categories)
if __name__ == '__main__':
    cli()
