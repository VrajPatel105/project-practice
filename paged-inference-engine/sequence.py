""" sequence file that defines the class for Sequence object"""


class Sequence:

    def __init__(self, seq_id, prompt_token_ids, max_token_to_generate_for_this_sequence):

        self.seq_id = seq_id
        self.prompt_token_ids = prompt_token_ids
        self.max_token_to_generate_for_this_sequence = max_token_to_generate_for_this_sequence
        self.token_ids = len(prompt_token_ids)
        self.is_finished = False 
