# TOPSIS Decision Support System

A complete web application for Multi-Criteria Decision Making using the TOPSIS (Technique for Order of Preference by Similarity to Ideal Solution) algorithm.

## Features

- Upload datasets in CSV or Excel format (.csv, .xlsx, .xls)
- Configure weights and impacts for each criterion
- Automated TOPSIS calculation with ranking
- Identify the best alternative (Rank 1)
- Download results as CSV
- Modern, responsive UI

## Project Structure

```
topsis_app/
├── main.py                 # FastAPI application
├── topsis_logic.py         # TOPSIS algorithm implementation
├── requirements.txt        # Python dependencies
├── templates/
│   ├── index.html         # Landing page
│   ├── configure.html     # Configuration page
│   └── result.html        # Results page
└── static/
    └── style.css          # Styles
```

## Installation & Setup

### 1. Create Virtual Environment

**Windows (Git Bash):**
```bash
python -m venv venv
source venv/Scripts/activate
```

**Windows (Command Prompt):**
```cmd
python -m venv venv
venv\Scripts\activate
```

**Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the Application

```bash
uvicorn main:app --reload
```

### 4. Access the Application

Open your browser and navigate to:
```
http://127.0.0.1:8000
```

## Dataset Requirements

Your dataset must meet the following criteria:

- **Minimum 3 columns**: 1 ID column + at least 2 numeric criteria columns
- **First column**: ID/Alternative name (can be text or numbers)
- **Criteria columns**: All must be numeric (integers or floats)
- **No missing values**: All criteria columns must have complete data
- **Supported formats**: CSV (.csv), Excel (.xlsx, .xls)

### Sample Dataset Format

| Product | Price | Quality | Durability | Rating |
|---------|-------|---------|------------|--------|
| A       | 100   | 8.5     | 7.2        | 4.5    |
| B       | 150   | 9.0     | 8.5        | 4.8    |
| C       | 120   | 7.8     | 8.0        | 4.2    |

## How to Use

1. **Upload Dataset**: Select and upload your CSV or Excel file
2. **Configure TOPSIS**: 
   - Set weights for each criterion (positive decimal numbers)
   - Select impact type:
     - **Benefit (+)**: Higher values are better (e.g., Quality, Rating)
     - **Cost (-)**: Lower values are better (e.g., Price)
3. **Run Analysis**: Click "Run TOPSIS" to calculate results
4. **View Results**: See ranked alternatives with TOPSIS scores
5. **Download**: Get results as CSV file

## TOPSIS Algorithm

The application implements the standard TOPSIS algorithm:

1. **Normalization**: Vector normalization of criteria matrix
2. **Weighted Matrix**: Apply weights to normalized values
3. **Ideal Solutions**: Calculate ideal best and worst for each criterion
4. **Separation Distances**: Euclidean distance from ideal solutions
5. **TOPSIS Score**: Relative closeness to ideal solution
6. **Ranking**: Rank alternatives by score (higher = better)

## Troubleshooting

**Port already in use:**
```bash
uvicorn main:app --reload --port 8001
```

**Module not found:**
Make sure you've activated the virtual environment and installed requirements.

**File upload error:**
Check that your dataset meets all requirements listed above.

## Technology Stack

- **Backend**: FastAPI, Python 3.7+
- **Frontend**: Jinja2 Templates, HTML5, CSS3
- **Libraries**: pandas, numpy, uvicorn
- **File Support**: openpyxl (for Excel files)

## License

This project is provided as-is for educational and commercial use.