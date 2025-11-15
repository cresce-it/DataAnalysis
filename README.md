# Data Analysis - Bills Analysis

Data analysis tools for analyzing utility bills from MongoDB, with automated weekly reporting to Glue.

## Features

- **Bills Analysis**: Comprehensive analysis of utility bills by week, vendor, and creator
- **Weekly Comparison**: Automated weekly reports comparing current week vs previous week
- **Glue Integration**: Automatic posting of weekly reports to Glue
- **MongoDB Integration**: Direct connection to MongoDB for real-time data analysis

## Prerequisites

- Python 3.8+
- MongoDB connection string
- Glue webhook URL (optional, for automated reporting)

## Setup

### 1. Clone the repository

```bash
git clone <repository-url>
cd DataAnalysis
```

### 2. Create virtual environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the root directory:

```bash
MONGODB_URI=mongodb+srv://user:password@host/database
GLUE_WEBHOOK_URL=https://api.gluegroups.com/webhook/wbh_.../...
GLUE_TARGET=grp_...  # or thr_... for thread
```

Or use the provided `setup.sh` script:

```bash
chmod +x setup.sh
./setup.sh
```

## Configuration

### Excluded Users

Edit `config.py` to exclude specific user IDs from analysis:

```python
EXCLUDED_USER_IDS = [
    "user_id_1",
    "user_id_2"
]
```

## Usage

### Bills Analysis

Run comprehensive bills analysis:

```bash
source venv/bin/activate
python bills_analysis.py
```

This generates:
- Weekly breakdown of bills
- Summary by creator (emails vs agents)
- Breakdown by vendor
- CSV export: `bills_analysis.csv`

### Weekly Comparison

Generate and post weekly comparison report:

```bash
source venv/bin/activate
python weekly_comparison.py
```

This will:
- Compare current week vs last week
- Show metrics with green/red indicators
- Display top 3 energy providers
- Display top 5 contributors
- Automatically post to Glue if configured

## GitHub Actions Setup

### 1. Add Secrets to GitHub

Go to your repository settings → Secrets and variables → Actions, and add:

- `MONGODB_URI`: Your MongoDB connection string
- `GLUE_WEBHOOK_URL`: Your Glue webhook URL
- `GLUE_TARGET`: Your Glue group or thread ID

### 2. Create Workflow File

Create `.github/workflows/weekly-report.yml`:

```yaml
name: Weekly Bills Report

on:
  schedule:
    - cron: '0 9 * * 1'  # Every Monday at 9 AM UTC
  workflow_dispatch:  # Allow manual trigger

jobs:
  weekly-report:
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
      
      - name: Run weekly comparison
        env:
          MONGODB_URI: ${{ secrets.MONGODB_URI }}
          GLUE_WEBHOOK_URL: ${{ secrets.GLUE_WEBHOOK_URL }}
          GLUE_TARGET: ${{ secrets.GLUE_TARGET }}
        run: |
          python weekly_comparison.py
```

### 3. Manual Trigger

You can also trigger the workflow manually:
- Go to Actions tab in GitHub
- Select "Weekly Bills Report"
- Click "Run workflow"

## Project Structure

```
DataAnalysis/
├── main.py                 # MongoDB connection class
├── config.py              # Configuration and excluded users
├── bills_analysis.py       # Comprehensive bills analysis
├── weekly_comparison.py    # Weekly comparison report
├── analyze.py              # Example analysis script
├── requirements.txt        # Python dependencies
├── setup.sh                # Setup script
├── .env                    # Environment variables (not in git)
└── README.md              # This file
```

## Scripts Overview

### `bills_analysis.py`

Generates comprehensive analysis of all bills:
- Groups bills by week
- Shows breakdown by vendor and creator
- Exports to CSV
- Excludes configured user IDs

### `weekly_comparison.py`

Generates weekly comparison report:
- Compares current week vs last week
- Shows metrics with percentage changes
- Highlights top 3 energy providers
- Highlights top 5 contributors
- Posts to Glue automatically

## Output Format

### Weekly Comparison Report

The report includes:
- **Overall Metrics**: Bills count, amounts, kWh, costs with week-over-week changes
- **Top Energy Providers**: Top 3 providers by bill count
- **Top Contributors**: Top 5 contributors by bill count

Indicators:
- 🟢 Green: Positive change (increase)
- 🔴 Red: Negative change (decrease)
- ⚪ Neutral: No significant change

## Troubleshooting

### MongoDB Connection Issues

- Verify your `MONGODB_URI` is correct
- Check network connectivity
- Ensure MongoDB allows connections from your IP

### Glue Webhook Issues

- Verify webhook URL is correct
- Check target ID (group or thread)
- Ensure webhook has proper permissions

### No Bills Found

- Check if bills are archived (`is_archived: false`)
- Verify excluded user IDs in `config.py`
- Check date ranges in your data

## Development

### Adding New Analysis

1. Create a new script in the root directory
2. Import `MongoDBConnection` from `main.py`
3. Use `config.EXCLUDED_USER_IDS` to maintain consistency
4. Follow the existing code patterns

### Testing

Run scripts locally before deploying:

```bash
source venv/bin/activate
python bills_analysis.py
python weekly_comparison.py
```

## License

[Add your license here]

## Support

For issues or questions, please open an issue in the repository.

