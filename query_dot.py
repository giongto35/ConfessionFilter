def classify(inverted_index, category, query, top_k=100, threshold=0.5):
    n_words = len(query)

    n_docs = inverted_index.n_docs
    distance = [float('inf')] * n_docs

    for i in range(n_words):
        if query[i] > 0:
            for j in range(inverted_index.index[i]):
                id = inverted_index.index[i][j]
                if distance[id] == float('inf'):
                    distance[id] = 0
                distance[id] = distance[id] + query[i] * inverted_index.tfidf[i][j]

    sorted(range(n_docs), key=lambda k: distance[k])
    top_k = min(top_k, n_docs)

    n_correct = 0
    for i in range(top_k):
        if category[i] == 1:
            n_correct = n_correct + 1

    if float(n_correct) / top_k > threshold:
        return 'OK'
    else:
        return 'ERR'
