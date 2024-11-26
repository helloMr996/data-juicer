from simhash import Simhash, SimhashIndex

# 示例中文文本数据
texts = [
    "rerank： 经过第一步使用cosin余弦相似度从密集向量数据库 + keyword search（稀疏向量召回）初步召回top K相似度的文本，按理来说就可以让LLM根据用户的query + 召回的context生成最终答案了，还要这个rerank干啥了？实际操作时，还是会发现一些问题：包含正确答案的文本在context中的排名可能并不靠前。比如query = “清华大学在哪座城市？” 。正确答案肯定是“北京”啦！但实际召回的context中包含北京的文本不一定排在前面，可能在中间甚至后面，给最后一个LLM输入的context会很大，直接导致LLM需要处理很长的文本，推理效率低不说，还容易出错，核心问题还是在于：初步召回的context还是有进一步压缩提炼的空间！造成这种现象的原因是啥了",
    "rerank： 经过第一步使用sim相似度从密集向量数据库 +关键词初步召回K个相似度的文本，按理来说就可以让LLM根据用户的问题 + 召回的文本生成最终答案了，还要这个重排干啥了？实际操作时，还是会发现一些问题：包含正确答案的文本在context中的排名可能并不靠前。比如问题 = “北京大学在哪座城市？” 。正确答案肯定是“北京”啦！但实际召回的context中包含北京的文本不一定排在前面，可能在中间甚至后面，给最后一个LLM输入的context会很大，直接导致LLM需要处理很长的文本，推理效率低不说，还容易出错，核心问题还是在于：初步召回的context还是有进一步压缩提炼的空间！造成这种现象的原因是啥了",
    "利用cosin求两个向量的相似度，本质是看两个向量的距离。比如“北京”、“上海”、“深圳”这些都是中国的一线大城市，这3个词的嵌入向量的余弦相似度会很近，所以使用cosin召回的时候也可能把“上海”、“深圳”这些不是正确答案的sentence召回，所以要用tf-idf这类稀疏向量补充召回部分向量，整个过程称为 hybrid search。经过hybird search后，召回的context变多，给最后一步的LLM生成最终答案带来了麻烦，所以需要进一步从context中继续提炼，优中选优！比如初步召回20条，需要通过重排选择更接近的3~5条，这个过程就是rerank！",
    "利用距离求两个向量的相似度，本质是看两个向量的距离。比如“北京”、“上海”、“深圳”这些都是中国的一线大城市，这3个词的embedding的cosin会很近，所以使用cosin召回的时候也可能把“上海”、“深圳”这些不是正确答案的sentence召回，所以要用tf-idf这类稀疏向量补充召回部分向量，整个过程称为 混合检索。经过混合检索后，召回的上下文变多，给最后一步的LLM生成最终答案带来了麻烦，所以需要进一步从context中继续提炼，优中选优！比如初步召回20条，需要通过rerank选择更接近的3~5条，这个过程就是rerank！",
    "确定要做rerank后，怎么做才能达到既定的目的？要想明白这个问题，还要回到最初的动机：cosin计算的是两个向量的距离，只考虑语义相似，不考虑字面符号是否一致；而稀疏检索tf-idf只考虑字面的符号， 不考虑语义，怎么整合这两种retrieve的优势，摒弃其劣势了？这就需要用到传统NLP常见的手段了：classifier",
]

# 计算每个文本的Simhash值
simhashes = [(str(i), Simhash(text)) for i, text in enumerate(texts)]

# 创建Simhash索引
index = SimhashIndex(simhashes, k=10)

# 检查文本是否重复
def is_duplicate(new_text, index):
    new_simhash = Simhash(new_text)
    duplicates = index.get_near_dups(new_simhash)
    return duplicates

# 检查每个文本是否重复
for i, text in enumerate(texts):
    duplicates = is_duplicate(text, index)
    if len(duplicates) > 1:  # 因为自己也会在重复列表中，所以长度大于1
        print(f"文本 {i} 是重复的，重复文本索引：{duplicates}")
    else:
        print(f"文本 {i} 没有重复。")

# 例如，添加一个新文本并检查是否重复
new_text = "按理来说就可以让LLM根据用户的query + 召回的context生成最终答案了，还要这个rerank干啥了？实际操作时，还是会发现一些问题：包含正确答案的文本在context中的排名可能并不靠前."
if is_duplicate(new_text, index):
    print("新文本是重复的。")
else:
    print("新文本没有重复。")
    # 如果没有重复，则将其添加到索引中
    index.add(str(len(texts)), Simhash(new_text))