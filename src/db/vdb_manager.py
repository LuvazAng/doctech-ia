"""PosgreSQL Vectore Database Manager with pgvector support"""

from datetime import datetime
from typing import Dict, List
import psycopg2
from psycopg2 import sql
from conf.config import (
    POSGRESQL_DB_HOST,
    POSGRESQL_DB_PORT,
    POSGRESQL_DB_NAME,
    POSGRESQL_DB_USER,
    POSGRESQL_DB_PSW,
    DIMENSION_EMBEDDING_DIMENSION,
)


class VectorDatabase:
    """Class to manage embeddings sotrage and similarity search in PosgreSQL with pgvector"""

    def __init__(self, logger, connection_params: Dict[str, str] = None):
        """
        Initialize the vector database connection

        Args:
            logger: Logger instance
            connection_params: Database connection parameters
                              If None, will try to get from environment variables
        """
        self.logger = logger
        self.connection = None
        self.connection_params = (
            connection_params or self._get_default_connection_params()
        )

    def _get_default_connection_params(self) -> Dict[str, str]:
        """Get connection parameters from environment variables"""
        return {
            "host": POSGRESQL_DB_HOST,
            "port": POSGRESQL_DB_PORT,
            "database": POSGRESQL_DB_NAME,
            "user": POSGRESQL_DB_USER,
            "password": POSGRESQL_DB_PSW,
        }

    def connect(self) -> bool:
        """
        Establish connection to PosgreSQL database

        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            self.connection = psycopg2.connect(**self.connection_params)
            self.connection.autocommit = False
            self.logger.info("Succesfully connect to PostgreSQL database")
            return True
        except psycopg2.Error as e:
            self.logger.error("Error connection to PostgreSQL: %s", e)
            return False

    def disconnect(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()
            self.logger.info("Database connection closed")

    def _ensure_connection(self) -> bool:
        """Ensure database conneciton is active"""
        if not self.connection or self.connection.closed:
            return self.connect()
        return True

    def setup_database(
        self,
        table_name: str = "default_table",
        vector_dimension: int = DIMENSION_EMBEDDING_DIMENSION,
    ) -> bool:
        """
        Create the necessary table and enable pgvector extension

        Args:
            table_name (str, optional): Name of the table to create. Defaults to 'default_table'.
            vector_dimension (int, optional): Dimension of the embedding vectors. Defaults to 768.

        Returns:
            bool: True if setup successful, False otherwise
        """
        if not self._ensure_connection():
            return False

        try:
            with self.connection.cursor() as cursor:
                # Enable pgvector extension
                cursor.execute("CREATE EXTENSION IF NOT EXISTS vector;")

                # Create table if it doesn0t exist
                create_table_query = sql.SQL(
                    """
                    CREATE TABLE IF NOT EXISTS {table} (
                        id SERIAL PRIMARY KEY, 
                        filename VARCHAR(500) NOT NULL,
                        chunk_order INTEGER DEFAULT 0, 
                        content TEXT, 
                        embedding VECTOR({dimension}),
                        create_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );
                    """
                ).format(
                    table=sql.Identifier(table_name),
                    dimension=sql.Literal(vector_dimension),
                )

                cursor.execute(create_table_query)

                # Create index for similarity search
                index_query = sql.SQL(
                    """
                    CREATE INDEX IF NOT EXISTS {index_name}
                    ON {table} USING ivfflat (embedding vector_cosine_ops)
                    WITH (lists = 100);
                    """
                ).format(
                    index_name=sql.Identifier(f"idx_{table_name}_embedding"),
                    table=sql.Identifier(table_name),
                )

                cursor.execute(index_query)

                self.connection.commit()
                self.logger.info(
                    "Database setup completed successfully for table '%s'", table_name
                )
                return True
        except psycopg2.Error as e:
            self.logger.error("Error setting up database: %s", e)
            self.connection.rollback()
            return False

    def insert_embedding(
        self,
        filename: str,
        content: str,
        embedding: List[float],
        chunk_order: int = 0,
        table_name: str = "default_table",
    ) -> bool:
        """
        Insert a new embedding record into the database

        Args:
            filename (str): Name of the file
            content (str): Content of the file/chunk
            embedding (List[float]): Embedding vecor
            table_name (str, optional): Name of the table. Defaults to "default_table".
            chunk_order (int, optional): Order of chunk if file was split. Defaults to 0.

        Returns:
            bool: True if insertion successful, False otherwise
        """
        if not self._ensure_connection():
            return False

        if not embedding or len(embedding) == 0:
            self.logger.error("Empty embedding vector provided")
            return False

        try:
            with self.connection.cursor() as cursor:
                insert_query = sql.SQL(
                    """
                    INSERT INTO {table} (filename, chunk_order, content, embedding)
                    VALUES (%s, %s, %s, %s)
                    """
                ).format(table=sql.Identifier(table_name))

                cursor.execute(
                    insert_query,
                    (filename, chunk_order, content, embedding),
                )

                self.connection.commit()
                self.logger.debug("Successfully inserted embedding for %s", filename)
                return True
        except psycopg2.Error as e:
            self.logger.error("Error inserting embedding for '%s': %s", filename, e)
            self.connection.rollback()
