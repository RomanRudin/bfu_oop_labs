import json

with open('Labs/Lab2/font.json', 'r') as file:
    info = json.load(file)
with open('Labs/Lab2/font.txt', 'w') as file:
    for sym in info.values():
        for line in sym:
            file.write(line)
            file.write('\n')
        file.write('-' * 15 + '\n')
    