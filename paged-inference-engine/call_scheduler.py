from scheduler import Scheduler
from block_manager import BlockManager
from config import config

BlockManager(block_size=config['block_size'], num_blocks=config['num_blocks'])
