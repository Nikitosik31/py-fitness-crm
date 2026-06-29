from django.db import migrations


def create_progressreport_table(apps, schema_editor):
    if schema_editor.connection.vendor != "postgresql":
        return
    schema_editor.execute("""
        CREATE TABLE IF NOT EXISTS "fitness_progressreport" (
            "id" bigserial NOT NULL PRIMARY KEY,
            "date" date NOT NULL,
            "weight" numeric(5, 2) NOT NULL,
            "chest" numeric(5, 2) NOT NULL,
            "waist" numeric(5, 2) NOT NULL,
            "hips" numeric(5, 2) NOT NULL,
            "arm" numeric(5, 2) NOT NULL,
            "notes" text NOT NULL DEFAULT '',
            "client_id" bigint NOT NULL REFERENCES "fitness_client" ("id") ON DELETE CASCADE
        )
    """)


class Migration(migrations.Migration):

    dependencies = [
        ("fitness", "0002_client_user_progressreport"),
    ]

    operations = [
        migrations.RunPython(
            create_progressreport_table,
            reverse_code=migrations.RunPython.noop,
        ),
    ]
