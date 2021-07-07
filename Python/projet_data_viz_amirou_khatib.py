# -*- coding: utf-8 -*-
"""projet_data_viz_Amirou_Khatib.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1v_mCde3jifTT6mepJs3gUhdA5hrkkU4f

A heart attack occurs when the flow of blood to the heart is blocked. The blockage is most often a buildup of fat, cholesterol and other substances, which form a plaque in the arteries that feed the heart (coronary arteries).

Sometimes, a plaque can rupture and form a clot that blocks blood flow. The interrupted blood flow can damage or destroy part of the heart muscle.

A heart attack, also called a myocardial infarction, can be fatal, but treatment has improved dramatically over the years. It's crucial to call 911 or emergency medical help if you think you might be having a heart attack.
"""

#@title
from IPython.display import Image
Image(url='http://25.media.tumblr.com/ca457fb1dc837412a04f9bbd4c97fa81/tumblr_mwksvePcte1rdj8nco2_r1_250.gif')

"""# <font color='blue'>Importing the libraries</font>



"""

#@title
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
import scipy.stats as ss





import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

"""<iframe src="https://www.kaggle.com/embed/creepycrap/heart-attack-pred?cellIds=15&kernelSessionId=65831008" height="300" style="margin: 0 auto; width: 100%; max-width: 950px;" frameborder="0" scrolling="auto" title="Heart Attack 🧡Pred....🤕"></iframe>"""

data_heart=pd.read_csv("heart.csv")
data_o2saturation=pd.read_csv("o2Saturation.csv")

"""# <font color='blue'> The heart dataset </font>"""

#@title
data_heart

"""# <font color='blue'> The O2 saturation dataset </font>"""

#@title
data_o2saturation

"""# <font color='blue'> Formatting the column names </font>"""

#@title

data_o2saturation.columns=["o2_saturation"]
df=data_heart.merge(data_o2saturation,left_index=True,right_index=True)
new_columns=['age','sex','chest pain','resting blood pressure','serum cholesterol in mg/L','fasting blood sugar','resting electrocardiographic result','maximum heart rate achieved','Exercice induced angina','ST depression induced by exercice relative to rest','The slope of the peak exercice ST exercice',' Number of major vessels','thal','Presence of heart disease','o2_saturation']
print(len(new_columns))
df.columns=new_columns

df.describe()

"""
# <font color='blue'> Distribution of heart disease presence/absence
"""

#@title

ax=sns.displot(data_heart.output, kde=False, rug=True)
ax.savefig('count.png', transparent=True)

plt.show()

"""# <font color='blue'> Cheking for null values in the data set"""

#@title

df.isnull().sum()

"""# <font color='blue'> Check if some rows are duplicated


"""

df['chest pain'].unique()
df['thal'].unique()

df[df.duplicated()]
df=df.drop_duplicates()

df[df.duplicated()]

"""# <font color='blue'> Categorical variables

"""

#@title

col_num=['age','resting blood pressure','serum cholesterol in mg/L','maximum heart rate achieved','ST depression induced by exercice relative to rest','o2_saturation']
col_cat=list(set(df.columns)-set(col_num))
col_cat

"""# <font color='blue'> Distribution by classe

"""

#@title

fig, axes = plt.subplots(2, 3, figsize=(14, 10))

fig.suptitle('Distributions par classes')
c=0
for i in range(2):
  for j in range(3):
    col = col_num[c]
    if col != 'output':
      sns.kdeplot(data=df,x=col,hue='Presence of heart disease',ax=axes[i, j],fill=True)
    c +=1
    if c==15:
      break

fig.savefig('distributionparclasse.png', transparent=True)

plt.show()

"""# <font color='blue'> Visualizing continuous data"""

#@title

import matplotlib
from mpl_toolkits.axes_grid1 import make_axes_locatable


df_tension = (df.groupby("Presence of heart disease", as_index=False)["resting blood pressure"]
                      .mean()
                      .sort_values(by="resting blood pressure"))


fig = plt.figure(figsize=(16, 8))
ax = fig.add_subplot()
#df = df.sample(frac=0.9)
# code adapted from https://stackoverflow.com/questions/40814612/map-data-points-to-colormap-with-seaborn-swarmplot
#Create a matplotlib colormap from the sns viridis color palette
cmap = plt.get_cmap("viridis")
# Normalize to the range of possible values from df["c"]
norm = matplotlib.colors.Normalize(vmin=df["serum cholesterol in mg/L"].min(), vmax=df["serum cholesterol in mg/L"].max())
# create a color dictionary (value in c : color from colormap) 
colors = {}
for cval in df["serum cholesterol in mg/L"].values:
    colors.update({cval : cmap(norm(cval))})

# swarmplot is longer to plot because it plots all points individually. Sampling may help. Data missing for the 15th is an issue then.
chart = sns.swarmplot(data=df, x="Presence of heart disease", y="resting blood pressure", 
                      hue="serum cholesterol in mg/L", palette=colors, ax=ax, order=df_tension["Presence of heart disease"],
                      alpha=0.5); # transparency
plt.gca().legend_.remove()

## create colorbar ##
divider = make_axes_locatable(plt.gca())
ax_cb = divider.new_horizontal(size="5%", pad=0.05)
fig.add_axes(ax_cb)
cb1 = matplotlib.colorbar.ColorbarBase(ax_cb, cmap=cmap,
                                norm=norm,
                                orientation='vertical')
cb1.set_label('mmg')
fig.savefig('continuousdata.png', transparent=True)

"""# <font color='blue'> Visualizing categorical *data*"""

#@title

#Pie plots 
fig = plt.figure(figsize=(16, 8))




for col in col_cat[2:]:
    ax=px.pie(df, names= col ,template= "plotly_dark",title=col,hole=0.7)
    ax.update_layout({
      'plot_bgcolor':'rgba(0,0,0)',
      'paper_bgcolor':'rgba(0,0,0,0)',
    })
    ax.write_image("pie"+col+".png")
    ax.show()


#Swarm Plots
#mettre des subplots
for col in col_cat[2:]:
    ax=sns.catplot(kind="swarm", data=df, x=col, y="age", palette="inferno", hue="sex")
    ax.savefig("catplot"+col+".png",transparent=True)


plt.show()

#@title

fig, axes = plt.subplots(3, 3, figsize=(12, 12))

fig.suptitle('Distributions par classes')
c=0
for i in range(3):
  for j in range(3):
    col = col_cat[c]
    sns.countplot(data=df,x='Presence of heart disease',hue=col,ax=axes[i, j])
    c +=1

fig.savefig('distributionparclasse.png', transparent=True)

plt.show()

"""# <font color='blue'> Multivariate analysis"""

#@title

fig=plt.figure(figsize=(10,10))
sns.heatmap(df.corr(),center=True)
fig.savefig('multivariateanalysis.png', transparent=True)

"""# <font color='blue'> Normalization of data"""

X=df.drop(columns=['Presence of heart disease'])
X_norm=(X-X.mean())/X.std()
y=df['Presence of heart disease']

"""# <font color='blue'> Apply PCA on the data"""

#@title

from sklearn.decomposition import PCA
pca=PCA(n_components=0.95)
fig=plt.figure(figsize=(10,10))
reduced_df=pca.fit_transform(X_norm)
pca_data = np.vstack((reduced_df[:,0:2].T, df['Presence of heart disease'])).T
pca_df = pd.DataFrame(data=pca_data, columns=("1st_principal", "2nd_principal","Presence of heart disease"))
#sns.scatterplot( x=reduced_df[:,0], y=reduced_df[:,1],c=df['Presence of heart disease'])
sns.FacetGrid(pca_df, hue="Presence of heart disease", size=6).map(plt.scatter, '1st_principal', '2nd_principal').add_legend()
fig.savefig('pca.png', transparent=True)

plt.show()

reduced_df.shape

"""# <font color='blue'> Variance as a function of the number of components"""

#@title

fig=plt.figure(figsize=(10,10))
plt.plot(pca.explained_variance_)
fig.savefig('plotpca.png', transparent=True)

"""# <font color='blue'> Applying the spectral embedding on the data"""

#@title

from sklearn.manifold import SpectralEmbedding
se=SpectralEmbedding(n_jobs=-1,n_components=4)
se_df=se.fit_transform(X_norm)
se_data = np.vstack((se_df[:,0:2].T, df['Presence of heart disease'])).T
fig=plt.figure(figsize=(15,15))

# creating a new data fram which help us in ploting the result data
se_df = pd.DataFrame(data=se_data, columns=("1st_principal", "2nd_principal","Presence of heart disease"))
sns.FacetGrid(se_df, hue="Presence of heart disease", size=6).map(plt.scatter, '1st_principal', '2nd_principal').add_legend()
fig.savefig('spectalembedding.png', transparent=True)

plt.show()

"""# <font color='blue'> Applying T-SNE on the *data*

"""

#@title

from sklearn.manifold import TSNE
tsne = TSNE(n_components=2, init='random', random_state=42, perplexity=30)
tsne_df = tsne.fit_transform(X) 
tsne_data = np.vstack((tsne_df[:,0:2].T, df['Presence of heart disease'])).T

fig=plt.figure(figsize=(10,10))
# creating a new data fram which help us in ploting the result data
tsne_df = pd.DataFrame(data=tsne_data, columns=("1st_principal", "2nd_principal","Presence of heart disease"))
sns.FacetGrid(tsne_df, hue="Presence of heart disease", size=6).map(plt.scatter, '1st_principal', '2nd_principal').add_legend()
fig.savefig('tsne.png', transparent=True)
plt.show()

"""# <font color='blue'> Applying uMap on the *data*"""


#@title

import umap
u_df=umap.UMAP().fit_transform(X_norm)
u_data = np.vstack((u_df[:,0:2].T, df['Presence of heart disease'])).T
# creating a new data fram which help us in ploting the result data
u_df = pd.DataFrame(data=u_data, columns=("1st_principal", "2nd_principal", "Presence of heart disease"))
sns.FacetGrid(u_df, hue="Presence of heart disease", size=6).map(plt.scatter, '1st_principal', '2nd_principal').add_legend()
plt.show()

"""# <font color='blue'> Using xgboost classifer"""

#@title

y=df['Presence of heart disease']
from sklearn.model_selection import train_test_split
xtrain,xtest,ytrain,ytest = train_test_split(X,y,test_size=0.2,random_state=20)
from sklearn.metrics import accuracy_score

#@title

from xgboost import XGBClassifier
xgb=XGBClassifier(n_estimators=35)
xgb.fit(xtrain,ytrain)
y_pred=xgb.predict(xtest)
print('test accuracy:',round(accuracy_score(ytest,y_pred),2))

#@title

dic={'colonne':X.columns,
    'importance':xgb.feature_importances_
}
fig=plt.figure(figsize=(10,10))

d=pd.DataFrame(dic).sort_values(by='importance')
plt.figure(figsize=(10,6))
plt.barh(d['colonne'],d['importance'])
fig.savefig('xgboost.png', transparent=True)
plt.show()

"""# <font color='blue'> Using Random Forest classifer"""

#@title

from sklearn.ensemble import RandomForestClassifier
rf=RandomForestClassifier(n_jobs=-1,random_state=15)
rf.fit(xtrain,ytrain)
y_pred=rf.predict(xtest)
print('test accuracy:',round(accuracy_score(ytest,y_pred),2))

#@title

dic={'colonne':X.columns,
    'importance':rf.feature_importances_
}
fig=plt.figure(figsize=(10,10))

d=pd.DataFrame(dic).sort_values(by='importance')
plt.figure(figsize=(10,6))
plt.barh(d['colonne'],d['importance'])
fig.savefig('randomforest.png', transparent=True)

plt.show()

