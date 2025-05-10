import logging

def init_logger(log_file='app.log', log_level=logging.DEBUG):
   
    logging.basicConfig(
        filename=log_file,  
        filemode='a',      
        format='%(asctime)s - %(levelname)s - %(message)s',
        level=log_level
    )

    
    logger = logging.getLogger()

  
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger
