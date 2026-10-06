""" sequence file that defines the class for Sequence object"""


class Sequence:

    def __init__(self, seq_id, prompt_token_ids, max_token_to_generate_for_this_sequence):

        self.seq_id = seq_id
        self.prompt_token_ids = prompt_token_ids
        self.max_token_to_generate_for_this_sequence = max_token_to_generate_for_this_sequence
        self.token_ids = list(prompt_token_ids)
        self.is_finished = False 

    def __repr__(self):
        return (
            f"Sequence("
            f"seq_id={self.seq_id}, "
            f"prompt_token_ids={self.prompt_token_ids}, "
            f"max_tokens={self.max_token_to_generate_for_this_sequence}, "
            f"token_ids={self.token_ids}, "
            f"is_finished={self.is_finished}"
            f")"
        )