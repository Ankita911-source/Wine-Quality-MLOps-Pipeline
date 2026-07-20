from mlProject.config.configuration import ConfigurationManager
from mlProject.components.data_validation import data_validation
from mlProject import logger

STAGE_NAME = "Data validation Stage"

class DataValidationTrainingPipeline:
    def __init__(self):
        pass

    def main(self):
        config = ConfigurationManager()
        data_validation_config = config.get_data_validation_config()
        data_validation_obj = data_validation(config=data_validation_config)
        data_validation_obj.run_validation()


if __name__ == "__main__":
    try:
        logger.info(f">>>>> stage {STAGE_NAME} started <<<<<")
        obj = DataValidationTrainingPipeline()
        obj.main()
        logger.info(f">>>>> stage {STAGE_NAME} completed!<<<<<\n\nx==========x")
    except Exception as e:
        logger.exception(e)
        raise e

        
