import ebooklib
from ebooklib import epub
import bs4
import pathlib

import string
import unicodedata

from functools import partial, reduce


class EBook:

    def __init__(self, path, clean_special_chars=False, min_chunk_length=512):
        book = self.load_from_path(path)
        self.book = book

        chunks = self.extract_chunks(book)
        self.raw_chunks = chunks

        chunks = self.clean_chunks(chunks, clean_special_chars)
        chunks = self._agglomerate(chunks, min_chunk_length=512)
        self.chunks = chunks  # cleaned and accumulated to minimum length

        self.text = ' '.join(chunks)

    def load_from_path(self, path):
        path = pathlib.Path(path)
        book = epub.read_epub(path.as_posix())
        return book

    def extract_chunks(self, book):
        """Load an `epub` file from disk and clean it up as a text file.

        Parameters
        ----------
        book: ebooklib.epub
            epub object

        Returns
        -------
        book_chunks_stripped: list[str]
            List of text chunks extracted from epub object.
        """
        book_chunks = filter(
            lambda x: x.get_type() == ebooklib.ITEM_DOCUMENT, book.get_items()
        )
        chunks = [
            ' '.join(
                bs4.BeautifulSoup(
                    c.get_body_content(),
                    features='lxml'
                ).find_all(string=True, recursive=True))
                # get_text skips some kinds of line breaks
            for c in book_chunks
        ]
        
        return chunks
    

    def clean_text(self, text, clean_special_chars=True):
        """
        """
        chunked = text.split('\n')
        text = ' '.join(chunked)
        text = unicodedata.normalize('NFKC', text)
        if clean_special_chars:
            text = ''.join(
                filter(
                    lambda x: x in string.printable,
                    text
                )
            )
        return text
    
    def clean_chunks(
            self,
            chunks,
            clean_special_chars=True):
        """
        """
        # clean each according to clean_text
        clean = partial(self.clean_text, clean_special_chars=clean_special_chars)
        chunks = list(map(clean, chunks))
        # remove empty chunks
        chunks = list(filter(lambda x: not x.isspace(), chunks))

        return chunks
    
    def _agglomerate(self, chunks, min_chunk_length):
        """
        """
        lengths = [(c, len(c)) for c in chunks]

        agglomerated = []
        c_array = []
        curr_len = []
        for c, length in lengths:
            if length < min_chunk_length:
                c_array.append(c)
                curr_len.append(length)
                continue
            
            if sum(curr_len) < min_chunk_length:
                c_array.append(c)
                agglomerated.append(c_array)

                c_array = []
                curr_len = []
            else:
                agglomerated.append(c_array)
                agglomerated.append([c])
                c_array = []
                curr_len = []

        agglomerated_chunks = []
        for c_array in agglomerated:
            new_c = reduce(lambda a, b: a + ' ' + b, c_array)
            agglomerated_chunks.append(new_c)

        return agglomerated_chunks

    def write(self, path):
        """
        """
        path = pathlib.Path(path)
        print(f'Writing to {path}')
        with open(path.as_posix(), 'w') as f:
            for c in self.chunks:
                f.write(c)