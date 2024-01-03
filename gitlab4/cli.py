"""Console script for gitlab4."""

import click


@click.command()
def main():
    """Main entrypoint."""
    click.echo("gitlab4")
    click.echo("=" * len("gitlab4"))
    click.echo("Gitlab API wrapper with Pydantic")


if __name__ == "__main__":
    main()  # pragma: no cover
