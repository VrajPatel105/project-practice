from scheduler import Scheduler
from block_manager import BlockManager
from sequence import Sequence
from scheduler import Scheduler_Output
from config import config

block_manager_obj = BlockManager(block_size=config['block_size'], num_blocks=config['num_blocks'])

scheduler_obj = Scheduler(block_manager=block_manager_obj, block_size=config['block_size'], max_len=config['max_len'], skip_threshold=config['skip_threshold'], lookahead_window=config['lookahead_window'])

def run():

    prompt_token_ids_vec = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
    sequence_obj_1 = Sequence(seq_id=1, prompt_token_ids=prompt_token_ids_vec, max_token_to_generate_for_this_sequence=60)


    prompt_token_ids_vec = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
    sequence_obj_2 = Sequence(seq_id=2, prompt_token_ids=prompt_token_ids_vec, max_token_to_generate_for_this_sequence=90)

    scheduler_obj.add_request(sequence_obj_1)
    scheduler_obj.add_request(sequence_obj_2)

    result = scheduler_obj.schedule()

    return result

def print_scheduler_output(output: Scheduler_Output):
    for name in ("prefill_seqs", "decode_seqs", "finished_seqs"):
        print(f"\n=== {name} ===")
        for seq in getattr(output, name):
            print(seq)


def main():

    result = run()
    if result:
        print("yes, result do exist")
    else:
        print("nope, it does not exist")
    print_scheduler_output(result)
if __name__ == "__main__":
    main()