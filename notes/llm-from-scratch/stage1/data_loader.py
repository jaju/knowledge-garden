from utils import script_main, run_script, print_kv_table
from utils.data import read_the_verdict
from stage1.tokenization import TikTokenWithSpecialV4

import torch
from torch.utils.data import Dataset, DataLoader

def input_target_pairs(tokenizer, text, context_size=4):
    encoded = tokenizer.encode(text)
    for i in range(0, len(encoded) - context_size):
        yield encoded[i:i + context_size], encoded[i + 1: i + context_size + 1]


class GPTDatasetV1(Dataset):
    def __init__(self, text, tokenizer, max_length=32, stride=1):
        self.input_ids = []
        self.target_ids = []

        token_ids = tokenizer.encode(text)

        for i in range(0, len(token_ids) - max_length, stride):
            input_chunk = token_ids[i:i + max_length]
            target_chunk = token_ids[i + 1: i + max_length + 1]
            self.input_ids.append(torch.tensor(input_chunk))
            self.target_ids.append(torch.tensor(target_chunk))


    def __len__(self):
        return len(self.input_ids)


    def __getitem__(self, idx):
        return self.input_ids[idx], self.target_ids[idx]


def create_dataloader_v1(dataset,
                         batch_size=4,
                         shuffle=True,
                         drop_last=True,
                         num_workers=0):
    dataloader = DataLoader(
        dataset,
        batch_size=batch_size,
        shuffle=shuffle,
        drop_last=drop_last,
        num_workers=num_workers
    )
    return dataloader


@script_main
def v1(count="10"):
    count = int(count)
    tokenizer = TikTokenWithSpecialV4()
    text = read_the_verdict()
    counter = 0
    results = []
    for context, desired in input_target_pairs(tokenizer, text, context_size=4):
        if counter > count:
            break
        results.append((f"#{counter} - Input/desired-output pair", (tokenizer.decode(context), tokenizer.decode(desired))))
        counter += 1
    print_kv_table(results)

@script_main
def v2():
    """
    This is v2.
    We are using the GPTDatasetV1 class to create a dataset from the text.
    """
    import itertools
    text = read_the_verdict()
    tokenizer = TikTokenWithSpecialV4()
    dataset = GPTDatasetV1(text, tokenizer, max_length=8, stride=1)

    results = []
    for a,b in itertools.islice(dataset, 3):
        results.append(('I/O Pair', (a, b)))
    print_kv_table(results)

    dl = create_dataloader_v1(dataset, batch_size=4)
    iterator = iter(dl)
    first_batch = next(iterator)
    print_kv_table([('First batch', first_batch)])
    print(f"First batch element shapes: {first_batch[0].shape}, {first_batch[1].shape}")


if __name__ == '__main__':
    run_script()
