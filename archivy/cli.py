import os

import click
from flask.cli import FlaskGroup, load_dotenv, routes_command, shell_command

from archivy import app
from archivy.check_changes import Watcher


def create_app():
    return app


def show_license(ctx, param, value):  # noqa:
    """Prints the license of the utility"""
    if not value or ctx.resilient_parsing:
        return
    click.echo(__doc__)
    ctx.exit()


@click.group(cls=FlaskGroup, create_app=create_app)
@click.option('--license', '--lic', is_flag=True,
              callback=show_license,
              expose_value=False, is_eager=True)
def cli():
    pass


# add built in commands:
cli.add_command(routes_command)
cli.add_command(shell_command)


@cli.command("run", short_help="Runs archivy web application")
def run():
    click.echo('Running archivy...')
    load_dotenv()
    # prevent pytest from hanging because of running thread
    watcher = Watcher(app)
    watcher.start()
    port = int(os.environ.get("ARCHIVY_PORT", 5000))
    os.environ["FLASK_RUN_FROM_CLI"] = "false"
    app.run(host='0.0.0.0', port=port)
    click.echo("Stopping archivy watcher")
    watcher.stop()
    watcher.join()


# @cli.command()
# def setup():
    # click.echo("Setting up archivy...")
