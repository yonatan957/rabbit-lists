from typing import List, Optional
class StreamAdapter:
    def __init__(
            self,
            chunk_size:int,
            search_list: Optional[List[int]] = None,
            replace_list: Optional[List[int]] = None):
        self.last_added = 2
        self.chunk_size = chunk_size
        self.search_list = search_list if search_list is not None else [5,5,5]
        self.replace_list = replace_list if replace_list is not None else [6,6,6]


    def change_search_list(self, new_search_list:List[int]):
        self.search_list = new_search_list


    def change_replace_list(self, new_replace_list):
        self.replace_list = new_replace_list



    def convert_sequences(self, message: List[int]) -> List[int]:
        i = 0
        while i <= len(message) - 3:
            triplet = message[i:i + 3]
            if triplet == self.search_list:
                message[i:i + 3] = self.replace_list
                i += 3
            else:
                i += 1
        return message


    def add_numbers_to_last_chunk(self, chunks:List[List[int]]) -> List[List[int]]:
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


    def GetStreamChunks(self, numbers_to_chunk: List[int]) -> List[List[int]]:
        """
        Expands the input list of numbers up to length 12 by adding alternating 1s and 2s.
        If the last number is 1,it adds 2 to the next list.

        :param numbers_to_chunk: (list of int) The original list of numbers.

        :return: list[list[int]] - List of 12-length number chunks
        """

        message = self.convert_sequences(numbers_to_chunk)

        chunks = []
        for i in range(0, len(message), self.chunk_size):
            chunk = message[i:i + self.chunk_size]
            chunks.append(chunk)

        if chunks:
            chunks = self.add_numbers_to_last_chunk(chunks)

        return chunks
