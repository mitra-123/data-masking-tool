# Data Masking Tool

A configurable command-line tool for masking sensitive PII (Personally Identifiable Information) across CSV, JSON, and SQLite databases.

Built with Python using object-oriented design and SOLID principles, this project simulates real-world data privacy workflows used in enterprise environments where production data must never be exposed in development or testing systems.

---

## Features

- Multiple masking strategies for sensitive data protection:
  - Redaction
  - Partial masking
  - Email masking
  - Credit card masking
  - Fake data generation using Faker (names, emails, phone numbers)
- Config-driven field mapping via YAML (no code changes required)
- Supports CSV, JSON, and SQLite database input/output
- Dry-run mode to preview transformations without writing output
- Structured logging to console and file (`masking.log`)
- Config validation command to detect errors before execution
- Masking summary report for each run (records + fields masked)
- Extensible architecture using the Strategy Pattern

---

## Tech Stack

| Tool | Purpose |
|------|---------|
| Python 3.14 | Core programming language |
| SQLite | Database support |
| Faker | Synthetic data generation |
| PyYAML | Configuration parsing |
| pytest | Unit testing |

---

## Installation

**1. Clone the repository:**
```bash
git clone https://github.com/YOUR_USERNAME/data-masking-tool.git
cd data-masking-tool
```

**2. Create and activate a virtual environment:**
```bash
python -m venv venv
source venv/bin/activate      # Mac/Linux
venv\Scripts\activate         # Windows
```

**3. Install dependencies:**
```bash
pip install -r requirements.txt
```

**4. (Optional) Seed the sample SQLite database:**
```bash
python database/seed.py
```

---

## Project Structure

```
data-masking-tool/
├── masking/
│   ├── __init__.py  
│   ├── strategies.py        # Masking + fake data strategies
│   ├── masker.py            # Core masking engine
│   ├── config_loader.py     # YAML config loader + validation
│   ├── logger.py            # Masking summary report
│   ├── app_logger.py        # Logging system (console + file)
│   └── exceptions.py        # Custom exception classes
│
├── data_io/
│   ├── __init__.py
│   ├── csv_handler.py       # CSV read/write
│   └── json_handler.py      # JSON read/write
│
├── database/
│   ├── __init__.py
│   ├── db_connector.py      # SQLite operations
│   └── seed.py              # Sample database generator
│
├── tests/
│   ├── __init__.py
│   ├── test_strategies.py
│   └── test_masker.py
│
├── config.yaml              # Field-to-strategy mapping
├── sample_data.csv          # Sample input data
├── main.py                  # CLI entry point
├── requirements.txt
└── README.md
```

---

## Usage

**Validate configuration before running:**
```bash
python main.py validate-config
```

**Dry-run — preview output without writing any files:**
```bash
python main.py --input sample_data.csv --output masked.csv --format csv --dry-run
```

**Mask a CSV file:**
```bash
python main.py --input sample_data.csv --output masked.csv --format csv
```

**Mask a JSON file:**
```bash
python main.py --input sample_data.json --output masked.json --format json
```

**Mask a SQLite database table:**
```bash
python main.py --format db --db sample.db --table customers
```

---

## Configuration

Fields and their masking strategies are defined in `config.yaml`:

```yaml
fields:
  email:
    strategy: fake_email
  name:
    strategy: fake_name
  credit_card:
    strategy: credit_card
  phone:
    strategy: fake_phone
```

---

## Available Strategies

| Strategy | Description | Example Output |
|----------|-------------|----------------|
| `redact` | Replaces value entirely | `***REDACTED***` |
| `partial` | Keeps first N chars, masks the rest | `647*******` |
| `email` | Masks local part of email | `j***@gmail.com` |
| `credit_card` | Masks all but last 4 digits | `****-****-****-3456` |
| `fake_name` | Replaces with realistic fake name | `Jane Smith` |
| `fake_email` | Replaces with realistic fake email | `user123@example.com` |
| `fake_phone` | Replaces with realistic fake phone | `+1-800-555-0199` |

The `partial` strategy accepts an optional `visible_chars` parameter:

```yaml
phone:
  strategy: partial
  visible_chars: 3
```

---

## Example Output

**Input:**
```
name,email,credit_card,phone
John Doe,john.doe@gmail.com,1234-5678-9012-3456,6471234567
```

**Output:**
```
name,email,credit_card,phone
Jane Smith,user847@example.com,****-****-****-3456,647*******
```

---

## Design

This project uses the **Strategy Pattern** — each masking algorithm is an independent class implementing a shared `MaskingStrategy` abstract interface:

```
MaskingStrategy (Abstract Base Class)
├── RedactStrategy
├── PartialMaskStrategy
├── EmailMaskStrategy
├── CreditCardMaskStrategy
├── FakeNameStrategy
├── FakeEmailStrategy
└── FakePhoneStrategy
```

**SOLID principles applied:**

- **Open/Closed Principle:** New strategies can be added by creating a new class and registering it in the strategy map — no existing code needs to change
- **Single Responsibility Principle:** Each class handles exactly one masking behaviour
- **Dependency Inversion Principle:** The `Masker` class depends on the `MaskingStrategy` interface, not on concrete implementations

---

## Running Tests

```bash
pytest tests/ -v
```

---

## Logging

Every run writes to `masking.log` with full timestamps:

```
2026-04-17 19:47:10,737 INFO: --- DRY RUN: No files written ---
2026-04-17 19:47:50,601 INFO: Masked CSV written to masked.csv
```

A summary report is also printed to the console after every run:

```
===== Masking Report =====
Total records processed: 2
Fields masked:
  - email: 2 values masked
  - credit_card: 2 values masked
  - name: 2 values masked
  - phone: 2 values masked
==========================
