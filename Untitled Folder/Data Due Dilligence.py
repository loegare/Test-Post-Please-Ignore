
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.formula.api as smf
import statsmodels.api as sm
import  scipy.stats
pd.options.display.float_format = '{:,.2f}'.format


# In[2]:


#Adjust graph size
plt.rcParams['figure.figsize'] = [20, 10]


# In[3]:


from IPython.core.display import display, HTML
#Increase output window size
display(HTML("<style>.container { width:100% !important; }</style>"))


# In[4]:


df=pd.read_excel('RD.xlsx')


# In[5]:


#Add feild MIncome - Monthly Household Income
df['MIncome'] = (df['HHIncome']/12)


# In[6]:


#Add feild SpendToIncome - Ratio of monthly spending to monthly household income
df['SpendToIncome'] = df['CardSpendMonth']/df['MIncome']


# In[7]:


# Add feild AgeBracket, splitting the group age into groups of approx 10 years
conditions = [df['Age'] <= 25,
              df['Age'] <= 35,
              df['Age'] <= 45,
              df['Age'] <= 55,
              df['Age'] <= 65
             ]
selections = ['18-25','26-35','36-45','46-55','56-65']
df['AgeBracket'] = np.select(conditions,selections,'65+')


# In[8]:


# Add feild EduBracket, splitting the group age into groups of approx 10 years
conditions = [df['EducationYears'] <= 8,
              df['EducationYears'] <= 12,
              df['EducationYears'] <= 16
             ]
selections = ['1. Elementary','2. Secondary','3. Post-Secondary']
df['EduBracket'] = np.select(conditions,selections,'4. Graduate')


# In[9]:


#View simple numerical statistics on all feilds
df.describe()


# In[10]:


#Split HHIncome into 5 sections and SpendToIncome into 10 sections
#HHIncomeBracket only contains the low value of the bracket to assist with ordering of the tables and graphs
df['HHIncomeBracket']=pd.qcut(df.HHIncome,5).astype(str).str.strip('()[]').str.split(', ').str[0].astype(np.float64)
df['SpendToIncomeBracket']=pd.qcut(df.SpendToIncome,10).astype(str)#.str.strip('()[]').str.replace(', ','-')


# In[11]:


df.hist('SpendToIncome',bins=100)


# In[12]:


#Bivariate Analysis of LoanDefault and SpendToIncome
print('\n','Mean')
display(pd.pivot_table(df,
               index=['LoanDefault'],
               values='SpendToIncome',
              aggfunc=np.mean))
print('\n','Count')
display(pd.pivot_table(df,
               index=['LoanDefault'],
               values='SpendToIncome',
              aggfunc='count'))
table = pd.pivot_table(df,
               index=['LoanDefault'],
               values='SpendToIncome',
              aggfunc=len,margins=True)
table3 = table.div( table.iloc[-1,:], axis=1 )

print('\n','%')
display(table3)
display(df.boxplot('SpendToIncome','LoanDefault'))


# In[13]:


#Multivariate Analysis of LoanDefault and SpendToIncome split by Region
print('\n','Mean')
display(pd.pivot_table(df,
               index=['LoanDefault'],
               columns='Region',
               values='SpendToIncome',
              aggfunc=np.mean))
print('\n','Count')
table = pd.pivot_table(df,
               index=['LoanDefault'],
               columns='Region',
               values='SpendToIncome',
              aggfunc=len,margins=True)
display(table)
table2 = table.div( table.iloc[:,-1], axis=0 )
table3 = table.div( table.iloc[-1,:], axis=1 )
print('\n','% Row')
display(table2)
print('\n','% Column')
display(table3)

#Chi-Square test for independence between Region and LoanDefault
chisq = scipy.stats.chi2_contingency(pd.crosstab(df['Region'],df['LoanDefault']))
print('Chi-Square:',chisq[0])
print('p:',chisq[1])

df.boxplot('SpendToIncome',['Region','LoanDefault'])


# In[14]:


#Multivariate Analysis of LoanDefault and SpendToIncome split by Gender
print('\n','Mean')
display(pd.pivot_table(df,
               index=['LoanDefault'],
               columns='Gender',
               values='SpendToIncome',
              aggfunc=np.mean))
print('\n','Count')
table = pd.pivot_table(df,
               index=['LoanDefault'],
               columns='Gender',
               values='SpendToIncome',
              aggfunc=len,margins=True)
display(table)
table2 = table.div( table.iloc[:,-1], axis=0 )
table3 = table.div( table.iloc[-1,:], axis=1 )
print('\n','% Row')
display(table2)
print('\n','% Column')
display(table3)

#Chi-Square test for independence between Gender and LoanDefault
chisq = scipy.stats.chi2_contingency(pd.crosstab(df['Gender'],df['LoanDefault']))
print('Chi-Square:',chisq[0])
print('p:',chisq[1])

df.boxplot('SpendToIncome',['Gender','LoanDefault'])


# In[15]:


#Bivariate Analysis of LoanDefault and SpendToIncome
#Looking at SpentToIncomeBrackets
print('\n','Count')
display(pd.pivot_table(df,
               index=['LoanDefault'],
               columns='SpendToIncomeBracket',
               values='SpendToIncome',
              aggfunc='count'))
table = pd.pivot_table(df,
               index=['LoanDefault'],
               columns='SpendToIncomeBracket',
               values='SpendToIncome',
              aggfunc=len,margins=True)
table3 = table.div( table.iloc[-1,:], axis=1 )
print('\n','% Column')
display(table3)

#Chi-Square test for independence between Spend to Income Brackets and LoanDefault
chisq = scipy.stats.chi2_contingency(pd.crosstab(df['SpendToIncomeBracket'],df['LoanDefault']))
print('Chi-Square:',chisq[0])
print('p:',chisq[1])


# In[16]:


#Multivariate Analysis of LoanDefault and SpendToIncome split by AgeBracket
print('\n','Mean')
display(pd.pivot_table(df,
               index=['LoanDefault'],
               columns='AgeBracket',
               values='SpendToIncome',
              aggfunc=np.mean))
print('\n','Count')
table = pd.pivot_table(df,
               index=['LoanDefault'],
               columns='AgeBracket',
               values='SpendToIncome',
              aggfunc=len,margins=True)
display(table)
table2 = table.div( table.iloc[:,-1], axis=0 )
table3 = table.div( table.iloc[-1,:], axis=1 )
print('\n','% Row')
display(table2)
print('\n','% Column')
display(table3)

#Chi-Square test for independence between Age Brackets and LoanDefault
chisq = scipy.stats.chi2_contingency(pd.crosstab(df['AgeBracket'],df['LoanDefault']))
print('Chi-Square:',chisq[0])
print('p:',chisq[1])

df.boxplot('SpendToIncome',['AgeBracket','LoanDefault'])


# In[17]:


#Multivariate Analysis of LoanDefault and SpendToIncome split by Education Level
print('\n','Mean')
display(pd.pivot_table(df,
               index=['LoanDefault'],
               columns='EduBracket',
               values='SpendToIncome',
              aggfunc=np.mean))
print('\n','Count')
table = pd.pivot_table(df,
               index=['LoanDefault'],
               columns='EduBracket',
               values='SpendToIncome',
              aggfunc=len,margins=True)
display(table)
table2 = table.div( table.iloc[:,-1], axis=0 )
table3 = table.div( table.iloc[-1,:], axis=1 )
print('\n','% Row')
display(table2)
print('\n','% Column')
display(table3)

#Chi-Square test for independence between Education Level and LoanDefault
chisq = scipy.stats.chi2_contingency(pd.crosstab(df['EduBracket'],df['LoanDefault']))
print('Chi-Square:',chisq[0])
print('p:',chisq[1])

df.boxplot('SpendToIncome',['EduBracket','LoanDefault'])


# In[18]:


#Multivariate Analysis of LoanDefault and SpendToIncome split by Voting History
print('\n','Mean')
display(pd.pivot_table(df,
               index=['LoanDefault'],
               columns='Votes',
               values='SpendToIncome',
              aggfunc=np.mean))
print('\n','Count')
table = pd.pivot_table(df,
               index=['LoanDefault'],
               columns='Votes',
               values='SpendToIncome',
              aggfunc=len,margins=True)
display(table)
table2 = table.div( table.iloc[:,-1], axis=0 )
table3 = table.div( table.iloc[-1,:], axis=1 )
print('\n','% Row')
display(table2)
print('\n','% Column')
display(table3)

#Chi-Square test for independence between Voting History and LoanDefault
chisq = scipy.stats.chi2_contingency(pd.crosstab(df['Votes'],df['LoanDefault']))
print('Chi-Square:',chisq[0])
print('p:',chisq[1])

df.boxplot('SpendToIncome',['Votes','LoanDefault'])


# In[19]:


#Multivariate Analysis of LoanDefault and SpendToIncome split by Income Brackets
print('\n','Mean')
display(pd.pivot_table(df,
               index=['LoanDefault'],
               columns='HHIncomeBracket',
               values='SpendToIncome',
              aggfunc=np.mean))
print('\n','Count')
table = pd.pivot_table(df,
               index=['LoanDefault'],
               columns='HHIncomeBracket',
               values='SpendToIncome',
              aggfunc=len,margins=True)
display(table)
table2 = table.div( table.iloc[:,-1], axis=0 )
table3 = table.div( table.iloc[-1,:], axis=1 )
print('\n','% Row')
display(table2)
print('\n','% Column')
display(table3)

#Chi-Square test for independence between Income Bracket and LoanDefault
chisq = scipy.stats.chi2_contingency(pd.crosstab(df['HHIncomeBracket'],df['LoanDefault']))
print('Chi-Square:',chisq[0])
print('p:',chisq[1])

df.boxplot('SpendToIncome',['HHIncomeBracket','LoanDefault'])


# In[20]:


#Multivariate Analysis of LoanDefault and SpendToIncome split by Home Ownership
print('\n','Mean')
display(pd.pivot_table(df,
               index=['LoanDefault'],
               columns='HomeOwner',
               values='SpendToIncome',
              aggfunc=np.mean))
print('\n','Count')
table = pd.pivot_table(df,
               index=['LoanDefault'],
               columns='HomeOwner',
               values='SpendToIncome',
              aggfunc=len,margins=True)
display(table)
table2 = table.div( table.iloc[:,-1], axis=0 )
table3 = table.div( table.iloc[-1,:], axis=1 )
print('\n','% Row')
display(table2)
print('\n','% Column')
display(table3)

#Chi-Square test for independence between Home Ownership and LoanDefault
chisq = scipy.stats.chi2_contingency(pd.crosstab(df['HomeOwner'],df['LoanDefault']))
print('Chi-Square:',chisq[0])
print('p:',chisq[1])

df.boxplot('SpendToIncome',['HomeOwner','LoanDefault'])


# In[21]:


#Multivariate Analysis of LoanDefault and SpendToIncome split by Internet Connected Devices
print('\n','Mean')
display(pd.pivot_table(df,
               index=['LoanDefault'],
               columns='Internet',
               values='SpendToIncome',
              aggfunc=np.mean))
print('\n','Count')
table = pd.pivot_table(df,
               index=['LoanDefault'],
               columns='Internet',
               values='SpendToIncome',
              aggfunc=len,margins=True)
display(table)
table2 = table.div( table.iloc[:,-1], axis=0 )
table3 = table.div( table.iloc[-1,:], axis=1 )
print('\n','% Row')
display(table2)
print('\n','% Column')
display(table3)


#Chi-Square test for independence between Internet Connected Devices and LoanDefault
chisq = scipy.stats.chi2_contingency(pd.crosstab(df['Internet'],df['LoanDefault']))
print('Chi-Square:',chisq[0])
print('p:',chisq[1])

df.boxplot('SpendToIncome',['Internet','LoanDefault'])

