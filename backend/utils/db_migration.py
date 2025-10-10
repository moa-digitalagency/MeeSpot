#
# MatchSpot
# MOA Digital Agency LLC
# Par : Aisance KALONJI
# Mail : moa@myoneart.com
# www.myoneart.com
#

from sqlalchemy import inspect, text
from backend import db

def check_and_add_column(table_name, column_name, column_definition):
    """Check if a column exists, and add it if it doesn't"""
    inspector = inspect(db.engine)
    columns = [col['name'] for col in inspector.get_columns(table_name)]
    
    if column_name not in columns:
        with db.engine.connect() as conn:
            conn.execute(text(f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_definition}"))
            conn.commit()
        print(f"✓ Column {column_name} added to {table_name}")
        return True
    return False

def run_migrations():
    """Run all necessary migrations"""
    try:
        check_and_add_column('subscription_plans', 'role', "VARCHAR(20) NOT NULL DEFAULT 'establishment'")
        check_and_add_column('subscription_plans', 'is_active', 'BOOLEAN NOT NULL DEFAULT TRUE')
    except Exception as e:
        print(f"Migration error (table may not exist yet): {e}")
