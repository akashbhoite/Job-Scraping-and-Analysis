# Importing the necessary libraries

import pandas as pd
import nltk
from nltk import word_tokenize
from nltk.corpus import stopwords
stop_words = stopwords.words('english')
import seaborn as sns
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import re
import string
get_ipython().run_line_magic('config', "InlineBackend.figure_format='retina'")

df = pd.read_csv('linkedinfinal.csv')

df.dropna(inplace=True)

df['State'] = df['State'].str.strip(' ')

plt.figure(figsize=(10,5))
df['State'].value_counts().head(10).plot(kind='barh')
plt.xticks(rotation = 0,fontsize=15)
plt.yticks(rotation = 0,fontsize=15)
plt.title('States with most Data-Science Jobs', fontsize = 15)


plt.figure(figsize=(10,5))
df['City'].value_counts().head(10).plot(kind='barh')
plt.xticks(rotation = 0,fontsize=15)
plt.yticks(rotation = 0,fontsize=15)
plt.title('Cities with most Data-Science Jobs', fontsize = 15)


def cleanTokens(desc):
    desc = word_tokenize(desc)
    desc = [word.lower() for word in desc if word.isalpha() and len(word) > 2]
    desc = [word for word in desc if word not in stop_words]
    return desc


tags_df=df['Description'].apply(cleanTokens)

from collections import Counter
result = tags_df.apply(Counter).sum().items()
result = sorted(result, key=lambda kv: kv[1],reverse=True)
result_series = pd.Series({k: v for k, v in result})


libraries = ["nltk","pandas","numpy","matplotlib","sklearn"]
tools = ["tableau","excel","python","aws","sql"]
ML = ["theano", "pytorch", "tensorflow", "keras","opencv"]
big_data = ["hadoop","bigquery","spark","storm"]
IDE = ["jupyter","pycharm","spyder","idle"]

filter_series = result_series.filter(items=tools)
filter_series.plot(kind='bar',figsize=(10,4))
plt.xticks(rotation = 0, fontsize=15)
plt.yticks(rotation = 0, fontsize=15)
plt.title('Popular Software/Programming lanaguges required for DS/ML Jobs',fontsize=15)


filter_series = result_series.filter(items=libraries)
filter_series.plot(kind='bar',figsize=(10,4))
plt.xticks(rotation = 0, fontsize=15)
plt.yticks(rotation = 0, fontsize=15)
plt.title('Popular PYTHON Libraries required for DS/ML Jobs',fontsize=15)


filter_series = result_series.filter(items=ML)
filter_series.plot(kind='bar',figsize=(10,4))
plt.xticks(rotation = 0, fontsize=15)
plt.yticks(rotation = 0, fontsize=15)
plt.title('Popular Machine Learning platforms',fontsize=15)


filter_series = result_series.filter(items=big_data)
filter_series.plot(kind='bar',figsize=(10,4))
plt.xticks(rotation = 0, fontsize=15)
plt.yticks(rotation = 0, fontsize=15)
plt.title('Popular Big Data Skills',fontsize=15)


filter_series = result_series.filter(items=IDE)
filter_series.plot(kind='bar',figsize=(10,4))
plt.xticks(rotation = 0, fontsize=15)
plt.yticks(rotation = 0, fontsize=15)
plt.title('Popular Python IDE/Notebooks',fontsize=15)


df_fang = df[df['Company'].isin(['Facebook','Amazon','Netflix','Google',
                                 'Twitter','Tesla','Microsoft','Apple','Uber'])].reset_index(drop = True)

plt.figure(figsize=(15,8))
plt.subplot(221)
plt.xlabel('City',fontsize=20)
plt.xticks(rotation = 90,fontsize=15)
plt.yticks(rotation = 0,fontsize=15)
plt.title('Data Science Positions by FANG across States', fontsize=15)
sns.countplot(df_fang['State'])
plt.subplot(222)
plt.xlabel('City',fontsize=20)
plt.xticks(rotation = 90,fontsize=15)
plt.yticks(rotation = 0,fontsize=15)
plt.title('Data Science Positions by FANG across Cities', fontsize=15)
sns.countplot(df_fang['City'])


def get_description(Name):
    
    d = []
    df_d = df[df['Company'] == Name]
    df_d.reset_index(drop=True)
    for i in range(0,len(df_d)):
        desc = df_d['Description'].iloc[i]
        d.append(desc)
        f = ''.join(d)
        
    return f

Amazon = get_description('Amazon')
Apple = get_description('Apple')
Netflix = get_description('Netflix')
Microsoft = get_description('Microsoft')
Twitter = get_description('Twitter')
Google = get_description('Google')
Tesla = get_description('Tesla')


df_ub = df[df['Company'] == 'Uber']
df_ub.reset_index(drop=True,inplace=True)
df_fb = df[df['Company'] == 'Facebook']
df_fb.reset_index(drop=True,inplace=True)


desc1 = df_ub['Description'][0]
tostr= ''.join(desc1)
Uber = []
Uber.append(tostr)


desc2 = df_fb['Description'][0]
tostr2 = ''.join(desc2)
fb = []
fb.append(tostr2)


df_description= pd.DataFrame({'Amazon':Amazon,'Apple':Apple,'Netflix':Netflix,
                              'Microsoft': Microsoft,'Twitter':Twitter,
                              'Google':Google,'Tesla':Tesla,'Uber':Uber,'Facebook':fb},index=['description'])

df_description = df_description.transpose()

def clean_text(text):
    '''Make text lowercase, remove text in square brackets, remove punctuation and remove words containing numbers.'''
    text = text.lower()
    text = re.sub('\[.*?\]’', '', text)
    text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
    text = re.sub('\w*\d\w*', '', text)
    text = text.replace("’","")
    return text

round1 = lambda x: clean_text(x)

def final_clean(texts):
    toks = word_tokenize(texts)
    stp = [word for word in toks if word not in stop_words]
    stpr = ' '.join(stp)
    return stpr

final_cl = lambda x: final_clean(x)

data_clean = pd.DataFrame(df_description.description.apply(round1))

more_stp_words = ['data','people','work','together','technical','facebooks',
                  'gender','business','experience','amazon','facebook','science',
                  'building','analysis','conducting','working', 'uber', 'variety',
                  'development','opportunity','solutions','netflix','apple','microsoft',
                  'twitter','analytic','engineering','computer','product','scientist',
                  'build','candidate','role','position','applicant','analytics',
                  'analytical','products','team','across','applicants','strong',
                  'youll','member','members','skills','quality','developing',
                  'tooling','tools','problem','problems','social','environmental',
                  'design','make','provide','knowledge','software','teams','andor',
                  'communicate','partners','move','novel','world']
stop_words.extend(more_stp_words)

data_clean_final = pd.DataFrame(data_clean.description.apply(final_cl))

wc = WordCloud(stopwords=stop_words, background_color="white", colormap="Dark2",
               max_font_size=150, random_state=42)

plt.rcParams['figure.figsize'] = [16, 8]
df_cols = data_clean_final.transpose()
comp_names = df_cols.columns
# Create subplots for each comedian
for index, company in enumerate(df_cols.columns):
    wc.generate(data_clean_final.description[company])
    
    plt.subplot(3, 4, index+1)
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.title(comp_names[index], fontsize=16)
    
plt.show()

from sklearn.feature_extraction.text import CountVectorizer

cv = CountVectorizer(stop_words=stop_words)
data_cv = cv.fit_transform(data_clean_final.description)
data_dtm = pd.DataFrame(data_cv.toarray(), columns=cv.get_feature_names())
data_dtm.index = data_clean.index
data_dtm

data_dtm = data_dtm.transpose()

top_dict = {}
for c in data_dtm.columns:
    top = data_dtm[c].sort_values(ascending=False).head(30)
    top_dict[c]= list(zip(top.index, top.values))

print('The top words in each job description are as mentioned below: \n')
for company, top_words in top_dict.items():
    print(company)
    print(', '.join([word for word, count in top_words[0:14]]))
    print('---')