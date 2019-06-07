import multiprocessing
from gensim.models import Word2Vec
import itertools
import numpy as np


def sum_matrix(matrix):
    """
    sum the matrix to a vector
    :param matrix: np.matrix
    :return: np.array
    """
    return np.sum(matrix,axis=0)


def avr_matrix(matrix):
    """
    avr the matrix to a vector
    :param matrix: np.matrix
    :return: np.array
    """
    return np.average(matrix,axis=0)


class HashTag2Vec:
    model = None
    vocab = None
    drop = None
    permutation = None
    method = None

    def __init__(self,permutation=True,permutation_drop=0.5,method="sum"):
        """
        :param permutation: boolean
        :param permutation_drop: float
        :param method: str sum => sum the vectors of tags avr => getting the avr of the tags
        """
        self.drop = permutation_drop
        self.permutation = permutation
        if method == "sum":
            self.method = sum_matrix
        elif method == "avr":
            self.method = avr_matrix
        else:
            raise Exception("method must be sum or avr default sum ")

    def train(self,tags,window=6, alpha=0.03, epochs=30,vic_size=150,min_count=.3):
        """
        :param min_count: int  Ignores all words with total absolute frequency lower than this - (2, 100)
        :param tags: Tag set list of hashTags
        :param window:  int - The maximum distance between the current and predicted word within a sentence.
         E.g. window words on the left and window words on the left of our target - (2, 10)
        :param alpha: float - The initial learning rate - (0.01, 0.05)
        :param epochs: int - Number of iterations (epochs) over the corpus - [10, 20, 30]
        :param vic_size:int - Dimensionality of the feature vectors. - (50, 300)
        :return: None
        """
        if self.permutation:
            tags = self._permutation(tags,drop=1)
        tags = self.flat(tags)
        cores = multiprocessing.cpu_count()
        self.model = Word2Vec(min_count=min_count,
                     window=window,
                     size=vic_size,
                     sample=6e-5,
                     alpha=alpha,
                     min_alpha=0.0007,
                     negative=20,
                     workers=cores)
        self.model.build_vocab([tags])
        self.model.train(tags, total_examples=self.model.corpus_count, epochs=epochs)


    @staticmethod
    def _permutation(tags, cut_window=0,drop=0.5):
        """
        :param tags: list of list tags
        :param cut_window: int
        :param drop: float the parentage of the output
        :return: list of list
        """
        result = []
        for op in tags:
            if type(op) != type(str):
                result += [op]
            p = list(itertools.permutations(op,len(op)-cut_window))
            p = [list(data) for data in p]
            result += p

        return result[0:int(len(result)*drop)]

    @staticmethod
    def flat(tags):
        """
        the function convert 2D list to 1 D
        :param tags: list of list of tag.type
        :return: list of tag.type
        """
        result =[]
        for tag in tags:
            result+=tag
        return result

    def op2vic(self,tags):
        """
        :param tags: list of tags that represent the opinion
        :return: numpy.array representations of opinion
        """
        if self.model is None:
            raise Exception("model is not trained yet")
        opinion_matrix = [self.model.wv[tag] for tag in tags]
        return self.method(opinion_matrix)
