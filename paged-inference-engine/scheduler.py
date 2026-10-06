from block_manager import BlockManager
from sequence import Sequence
from dataclasses import dataclass
import math

@dataclass
class Scheduler_Output:
    prefill_seqs : list[Sequence]
    decode_seqs : list[Sequence]
    finished_seqs : list[Sequence]


# main scheduler  class
class Scheduler():

    def __init__(self, block_manager : BlockManager, block_size, max_len, skip_threshold, lookahead_window):

        self.block_manager = block_manager
        self.block_size = block_size
        self.max_len = max_len
        self.skip_threshold = skip_threshold
        self.lookahead_window = lookahead_window

        self.running_seqs = []
        self.waiting_seqs = []
        self.skip_counts = {}
        self.finished_seqs = []
        print("Initialized  scheduler object \n")



    # we need total of 4 steps to be done 
    # 1. firstly check the finished sequences
    # 2. allocate the pending decode sequences
    # 3. admit the new waiting sequences
    # 4. fially return the scheduler output at every time step


    def add_request(self, seq: Sequence):
        print("Adding add_request \n")
        self.waiting_seqs.append(seq)

    def schedule(self):
        print("calling  free finished seq \n")
        self._free_finished_seq()
        print("calling  allocate decode seq \n")
        self._allocate_decode()
        print("calling  admit waiting seq \n")
        self._admit_waiting_seq()
        print("calling return statement for the seq \n")
        return self.build_scheduler_output()

    def _free_finished_seq(self):

        running_seqs_cpy = self.running_seqs.copy()

        for sequence in running_seqs_cpy:
            if sequence.is_finished or len(sequence.token_ids) >= sequence.max_token_to_generate_for_this_sequence + sequence.prompt_token_ids or len(sequence.token_ids) > self.max_len:
                sequence.is_finished = True
                self.finished_seqs.append(sequence)
                self.block_manager.release_blocks(sequence.seq_id)
                self.running_seqs.remove(sequence)


    def _allocate_decode(self):

        for sequence in self.running_seqs:

            blocks_assigned = len(self.block_manager.block_table[sequence.seq_id])
            blocks_required =  math.ceil(len(sequence.token_ids) + 1 / self.block_size)

            if blocks_required > blocks_assigned:
                if self.block_manager.can_allocate(blocks_required - blocks_assigned):
                    self.block_manager.allocate(sequence.seq_id, blocks_required - blocks_assigned)

    def _admit_waiting_seq(self):

        # I will apply loose fcfs. 

        front_sequence = self.waiting_seqs[0]
        print("front_sequence.seq_id ", front_sequence.seq_id)
        print("front_sequence.prompt_token_ids ", len(front_sequence.prompt_token_ids))

        if self.skip_counts.get(front_sequence.seq_id, 0) >= self.skip_threshold:
            blocks_required = len(front_sequence.prompt_token_ids) / self.block_size
            print("\n blocks required", blocks_required)
            if self.block_manager.can_allocate(blocks_required):
                    self.block_manager.allocate(seq_id=sequence.seq_id, num_block_for_seq=blocks_required)
                    self.running_seqs.append(sequence)
                    del self.skip_counts[sequence.seq_id]
                    self.waiting_seqs.remove(sequence)
            return

        else:
            for sequence in self.waiting_seqs[:self.lookahead_window]:
                blocks_required = len(sequence.prompt_token_ids) // self.block_size
                print("\n blocks required : ", blocks_required)
                if self.block_manager.can_allocate(blocks_required):
                    self.block_manager.allocate(seq_id=sequence.seq_id, num_block_for_seq=blocks_required)
                    self.running_seqs.append(sequence)
                    del self.skip_counts[sequence.seq_id]
                    self.waiting_seqs.remove(sequence)
                else:
                    current_skip_count = self.skip_counts.get(sequence.seq_id, 0)
                    self.skip_counts[sequence.seq_id] = current_skip_count + 1

    def build_scheduler_output(self):

        prefill_seqs = []
        decode_seqs = []

        # we simply check if the current sequence is prefill or decode by just identifying the length of the entire sequence tokens so far.
        # if the tokens so far is same as the initial length of prompt token ids then it's prefill and even if it's just increased by 1, it's decode

        for sequence in self.running_seqs:

            if len(sequence.prompt_token_ids) == len(sequence.seq_id):
                prefill_seqs.append(sequence)
            elif (len(sequence.prompt_token_ids) > len(sequence.seq_id)):
                decode_seqs.append(sequence)

        return Scheduler_Output(prefill_seqs=prefill_seqs, decode_seqs=decode_seqs, finished_seqs=self.finished_seqs)