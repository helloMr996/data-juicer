#!/bin/bash

# positive_datasets: (Optional. Default: None) the paths to the positive datasets. It could be a string for a single dataset, e.g. 'pos.parquet', or a list of strings for multiple datasets, e.g. '["pos1.parquet", "pos2.parquet"]'.
# negative_datasets: (Optional. Default: None) the paths to the negative datasets. Similar to positive_datasets.
# model_path: (Optional. Default: "my_quality_model") the path to the model to be evaluated. You can evaluate one of the models we provide [gpt3, chinese, code]. Or you can evaluate the model trained by yourself using the train.py script.
# tokenizer: (Optional. Default: None) the tokenizer to tokenize texts to be classified. If it's None, the standard Tokenizer of PySpark will be used. Besides, you can use one of the tokenizers we provide [zh.sp.model, code.sp.model]. Or you can set it to a path to your own sentencepiece model.
# text_key: (Optional. Default: "text") the field name to store texts to be classified in the input dataset.

python tools/quality_classifier/eval.py \
    --positive_datasets /mnt/tmp/apps/cmss-yangjiandong/data-juicer/outputs/starcoder-sandbox/starcoderdata/python/syntax/train-00001-of-00059.parquet \
    --negative_datasets '["/mnt/tmp/apps/cmss-yangjiandong/data-juicer/outputs/starcoderdata/python/trace/filter-alphanumeric_filter.jsonl","/mnt/tmp/apps/cmss-yangjiandong/data-juicer/outputs/starcoderdata/python/trace/filter-average_line_length_filter.jsonl"]' \
    --model code \
    --tokenizer code.sp.model \
    --text_key content > evel.log