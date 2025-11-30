#!/usr/bin/env python3
"""
Grammy Awards Dataset Server
Fetches Kaggle data via MLCroissant (Croissant ML framework) and serves as JSON
Dataset: https://www.kaggle.com/datasets/johnpendenque/grammy-winners-and-nominees-from-1965-to-2024
"""

from flask import Flask, jsonify
from flask_cors import CORS
import pandas as pd
import mlcroissant as mlc
import logging

app = Flask(__name__)
CORS(app)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Cache the dataset to avoid repeated API calls
GRAMMY_DF = None
CACHE_INITIALIZED = False

def fetch_grammy_data():
    """
    Fetch Grammy dataset via MLCroissant (Croissant JSON-LD format)
    Returns: pandas DataFrame with Grammy winners/nominees data
    """
    global GRAMMY_DF, CACHE_INITIALIZED
    
    if CACHE_INITIALIZED and GRAMMY_DF is not None:
        return GRAMMY_DF
    
    try:
        logger.info("Fetching Kaggle dataset via MLCroissant...")
        
        # Fetch the Croissant JSON-LD metadata
        croissant_dataset = mlc.Dataset(
            'https://www.kaggle.com/datasets/johnpendenque/grammy-winners-and-nominees-from-1965-to-2024/croissant/download'
        )
        
        # Get available record sets
        record_sets = croissant_dataset.metadata.record_sets
        logger.info(f"Found {len(record_sets)} record set(s): {[rs.name for rs in record_sets]}")
        
        if not record_sets:
            raise ValueError("No record sets found in Croissant dataset")
        
        # Fetch first record set as DataFrame
        GRAMMY_DF = pd.DataFrame(
            croissant_dataset.records(record_set=record_sets[0].uuid)
        )
        
        logger.info(f"Successfully loaded {len(GRAMMY_DF)} records")
        logger.info(f"Columns: {list(GRAMMY_DF.columns)}")
        
        CACHE_INITIALIZED = True
        return GRAMMY_DF
        
    except Exception as e:
        logger.error(f"Error fetching Grammy dataset: {str(e)}")
        raise

def process_grammy_data(df):
    """
    Process Grammy dataset for visualization
    Returns: dict with processed data for charts
    """
    try:
        # Normalize column names (lowercase, replace spaces)
        df.columns = df.columns.str.lower().str.strip()
        
        # Attempt to extract key columns (column names vary in dataset)
        year_col = next((col for col in df.columns if 'year' in col), None)
        winner_col = next((col for col in df.columns if 'name' in col or 'artist' in col or 'winner' in col), None)
        category_col = next((col for col in df.columns if 'category' in col), None)
        
        # Prepare polar chart data (top categories by count)
        if category_col:
            top_categories = df[category_col].value_counts().head(8)
            polar_data = {
                'labels': top_categories.index.tolist(),
                'data': top_categories.values.tolist()
            }
        else:
            polar_data = {'labels': [], 'data': []}
        
        # Prepare evolution chart data (wins over time)
        if year_col:
            evolution_by_year = df[year_col].value_counts().sort_index()
            evolution_data = {
                'labels': evolution_by_year.index.astype(str).tolist(),
                'data': evolution_by_year.values.tolist()
            }
        else:
            evolution_data = {'labels': [], 'data': []}
        
        # Scatter chart data (sample artists with varied stats)
        if winner_col and year_col:
            artist_stats = df.groupby(winner_col).agg({
                year_col: ['min', 'max', 'count']
            }).reset_index()
            artist_stats.columns = ['Artist', 'FirstWin', 'LatestWin', 'TotalNominations']
            artist_stats = artist_stats.sort_values('TotalNominations', ascending=False).head(15)
            
            scatter_data = {
                'labels': artist_stats['Artist'].tolist(),
                'datasets': [{
                    'label': 'First Win vs Total Nominations',
                    'data': [
                        {'x': int(row['FirstWin']), 'y': row['TotalNominations']}
                        for _, row in artist_stats.iterrows()
                    ]
                }]
            }
        else:
            scatter_data = {'labels': [], 'datasets': []}
        
        # Big 4 grammy categories (estimate)
        big_4_categories = ['Record Of The Year', 'Album Of The Year', 'Song Of The Year', 'Best New Artist']
        if category_col:
            big_4_data = df[df[category_col].isin(big_4_categories)][category_col].value_counts()
            big_4_chart = {
                'labels': big_4_data.index.tolist() or big_4_categories[:4],
                'data': big_4_data.values.tolist() or [0, 0, 0, 0]
            }
        else:
            big_4_chart = {'labels': big_4_categories, 'data': [0, 0, 0, 0]}
        
        return {
            'polar': polar_data,
            'evolution': evolution_data,
            'scatter': scatter_data,
            'big4': big_4_chart,
            'meta': {
                'total_records': len(df),
                'columns': list(df.columns),
                'year_range': f"{int(df[year_col].min())}-{int(df[year_col].max())}" if year_col else "Unknown"
            }
        }
        
    except Exception as e:
        logger.error(f"Error processing Grammy data: {str(e)}")
        return {
            'polar': {'labels': [], 'data': []},
            'evolution': {'labels': [], 'data': []},
            'scatter': {'labels': [], 'datasets': []},
            'big4': {'labels': [], 'data': []},
            'meta': {'error': str(e)}
        }

@app.route('/api/grammy', methods=['GET'])
def get_grammy_data():
    """
    Endpoint: GET /api/grammy
    Returns: JSON with Grammy dataset processed for visualizations
    """
    try:
        df = fetch_grammy_data()
        processed = process_grammy_data(df)
        return jsonify(processed), 200
    except Exception as e:
        logger.error(f"API error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'ok', 'service': 'grammy-server'}), 200

if __name__ == '__main__':
    logger.info("Starting Grammy Awards Dataset Server...")
    logger.info("Endpoint: http://localhost:5000/api/grammy")
    logger.info("Dataset: Kaggle Croissant - johnpendenque/grammy-winners-and-nominees-from-1965-to-2024")
    app.run(debug=True, port=5000)
