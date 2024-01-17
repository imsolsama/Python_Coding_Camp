import re
from typing import List, Union, Optional, Tuple
from collections import defaultdict, Counter

class BPETokenizer:
    def __init__(self, corpus: Optional[Union[List[str], str]] = None, vocab_size: Optional[int] = 10000): #단어 수 제한
        self.vocab = defaultdict(int)
        self.bpe_codes = {}
        self.vocab_token_index = {}
        self.vocab_size = vocab_size

        if corpus is not None:
            self.add_corpus(corpus)

    def add_corpus(self, corpus: Union[List[str], str]) -> None:
        if isinstance(corpus, str):
            corpus = [corpus]

        for line in corpus:
            self.add_line_to_vocab(line)

    def add_line_to_vocab(self, line: str):
        for word in line.strip().split():
            word = ' '.join(list(word)) + ' </w>'
            self.vocab[word] += 1

    def get_stats(self): #빈번한 문자쌍을 통계로 변환
        pairs = defaultdict(int)
        for word, freq in self.vocab.items():
            symbols = word.split()
            for i in range(len(symbols) - 1):
                pairs[symbols[i], symbols[i + 1]] += freq
        return pairs

    def merge_vocab(self, pair: Tuple[str, str]): #가장 빈번한 문자 쌍을 병합하여 단어사전 업데이트
        bigram = re.escape(' '.join(pair))
        p = re.compile(r'(?<!\S)' + bigram + r'(?!\S)')
        new_vocab = defaultdict(int)
        for word in self.vocab:
            w_out = p.sub(''.join(pair), word)
            new_vocab[w_out] = self.vocab[word]
        self.vocab = new_vocab

    def train(self, n_iter: Optional[int] = None) -> None:
        if n_iter is None:
            n_iter = self.vocab_size - len(self.vocab) - 1  # Subtract existing vocab and special tokens

        for i in range(n_iter):
            pairs = self.get_stats()
            if not pairs:
                break
            best = max(pairs, key=pairs.get)
            self.merge_vocab(best)
            self.bpe_codes[best] = i
        self.update_vocab_token_index()

    def tokenize(self, text: Union[List[str], str], padding: bool = False, max_length: Optional[int] = None) -> Union[List[List[int]], List[int]]: #입력된 텍스트를 토큰화하여 리스트로 반환
        if isinstance(text, str):
            text = [text]

        tokenized_texts = []
        for line in text:
            word = ' '.join(list(line)) + ' </w>'
            tokens = word.split()
            tokenized_text = [self.vocab_token_index[token] for token in tokens if token in self.vocab_token_index]
            tokenized_texts.append(tokenized_text)

        if padding:
            max_len = max_length or max(len(t) for t in tokenized_texts)
            tokenized_texts = [t + [self.vocab_token_index['</w>']] * (max_len - len(t)) for t in tokenized_texts]

        if max_length is not None:
            tokenized_texts = [t[:max_length] for t in tokenized_texts]

        return tokenized_texts if len(tokenized_texts) > 1 else tokenized_texts[0]

    def __call__(self, text: Union[List[str], str], padding: bool = False, max_length: Optional[int] = None) -> Union[List[List[int]], List[int]]: #class 사용
        return self.tokenize(text, padding, max_length)

    def update_vocab_token_index(self):
        """Update the token index after each merge."""
        self.vocab_token_index = {token: idx for idx, token in enumerate(self.vocab)}


class WordTokenizer:
    def __init__(self, corpus: Optional[Union[List[str], str]] = None):
        self.vocab = defaultdict(int)
        self.vocab_token_index = {}

        if corpus is not None:
            self.add_corpus(corpus)

    def add_corpus(self, corpus: Union[List[str], str]) -> None:
        if isinstance(corpus, str):
            corpus = [corpus]

        for line in corpus:
            self.add_line_to_vocab(line)

    def add_line_to_vocab(self, line: str):
        for word in line.strip().split():
            self.vocab[word] += 1

    def build_vocab(self, *args, **kwargs) -> None:
        sorted_vocab = sorted(self.vocab.items(), key=lambda item: item[1], reverse=True)
        self.vocab_token_index = {word: idx for idx, (word, freq) in enumerate(sorted_vocab)}

    def tokenize(self, text: Union[List[str], str]) -> Union[List[List[int]], List[int]]:
        if isinstance(text, str):
            text = [text]

        tokenized_texts = []
        for line in text:
            tokens = line.strip().split()
            tokenized_text = [self.vocab_token_index.get(token, -1) for token in tokens]
            tokenized_texts.append(tokenized_text)

        return tokenized_texts if len(tokenized_texts) > 1 else tokenized_texts[0]

    def __call__(self, text: Union[List[str], str], *args, **kwargs) -> Union[List[List[int]], List[int]]:
        return self.tokenize(text)