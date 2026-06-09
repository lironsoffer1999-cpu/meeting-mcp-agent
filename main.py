import logging
import time
from scheduler import AgentScheduler

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    """
    Main entry point for the Meeting MCP Agent.
    Initializes the scheduler and starts the 15-minute polling loop.
    """
    logger.info("Starting Meeting MCP Agent...")
    
    try:
        scheduler = AgentScheduler()
        scheduler.start()
        
        # Keep the main thread alive
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        logger.info("Agent stopped by user.")
    except Exception as e:
        logger.error(f"Critical error in main loop: {e}")

if __name__ == "__main__":
    main()
