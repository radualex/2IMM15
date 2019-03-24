def add_tuples_to_dictionary(set, videoId, dictionary):
    for tuple in set:
        if tuple in dictionary.keys():
            dictionary[tuple].append(videoId)
        else:
            dictionary[tuple] = []
            dictionary[tuple].append(videoId)
