import os
import json
import logging
from typing import Optional, List, Dict, Any
from langchain_core.tools import tool

logger = logging.getLogger(__name__)

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "outputs")
os.makedirs(OUTPUT_DIR, exist_ok=True)


class DataProcessor:
    @tool("clean_dataset")
    def clean_dataset(
        file_path: str,
        remove_duplicates: bool = True,
        fill_nulls_method: str = "mean",
        drop_columns: Optional[str] = None
    ) -> str:
        """
        Cleans a CSV dataset by removing duplicates, filling null values, and dropping columns.

        Args:
            file_path: Path to the CSV file
            remove_duplicates: Whether to remove duplicate rows (default: True)
            fill_nulls_method: Method to fill nulls - "mean", "median", "mode", "drop", or "none" (default: "mean")
            drop_columns: Comma-separated column names to drop (optional)

        Returns:
            JSON string with cleaning results
        """
        try:
            import pandas as pd
        except ImportError:
            return json.dumps({
                "success": False,
                "error": "pandas not installed. Run: pip install pandas"
            })

        try:
            if not os.path.exists(file_path):
                return json.dumps({
                    "success": False,
                    "error": f"File not found: {file_path}"
                })

            df = pd.read_csv(file_path)
            original_rows = len(df)
            original_cols = len(df.columns)

            if remove_duplicates:
                df = df.drop_duplicates()

            cols_to_drop = []
            if drop_columns:
                cols_to_drop = [c.strip() for c in drop_columns.split(",")]
                existing_cols = [c for c in cols_to_drop if c in df.columns]
                df = df.drop(columns=existing_cols)

            null_counts = df.isnull().sum().to_dict()
            null_total = sum(null_counts.values())

            if fill_nulls_method != "none" and null_total > 0:
                numeric_cols = df.select_dtypes(include=['number']).columns
                
                if fill_nulls_method == "mean":
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                elif fill_nulls_method == "median":
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())
                elif fill_nulls_method == "mode":
                    for col in numeric_cols:
                        df[col] = df[col].fillna(df[col].mode()[0] if not df[col].mode().empty else 0)
                elif fill_nulls_method == "drop":
                    df = df.dropna()

            output_filename = f"cleaned_{os.path.basename(file_path)}"
            output_path = os.path.join(OUTPUT_DIR, output_filename)
            df.to_csv(output_path, index=False)

            return json.dumps({
                "success": True,
                "original_rows": original_rows,
                "final_rows": len(df),
                "original_cols": original_cols,
                "final_cols": len(df.columns),
                "duplicates_removed": original_rows - len(df) if remove_duplicates else 0,
                "null_values_filled": null_total,
                "output_file": output_path,
                "preview": df.head(5).to_dict(orient="records")
            })

        except Exception as e:
            logger.error(f"Data cleaning failed: {e}")
            return json.dumps({
                "success": False,
                "error": str(e)
            })

    @tool("detect_outliers")
    def detect_outliers(
        file_path: str,
        columns: Optional[str] = None,
        method: str = "iqr",
        threshold: float = 1.5
    ) -> str:
        """
        Detects outliers in numeric columns using Z-score or IQR method.

        Args:
            file_path: Path to the CSV file
            columns: Comma-separated column names to check (optional - checks all numeric if not provided)
            method: "iqr" (Interquartile Range) or "zscore" (default: "iqr")
            threshold: Threshold for outlier detection (default: 1.5 for IQR, 3.0 for Z-score)

        Returns:
            JSON string with outlier detection results
        """
        try:
            import pandas as pd
            import numpy as np
        except ImportError:
            return json.dumps({
                "success": False,
                "error": "pandas not installed. Run: pip install pandas"
            })

        try:
            if not os.path.exists(file_path):
                return json.dumps({
                    "success": False,
                    "error": f"File not found: {file_path}"
                })

            df = pd.read_csv(file_path)

            if columns:
                cols_to_check = [c.strip() for c in columns.split(",")]
                cols_to_check = [c for c in cols_to_check if c in df.columns]
            else:
                cols_to_check = df.select_dtypes(include=['number']).columns.tolist()

            if not cols_to_check:
                return json.dumps({
                    "success": False,
                    "error": "No numeric columns found"
                })

            results = {}

            for col in cols_to_check:
                if method == "iqr":
                    Q1 = df[col].quantile(0.25)
                    Q3 = df[col].quantile(0.75)
                    IQR = Q3 - Q1
                    lower_bound = Q1 - threshold * IQR
                    upper_bound = Q3 + threshold * IQR
                    
                    outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)]
                    results[col] = {
                        "method": "iqr",
                        "threshold": threshold,
                        "lower_bound": float(lower_bound),
                        "upper_bound": float(upper_bound),
                        "outlier_count": len(outliers),
                        "outlier_percentage": round(len(outliers) / len(df) * 100, 2),
                        "outlier_values": outliers[col].tolist()[:10]
                    }
                else:
                    mean = df[col].mean()
                    std = df[col].std()
                    z_scores = np.abs((df[col] - mean) / std)
                    outliers = df[z_scores > threshold]
                    
                    results[col] = {
                        "method": "zscore",
                        "threshold": threshold,
                        "mean": float(mean),
                        "std": float(std),
                        "outlier_count": len(outliers),
                        "outlier_percentage": round(len(outliers) / len(df) * 100, 2),
                        "outlier_values": outliers[col].tolist()[:10]
                    }

            return json.dumps({
                "success": True,
                "method": method,
                "columns_analyzed": cols_to_check,
                "results": results
            })

        except Exception as e:
            logger.error(f"Outlier detection failed: {e}")
            return json.dumps({
                "success": False,
                "error": str(e)
            })

    @tool("generate_statistics")
    def generate_statistics(file_path: str) -> str:
        """
        Generates descriptive statistics for a CSV file.

        Args:
            file_path: Path to the CSV file

        Returns:
            JSON string with descriptive statistics
        """
        try:
            import pandas as pd
        except ImportError:
            return json.dumps({
                "success": False,
                "error": "pandas not installed"
            })

        try:
            df = pd.read_csv(file_path)
            
            stats = {
                "success": True,
                "file": os.path.basename(file_path),
                "shape": {"rows": len(df), "columns": len(df.columns)},
                "columns": list(df.columns),
                "dtypes": df.dtypes.apply(str).to_dict(),
                "missing_values": df.isnull().sum().to_dict(),
                "numeric_summary": df.describe().to_dict() if len(df.select_dtypes(include=['number']).columns) > 0 else {},
                "categorical_summary": {}
            }

            cat_cols = df.select_dtypes(include=['object']).columns
            for col in cat_cols:
                stats["categorical_summary"][col] = {
                    "unique_values": df[col].nunique(),
                    "top_values": df[col].value_counts().head(5).to_dict()
                }

            return json.dumps(stats, default=str)

        except Exception as e:
            logger.error(f"Statistics generation failed: {e}")
            return json.dumps({
                "success": False,
                "error": str(e)
            })


data_processor_tools = [
    DataProcessor.clean_dataset,
    DataProcessor.detect_outliers,
    DataProcessor.generate_statistics
]
