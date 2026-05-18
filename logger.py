import logging
 
logging.basicConfig(
    filename="sim_engineer.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
 
_logger = logging.getLogger("sim_engineer")
 
 
def log_api_call(mode: str, sim: str, track: str, provider: str, model: str) -> None:
    """Logs a successful API call — which provider and model was used."""
    _logger.info(
        f"mode={mode} | provider={provider} | model={model} | sim={sim} | track={track}"
    )
 
 
def log_error(context: str, detail: str) -> None:
    """Logs an error with a context label and exception detail."""
    _logger.error(f"{context} | {detail}")