"""PostgreSQL / psql database assistant plugin."""

from __future__ import annotations

from .base import ToolPlugin, register_plugin_class


POSTGRES_SYSTEM_PROMPT = (
    "You are an expert PostgreSQL database administrator and SQL assistant. "
    "The user has the `psql` client (and optionally `pg_dump`, `pg_restore`, "
    "`createdb`, `dropdb`). Help them connect to databases, write and optimize "
    "SQL queries, manage schemas, indexes, roles, extensions, and perform "
    "backup/restore operations. "
    "When you provide a command, enclose it in a ```bash ... ``` markdown block. "
    "For interactive SQL, prefer `psql` with clear connection strings or "
    "environment variables (PGHOST, PGUSER, PGDATABASE). "
    "Always warn before DROP, TRUNCATE, DELETE without WHERE, or destructive "
    "maintenance commands. Explain EXPLAIN plans and common performance patterns "
    "when helpful."
)


@register_plugin_class
class PostgresPlugin(ToolPlugin):
    id = "postgres"
    name = "Postgres Assistant"
    description = "AI help for PostgreSQL, psql, queries and admin tasks"
    system_prompt = POSTGRES_SYSTEM_PROMPT
    start_command = ["bash"]
    requires_pty = True
    color_key = "info"

    def check_available(self) -> bool:
        import shutil
        return shutil.which("psql") is not None
