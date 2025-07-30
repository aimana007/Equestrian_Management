from src.data.database import init_db, SessionLocal
from src.core.services import register_entry, add_score, list_entries
from src.core.age_categories import AgeCategoriesService  # NEW IMPORT
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
                             default=0, show_default=False)
    horse_name = click.prompt("Enter horse name", type=str)
    horse_age = click.prompt("Enter horse age", type=int,
                             default=0, show_default=False)
    event_name = click.prompt("Enter event name", type=str)
    
    # NEW: Age category selection
    age_service = AgeCategoriesService()
    age_service.list_categories_for_cli()
    
    while True:
        try:
            age_category_id = click.prompt("Select age category (enter number)", type=str)
            selected_category = age_service.get_category_by_selection(age_category_id)
            if selected_category:
                click.echo(f"Selected: {selected_category['name']}")
                break
            else:
                click.echo("Invalid selection. Please try again.")
        except (ValueError, KeyboardInterrupt):
            click.echo("Invalid input. Please enter a number.")

    with SessionLocal() as session:
        entry = register_entry(session, rider_name, rider_age, horse_name, 
                              horse_age, event_name, selected_category['name'])  # NEW PARAMETER
        click.echo(
            f"Registered entry ID: {entry.id} for {rider_name} on {horse_name} in {event_name} (Category: {selected_category['name']})")


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
            age_category = f" - Category: {entry.age_category}" if entry.age_category else ""
            click.echo(
                f"Entry {entry.id}: {entry.rider.name} ({entry.rider.age}) on {entry.horse.name} ({entry.horse.age}) in {entry.event_name}{age_category} - Score: {entry.score}")


# NEW COMMAND: List age categories
@cli.command()
def categories():
    """List all available age categories."""
    age_service = AgeCategoriesService()
    age_service.list_categories_for_cli()


if __name__ == "__main__":
    cli()