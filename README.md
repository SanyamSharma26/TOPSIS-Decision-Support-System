# TOPSIS Decision Support System

A complete web application for Multi-Criteria Decision Making using the TOPSIS (Technique for Order of Preference by Similarity to Ideal Solution) algorithm.

[![Python](https://img.shields.io/badge/Python-3.11%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 🎯 Features

- ✅ Upload datasets in CSV or Excel format (.csv, .xlsx, .xls)
- ✅ Configure weights and impacts for each criterion
- ✅ Automated TOPSIS calculation with ranking
- ✅ Identify the best alternative (Rank 1)
- ✅ Download results as CSV
- ✅ Modern, responsive UI
- ✅ Session-based analysis (no registration required)
- ✅ Health check endpoint for monitoring

## 📸 Screenshots

### Landing Page
![Landing Page](screenshots/1-landing-page.png)
*Upload your dataset to get started*

### Configuration Page
![Configuration](screenshots/2-configure-page.png)
*Set weights and impacts for each criterion*

### Results Page
![Results](screenshots/3-results-page.png)
*View ranked alternatives with TOPSIS scores*

## 🚀 Live Demo

**Deployed at:** [https://topsis-decision-support-system.onrender.com](https://topsis-decision-support-system.onrender.com)

Try it out with the included sample datasets!

## 📁 Project Structure

```
topsis_app/
├── main.py                 # FastAPI application (main entry point)
├── topsis_logic.py         # TOPSIS algorithm implementation
├── requirements.txt        # Python dependencies
├── render.yaml             # Render deployment configuration
├── .gitignore             # Git ignore rules
├── config.py              # Configuration settings
├── templates/
│   ├── index.html         # Landing page with file upload
│   ├── configure.html     # Configuration page
│   └── result.html        # Results display page
├── static/
│   └── style.css          # Application styles
├── screenshots/           # App screenshots (for README)
├── sample_data.csv        # Sample dataset (CSV format)
└── sample_data.xlsx       # Sample dataset (Excel format)
```

## 🛠️ Installation & Setup

### Prerequisites

- Python 3.11 or higher
- pip (Python package manager)
- Git

### 1. Clone Repository

```bash
git clone https://github.com/SanyamSharma26/TOPSIS-Decision-Support-System.git
cd TOPSIS-Decision-Support-System
```

### 2. Create Virtual Environment

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

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Application

```bash
uvicorn main:app --reload
```

### 5. Access the Application

Open your browser and navigate to:
```
http://127.0.0.1:8000
```

## 📊 Dataset Requirements

Your dataset must meet the following criteria:

| Requirement | Description |
|------------|-------------|
| **Minimum Columns** | At least 3 columns (1 ID + 2 criteria) |
| **First Column** | ID/Alternative name (text or numbers) |
| **Criteria Columns** | Must be numeric (integers or floats) |
| **Missing Values** | Not allowed in criteria columns |
| **File Formats** | CSV (.csv), Excel (.xlsx, .xls) |

### Sample Dataset Format

| Product | Price | Quality | Durability | Rating |
|---------|-------|---------|------------|--------|
| Laptop A | 45000 | 8.5 | 7.2 | 4.5 |
| Laptop B | 55000 | 9.0 | 8.5 | 4.8 |
| Laptop C | 35000 | 7.8 | 8.0 | 4.2 |
| Laptop D | 48000 | 8.8 | 7.8 | 4.6 |

**Sample datasets are included in the repository:**
- `sample_data.csv` - 7 laptop alternatives with 5 criteria
- `sample_data.xlsx` - Same data in Excel format

## 📖 How to Use

### Step 1: Upload Dataset
1. Click "Choose File" on the landing page
2. Select your CSV or Excel file
3. Click "Upload Dataset"

### Step 2: Configure TOPSIS
For each criterion, specify:

- **Weight** (decimal number > 0)
  - Higher weight = More important criterion
  - Examples: 1.0, 2.5, 3.0
  
- **Impact** (+ or -)
  - **Benefit (+)**: Higher values are better
    - Examples: Quality, Rating, Performance, Durability
  - **Cost (-)**: Lower values are better
    - Examples: Price, Cost, Time, Defects

#### Example Configuration (for laptops):
- **Price**: Weight = 1.0, Impact = - (lower is better)
- **Quality**: Weight = 2.5, Impact = + (higher is better)
- **Durability**: Weight = 2.0, Impact = + (higher is better)
- **Customer Rating**: Weight = 3.0, Impact = + (higher is better)
- **Warranty**: Weight = 1.5, Impact = + (higher is better)

### Step 3: Run Analysis
Click "Run TOPSIS" to calculate results

### Step 4: View Results
- See the **best option** highlighted (Rank 1)
- View complete ranked table with TOPSIS scores
- All alternatives sorted by rank

### Step 5: Download Results
Click "Download Result CSV" to save results to your computer

## 🧮 TOPSIS Algorithm

The application implements the standard TOPSIS algorithm with the following steps:

### 1. Vector Normalization
Normalize criteria matrix using vector normalization:
```
norm_ij = x_ij / sqrt(sum(x_ij²))
```

### 2. Weighted Normalized Matrix
Apply weights to normalized values:
```
v_ij = norm_ij × weight_j
```

### 3. Ideal Solutions
Determine ideal best and ideal worst:
- **Benefit criteria**: Best = max, Worst = min
- **Cost criteria**: Best = min, Worst = max

### 4. Separation Distances
Calculate Euclidean distances:
- **S+**: Distance from ideal best
- **S-**: Distance from ideal worst

### 5. TOPSIS Score
Calculate relative closeness:
```
TOPSIS Score = S- / (S+ + S-)
```

### 6. Ranking
Rank alternatives by TOPSIS score (higher = better)

## 🔧 Troubleshooting

### Port Already in Use
```bash
uvicorn main:app --reload --port 8001
```

### Module Not Found Error
Make sure you've activated the virtual environment:
```bash
source venv/Scripts/activate  # Git Bash
venv\Scripts\activate         # Windows CMD
```
Then reinstall:
```bash
pip install -r requirements.txt
```

### File Upload Error
Check that your dataset meets all requirements:
- At least 3 columns
- First column is ID
- Other columns are numeric
- No missing values

### Static Files Not Loading
Hard refresh your browser:
- **Windows**: Ctrl + F5
- **Mac**: Cmd + Shift + R

## 💻 Technology Stack

| Component | Technology |
|-----------|-----------|
| **Backend Framework** | FastAPI 0.104.1 |
| **Server** | Uvicorn 0.24.0 |
| **Templating** | Jinja2 3.1.2 |
| **Data Processing** | pandas 2.1.3, NumPy 1.26.2 |
| **File Handling** | openpyxl 3.1.2 (Excel support) |
| **Language** | Python 3.11+ |
| **Frontend** | HTML5, CSS3 (Vanilla) |
| **Deployment** | Render.com |

## 🚀 Deployment

This application is deployed on [Render](https://render.com) with automatic deployments from the `main` branch.

### Deploy Your Own Instance

1. **Fork this repository**
2. **Sign up on [Render](https://render.com)** (free)
3. **Create a new Web Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Render auto-detects configuration from `render.yaml`
4. **Click "Create Web Service"**
5. **Wait 3-5 minutes** for deployment
6. **Your app is live!** 🎉

### Configuration

All deployment settings are in `render.yaml`:
- Python version: 3.11.0
- Region: Singapore (best for India)
- Build command: `pip install -r requirements.txt`
- Start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

### Environment Variables

Optional environment variables:
- `DEBUG`: Set to `false` for production
- `MAX_FILE_SIZE`: Maximum upload size in bytes (default: 10MB)

## 📊 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Landing page with file upload |
| `/upload` | POST | Upload and validate dataset |
| `/run` | POST | Run TOPSIS analysis |
| `/download` | GET | Download results as CSV |
| `/health` | GET | Health check endpoint |
| `/docs` | GET | Auto-generated API documentation |

## 🧪 Testing

### Run with Sample Data

1. Start the application
2. Upload `sample_data.csv`
3. Use these weights and impacts:
   - Price: 1.0, -
   - Quality: 2.5, +
   - Durability: 2.0, +
   - Customer Rating: 3.0, +
   - Warranty: 1.5, +
4. Expected result: **Laptop B** ranked #1

### Create Your Own Dataset

Use this format:
```csv
Alternative,Criterion1,Criterion2,Criterion3
Option A,100,8.5,7
Option B,150,9.0,8
Option C,120,7.5,9
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### Guidelines
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is provided as-is for educational and commercial use.

## 👨‍💻 Author

**Sanyam Sharma**
- GitHub: [@SanyamSharma26](https://github.com/SanyamSharma26)
- Project: [TOPSIS Decision Support System](https://github.com/SanyamSharma26/TOPSIS-Decision-Support-System)

## 🙏 Acknowledgments

- TOPSIS algorithm based on the paper by Hwang and Yoon (1981)
- Built with [FastAPI](https://fastapi.tiangolo.com/)
- Deployed on [Render](https://render.com)
- UI design inspired by modern web applications

## 📚 References

1. Hwang, C.L.; Yoon, K. (1981). *Multiple Attribute Decision Making: Methods and Applications*. New York: Springer-Verlag.
2. FastAPI Documentation: https://fastapi.tiangolo.com/
3. TOPSIS Method: https://en.wikipedia.org/wiki/TOPSIS

## 🔗 Links

- **Live Demo**: https://topsis-decision-support-system.onrender.com
- **GitHub Repository**: https://github.com/SanyamSharma26/TOPSIS-Decision-Support-System
- **Issue Tracker**: https://github.com/SanyamSharma26/TOPSIS-Decision-Support-System/issues

---

<div align="center">

⭐ **Star this repository if you found it helpful!** ⭐

Made with ❤️ by Sanyam Sharma

</div>
