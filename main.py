from fastapi import FastAPI, UploadFile, File, Form, Request
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import pandas as pd
import uuid
import io
from typing import Dict
from topsis_logic import run_topsis, TopsisError

app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Setup templates
templates = Jinja2Templates(directory="templates")

# In-memory storage
DATASTORE: Dict[str, pd.DataFrame] = {}
RESULTSTORE: Dict[str, bytes] = {}


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """Landing page with file upload form"""
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/upload", response_class=HTMLResponse)
async def upload_file(request: Request, dataset: UploadFile = File(...)):
    """Handle file upload and validate dataset"""
    try:
        # Validate file extension
        filename = dataset.filename.lower()
        if not (filename.endswith('.csv') or filename.endswith('.xlsx') or filename.endswith('.xls')):
            raise TopsisError("Invalid file format. Please upload a CSV or Excel file (.csv, .xlsx, .xls)")
        
        # Read file into DataFrame
        content = await dataset.read()
        
        if filename.endswith('.csv'):
            df = pd.read_csv(io.BytesIO(content))
        else:
            df = pd.read_excel(io.BytesIO(content))
        
        # Strip column names
        df.columns = df.columns.str.strip()
        
        # Validate dataset
        if len(df.columns) < 3:
            raise TopsisError("Dataset must have at least 3 columns (1 ID column + at least 2 criteria columns)")
        
        # First column is ID/Alternative name
        id_col = df.columns[0]
        criteria_cols = df.columns[1:]
        
        if len(criteria_cols) < 2:
            raise TopsisError("Dataset must have at least 2 criteria columns")
        
        # Check if criteria columns are numeric
        for col in criteria_cols:
            if not pd.api.types.is_numeric_dtype(df[col]):
                raise TopsisError(f"Column '{col}' must be numeric. All criteria columns must contain numeric values.")
        
        # Check for missing values in criteria columns
        if df[criteria_cols].isnull().any().any():
            raise TopsisError("Missing values detected in criteria columns. Please ensure all criteria columns have complete data.")
        
        # Generate token and store dataframe
        token = str(uuid.uuid4())
        DATASTORE[token] = df
        
        # Prepare criteria information for configuration page
        criteria_info = []
        for col in criteria_cols:
            criteria_info.append({
                'name': col,
                'index': list(df.columns).index(col)
            })
        
        return templates.TemplateResponse("configure.html", {
            "request": request,
            "token": token,
            "criteria": criteria_info,
            "num_alternatives": len(df)
        })
    
    except TopsisError as e:
        return templates.TemplateResponse("index.html", {
            "request": request,
            "error": str(e)
        })
    except Exception as e:
        return templates.TemplateResponse("index.html", {
            "request": request,
            "error": f"Error processing file: {str(e)}"
        })


@app.post("/run", response_class=HTMLResponse)
async def run_topsis_analysis(request: Request):
    """Run TOPSIS analysis with user-provided weights and impacts"""
    try:
        # Get form data
        form_data = await request.form()
        token = form_data.get('token')
        
        if not token or token not in DATASTORE:
            raise TopsisError("Invalid session. Please upload your dataset again.")
        
        df = DATASTORE[token]
        criteria_cols = df.columns[1:]
        
        # Extract weights and impacts
        weights = []
        impacts = []
        
        for i, col in enumerate(criteria_cols):
            # Get weight
            weight_key = f'weight_{i}'
            weight_value = form_data.get(weight_key)
            
            if not weight_value:
                raise TopsisError(f"Weight for '{col}' is required")
            
            try:
                weight = float(weight_value)
                if weight <= 0:
                    raise ValueError()
                weights.append(weight)
            except ValueError:
                raise TopsisError(f"Weight for '{col}' must be a positive number")
            
            # Get impact
            impact_key = f'impact_{i}'
            impact_value = form_data.get(impact_key)
            
            if impact_value not in ['+', '-']:
                raise TopsisError(f"Impact for '{col}' must be either '+' (Benefit) or '-' (Cost)")
            
            impacts.append(impact_value)
        
        # Run TOPSIS
        result_df = run_topsis(df.copy(), weights, impacts)
        
        # Save result to CSV bytes
        csv_buffer = io.BytesIO()
        result_df.to_csv(csv_buffer, index=False)
        csv_bytes = csv_buffer.getvalue()
        RESULTSTORE[token] = csv_bytes
        
        # Find best alternative (Rank = 1)
        best_row = result_df[result_df['Rank'] == 1].iloc[0]
        best_id = best_row[df.columns[0]]
        
        # Prepare table preview (first 100 rows)
        preview_df = result_df.head(100)
        
        return templates.TemplateResponse("result.html", {
            "request": request,
            "token": token,
            "num_alternatives": len(result_df),
            "best_id": best_id,
            "table_html": preview_df.to_html(classes='result-table', index=False, float_format='%.6f'),
            "total_rows": len(result_df),
            "showing_rows": len(preview_df)
        })
    
    except TopsisError as e:
        # If error occurs, try to re-render configure page with error
        if token and token in DATASTORE:
            df = DATASTORE[token]
            criteria_cols = df.columns[1:]
            criteria_info = []
            for col in criteria_cols:
                criteria_info.append({
                    'name': col,
                    'index': list(df.columns).index(col)
                })
            
            return templates.TemplateResponse("configure.html", {
                "request": request,
                "token": token,
                "criteria": criteria_info,
                "num_alternatives": len(df),
                "error": str(e)
            })
        else:
            return templates.TemplateResponse("index.html", {
                "request": request,
                "error": str(e)
            })
    except Exception as e:
        return templates.TemplateResponse("index.html", {
            "request": request,
            "error": f"Error running TOPSIS: {str(e)}"
        })


@app.get("/download")
async def download_result(token: str):
    """Download TOPSIS result as CSV"""
    if token not in RESULTSTORE:
        return {"error": "Result not found. Please run TOPSIS analysis first."}
    
    csv_bytes = RESULTSTORE[token]
    
    return StreamingResponse(
        io.BytesIO(csv_bytes),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=topsis_result.csv"}
    )