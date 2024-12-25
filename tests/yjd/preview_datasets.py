import argparse
from datasets import load_dataset

def preview_dataset(dataset_name, split, num_records):
    try:
        # 加载数据集
        dataset = load_dataset(dataset_name, split=split)
        print(f"加载的数据集：{dataset_name}，拆分：{split}，总记录数：{len(dataset)}")
        print(f"预览前 {num_records} 条记录：\n")
        
        # 打印指定数量的记录
        for idx, record in enumerate(dataset.select(range(min(num_records, len(dataset))))):
            print(f"记录 {idx + 1}: {record}\n")
    except Exception as e:
        print(f"加载数据集失败：{e}")

def main():
    # 设置命令行参数
    parser = argparse.ArgumentParser(description="预览 Hugging Face 数据集")
    parser.add_argument("--dataset", type=str, required=True, help="数据集名称，例如：'imdb'")
    parser.add_argument("--split", type=str, default="train", help="数据集拆分，例如：'train', 'test'")
    parser.add_argument("--num_records", type=int, default=5, help="预览的记录条数")
    
    args = parser.parse_args()
    
    # 调用预览函数
    preview_dataset(args.dataset, args.split, args.num_records)

if __name__ == "__main__":
    main()
# python preview_dataset.py --dataset imdb --split train --num_records 3
