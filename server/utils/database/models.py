import sqlalchemy
from .connection import metadata

conversations = sqlalchemy.Table(
    "conversations",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("to", sqlalchemy.String(255)),
    sqlalchemy.Column("from_number", sqlalchemy.String(255)),
    sqlalchemy.Column("incoming_msg", sqlalchemy.Text),
    sqlalchemy.Column("response", sqlalchemy.Text),
    sqlalchemy.Column("type_response", sqlalchemy.String(100)),
    sqlalchemy.Column("created_at", sqlalchemy.DateTime, server_default=sqlalchemy.func.now())
)