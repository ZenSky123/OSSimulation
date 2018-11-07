from random import randint, random


def ran_data(filename='default.dat'):
    filepath = 'data/{}'.format(filename)
    process_number = randint(5, 10)
    data = []
    for _ in range(process_number):
        page_number = randint(8, 32)
        memory_needed = page_number * 4096

        process_data = [memory_needed]

        used_number = randint(page_number * 2, page_number * 5)
        for _ in range(used_number):
            memory_use = randint(0, memory_needed - 1)
            if memory_use > memory_needed // 5:
                if random() > 0.8:
                    process_data.append(memory_use)
            else:
                if random() > 0.2:
                    process_data.append(memory_use)
        data.append(process_data)
    with open(filepath, 'w') as f:
        for process_data in data:
            f.write(' '.join(map(str, process_data)))
            f.write("\n")


