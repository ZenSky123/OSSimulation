import random


def generate_random_data(number, filename):
    filepath = "data/{}".format(filename)
    tasks = []
    for i in range(number):
        pid = i
        reachTime = random.randint(0, 100)
        needTime = random.randint(5, 100)
        priority = random.randint(0, 100)

        process_info = [pid, reachTime, needTime, priority]
        tasks.append(process_info)

    tasks.sort(key=lambda x: x[1])

    with open(filepath, 'w') as f:
        for process_info in tasks:
            process_line = ' '.join(map(str, process_info))

            f.write(process_line + '\n')
