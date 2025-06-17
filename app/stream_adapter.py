class StreamAdapter:
    def __init__(self, chunk_size):
        self.last_added = 2
        self.chunk_size = chunk_size
    def GetStreamChunks(self, list_of_nums):
        """
        Expands the input list of numbers up to length 12 by adding alternating 1s and 2s.
        If the last number is 1,it adds 2 to the next list.

        :param list_of_nums: (list of int) The original list of numbers.

        :return: list[list[int]] - List of 12-length number chunks
        """
        i = 0
        while i < len(list_of_nums) - 2:
            if list_of_nums[i] == list_of_nums[i + 1] == list_of_nums[i + 2] == 5:
                list_of_nums[i] = list_of_nums[i + 1] = list_of_nums[i + 2] = 6
                i += 3
            else:
                i += 1

        chunks = [list_of_nums[i:i + 12] for i in range(0, len(list_of_nums), self.chunk_size)]

        if chunks:
            last_chunk = chunks[-1]
            needed = self.chunk_size - len(last_chunk)

            if needed > 0:
                if self.last_added == 1:
                    last_chunk.insert(0, 2)
                    needed -= 1
                    self.last_added = 2

                next_num = 1
                for _ in range(needed):
                    last_chunk.append(next_num)
                    next_num = 1 if next_num == 2 else 2

                self.last_added = 1 if next_num == 2 else 2
                chunks[-1] = last_chunk

        return chunks
