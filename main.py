import argparse
from masking.masker import Masker, STRATEGY_MAP
from masking.config_loader import load_config, validate_config
from masking.exceptions import MaskingConfigError, FileHandlerError, UnsupportedStrategyError
from masking.app_logger import get_logger
from data_io.csv_handler import read_csv, write_csv
from data_io.json_handler import read_json, write_json
from database.db_connector import Database

logger = get_logger()

def run_masking(args, masker, records):
    masked = [masker.mask_record(r) for r in records]

    if args.dry_run:
        logger.info("--- DRY RUN: No files written ---")
        print("\nSample of masked output (first 3 records):")
        for record in masked[:3]:
            print(record)
        print()

    return masked

def main():
    parser = argparse.ArgumentParser(description="Data Masking Tool")
    parser.add_argument("--input", help="Path to input file")
    parser.add_argument("--output", help="Path to output file")
    parser.add_argument("--config", default="config.yaml", help="Path to config file")
    parser.add_argument("--format", choices=["csv", "json", "db"], default="csv")
    parser.add_argument("--db", help="Path to SQLite database")
    parser.add_argument("--table", help="Table name to mask")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview masking without writing any output"
    )
    parser.add_argument(
        "command",
        nargs="?",
        choices=["validate-config"],
        help="Optional command to run"
    )
    args = parser.parse_args()

    if args.command == "validate-config":
        errors = validate_config(args.config, STRATEGY_MAP)
        if errors:
            print("Config validation failed:")
            for error in errors:
                print(f"  - {error}")
        else:
            print("Config is valid")
        return

    try:
        config = load_config(args.config)
        masker = Masker(config)

        if args.format == "db":
            if not args.db or not args.table:
                logger.error("--db and --table are required for database mode")
                return
            db = Database(args.db)
            records = db.read_table(args.table)
            masked = run_masking(args, masker, records)
            if not args.dry_run:
                db.write_table(args.table, masked)
                logger.info(f"Masked table saved as masked_{args.table} in {args.db}")
            db.close()

        elif args.format == "csv":
            records = read_csv(args.input)
            masked = run_masking(args, masker, records)
            if not args.dry_run:
                write_csv(args.output, masked)
                logger.info(f"Masked CSV written to {args.output}")

        else:
            records = read_json(args.input)
            masked = run_masking(args, masker, records)
            if not args.dry_run:
                write_json(args.output, masked)
                logger.info(f"Masked JSON written to {args.output}")

        masker.report.print_summary()

    except (MaskingConfigError, FileHandlerError, UnsupportedStrategyError) as e:
        logger.error(str(e))
    except Exception as e:
        logger.error(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()
