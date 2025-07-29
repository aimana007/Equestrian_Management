from src.data.database import init_db, SessionLocal
from src.core.services import register_entry, add_score, list_entries
import click
import sys
import os

# Dynamically add the project root to sys.path
project_root = os.path.abspath(os.path.join(
    os.path.dirname(__file__), '..', '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)


@click.group()
def cli():
    init_db()  # Ensure DB is initialized


@cli.command()
def register():
    """Interactively register a rider-horse entry for an event."""
    rider_name = click.prompt("Enter rider name", type=str)
    rider_age = click.prompt("Enter rider age", type=int,
                             default=0, show_default=False)  # Prompts until valid int
    horse_name = click.prompt("Enter horse name", type=str)
    horse_age = click.prompt("Enter horse age", type=int,
                             default=0, show_default=False)
    event_name = click.prompt("Enter event name", type=str)

    with SessionLocal() as session:
        entry = register_entry(session, rider_name,
                               rider_age, horse_name, horse_age, event_name)
        click.echo(
            f"Registered entry ID: {entry.id} for {rider_name} on {horse_name} in {event_name}")


@cli.command()
def score():
    """Interactively add or update a score for an entry."""
    entry_id = click.prompt("Enter entry ID", type=int)
    score = click.prompt("Enter score", type=int)

    with SessionLocal() as session:
        entry = add_score(session, entry_id, score)
        if entry:
            click.echo(f"Updated score for entry {entry_id} to {score}")
        else:
            click.echo("Entry not found")


@cli.command()
def list():
    """List all entries with details."""
    with SessionLocal() as session:
        entries = list_entries(session)
        if not entries:
            click.echo("No entries found.")
            return
        for entry in entries:
            click.echo(
                f"Entry {entry.id}: {entry.rider.name} ({entry.rider.age}) on {entry.horse.name} ({entry.horse.age}) in {entry.event_name} - Score: {entry.score}")


if __name__ == "__main__":
    cli()
