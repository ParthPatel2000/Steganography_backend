import yaml

with open("raw_data.yaml","r") as raw:
    raw_data = yaml.safe_load(raw)
print(raw_data)

with open("config.yaml","r") as conf:
    final = yaml.safe_load(conf)
    final['environment']['cover_image'] = raw_data['cover_path']
    final['kafka']['bootstrap_servers'] = raw_data['ip']
    final['kafka']['topic'] = raw_data['topic']
    final['key'] = raw_data['key']
    print(final)

with open("config.yaml","w") as conf:
    yaml.safe_dump(final, conf)