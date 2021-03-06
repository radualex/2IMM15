import textwrap
from text_processing import tokenize_filter_punctuation, remove_words_from_query, extract_operators_from_query, remove_non_alpha_from_string

booleanOperators = ['AND', 'OR', 'NOT', 'and', 'or', 'not']


def split_query_into_words_and_operators(query):
    tokens = tokenize_filter_punctuation(query)
    tokens = remove_words_from_query(tokens, booleanOperators)
    operators = extract_operators_from_query(query, booleanOperators)

    dict = {'tokens': tokens, 'operators': operators}

    return dict


# actual checking (if key(from db) contains token or token contains key(from db). both normalized)
def create_incidence_matrices(dict, tokens, videos):
    incidence_matrices = []
    for token in tokens:
        incidence_matrix = [0] * len(videos)
        for keys, values in dict.items():
            key_norm = keys.lower()
            token_norm = token.lower()
            if token_norm in key_norm or key_norm in token_norm:
                for value in values:
                    index = videos.index(value)
                    incidence_matrix[index] = 1
        incidence_matrices.append(incidence_matrix)

    return incidence_matrices


def calculate_binary_value_from_not_operator(matrix):
    arr = [0] * len(matrix)
    i = 0
    while(i < len(matrix)):
        if(matrix[i] == 1):
            arr[i] = 0
        else:
            arr[i] = 1
        i += 1
    return arr


def calculate_binary_value_from_and_operator(matrix1, matrix2):
    arr = [0] * len(matrix1)
    i = 0
    while(i < len(arr)):
        if(matrix1[i] == 1 and matrix2[i] == 1):
            arr[i] = 1
        else:
            arr[i] = 0
        i += 1
    return arr


def calculate_binary_value_from__or_operator(matrix1, matrix2):
    arr = [0] * len(matrix1)
    i = 0
    while(i < len(arr)):
        if(matrix1[i] == 0 and matrix2[i] == 0):
            arr[i] = 0
        else:
            arr[i] = 1
        i += 1
    return arr


def calculate_binary_value_and_or(matrix1, matrix2, operator):
    if(operator == 'and'):
        return calculate_binary_value_from_and_operator(matrix1, matrix2)
    else:
        return calculate_binary_value_from__or_operator(matrix1, matrix2)


def process_final_matrix(inc_matrices, operators):
    if(len(inc_matrices) == 1):
        return inc_matrices[0]
    else:
        result = calculate_binary_value_and_or(
            inc_matrices[0], inc_matrices[1], operators[0])
        new_matrices = []
        new_matrices.append(result)
        if(len(inc_matrices[2:]) != 0):
            for arr in inc_matrices[2:]:
                new_matrices.append(arr)
        new_operators = []
        for arr in operators[1:]:
            new_operators.append(arr)
        return process_final_matrix(new_matrices, new_operators)


# we assume that for n tokens there are n-1 operators
def process_matrices(inc_matrices, operators):
    # process 'not' operator first
    if(len(inc_matrices) == 1 and len(operators) == 1 and operators[0] == 'not'):
        return calculate_binary_value_from_not_operator(inc_matrices[0])
    else:
        i = 1
        while(i < len(inc_matrices)):
            if(operators[i - 1] == 'not'):
                new_matrix = calculate_binary_value_from_not_operator(
                    inc_matrices[i])
                inc_matrices[i] = new_matrix
                operators[i - 1] = 'and'
            i += 1

        final_matrix = process_final_matrix(inc_matrices, operators)
        return final_matrix


def extract_video_names_from_final_matrix(final_matrix, videos):
    final_videos = []

    i = 0
    while(i < len(final_matrix)):
        if(final_matrix[i] == 1):
            final_videos.append(videos[i])
        i += 1

    return final_videos


# convert the array of videos to json format string
def jsonify(array):
    if(len(array) == 0):
        return "{}"
    else:
        jsonified = "{\"videos\":["
        for item in array:
            print("item:")
            print(item)
            jsonified += "{"
            jsonified += "\"id\":\"" + item[0] + "\","
            jsonified += "\"title\":\"" + item[1].replace("\"", "'") + "\","
            jsonified += "\"description\":\"" + \
                repr(textwrap.fill(textwrap.dedent(item[2]))).replace("\n", "").replace(
                    "\r", "").replace("\\", "").replace(
                    "\"", "'").replace("'", "") + "\","
            jsonified += "\"publishedAt\":\"" + \
                item[3].strftime("%Y-%m-%d") + "\","
            jsonified += "\"duration\":\"" + item[4] + "\","
            jsonified += "\"channelId\":\"" + item[5] + "\","
            jsonified += "\"channelTitle\":\"" + \
                item[6].replace("\"", "'") + "\","
            jsonified += "\"viewCount\":\"" + str(item[7]) + "\","
            jsonified += "\"likeCount\":\"" + str(item[8]) + "\","
            jsonified += "\"dislikeCount\":\"" + str(item[9]) + "\","
            jsonified += "\"url\":\"" + str(item[10]) + "\","
            jsonified += "\"width\":\"" + str(item[11]) + "\","
            jsonified += "\"height\":\"" + str(item[12]) + "\""
            jsonified += "}"
            jsonified += ","

        jsonified = jsonified[:-1]
        jsonified += "]"
        jsonified += "}"

        return jsonified
