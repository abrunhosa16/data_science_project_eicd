import streamlit as st, pandas as pd, pickle

with open('variables/variables.pkl', 'rb') as f:
    data = pickle.load(f)

continuous_features = data['continuous_features']
categorical_features = data['categorical_features']

df = pd.read_csv('dataset/hcc_dataset.csv')

st.title('My first app!')

with st.form( key= 'my_form' ): #iniciar formulario
    
    features = [] #lista dos valores
    
    for col in df.columns:
        
        if col in categorical_features:
            possible_values = list( set( df[col].values ) )
            value = st.selectbox(str(col) + ': ', possible_values)
            
        else:
            value = st.number_input(str(col) + ': ', min_value= 0.0, step= 0.1)
        
        features.append( value )
    
    row = pd.DataFrame( [features], columns= df.columns)
        
    submit_button = st.form_submit_button( label= 'Submit' )
    
if submit_button:
    st.write('You selected:')
    st.dataframe(row)
