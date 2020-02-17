import operator


def calculate_frequency():
    text_path = "C:/Users/87173/Desktop/term6/CyberSec/lab/lab_2/ascii_frequency.txt"
    with open(text_path) as f:
        content = f.readlines()
    # you may also want to remove whitespace characters like `\n` at the end of each line
    content = [x.strip().split() for x in content]
    ascii_freq_map = {}
    for sub_list in content:
        ascii_freq_map[sub_list[1]] = sub_list[4][:-2]  # use character as key
        # ascii_freq_map[sub_list[0]] = sub_list[4][:-2]  # use ascii oder as key

    sorted_freq_map = dict(sorted(ascii_freq_map.items(), key=operator.itemgetter(1), reverse=True))
    ascii_freq_result = list(sorted_freq_map.keys())
    print(sorted_freq_map)
    print(ascii_freq_result)


def calculate_freq_v2():
    text_path = "C:/Users/87173/Desktop/term6/CyberSec/lab/lab_2/ascii_frequency_v2.txt"
    with open(text_path) as f:
        content = f.readlines()
    # you may also want to remove whitespace characters like `\n` at the end of each line
    content = [x.strip().replace('   ', '') for x in content if x.strip() != '']
    ascii_freq_map = {}
    for sub_list in content:
        ascii_freq_map[sub_list[0]] = sub_list[2:]

    sorted_freq_map = dict(sorted(ascii_freq_map.items(), key=operator.itemgetter(1), reverse=True))
    ascii_freq_result = list(sorted_freq_map.keys())
    ascii_freq_result_ord = [ord(char) for char in ascii_freq_result]
    print(ascii_freq_result_ord)


def analyse_freq(text):
    char_freq = {}
    text = open(text, mode='r', encoding='utf-8', newline='\n').read()       # read mode
    # origin_txt = text.decode("ascii")
    print("get text content ... and doing analysis now ...")
    for char in text:
        print("hahah")
        char_freq[ord(char)] = text.count(char)
    sorted_char_freq = dict(sorted(char_freq.items(), key=operator.itemgetter(1), reverse=True))
    print(sorted_char_freq)
    char_freq_result = list(sorted_char_freq.keys())
    print(char_freq_result)
    return char_freq_result

# calculate_frequency()
# calculate_freq_v2()
sherlock_path = "C:/Users/87173/Desktop/term6/CyberSec/lab/lab_2/large/world192.txt"
analyse_freq(sherlock_path)
