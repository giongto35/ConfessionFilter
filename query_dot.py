def classify(inverted_index, category, query, top_k=50, ratio_threshold=0.60, distance_threshold=0.0003):
    n_words = len(query)

    n_docs = inverted_index.n_docs
    distance = [float('inf')] * n_docs

    for i in range(n_words):
        if query[i] > 0:
            for j in range(len(inverted_index.index[i])):
                id = inverted_index.index[i][j]
                if distance[id] == float('inf'):
                    distance[id] = 0
                distance[id] = distance[id] + query[i] * inverted_index.tfidf[i][j]

    ranked_list = sorted(range(n_docs), key=lambda k: distance[k])
    top_k = min(top_k, n_docs)

    n_correct = 0
    for i in range(min(top_k, n_docs)):
        id = ranked_list[i]
        if distance[id] == float('inf') or distance[id] > distance[ranked_list[0]] * 2 or distance[id] > distance_threshold:
            top_k = i
            break
        if category[id] == 1:
            n_correct = n_correct + 1

    if top_k == 0:
        return 'ERR'

    print '%d / %d - %f, %f' % (n_correct, top_k, distance[ranked_list[0]], distance[ranked_list[top_k - 1]])

    if float(n_correct) / top_k > ratio_threshold:
        return 'OK'
    else:
        return 'ERR'
