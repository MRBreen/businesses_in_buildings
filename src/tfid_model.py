import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import confusion_matrix

class Tfid_describe(object):
    """A text classifier model:
    - Vectorize the raw text into features.
    - Fit a naive bayes model
    - Find best threshold
    - Make a prediction - both probability and classification for fraud
    """

    def __init__(self, n_features):
        self._vectorizer = TfidfVectorizer(max_features=n_features, stop_words='english')
        self._classifier = MultinomialNB()
        self.n_features = 10000
        self.tfidf = None
        self.thresh_max = 0.5
        self.confusion_matrix = confusion_matrix

    def fit(self, X, y):
        """Fit a text classifier model.

        Keyword arguments:
        X -- A numpy array or list of text fragments, to be used as predictors.
        y -- A numpy array or python list of labels, to be used as responses.

        Returns:
        self: The fit model object.
        """
        self.tfidf = self._vectorizer.fit_transform(X)
        self._classifier.fit(self.tfidf, y)
        return self

    def predict_proba(self, X):
        """Make probability predictions on new data.

        Keyword arguments:
        X -- A numpy array or list of text fragments, to be used as predictors.

        Returns:
        probs: A (n_obs, n_classes) numpy array of predicted class probabilities.
        """
        X = self._vectorizer.transform(X)
        return self._classifier.predict_proba(X)[:,1]

    def predict(self, X):
        """Make class predictions and converts to 1 if active or 0 ignore.
        Since this model uses an ensemble model, we can preserve information
        by also using predict_proba in the final model.

        Keyword arguments:
        X -- A numpy array or list of text fragments, to be used as predictors.

        Returns:
        preds: A (n_obs,) numpy array containing the predicted class for each
        observation (i.e. the class with the maximal predicted class probabilitiy.
        """
        return (self.predict_proba(X) > self.thresh_max).astype(int)

    def get_data(self,datafile):
        '''
        Keyword arguments:
        datafile -- Path of input file (JSON)

        Returns
        pandas df ready for modeling
        '''

        raw_data_df = pd.read_json(datafile)
        raw_data_df['description'].fillna(0, inplace=True)

        data = ['Interest', 'fraudster_event']
        data = (raw_data_df.acct_type.isin(data_list)).astype(int)

        return raw_data_df, fraud

def optimize(self, y, steps=1000):
        """figures out optimal threhold setting parameters
        ...the automatic python best value for a threshold was lacking
        ----------
        X: A numpy array or list of text fragments, to be used as predictors.
        y: A numpy array or python list of labels, to be used as responses.
        steps: number steps from min value to median
        Returns
        -------
        probs: A (n_obs, n_classes) numpy array of predicted class probabilities.
        """

        #y_predict = self._classifier.predict_log_proba(self.tfidf)
        y_predict = self._classifier.predict_proba(self.tfidf)

        print 'low: ' , y_predict[:,1].min()
        high = y_predict[:,1].max()
        print 'high: ' , high
        print 'std:' , y_predict[:,1].std()
        print 'median:' , np.median(y_predict[:,1])
        span = y_predict[:,1].max()-np.median(y_predict[:,1])
        print span
        low = y_predict[:,1].max()

        con_mat = np.zeros((steps, 4))
        print "total in business: " , np.sum(y)
        print "total data: " , y.shape
        print "percent of fraud in data: " , np.sum(y)*1.0/y.shape[0]
        for i, thresh in enumerate(np.linspace(np.median(y_predict[:,1]), high, steps)):
            y_pred_thresh = (y_predict[:,1] > thresh).astype(int)
            con_mat[i] = confusion_matrix(y_pred_thresh, y).flatten()
        profit_mat = np.dot(con_mat, self.profit_weight)
        step_max = profit_mat.argmax(axis = 0)
        self.thresh_max = low-.5*span + step_max*(.5*span)/steps
        self.opt_confusion_mat = con_mat[step_max]
        y_binary = (y_predict[:,1] > self.thresh_max).astype(int)
        return y_binary, y_predict[:,1]


if __name__=='__main__':
    #datafile = '../data/bizmarch.json'
    #myko = MykoModel(GradientBoostingClassifier())
    #X,y = myko.get_data(datafile)
    #X_train, X_test, y_train, y_test = train_test_split(X,y)
    #myko.fit(X_train, y_train)
    #with open('model.pkl', 'w') as f:
    #    pickle.dump(myko, f)
