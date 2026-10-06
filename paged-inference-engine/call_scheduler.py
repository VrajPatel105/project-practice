from scheduler import Scheduler
from block_manager import BlockManager
from sequence import Sequence
from scheduler import Scheduler_Output
from config import config

block_manager_obj = BlockManager(block_size=config['block_size'], num_blocks=config['num_blocks'])

scheduler_obj = Scheduler(block_manager=block_manager_obj, block_size=config['block_size'], max_len=config['max_len'], skip_threshold=config['skip_threshold'], lookahead_window=config['lookahead_window'])

def run():
    prompt_token_ids_vec = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]

    sequence_obj_1 = Sequence(seq_id=1, prompt_token_ids=prompt_token_ids_vec, max_token_to_generate_for_this_sequence=60)

    scheduler_obj.add_request(sequence_obj_1)

    result = scheduler_obj.schedule()

    return result

def print_scheduler_output(scheduler_output: Scheduler_Output):
    print("=== Prefill Sequences ===")
    for seq in scheduler_output.prefill_seqs:
        print(seq)

    # print("\n=== Decode Sequences ===")
    # for seq in scheduler_output.decode_seqs:
    #     print(seq)

    # print("\n=== Finished Sequences ===")
    # for seq in scheduler_output.finished_seqs:
    #     print(seq)

def main():

    result = run()
    if result:
        print("yes, result do exist")
    else:
        print("nope, it does not exist")
    print_scheduler_output(result)

if __name__ == "__main__":
    main()