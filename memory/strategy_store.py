import sqlite3
import json
from datetime import datetime


class StrategyMemory:

    def __init__(
        self,
        db_path="memory/logistics_memory.db"
    ):

        self.conn = sqlite3.connect(db_path)

        self.create_table()

    def create_table(self):

        cursor = self.conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS strategies (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            product_name TEXT,

            timestamp TEXT,

            inventory_insights TEXT,

            delivery_insights TEXT,

            strategy TEXT,

            critique TEXT,

            final_strategy TEXT
        )
        """)

        self.conn.commit()

    def save_strategy(
        self,
        product_name,
        inventory_insights,
        delivery_insights,
        strategy,
        critique,
        final_strategy
    ):

        cursor = self.conn.cursor()

        cursor.execute("""
        INSERT INTO strategies (

            product_name,
            timestamp,
            inventory_insights,
            delivery_insights,
            strategy,
            critique,
            final_strategy

        ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            product_name,
            datetime.now().isoformat(),

            json.dumps(inventory_insights),
            json.dumps(delivery_insights),

            json.dumps(strategy),
            json.dumps(critique),

            json.dumps(final_strategy)
        ))

        self.conn.commit()

    def get_product_history(self, product_name):
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT timestamp, final_strategy 
            FROM strategies 
            WHERE product_name = ? 
            ORDER BY timestamp DESC
        """, (product_name,))
        
        rows = cursor.fetchall()
        
        history = []
        for row in rows:
            timestamp = row[0]
            raw_strategy = row[1]
            
            # Unpack text back into a valid Python dictionary structure
            try:
                parsed_strategy = json.loads(raw_strategy) if raw_strategy else {}
            except json.JSONDecodeError:
                parsed_strategy = {"raw_output": raw_strategy}
                
            history.append((timestamp, parsed_strategy))
            
        return history
    
    def get_latest_strategy(
        self,
        product_name
    ):

        cursor = self.conn.cursor()

        cursor.execute("""
        SELECT final_strategy
        FROM strategies
        WHERE product_name = ?
        ORDER BY timestamp DESC
        LIMIT 1
        """,
        (product_name,)
        )

        row = cursor.fetchone()

        if not row:
            return None

        strategy = row[0]

        if isinstance(strategy, str):
            try:
                return json.loads(strategy)
            except:
                pass

        return strategy

    def get_all_products(self):

        cursor = self.conn.cursor()

        cursor.execute("""
            SELECT DISTINCT product_name
            FROM strategies
            WHERE product_name IS NOT NULL
        """)

        rows = cursor.fetchall()

        products = sorted(
            {
                row[0].strip()
                for row in rows
                if row[0]
            }
        )

        return products
    
    def get_product_run_timeline(
        self,
        product_name
    ):

        cursor = self.conn.cursor()

        cursor.execute("""
            SELECT
                timestamp,
                final_strategy
            FROM strategies
            WHERE product_name = ?
            ORDER BY timestamp DESC
        """,
        (product_name,)
        )

        rows = cursor.fetchall()

        timeline = []

        for timestamp, strategy in rows:

            try:

                if isinstance(strategy, str):
                    strategy = json.loads(strategy)

            except Exception:
                pass

            timeline.append({
                "timestamp": timestamp,
                "strategy": strategy
            })

        return timeline