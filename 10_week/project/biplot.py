import matplotlib.pyplot as plt

def biplot(score,coeff,labels=None,ax=None):
    """Biplot for PCA
    
    score : 2D array of shape (_,2)
        Projected data.
    coeff : 2D array of shape (_,2)
        Eigenvectors projected accordingly into 2D.
    labels : list of str
        Labels for coeff.
    ax : matplotlib ax object
        Plot on this ax object, if given.

    Adapted from https://stackoverflow.com/a/46766116
    """
    if ax is None:
        ax = plt.gca()
    
    xs = score[:,0]
    ys = score[:,1]
    n = coeff.shape[0]
    scalex = 1.0/(xs.max() - xs.min())
    scaley = 1.0/(ys.max() - ys.min())
    ax.scatter(xs * scalex,ys * scaley, c = '#add8e6', alpha = 0.3)
    for i in range(n):
        ax.arrow(0, 0, coeff[i,0], coeff[i,1],color = 'r',alpha = 1)
        if labels is None:
            ax.text(coeff[i,0]* 1.15, coeff[i,1] * 1.15, "Var"+str(i+1), color = 'k', ha = 'center', va = 'center')
        else:
            ax.text(coeff[i,0]* 1.15, coeff[i,1] * 1.15, labels[i], color = 'k', ha = 'center', va = 'center')
    ax.set_xlim(-1,1)
    ax.set_ylim(-1,1)
    ax.set_xlabel("PC{}".format(1))
    ax.set_ylabel("PC{}".format(2))
    ax.grid()
