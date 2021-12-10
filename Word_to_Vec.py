from gensim.models import Word2Vec
import multiprocessing

d = Word2Vec.load('word2vec_model_parsivar/w2v_150k_parsivar_300.model.trainables.syn1neg.npy')

print(d)