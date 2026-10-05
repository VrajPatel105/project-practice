from scheduler import Scheduler
from block_manager import BlockManager
from sequence import Sequence
from config import config

block_manager_obj = BlockManager(block_size=config['block_size'], num_blocks=config['num_blocks'])

scheduler_obj = Scheduler(block_manager=block_manager_obj, block_size=config['block_size'], max_len=config['max_len'], skip_threshold=config['skip_threshold'], lookahead_window=config['lookahead_window'])

def run():
    prompt_token_ids_vec = [1,2,3,4,5,6,7,8,9]

    sequence_obj_1 = Sequence(seq_id=1, prompt_token_ids=prompt_token_ids_vec, max_token_to_generate_for_this_sequence=60)

    result = scheduler_obj.add_request(sequence_obj_1)

    return result

def print_sequences(sequences):
    for seq in sequences:
        print(
            f"Sequence("
            f"seq_id={seq.seq_id}, "
            f"prompt_token_ids={seq.prompt_token_ids}, "
            f"max_token_to_generate_for_this_sequence="
            f"{seq.max_token_to_generate_for_this_sequence}, "
            f"token_ids={seq.token_ids}, "
            f"is_finished={seq.is_finished}"
            f")"
        )

def main():

    result = run()
    print_sequences(result)