import pandas as pd
from sklearn.model_selection import train_test_split
from mlProject import logger
from mlProject.entity.config_entity import DataTransformationConfig


class data_transformation:
    def __init__(self, config: DataTransformationConfig):
        self.config = config
        self.data = pd.read_csv(self.config.data_path)


    def handle_missing_and_duplicates(self) -> pd.DataFrame:

        with open(self.config.STATUS_FILE , "r") as fh :
            report = fh.read()

#---Missing Values---

        missing_line = next(
            (line for line in report.splitlines() if line.startswith("Missing values by column:")),""
        )

        has_missing = "None" not in missing_line

        if has_missing:
            before_rows = len(self.data)
            self.data = self.data.dropna()
            dropped_rows = before_rows - len(self.data)
            logger.info(f"Dropped {dropped_rows} rows containing missing values")
            logger.info(f"Number of rows after handling missing values : {len(self.data)}")
        else:
            logger.info("No missing values found!")


#---Duplicate Values---

        dup_line = next(
        (line for line in report.splitlines() if line.startswith("Duplicate rows:")),
        "Duplicate rows: 0"
       )
        reported_duplicates = int(dup_line.split(":")[1].strip())

        if reported_duplicates > 0:
            before = len(self.data)
            self.data = self.data.drop_duplicates()
            after = len(self.data)
            logger.info(f"Dropped {before - after} duplicate rows!")
            logger.info(f"Final number of rows : {after}")

        else:
            logger.info("No duplicate rows found!")


        return self.data
    
    def train_test_splitting(self):
        """
        Stratified on binned quality so rare extreme-quality wines
        (e.g. quality < 3 or > 7) aren't left out of either split entirely.
        """
        bins = pd.cut(self.data["quality"], bins=[0, 4, 6, 10], labels=["low", "mid", "high"])
 
        train, test = train_test_split(
            self.data,
            test_size=0.2,
            random_state=42,
            stratify=bins,
        )
 
        train.to_csv(self.config.train_data_path, index=False)
        test.to_csv(self.config.test_data_path, index=False)
 
        logger.info(f"Train shape: {train.shape}")
        logger.info(f"Test shape: {test.shape}")
    
    
    def run_transformation(self):
        self.handle_missing_and_duplicates()
        self.train_test_splitting()


