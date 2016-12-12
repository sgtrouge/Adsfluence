import lda
import numpy as np
import json
from scipy import sparse
from nltk.corpus import stopwords

def find_vocab(list_doc):
    pass

vocab_to_id = {}
def readTweet(filename):
    f = open(filename, 'r')
    global vocab_to_id
    data = f.read()
    splits = data.split('}{')
    splits[0] = splits[0][1:]
    # For some reason the last one isn't built correctly, need to append ]]
    splits[-1] = splits[-1][:-1] +']]'
    ider = 0
    vocab = []
    for js in splits:
        try:
            jss = '{' + js + '}'
            tweet_map = json.loads(jss)
            content = tweet_map["content"]
            words = content.split()
            for word in words:
                if word not in vocab_to_id:
                    if word in stopwords.words('english'):
                        continue
                    vocab_to_id[word] = ider
                    ider += 1
                    vocab.append(word)

        except:
            pass
    print "Number of words: " , len(vocab_to_id)
    sparse_data = []
    sparse_row_ind = []
    sparse_col_ind = []

    doc_id = 0
    # Now re-read and make the scipy matrix
    print "Number of documents: ", len(splits)
    for js in splits:
        vocab_count = {}
        try:
            jss = '{' + js + '}'
            tweet_map = json.loads(jss)
            content = tweet_map["content"]
            words = content.split()
            for word in words:
                if word in stopwords.words('english'):
                    continue
                if word in vocab_count:
                    vocab_count[word] += 1
                else:
                    vocab_count[word] = 1
            for word, count in vocab_count.iteritems():
                sparse_data.append(count)
                sparse_row_ind.append(doc_id)
                sparse_col_ind.append(vocab_to_id[word])
            doc_id += 1
        except:
            pass

    sparse_tweet_vocab = sparse.coo_matrix((sparse_data, (sparse_row_ind, sparse_col_ind)))
    X = sparse.coo_matrix((sparse_data, (sparse_row_ind, sparse_col_ind)))
    model = lda.LDA(n_topics=5, n_iter=1500, random_state=1)
    model.fit(X)  # model.fit_transform(X) is also available
    topic_word = model.topic_word_  # model.components_ also works
    n_top_words = 8
    for i, topic_dist in enumerate(topic_word):
        topic_words = np.array(vocab)[np.argsort(topic_dist)][:-(n_top_words+1):-1]
        topic_words = [x.encode('utf-8') for x in topic_words]
        print('Topic {}: {}'.format(i, ' '.join(topic_words)))

readTweet('./goodData/thanksgiving.txt')
# readTweet('./thanksgiving/thanks.txt')