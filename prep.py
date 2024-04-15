with open('2024q1.tsv', 'r', encoding='utf-8') as f:
    data = [line.strip().split('\t') for line in f]

with open('2024q1_dns.tsv', 'r', encoding='utf-8') as f:
    dns = [line.strip().split('\t') for line in f]

for dns_item in dns:
    temp = []

    for data_item in data:
        if dns_item[0] == data_item[1]:
            temp.append(data_item)
    
    with open(f'imgs/2024q1_{dns_item[0]}.tsv', 'w', encoding='utf-8') as f:
        for item in temp:
            f.write('\t'.join(item) + '\n')
        print(f'imgs/2024q1_{dns_item[0]}.tsv created')