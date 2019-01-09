#!/usr/bin/env python
# coding: utf-8

# > **Tip**: Welcome to the Investigate a Dataset project! You will find tips in quoted sections like this to help organize your approach to your investigation. Before submitting your project, it will be a good idea to go back through your report and remove these sections to make the presentation of your work as tidy as possible. First things first, you might want to double-click this Markdown cell and change the title so that it reflects your dataset and investigation.
# 
# # Project: Investigate No-show appointments Dataset
# 
# ## Table of Contents
# <ul>
# <li><a href="#intro">Introduction</a></li>
# <li><a href="#wrangling">Data Wrangling</a></li>
# <li><a href="#eda">Exploratory Data Analysis</a></li>
# <li><a href="#conclusions">Conclusions</a></li>
# </ul>

# <a id='intro'></a>
# ## Introduction
# >* This dataset collects information from 100k medical appointments in Brazil and is focused on the question of whether or not patients show up for their appointment. A number of characteristics about the patient are included in each row.
# 
# >* ScheduledDay: tells us on what day the patient set up their appointment.
# Neighborhood: indicates the location of the hospital.
# Scholarship: indicates whether or not the patient is enrolled in Brasilian welfare program Bolsa Família.
# No-show: it says ‘No’ if the patient showed up to their appointment, and ‘Yes’ if they did not show up.
# I performed my analysis to answer the following questions:
# 
# >*1. Which is the most age category patients have attended to thier appointment?
# 
# >*2. Which Gender have the highest percentage of attending to the appointments?
# 

# In[2]:


# Use this cell to set up import statements for all of the packages that you
#   plan to use.

# Remember to include a 'magic word' so that your visualizations are plotted
#   inline with the notebook. See this page for more:
#   http://ipython.readthedocs.io/en/stable/interactive/magics.html
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')


# <a id='wrangling'></a>
# ## Data Wrangling
# 
# > **First**: In this section of the report, Import the necessary package and use pd.read_csv to load the movie dataset, then print the first rows.
# 
# 
# ### General Properties

# In[3]:


# Load your data and print out a few lines. Perform operations to inspect data
#   types and look for instances of missing or possibly errant data.
df= pd.read_csv('noshowappointments-kagglev2-may-2016.csv')
df.head()


# In[4]:


df.shape


# It has 110527 columns and 14 rows.

# In[5]:


df.info()


# In[6]:


df.describe()


# In[7]:


df.isnull().sum()


# Great.. There are no missing values.

# In[8]:


df.duplicated().sum()


# Great.. There are no duplicated values too..

# In[9]:


df.nunique()


# 
# ### Data Cleaning (Correting Typos)
# >**In this step**: I will do
# >* using .rename function to rename typos coulmns.
# 

# In[10]:


#After discussing the structure of the data and any problems that need to be
#cleaned, perform those cleaning steps in the second part of this section.
df.rename(columns = {'Hipertension': 'Hypertension', 'Handcap': 'Handicap', 'No-show': 'No_Show'}, inplace=True)
print(df.columns)


# ## Converting into DateTime

# I want to convert the two columns (AppointmentDay & ScheduledDay) into a correct Datetime format.

# In[11]:


df.ScheduledDay = df.ScheduledDay.apply(np.datetime64)
df.AppointmentDay = df.AppointmentDay.apply(np.datetime64)


# ## Checking datatypes to observe any outliers or unlogic values

# In[12]:


print('Gender:',df.Gender.unique())
print('Age:',sorted(df.Age.unique()))
print('Scholarship:',df.Scholarship.unique())
print('Hypertension:',df.Hypertension.unique())
print('Diabetes:',df.Diabetes.unique())
print('Alcoholism:',df.Alcoholism.unique())
print('Handicap:',df.Handicap.unique())
print('SMS_received:',df.SMS_received.unique())
print('No_Show:',df.No_Show.unique())


# >* We notice here that the age has a strange value for some patients, some patients are above 100, there is also negative values and zero values, which can't make sense.

# >* Therefore, I will filter the age variables to be between 1 to 100 years old, and then add a function that format the age variables and classify
# the age into cetegories.

# In[13]:


df = df[(df['Age'] < 100) & (df['Age'] > 0 )]
print('Age:',sorted(df.Age.unique()))


# In[14]:


def AgeFormat(age):
    if age['Age'] > 0 and age['Age'] <= 11:
        return 'Children'
    elif age['Age'] >= 12 and age['Age'] <= 17:
        return 'Teenager'
    elif age['Age'] >= 18 and age['Age'] <= 44:
        return 'Adults'
    elif age['Age'] >= 45 and age['Age'] < 65:
        return 'Middle Age'
    else:
        return 'Senior'


# In[15]:


df['Age_category'] = df.apply(AgeFormat, axis=1)


# <a id='eda'></a>
# ## Exploratory Data Analysis
# 
# 

# ## Research Question 1
# >* Age Category:
# Which is the most age category patients have attended to thier appointment?
# just to clarify that the column No_Show have two values, No which means that the patient attended the appointment, and Yes which means that the
# patient did not attend to the appointment.

# In[16]:


print (df.groupby('Age_category')['No_Show'].value_counts())
sns.set_style('white')
fig = sns.countplot(x='Age_category',hue='No_Show', palette="Blues", data=df);
plt.title('Number of No_Show by Age Category')
plt.xlabel('Age Category')
plt.ylabel('Number of Patients')
plt.show()


# This Bar shows the highest number who attended the appointment based on age category. We notice here that the highest number of attendence is for Adults, where their age comes between 18 and 44 years old, and the same category who missed the appointment.

# ## Research Question 2
# >* Gender based exploration:
# Which Gender have the highest percentage of attending to the appointments?

# In[17]:


gender_plt = sns.countplot(x='Gender', hue='No_Show', data=df)
gender_plt.set_title('Number of No_Show by Gender')
plt.xlabel('Gender')
plt.ylabel('Number of Patients')
plt.show()


# The figure shows that the female has the highest number of appointment attending, even though, It is not clear what the exact percent is of no_show
# between male and female.

# In[18]:


no_male=df[(df['Gender']=='M') & (df['No_Show']=='No')].count()
no_female=df[(df['Gender']=='F') & (df['No_Show']=='No')].count()
total_male=len((df['Gender']=='M'))
total_female=len((df['Gender']=='F'))
percentage_of_male=(no_male/total_male)*100
percentage_of_female=(no_female/total_female)*100
print('Percentage of Male who attended to thier appointment:',np.round(percentage_of_male['Gender']),'%')
print('Percentage of Female who did not show up:',np.round(percentage_of_female['Gender']),'%')


# In[19]:


labels='Females','Males'
sizes=[52,28]
plt.pie(sizes, labels=labels, autopct='%1.1f%%',
shadow=True, startangle=90)
plt.title('Percent of males and females')
#draw circle
centre_circle = plt.Circle((0,0),0.70,fc='white')
fig = plt.gcf()
fig.gca().add_artist(centre_circle)
# Equal aspect ratio ensures that pie is drawn as a circle
plt.axis('equal')
plt.tight_layout()
plt.show()


# In terms of percentage. We Can clearly see that females have more attending appointment than males do. The women are most likely visit the
# hospitals than men this may due to several reasons, women take care about her health than men, when we focus on the appointment attending
# variable, we can see 52 % of female attended to their appointment compared to 28 % of male, so women and men are most likely to have the highest
# the rate of attendance.

# Next, I want to check which medical disease each Gender is suffering from

# In[20]:


disease = df[['Gender','Hypertension', 'Diabetes', 'Alcoholism',
'Handicap']].groupby(['Gender']).sum()
disease.head()


# In[21]:


disease_plot = df[['Gender','Hypertension', 'Diabetes', 'Alcoholism',
'Handicap']].groupby(['Gender']).sum().plot(kind='bar'
, figsize=(10,10))
plt.xlabel('Gender')
plt.ylabel('Number of Patients');


# From the Bar above, we can observe that Hypertension is common in both genders except for female is more than males, the Diabetes comes in the second place which is two times for females than males. On the other hand, males are more alcoholic than females. It may be that the reason that a pregnant woman usually is vulnerable to be affected of such diseases due to the pregnancy duration and physical conditions that make them visit the hospital regularly.
# 
# 

# From the above figure, we can predict that females must be enrolled in Scholarship - Bolsa Família (Family Allowance) program more than males.
# 

# In[22]:


family_allowence = df.groupby(['No_Show','Scholarship'])['Scholarship'].count()
family_allowence.head()


# In[23]:


scholarship_plt = sns.countplot( x ='Scholarship',data=df, hue='Gender')
scholarship_plt.set_title('Number of Scholarship Program by Gender')
plt.xlabel('Scholarship')
plt.ylabel('Number of Patients')
plt.show()


# We can notice that females are enrolled in Scholarship program more than male with more than 77,000 patients.

# ## Conclusions
# Adults patients category appears to have the highest rate of attending for the appointments.
# - Females patients attending to their appointment more than males patients.
# - Females patients have the highest percent of diseases than the males patients.
# - Females patients are enrolled in scholarship programs more than males patients.
# ## Limitations
# - There are number of limitations with the No-show appointments Dataset, which are caused by
#  Outliers in age data:
#  Handling age outliers cause to exclude ages equals to or less than 0 and equals to or more than 100.

# In[24]:


from subprocess import call
call(['python', '-m', 'nbconvert', 'Investigate_a_Dataset.ipynb'])

