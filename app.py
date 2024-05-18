import streamlit as st, pandas as pd, pickle
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier

#features
binary_features = ['Symptoms_Yes', 'PVT_Yes', 'Metastasis_Yes']
binary_features_names = ['Symptoms', 'PVT', 'Metastasis']
bin_dic = {'Yes': 1, 'No': 0, 'True': 1, 'False': 0}

ps = ['PS_Active', 'PS_Disabled', 'PS_Selfcare']
ps_values = ['Active', 'Disabled', 'Selfcare']

ascites = ['Ascites_Moderate/Severe', 'Ascites_No']
ascites_values = ['Moderate/Severe', 'No']

continuous_features = ['AFP', 'Hemoglobin', 'Albumin', 'AST', 'ALP', 'Dir_Bil', 'Iron', 'Ferritin']

target = 'Class'
pred_dic = {1: 'Lives', 0: 'Dies'}

#models
with open('variables/models.pkl', 'rb') as f:
    models = pickle.load(f)

model_dic = {'Decision Tree': models.get('decision_tree'), 
             'Random Forest': models.get('random_forest'), 
             'Logistic Regression': models.get('logistic_regression'), 
             'SVM': models.get('svm'), 
             'KNN': models.get('knn')}

#dfs
df = pd.read_csv('dataset/hcc_dataset.csv')
final_df = pd.read_csv('dataset/final_hcc_dataset.csv')

st.title('Predicitons app')

with st.form( key= 'my_form' ): #iniciar formulario
    
    model = st.selectbox('Which model: ', ['Decision Tree', 'Random Forest', 'Logistic Regression', 'SVM', 'KNN'])
    
    features_values = [] #lista dos valores
    
    #cont features
    for continuous_feature in continuous_features:
        features_values.append(st.number_input(continuous_feature + ': ', min_value= 0.0, step= 0.1))
        
    #binary features
    for binary_feature in binary_features_names:
        possible_values = ['Yes', 'No']
        value = st.selectbox(binary_feature + ': ', possible_values)
        features_values.append(bin_dic.get( value ))
    
    #ps
    ps_value = st.selectbox('PS: ', ps_values + ['Other'])
    features_values.append(ps_value)

    
    #ascites
    asc_value = st.selectbox('Ascites: ', ascites_values + ['Other'])
    features_values.append(asc_value)
        
    submit_button = st.form_submit_button( label= 'Submit' )
    
    
if submit_button:
    final_features_values = features_values[:-2]
    
    for feature in ps:
        if 'PS_' + str(ps_value) == feature: final_features_values.append(1)
        else: final_features_values.append(0)   
    
    for feature in ascites:
        if 'Ascites_' + str(asc_value) == feature: final_features_values.append(1)
        else: final_features_values.append(0)    
        
    row = pd.DataFrame([final_features_values], columns= final_df.columns[:-1])
    
    st.write('You selected:')
    st.dataframe(row)
    
    model = model_dic.get(model)
    
    pred = model.predict(row)
    st.write(pred_dic.get(int(pred)))
