import click

from models import User, Role


@click.group()
def main():
    pass


@main.command(help='Create superuser')
@click.option('--login', prompt='login')
@click.password_option()
def createsuperuser(login, password):
    if User.query.filter_by(login=login).first():
        click.echo(f'Superuser {login} already exists.')
        return

    if not Role.query.filter_by(title='superadmin').first():
        role = Role('superadmin')
        role.save()

    u = User(login, password, role='superadmin')
    u.save()
    click.echo(f'Superuser {login} created.')


if __name__ == '__main__':
    main()
