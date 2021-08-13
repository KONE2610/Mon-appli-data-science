from pycaret.regression import load_model, predict_model
import streamlit as st
import pandas as pd
import numpy as np

model = load_model('rf_saved_12082021')

def predict (model, input_df):
    predictions_df=predict_model(estimator=model, data=input_df)
    predictions = predictions_df['Label'][0]
    return predictions

def run():

    from PIL import Image
    image = Image.open('logo.png')
    bank_image = Image.open('image_bank.png')

    st.image(image,use_column_width=False)

    add_selectbox = st.sidebar.selectbox('Comment voulez-vous faire la prédiction ?', ('En ligne', 'en Batch'))

    st.sidebar.info('Cette application est utilisée pour prédire l\'attitude des clients')
    st.sidebar.success('https://www.myapp.org')

    st.sidebar.image(bank_image)

    st.title ('Prédiction de l\'attitude des clients')

    if add_selectbox == 'En ligne':
        Total_Trans_Ct = st.number_input('Total_Trans_Ct', min_value=10, max_value=139, value=100)
        Total_Revolving_Bal = st.number_input('Total_Revolving_Bal', min_value=0, max_value=2517, value=100)
        Total_Trans_Amt = st.number_input('Total_Trans_Amt',min_value=510, max_value=18484,value=1000)
        Total_Ct_Chng_Q4_Q1 = st.number_input('Total_Ct_Chng_Q4_Q1',min_value=0,max_value=4,value=1)
        Total_Amt_Chng_Q4_Q1 = st.number_input('Total_Amt_Chng_Q4_Q1',min_value=0,max_value=4,value=1)
        Customer_Age = st.number_input('Customer_Age', min_value=26, max_value=73,value=30)
        Total_Relationship_Count = st.number_input('Total_Relationship_Count',min_value=1,max_value=6,value=3)
        Credit_Limit = st.number_input('Credit_Limit',min_value=1438,max_value=35600,value=20000)
        Months_on_book = st.number_input('Months_on_book',min_value=13,max_value=56, value=20)

        output = ''

        input_dict = {'Total_Trans_Ct': [Total_Trans_Ct], 'Total_Revolving_Bal': [Total_Revolving_Bal], 'Total_Trans_Amt' : [Total_Trans_Amt],
                       'Total_Ct_Chng_Q4_Q1' : [Total_Ct_Chng_Q4_Q1], 'Total_Amt_Chng_Q4_Q1' : [Total_Amt_Chng_Q4_Q1], 'Customer_Age': [Customer_Age],
                       'Total_Relationship_Count': [Total_Relationship_Count], 'Credit_Limit': [Credit_Limit],
                       'Months_on_book' : [Months_on_book]}

        input_df = pd.DataFrame(input_dict)

        if st.button('Prédire'):
            output = predict(model=model,input_df=input_df)
            if output == '1':
                st.success('Ce client maintiendra son abonnement')
            else: st.success('Ce client mettra fin à son abonnement')

            #output = '$' + str(output)

        #st.success('The output is {}' .format(output))

    if add_selectbox == 'en Batch':

        file_upload = st.file_uploader("Charger le fichier csv pour prédictions", type=["csv"])

        if file_upload is not None:
            data = pd.read_csv(file_upload)
            predictions = predict_model(estimator=model,data=data)
            st.write(predictions)

if __name__ == '__main__':
    run()   