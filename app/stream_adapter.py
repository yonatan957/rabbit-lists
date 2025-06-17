from typing import List
class StreamAdapter:
    def __init__(self, chunk_size):
        self.last_added = 2
        self.chunk_size = chunk_size
    def GetStreamChunks(self, message_from_queue: List[int]) -> List[List[int]]:
        """
        Expands the input list of numbers up to length 12 by adding alternating 1s and 2s.
        If the last number is 1,it adds 2 to the next list.

        :param message_from_queue: (list of int) The original list of numbers.

        :return: list[list[int]] - List of 12-length number chunks
        """
        i = 0
        while i <= len(message_from_queue) - 3:
            triplet = message_from_queue[i:i + 3]
            if triplet == [5, 5, 5]:
                message_from_queue[i:i + 3] = [6, 6, 6]
                i += 3
            else:
                i += 1

        chunks = []
        for i in range(0, len(message_from_queue), self.chunk_size):
            chunk = message_from_queue[i:i + self.chunk_size]
            chunks.append(chunk)

        if chunks:
            last_chunk = chunks[-1]
            numbers_to_add = self.chunk_size - len(last_chunk)

            if numbers_to_add > 0:
                if self.last_added == 1:
                    last_chunk.insert(0, 2)
                    numbers_to_add -= 1
                    self.last_added = 2

                next_num = 1
                for _ in range(numbers_to_add):
                    last_chunk.append(next_num)
                    next_num = 1 if next_num == 2 else 2

                self.last_added = 1 if next_num == 2 else 2
                chunks[-1] = last_chunk

        return chunks
