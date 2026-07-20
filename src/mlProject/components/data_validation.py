import pandas as pd
from mlProject.entity.config_entity import DataValidationConfig
from mlProject import logger


class data_validation:
    def __init__(self, config: DataValidationConfig):
        self.config = config
        self.data = pd.read_csv(self.config.data_path)
        self.report_lines = []

    def validate_columns_present(self) -> bool:
        """Check every expected column exists (extra columns are also flagged)."""
        expected_cols = set(self.config.all_schema.keys())
        actual_cols = set(self.data.columns)

        missing_cols = expected_cols - actual_cols
        extra_cols = actual_cols - expected_cols

        if missing_cols:
            self.report_lines.append(f"Missing Columns: {missing_cols}")
        if extra_cols:
            self.report_lines.append(f"Extra Columns: {extra_cols}")

        status = len(missing_cols) == 0
        self.report_lines.append(f"Columns present check: {status}")
        return status

    def validate_column_types(self) -> bool:
        # Check datatype of each column
        status = True
        for col, expected_dtype in self.config.all_schema.items():
            if col not in self.data.columns:
                continue 
            actual_dtype = str(self.data[col].dtype)
            if actual_dtype != expected_dtype:
                self.report_lines.append(
                    f"DATATYPE MISMATCH - {col}: expected {expected_dtype}, got {actual_dtype}"
                )
                status = False
        self.report_lines.append(f"Columns datatype match status: {status}")
        return status

    def check_missing_values(self) -> dict:

        missing = self.data.isnull().sum()
        missing = missing[missing > 0].to_dict()
        self.report_lines.append(f"Missing values by column: {missing if missing else 'None'}")
        return missing

    def check_duplicate_rows(self) -> int:
        
        dup_count = int(self.data.duplicated().sum())
        self.report_lines.append(f"Duplicate rows: {dup_count}")
        return dup_count

    def run_validation(self) -> bool:
        """
        Orchestrates all checks. Schema checks (columns present, dtypes) gate the
        pipeline - if they fail, status is False and downstream stages should not run.
        # Missing values , duplicates are diagnostic 
        """
        cols_ok = self.validate_columns_present()
        types_ok = self.validate_column_types()
        self.check_missing_values()
        self.check_duplicate_rows()

        overall_status = cols_ok and types_ok

        with open(self.config.STATUS_FILE, "w") as f:
            f.write(f"Validation status: {overall_status}\n\n")
            f.write("\n".join(self.report_lines))

        # Pass data forward unchanged - validation diagnoses, it does not fix.
        if overall_status:
            self.data.to_csv(self.config.valid_data_path, index=False)

        return overall_status