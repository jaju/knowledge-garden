from utils import downloaders, script_main, run_script, print_kv_table
from utils.downloaders import download_the_verdict, THE_VERDICT_FILE
from utils.data import read_the_verdict
import re
from functools import cache
import tiktoken


# Constants
UNK = '<|unk|>'
END_OF_TEXT = '<|endoftext|>'

__PATTERN = r'([,.:;?_!"()\']|--|\s)'
def preprocess(text: str) -> str:
    preprocessed = re.split(__PATTERN, text)
    preprocessed = [item.strip() for item in preprocessed if item.strip()]
    return preprocessed


def to_sorted_set(preprocessed_text):
    return sorted(set(preprocessed_text))


def to_vocab(sorted_set):
    return {word: i for i, word in enumerate(sorted_set)}


def remove_spaces_before_punctuations(text):
    return re.sub(r'\s+([,.?!"()\'])', r'\1', text)


class Tokenizer:
    def encode(self, text):
        pass

    
    def decode(self, ids):
        pass


class SimpleTokenizerV1(Tokenizer):
    """
    Simple Tokenizer Version 1.
    Will not handle unknown words.
    """
    def __init__(self, vocab):
        self.str_to_int = vocab
        self.int_to_str = {v: k for k, v in vocab.items()}

    
    def encode(self, text):
        preprocessed = preprocess(text)
        ids = [self.str_to_int[word] for word in preprocessed]
        return ids

    
    def decode(self, ids):
        words = [self.int_to_str[i] for i in ids]
        text = ' '.join(words)
        return remove_spaces_before_punctuations(text)


class SimpleTokenizerV2(SimpleTokenizerV1):
    """
    Simple Tokenizer Version 2.
    Will handle unknown words. We also encode special context details like
    the end of documents, and use that during training.
    """
    def __init__(self, vocab):
        super().__init__(vocab)
        

    def encode(self, text):
        preprocessed = preprocess(text)
        preprocessed = [item if item in self.str_to_int else UNK for item in preprocessed]
        ids = [self.str_to_int[word] for word in preprocessed]
        return ids


class TikTokenV3(Tokenizer):
    def __init__(self):
        self.tokenizer = tiktoken.get_encoding('gpt2')

    def encode(self, text):
        return self.tokenizer.encode(text)

    def decode(self, ids):
        return self.tokenizer.decode(ids)

    def vocabulary_size(self):
        return len(self.tokenizer.vocabulary_size())


class TikTokenWithSpecialV4(TikTokenV3):
    def encode(self, text):
        return self.tokenizer.encode(text, allowed_special={END_OF_TEXT})


preprocessed_text = None

def common_setup():
    download_the_verdict()
    global preprocessed_text
    preprocessed_text = load_and_preprocess_the_verdict()
    return preprocessed_text


@cache
def load_and_preprocess_the_verdict():
    text = read_the_verdict()
    preprocessed_text = preprocess(text)
    return preprocessed_text


def vocab_set_v1(preprocessed_text):
    sorted_words = to_sorted_set(preprocessed_text)
    vocab = to_vocab(sorted_words)
    return vocab


def vocab_set_v2(preprocessed_text):
    sorted_words = to_sorted_set(preprocessed_text)
    sorted_words.extend([END_OF_TEXT, UNK])
    vocab = to_vocab(sorted_words)
    return vocab


text = "three she draggees equally"

@script_main
def v1():
    common_setup()
    vocab_v1 = vocab_set_v1(preprocessed_text)
    tokenizer_v1 = SimpleTokenizerV1(vocab_v1)

    try:
        encoded = tokenizer_v1.encode(text)
        print_kv_table([('Input', text), ('Encoded', encoded), ('Decoded', tokenizer_v1.decode(encoded))])
    except KeyError as e:
        print(f"Error: Token {e} not found in vocab.")

@script_main
def v2():
    common_setup()
    vocab_v2 = vocab_set_v2(preprocessed_text)
    tokenizer_v2 = SimpleTokenizerV2(vocab_v2)
    encoded = tokenizer_v2.encode(text)
    print_kv_table([('Input', text), ('Encoded', encoded), ('Decoded', tokenizer_v2.decode(encoded))])


@script_main
def v3():
    common_setup()
    tokenizer_v3 = TikTokenV3()
    encoded = tokenizer_v3.encode(text)
    print_kv_table([('Input', text), ('Encoded', encoded), ('Decoded', tokenizer_v3.decode(encoded))])


@script_main
def v4():
    common_setup()
    tokenizer_v4 = TikTokenWithSpecialV4()
    text = f"three she dragged equally. {END_OF_TEXT} This is the end of the document."
    encoded = tokenizer_v4.encode(text)
    print_kv_table([('Input', text), ('Encoded', encoded), ('Decoded', tokenizer_v4.decode(encoded))])


@script_main
def v4bpe():
    text = "asd asdjfkjsdf ksjfksa sdkfjsj   powiuosadoapofqfvv"
    bpe_tokenizer = TikTokenWithSpecialV4()
    encoded = bpe_tokenizer.encode(text)
    decoded = bpe_tokenizer.decode(encoded)
    assert text == decoded
    print_kv_table([('Input', text), ('Encoded', encoded), ('Decoded', decoded)])


if __name__ == '__main__':
    run_script()
