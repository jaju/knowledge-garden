from functools import cache

import torch

from utils import script_main, run_script, print_kv_table
from utils.data import read_the_verdict

from stage1.tokenization import TikTokenWithSpecialV4
from stage1.data_loader import GPTDatasetV1, create_dataloader_v1


@cache
def create_tokenizer_and_data_loader():
    """
    Create a tokenizer and data loader for the given text.
    """
    tokenizer = TikTokenWithSpecialV4()
    text = read_the_verdict()
    dataset = GPTDatasetV1(text, tokenizer, max_length=4)
    dataloader = create_dataloader_v1(dataset, batch_size=8)
    return tokenizer, dataloader


@script_main
def v0(vocab_size='10', output_dim='3'):
    torch.manual_seed(0)
    vocab_size = int(vocab_size)
    output_dim = int(output_dim)
    embedding_layer = torch.nn.Embedding(vocab_size, output_dim)
    print('Pseudo-randomly initialized embedding layer:')
    token_id = 5
    print_kv_table([
        ('Vocab Size', vocab_size),
        ('Output Dimension', output_dim),
        ('Embedding Layer', embedding_layer),
        ('Layer Weights', embedding_layer.weight),
        (f'Embedding for token_id {token_id}', embedding_layer(torch.tensor(token_id)))
    ])

    more_token_ids = [2, 4, 6]
    print_kv_table([
        (f'Embedding for token_ids {more_token_ids}', embedding_layer(torch.tensor(more_token_ids)))
    ])

@script_main
def v1(vocab_size="50257", embedding_size="256", input_length="4", batch_size="8"):
    """
    Tokenizing and converting to embeddings with positional encoding.
    """
    vocab_size = int(vocab_size)
    embedding_size = int(embedding_size)
    input_length = int(input_length)
    batch_size = int(batch_size)

    print_kv_table((
        ("vocab_size", vocab_size),
        ("embedding_size", embedding_size),
        ("input_length", input_length),
        ("batch_size", batch_size)
    ))

    embedding_layer = torch.nn.Embedding(vocab_size, embedding_size)
    print("Embedding Layer:", embedding_layer.weight)

    tokenizer, dataloader = create_tokenizer_and_data_loader()

    iterator = iter(dataloader)
    inputs, targets = next(iterator)
    print("Inputs shape:", inputs.shape)
    print("Targets shape:", targets.shape)

    input_tensor = torch.randint(0, vocab_size, (1, input_length))
    print("Input tensor shape: ", input_tensor.shape)
    print("Input Tensor:", input_tensor)
    output_tensor = embedding_layer(input_tensor)
    print("Output tensor shape: ", output_tensor.shape)
    print("Output Tensor:", output_tensor)


@script_main
def v2pos(vocab_size="50257", embedding_size="256", input_length="4", batch_size="8"):
    """
    Tokenizing and converting to embeddings with positional encoding.
    """
    vocab_size = int(vocab_size)
    embedding_size = int(embedding_size)
    input_length = int(input_length)
    batch_size = int(batch_size)

    print_kv_table((
        ("vocab_size", vocab_size),
        ("embedding_size", embedding_size),
        ("input_length", input_length),
        ("batch_size", batch_size)
    ))

    embedding_layer = torch.nn.Embedding(vocab_size, embedding_size)
    pos_embedding_layer = torch.nn.Embedding(input_length, embedding_size)
    pos_embeddings = pos_embedding_layer(torch.arange(input_length))
    print("Embedding Layer:", embedding_layer.weight)
    print("Positional Embedding Layer:", pos_embedding_layer.weight)

    tokenizer, dataloader = create_tokenizer_and_data_loader()

    iterator = iter(dataloader)
    inputs, targets = next(iterator)

    token_embeddings = embedding_layer(inputs)
    input_embeddings = token_embeddings + pos_embeddings

    print("Input shape: ", input_embeddings.shape)
    print("Plain token embeddings: ", token_embeddings)
    print("Positional embeddings: ", input_embeddings)

if __name__ == "__main__":
    run_script()
