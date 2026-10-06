from enum import Enum
from dataclasses import dataclass
from pprint import pprint

class AllocStatus(Enum):
    SUCCESS = 0
    FAILURE = 1
    INSUFFICIENT_MEMORY = 2

@dataclass
class AllocResult:
    AllocStatus : AllocStatus
    block_ids : list[int]

class BlockManager:

    def __init__(self, block_size, num_blocks):

        self.block_size = block_size
        self.num_blocks = num_blocks
        self.st = list(range(num_blocks))
        self.block_table : dict[int, list[int]] = {}

    def allocate(self, seq_id, num_block_for_seq):

        total_num_blocks_available = self.check_num_block()

        print("check total num block available : ")
        print(total_num_blocks_available)

        if total_num_blocks_available < num_block_for_seq:
            print("\n inside print statement of if block \n")
            return AllocResult(AllocStatus.INSUFFICIENT_MEMORY, None)

        print("num block for seq")
        print(num_block_for_seq)
        for _ in range(num_block_for_seq):

            if seq_id in self.block_table:
                self.block_table[seq_id].append(self.st.pop())

            else:
                self.block_table[seq_id] = [self.st.pop()]

        return AllocResult(AllocStatus.SUCCESS, self.block_table[seq_id])


    def release_blocks(self, seq_id):
        """Function for releasing the blocks  when the scheduler asks for """

        for i in self.block_table[seq_id]:
            self.st.append(i)

        if(self.block_table[seq_id]):
            del self.block_table[seq_id]
        else:
            return AllocResult(AllocStatus.FAILURE, None)

        return AllocResult(AllocStatus.SUCCESS, None)


    def check_num_block(self) -> int:

        return len(self.st)

    def can_allocate(self, blocks) -> bool : 

        if(len(self.st) > 0):
            return True

        return False

    def print_stack(self):
        for i in self.st:
            print(i)

    def print_block_table(self):
        pprint(self.block_table)

def main():
    block_manager_obj = BlockManager(16, 50)
    print("print the stack after allocation \n")
    block_manager_obj.print_stack()
    print("lengtht of stack \n")
    num_blocks_available = block_manager_obj.check_num_block()
    print(num_blocks_available)
    print("calling allocate function \n ")
    block_manager_obj.allocate(1, 3)
    num_blocks_available = block_manager_obj.check_num_block()
    print(num_blocks_available)

    block_manager_obj.allocate(2, 35)
    num_blocks_available = block_manager_obj.check_num_block()
    print(num_blocks_available)


    print("print block table")
    block_manager_obj.print_block_table()


if __name__ == "__main__":
    main()