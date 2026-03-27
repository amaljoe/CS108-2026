import sys
import csv
from collections import defaultdict, deque

def load_translations(filename):
    graph = defaultdict(list)  # (lang, word) -> [(lang, word)]
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) == 4:
                l1, w1, l2, w2 = [x.strip() for x in row]
                graph[(l1, w1)].append((l2, w2))
                graph[(l2, w2)].append((l1, w1))
    return graph

def find_translation(graph, lang1, word, lang2):
    start = (lang1, word)
    if start not in graph:
        return None
    visited = {start}
    queue = deque([start])
    while queue:
        curr = queue.popleft()
        for neighbor in graph[curr]:
            if neighbor[0] == lang2:
                return neighbor[1]
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    return None

def get_all_words(graph, lang):
    return {w for (l, w) in graph if l == lang}

def main():
    mode = int(sys.argv[1])
    graph = load_translations('translations.csv')

    if mode == 1:
        lang = sys.argv[2]
        result = sorted(get_all_words(graph, lang), reverse=True)
        print(result)

    elif mode == 2:
        lang1 = sys.argv[2]
        lang2 = sys.argv[3]
        pairs = set()
        for word in get_all_words(graph, lang1):
            trans = find_translation(graph, lang1, word, lang2)
            if trans:
                pairs.add((word, trans))
        print(sorted(pairs))

    elif mode == 3:
        lang1 = sys.argv[2]
        lang2 = sys.argv[3]
        word = sys.argv[4]
        trans = find_translation(graph, lang1, word, lang2)
        print(trans if trans else "UNK")

if __name__ == '__main__':
    main()
