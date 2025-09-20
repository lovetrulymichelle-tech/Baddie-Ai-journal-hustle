#!/usr/bin/env python3
"""
SQLite to PostgreSQL Migration Script for Baddie AI Journal

This script migrates journal entries from a local SQLite database to a PostgreSQL database.
It supports dry-run mode for verification before actual migration.

Usage:
    python migrate_sqlite_to_postgres.py [--dry-run]

Environment Variables Required:
    SQLALCHEMY_DATABASE_URI_SRC: Source SQLite database URI (e.g., sqlite:///journal.db)
    SQLALCHEMY_DATABASE_URI_DST: Destination PostgreSQL database URI
"""

import os
import sys
import argparse
import logging
from sqlalchemy import create_engine, MetaData
from sqlalchemy.exc import SQLAlchemyError

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def validate_environment():
    """Validate required environment variables are set."""
    src_uri = os.getenv('SQLALCHEMY_DATABASE_URI_SRC')
    dst_uri = os.getenv('SQLALCHEMY_DATABASE_URI_DST')

    if not src_uri:
        logger.error("SQLALCHEMY_DATABASE_URI_SRC environment variable not set")
        return False, None, None

    if not dst_uri:
        logger.error("SQLALCHEMY_DATABASE_URI_DST environment variable not set")
        return False, None, None

    if not src_uri.startswith('sqlite://'):
        logger.error("Source URI must be a SQLite database (sqlite://)")
        return False, None, None

    if not dst_uri.startswith('postgresql://'):
        logger.error("Destination URI must be a PostgreSQL database (postgresql://)")
        return False, None, None

    logger.info(f"Source database: {src_uri}")
    logger.info(f"Destination database: {dst_uri.split('@')[0]}@[HIDDEN]")

    return True, src_uri, dst_uri


def get_table_row_count(engine, table_name):
    """Get row count for a table."""
    try:
        with engine.connect() as conn:
            result = conn.execute(f"SELECT COUNT(*) FROM {table_name}")
            return result.scalar()
    except SQLAlchemyError as e:
        logger.warning(f"Could not get row count for {table_name}: {e}")
        return 0


def migrate_data(src_uri, dst_uri, dry_run=False):
    """Migrate data from SQLite to PostgreSQL."""
    try:
        # Create engines
        logger.info("Connecting to databases...")
        src_engine = create_engine(src_uri)
        dst_engine = create_engine(dst_uri)

        # Test connections
        src_engine.connect().close()
        dst_engine.connect().close()
        logger.info("Database connections successful")

        # Reflect source database schema
        src_metadata = MetaData()
        src_metadata.reflect(bind=src_engine)

        if not src_metadata.tables:
            logger.warning("No tables found in source database")
            return True

        logger.info(f"Found {len(src_metadata.tables)} tables in source database")

        migration_summary = {}

        for table_name, table in src_metadata.tables.items():
            logger.info(f"Processing table: {table_name}")

            # Get row count from source
            src_count = get_table_row_count(src_engine, table_name)
            logger.info(f"  Source rows: {src_count}")

            if src_count == 0:
                logger.info(f"  Skipping empty table: {table_name}")
                migration_summary[table_name] = {'source': 0, 'migrated': 0, 'status': 'skipped'}
                continue

            if dry_run:
                logger.info(f"  [DRY RUN] Would migrate {src_count} rows")
                migration_summary[table_name] = {'source': src_count, 'migrated': 0, 'status': 'dry_run'}
                continue

            # Perform actual migration
            try:
                with src_engine.connect() as src_conn:
                    # Read all data from source table
                    result = src_conn.execute(table.select())
                    rows = result.fetchall()

                    if rows:
                        # Insert data into destination
                        with dst_engine.connect() as dst_conn:
                            # Ensure table exists in destination
                            table.metadata.bind = dst_engine
                            table.create(checkfirst=True)

                            # Insert rows
                            dst_conn.execute(table.insert(), [dict(row._mapping) for row in rows])
                            dst_conn.commit()

                        logger.info(f"  Successfully migrated {len(rows)} rows")
                        migration_summary[table_name] = {
                            'source': src_count,
                            'migrated': len(rows),
                            'status': 'success'
                        }
                    else:
                        migration_summary[table_name] = {
                            'source': src_count,
                            'migrated': 0,
                            'status': 'no_data'
                        }

            except SQLAlchemyError as e:
                logger.error(f"  Failed to migrate table {table_name}: {e}")
                migration_summary[table_name] = {
                    'source': src_count,
                    'migrated': 0,
                    'status': 'error',
                    'error': str(e)
                }

        # Print migration summary
        logger.info("\nMigration Summary:")
        logger.info("=" * 50)
        for table_name, summary in migration_summary.items():
            status = summary['status']
            if status == 'success':
                logger.info(f"{table_name}: {summary['migrated']}/{summary['source']} rows migrated successfully")
            elif status == 'dry_run':
                logger.info(f"{table_name}: {summary['source']} rows ready for migration (dry run)")
            elif status == 'skipped':
                logger.info(f"{table_name}: Skipped (empty table)")
            elif status == 'error':
                logger.error(f"{table_name}: Migration failed - {summary.get('error', 'Unknown error')}")

        return True

    except SQLAlchemyError as e:
        logger.error(f"Database error: {e}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return False


def main():
    """Main function."""
    parser = argparse.ArgumentParser(
        description="Migrate journal data from SQLite to PostgreSQL"
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Perform a dry run without actually migrating data'
    )

    args = parser.parse_args()

    logger.info("Starting SQLite to PostgreSQL migration")
    logger.info(f"Mode: {'DRY RUN' if args.dry_run else 'ACTUAL MIGRATION'}")

    # Validate environment
    valid, src_uri, dst_uri = validate_environment()
    if not valid:
        logger.error("Environment validation failed")
        sys.exit(1)

    # Perform migration
    success = migrate_data(src_uri, dst_uri, dry_run=args.dry_run)

    if success:
        if args.dry_run:
            logger.info("Dry run completed successfully")
            logger.info("Run without --dry-run to perform actual migration")
        else:
            logger.info("Migration completed successfully")
        sys.exit(0)
    else:
        logger.error("Migration failed")
        sys.exit(1)


if __name__ == '__main__':
    main()
