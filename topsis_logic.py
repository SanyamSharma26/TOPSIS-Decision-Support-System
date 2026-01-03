import pandas as pd
import numpy as np
from typing import List


class TopsisError(Exception):
    """Custom exception for TOPSIS-related errors"""
    pass


def run_topsis(df: pd.DataFrame, weights: List[float], impacts: List[str]) -> pd.DataFrame:
    """
    Run TOPSIS algorithm on the given dataframe
    
    Parameters:
    -----------
    df : pd.DataFrame
        DataFrame with first column as ID/Alternative and remaining as criteria
    weights : List[float]
        List of weights for each criterion (must be positive)
    impacts : List[str]
        List of impacts ('+' for benefit, '-' for cost) for each criterion
    
    Returns:
    --------
    pd.DataFrame
        Original dataframe with added 'TOPSIS Score' and 'Rank' columns
    """
    
    # Extract ID column and criteria columns
    id_col = df.columns[0]
    criteria_cols = df.columns[1:]
    
    # Validate inputs
    if len(weights) != len(criteria_cols):
        raise TopsisError(f"Number of weights ({len(weights)}) must match number of criteria columns ({len(criteria_cols)})")
    
    if len(impacts) != len(criteria_cols):
        raise TopsisError(f"Number of impacts ({len(impacts)}) must match number of criteria columns ({len(criteria_cols)})")
    
    # Extract criteria matrix
    criteria_matrix = df[criteria_cols].values
    
    # Step 1: Vector Normalization
    # For each column j: norm_ij = x_ij / sqrt(sum_i x_ij^2)
    normalized_matrix = np.zeros_like(criteria_matrix, dtype=float)
    
    for j in range(criteria_matrix.shape[1]):
        column = criteria_matrix[:, j]
        sum_of_squares = np.sum(column ** 2)
        
        if sum_of_squares == 0:
            raise TopsisError(f"Column '{criteria_cols[j]}' has all zeros, cannot normalize")
        
        normalized_matrix[:, j] = column / np.sqrt(sum_of_squares)
    
    # Step 2: Weighted Normalized Matrix
    # v_ij = norm_ij * w_j
    weights_array = np.array(weights)
    weighted_matrix = normalized_matrix * weights_array
    
    # Step 3: Determine Ideal Best and Ideal Worst
    ideal_best = np.zeros(len(criteria_cols))
    ideal_worst = np.zeros(len(criteria_cols))
    
    for j, impact in enumerate(impacts):
        if impact == '+':
            # Benefit: best is maximum, worst is minimum
            ideal_best[j] = np.max(weighted_matrix[:, j])
            ideal_worst[j] = np.min(weighted_matrix[:, j])
        elif impact == '-':
            # Cost: best is minimum, worst is maximum
            ideal_best[j] = np.min(weighted_matrix[:, j])
            ideal_worst[j] = np.max(weighted_matrix[:, j])
        else:
            raise TopsisError(f"Invalid impact value '{impact}'. Must be '+' or '-'")
    
    # Step 4: Calculate Separation Distances
    # S+ = sqrt(sum_j (v_ij - ideal_best_j)^2)
    # S- = sqrt(sum_j (v_ij - ideal_worst_j)^2)
    
    s_plus = np.sqrt(np.sum((weighted_matrix - ideal_best) ** 2, axis=1))
    s_minus = np.sqrt(np.sum((weighted_matrix - ideal_worst) ** 2, axis=1))
    
    # Step 5: Calculate TOPSIS Score
    # score_i = S- / (S+ + S-)
    # Handle division by zero
    denominator = s_plus + s_minus
    
    if np.any(denominator == 0):
        raise TopsisError("Division by zero encountered in TOPSIS score calculation")
    
    topsis_scores = s_minus / denominator
    
    # Step 6: Rank alternatives
    # Higher score = better; Rank 1 = highest score
    ranks = pd.Series(topsis_scores).rank(ascending=False, method='min').astype(int)
    
    # Add TOPSIS Score and Rank to dataframe
    df['TOPSIS Score'] = topsis_scores
    df['Rank'] = ranks
    
    # Sort by Rank for better readability
    df = df.sort_values('Rank')
    
    return df