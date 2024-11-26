import yaml

# 读取yaml文件
with open('/mnt/tmp/apps/cmss-yangjiandong/data-juicer/configs/demo/dedup-code.yaml', 'r') as file:
    config = yaml.safe_load(file)

# 修改指定属性的值
config['dataset_path'] = '/mnt/hh/'

# 将修改后的配置写回yaml文件
with open('/mnt/tmp/apps/cmss-yangjiandong/data-juicer/configs/demo/dedup-code.yaml', 'w') as file:
    yaml.safe_dump(config, file, default_flow_style=False)



