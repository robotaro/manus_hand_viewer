import logging


def get_logger(project_logger_name="project_logger"):
    logger = logging.getLogger(project_logger_name)
    logger.setLevel(logging.DEBUG)  # Set the desired logging level for your project

    # Check if the logger already has any handlers
    if not logger.handlers:
        # Create and configure your desired logging handler and formatter here
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(formatter)

        logger.addHandler(console_handler)

    return logger