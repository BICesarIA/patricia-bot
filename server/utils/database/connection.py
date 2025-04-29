import databases
import sqlalchemy

DATABASE_URL = "postgresql://patricia_bot_db_user:WhQDAdcZ1BvK5CddahuyFxaJaJYI2gqL@dpg-d07vit9r0fns73d96a4g-a.oregon-postgres.render.com/patricia_bot_db"
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()
