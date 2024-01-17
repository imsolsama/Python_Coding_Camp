# main.py
from YBIGTA.tokenizers import BPETokenizer, WordTokenizer

def main(use_bpe, n_corpus, n_iter):
    corpus = ["hug", "hun", "hup", "pun", "hup"]

    if use_bpe:
        tokenizer = BPETokenizer(corpus, vocab_size=n_corpus)
        tokenizer.train(n_iter)
    else:
        tokenizer = WordTokenizer(corpus)
        tokenizer.build_vocab() 

    test_text = "hup hun hug pun hup"
    tokenized_text = tokenizer.tokenize(test_text)

    print(tokenized_text)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--use_bpe', type=bool, default=True)
    parser.add_argument('--n_corpus', type=int, default=30000)
    parser.add_argument('--n_iter', type=int, default=10000)

    args = parser.parse_args()

    main(args.use_bpe, args.n_corpus, args.n_iter)
