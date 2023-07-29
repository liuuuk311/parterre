import psycopg2
from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand


DATABASE_CONNECTION_DETAILS = {}
for database, conn_details in settings.DATABASES.items():
    DATABASE_CONNECTION_DETAILS[database] = {
        key.lower().replace("name", "dbname"): value
        for key, value in conn_details.items()
        if value and key.lower() in ["name", "user", "password", "host", "port"]
    }


class Command(BaseCommand):
    """DEV ONLY: Dumps the entire DB and sets up everything anew."""

    help = "DEV ONLY: Dumps the entire DB and sets up everything anew."

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.verbosity = 0

    @staticmethod
    def _get_cursor(db):
        conn_kwargs = DATABASE_CONNECTION_DETAILS[db]
        postgres_db_conn_kwargs = conn_kwargs.copy()
        postgres_db_conn_kwargs["dbname"] = "postgres"
        conn = psycopg2.connect(**postgres_db_conn_kwargs)
        conn.autocommit = True
        return conn.cursor()

    def _create_schema(self, db):
        """Sets up the database"""
        cur = self._get_cursor(db)
        cur.execute(
            "CREATE SCHEMA public; GRANT ALL ON SCHEMA public TO postgres; GRANT ALL ON SCHEMA public TO public;"
        )

    def _drop_schema(self, db):
        """Drops the database"""
        cur = self._get_cursor(db)
        # DANGER: Not using prepared variables here. hardcore python formatting.
        cur.execute("DROP SCHEMA public CASCADE;")

    def _drop_and_create_schema(self, db):
        """creates or recreates the database"""
        conn_kwargs = DATABASE_CONNECTION_DETAILS[db]
        psycopg2.connect(**conn_kwargs)
        self._drop_schema(db)
        self._create_schema(db)

    def handle(self, *args, **options):
        """entry point"""
        self.verbosity = options["verbosity"]
        if not settings.DEBUG:
            raise RuntimeError("Command can not be run in production.")

        for db in settings.DATABASES.keys():
            self._drop_and_create_schema(db)

        call_command("migrate", verbosity=self.verbosity)
        if self.verbosity > 0:
            self.stdout.write("Migrations done.")

        call_command("total_setup", verbosity=self.verbosity)
