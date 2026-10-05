from block_manager import BlockManager
from sequence import Sequence
from dataclasses import dataclass


@dataclass
class scheduler_output:
    prefill_seqs : list[Sequence]
    decode_seqs : list[Sequence]
    finished_seqs : list[Sequence]

