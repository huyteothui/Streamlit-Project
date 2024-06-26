import streamlit as st

def cost(i, j, source, target):
    if source[i - 1] == target[j - 1]:
        return 0
    else:
        return 1


def levenshtein_distance(source, target):
    matrix = [[0 for _ in range(len(target) + 1)] for _ in range(len(source) + 1)]
    for i in range(len(target) + 1):
        matrix[0][i] = i
    for i in range(len(source) + 1):
        matrix[i][0] = i
    for i in range(1, len(source) + 1):
        for j in range(1, len(target) + 1):
            matrix[i][j] = min(matrix[i - 1][j] + 1,
                               matrix[i][j - 1] + 1,
                               matrix[i - 1][j -1] + cost(i, j, source, target))
    return matrix[len(source)][len(target)]

def vocab(file_path):
    with open(file_path, "r") as file:
        contents = file.readlines()
    words = sorted(set([line.strip().lower() for line in contents]))
    return words

vocabs = vocab("data/vocab.txt")
def main():
    st.title("Word correction using Levenshtein Distance")
    word = st.text_input("Word:")
    if st.button("Compute"):
        levenshtein_distances = dict()
        for vocab in vocabs:
            levenshtein_distances[vocab] = levenshtein_distance(word, vocab)

        sorted_distances = dict(sorted(levenshtein_distances.items(), key=lambda item: item[1]))
        correct_word = list(sorted_distances.keys())[0]
        st.write("Correct word: ", correct_word)

        col1, col2 = st.columns(2)
        col1.write("Vocabulary:")
        col1.write(vocabs)

        col2.write("Distances:")
        col2.write(sorted_distances)

if __name__ == "__main__":
    main()
