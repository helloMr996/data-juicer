#!/bin/bash

# 预测数据集的 doc_score
# dataset_path: 输入数据集路径。要求路径的后缀为 [json, jsonl, parquet] 之一。
# result_path: 存储带有预测结果的数据集的路径。要求路径的后缀为[json, jsonl, parquet]之一。
# model_path: (可选，默认为 gpt3) 用于预测的模型的路径。您可以使用我们提供的模型之一[gpt3, chinese,code]。或者您可以使用train.py脚本使用自己训练的模型。
# tokenizer: (可选，默认为 None) 用于标记要分类的文本的标记器。 如果为 None，则将使用 PySpark 的 standard Tokenizer。 此外，您可以使用我们提供的标记器[zh.sp.model, code.sp.model]之一。您也可以将其设置为您自己的 sentencepiece 模型的路径。
# keep_method: (可选，默认为 gpt3) 根据 doc_score 决定是否保留样本的方法。应为 [gpt3, label] 之一。
# text_key: (可选，默认为 text) 用于存储输入数据集中需要被分类的文本的字段名称。
# overall_stats: (可选，默认为 False) 是否生成文档分数的汇总统计报告。

python tools/quality_classifier/predict.py \
    /mnt/tmp/apps/cmss-yangjiandong/staging_stack_v1/filter/staging-stack-v1-python-filter.parquet \
    /mnt/tmp/apps/cmss-yangjiandong/staging_stack_v1/score/staging-stack-v1-python-score.parquet \
    --model code \
    --tokenizer code.sp.model \
    --keep_method label \
    --text_key content \
    --overall_stats true > predict.log 