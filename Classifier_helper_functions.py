import matplotlib.pyplot as plt
import itertools
import numpy as np
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import accuracy_score

def plot_confusion_matrix(cm, classes,
                          normalize=False,
                          title='Confusion matrix',
                          cmap=plt.cm.Blues):
    #Add Normalization Option
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')

    print(cm)

    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes)
    plt.yticks(tick_marks, classes)

    fmt = '.2f'
    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, format(cm[i, j], fmt),
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')

def plot_AUC_ROC(y_score,fpr,tpr):
    sns.set_style("darkgrid", {"axes.facecolor": ".9"})
    print('AUC: {}'.format(auc(fpr, tpr)))
    plt.figure(figsize=(10,8))
    lw = 2
    plt.plot(fpr, tpr, color='darkorange',
         lw=lw, label='ROC curve')
    plt.plot([0, 1], [0, 1], color='navy', lw=lw, linestyle='--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.yticks([i/20.0 for i in range(21)])
    plt.xticks([i/20.0 for i in range(21)])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver operating characteristic (ROC) Curve')
    plt.legend(loc="lower right")
    plt.show()
    
def stratified_k_fold(model_object,n_splits,df,y):
    skf = StratifiedKFold(n_splits=n_splits,shuffle=True)
    test_scores = []
    train_scores = []
    for i in range(n_splits):
        result=next(skf.split(df,y))
        x_train=df.iloc[result[0]]
        x_test=df.iloc[result[1]]
        y_train=y.iloc[result[0]]
        y_test=y.iloc[result[1]]
#         print(y_test)
        model=model_object.fit(x_train,y_train)
        y_hat_train=model_object.predict(x_train)
        y_hat_test=model_object.predict(x_test)
        test_score = accuracy_score(y_hat_test,y_test)
        train_score= accuracy_score(y_hat_train,y_train)
        test_scores.append(test_score)
        train_scores.append(train_score)
    return f'Train scores from each iteration:{train_scores}',f'Average K-Fold train score: {np.mean(train_scores)}',f'Test scores from each iteration:{test_scores}',f'Average K-Fold test score: {np.mean(test_scores)}'