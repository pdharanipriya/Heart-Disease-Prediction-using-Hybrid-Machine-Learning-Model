import pickle
import streamlit as st
from fpdf import FPDF

# Set page configuration
st.set_page_config(page_title="Health Assistant",
                   layout="wide",
                   page_icon="🧑‍⚕️")

# Load the saved model
heart_disease_model = pickle.load(open('C:/Users/admin/Desktop/Mini/heart_model.sav', 'rb'))

# Heart Disease Prediction Page
st.title('Heart Disease Prediction using ML')

# User inputs with keys for smoother navigation
col1, col2, col3 = st.columns(3)

with col1:
    age = st.text_input('Age', key="age")
    trestbps = st.text_input('Resting Blood Pressure', key="trestbps")
    
    # Dropdown for Resting Electrocardiographic Results
    restecg_options = {
    "choose an option": None,
    "0 - Normal": 0,
    "1 - ST-T wave abnormality": 1,
    "2 - Left ventricular hypertrophy": 2
    }
    restecg_label = st.selectbox('Resting Electrocardiographic Results', options=list(restecg_options.keys()), index=0, key="restecg")
    restecg = restecg_options.get(restecg_label)  # Get the numeric value corresponding to the label

    oldpeak = st.text_input('ST depression induced by exercise', key="oldpeak")
    thal = st.text_input('thal: 0 = normal; 1 = fixed defect; 2 = reversible defect', key="thal")

with col2:
    # Dropdown for Sex with options
    sex_options = {
    "choose your gender": None,
    "0 - Female": 0,
    "1 - Male": 1
    }
    sex_label = st.selectbox('Sex', options=list(sex_options.keys()), index=0, key="sex")
    sex = sex_options.get(sex_label)  # Get the numeric value corresponding to the label

    chol = st.text_input('Serum Cholesterol in mg/dl', key="chol")
    
    thalach = st.text_input('Maximum Heart Rate achieved', key="thalach")
   
    # Dropdown for Slope with options
    slope_options = {
    "choose an option": None,
    "0 - Upsloping": 0,
    "1 - Flat": 1,
    "2 - Downsloping": 2
    }
    slope_label = st.selectbox('Slope of the peak exercise ST segment', options=list(slope_options.keys()), index=0, key="slope")
    slope = slope_options.get(slope_label)  # Get the numeric value corresponding to the label

with col3:
    # Dropdown for Chest Pain Type with "choose an option"
    cp_options = {
        "choose an option": None,
        "0 - Typical Angina": 0,
        "1 - Atypical Angina": 1,
        "2 - Non-Anginal Pain": 2,
        "3 - Asymptomatic": 3
    }
    cp_label = st.selectbox('Chest Pain Type', options=list(cp_options.keys()), index=0, key="cp")
    cp = cp_options.get(cp_label)  # Get the numeric value corresponding to the label

    # Fasting blood sugar
    fbs_input = st.text_input('Fasting Blood Sugar in mg/dl', key="fbs")
    
    # Convert fbs input to 0 or 1 based on the value entered
    try:
        fbs = 0 if float(fbs_input) <= 120 else 1
    except ValueError:
        fbs = None  # Handle invalid input
    
    # Exercise induced angina  
    exang = st.text_input('Exercise Induced Angina(0 = no, 1 = yes)', key="exang")
    
    ca = st.text_input('Major vessels colored by fluoroscopy', key="ca")

# Code for prediction
heart_diagnosis = ''

# Check if all required inputs are valid
if all([age, sex is not None, cp is not None, trestbps, chol, fbs is not None, restecg is not None, thalach, exang, oldpeak, slope is not None, ca, thal]):
    # Button for prediction
    if st.button('Heart Disease Test Result'):
        # Collecting the input data
        user_input = [age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal]
        
        # Convert inputs to float for prediction
        try:
            user_input = [float(x) if x is not None else 0.0 for x in user_input]
            heart_prediction = heart_disease_model.predict([user_input])

            if heart_prediction[0] == 1:
                heart_diagnosis = 'The person is having heart disease'
                diagnosis_color = (255, 0, 0)  # Red for positive diagnosis
            else:
                heart_diagnosis = 'The person does not have any heart disease'
                diagnosis_color = (0, 128, 0)  # Green for negative diagnosis

            st.success(heart_diagnosis)
        except ValueError:
            st.error("Please enter valid numerical values.")
        
        # Convert sex input to display text for PDF
        sex_display = "Female" if sex == 0 else "Male" if sex == 1 else "Unknown"
        
        # Map chest pain types to descriptive labels
        chest_pain_labels = {
            0: "Typical Angina",
            1: "Atypical Angina",
            2: "Non-Anginal Pain",
            3: "Asymptomatic"
        }
        cp_display = chest_pain_labels.get(cp, "Unknown")
        
        # Convert Exercise Induced Angina input (exang) to text for PDF
        exang_display = "Yes" if exang == "1" else "No" if exang == "0" else "Unknown"
        
        # Map Resting Electrocardiographic Results (restecg) to descriptive text
        restecg_labels = {
            0: "Normal",
            1: "ST-T wave abnormality",
            2: "Left ventricular hypertrophy"
            }

            # Now use this mapping in the PDF generation section
        restecg_display = restecg_labels.get(restecg, "Unknown")  # Default to "Unknown" if not found

        # Map Slope of the peak exercise ST segment to descriptive text
        slope_labels = {
            0: "Upsloping",
            1: "Flat",
            2: "Downsloping"
            }

        # Now use this mapping in the PDF generation section
        slope_display = slope_labels.get(slope, "Unknown")  # Default to "Unknown" if not found
        # Data for PDF, including Reference Values and Units
        data = [
            {"Parameter": "Age", "Value": age, "Reference Value": "N/A", "Units": "years"},
            {"Parameter": "Sex", "Value": sex_display, "Reference Value": "N/A", "Units": "--"},
            {"Parameter": "Chest Pain Type", "Value": cp_display, "Reference Value": "N/A", "Units": "--"},
            {"Parameter": "Resting Blood Pressure", "Value": trestbps, "Reference Value": "<= 120", "Units": "mm Hg"},
            {"Parameter": "Serum Cholesterol", "Value": chol, "Reference Value": "< 200", "Units": "mg/dl"},
            {"Parameter": "Fasting Blood Sugar", "Value": fbs_input, "Reference Value": "<= 120", "Units": "mg/dl"},
            {"Parameter": "Rest ECG", "Value": restecg_display, "Reference Value": "N/A", "Units": "--"},
            {"Parameter": "Max Heart Rate", "Value": thalach, "Reference Value": "N/A", "Units": "bpm"},
            {"Parameter": "Exercise Induced Angina", "Value": exang_display, "Reference Value": "N/A", "Units": "--"},
            {"Parameter": "Oldpeak", "Value": oldpeak, "Reference Value": "0-2", "Units": "mm"},
            {"Parameter": "Slope", "Value": slope_display, "Reference Value": "N/A", "Units": "--"},
            {"Parameter": "Major Vessels", "Value": ca, "Reference Value": "0-3", "Units": "--"},
            {"Parameter": "Thal", "Value": thal, "Reference Value": "N/A", "Units": "g/dL"}
        ]
        
        # PDF Generation without grid lines
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", "B", 16)
        pdf.cell(200, 10, "Heart Disease Prediction Report", 0, 1, "C")

        # Add table headers in a single row
        pdf.set_font("Arial", "B", 10)
        pdf.cell(50, 10, "Parameter", border=0, align="C")
        pdf.cell(50, 10, "Value", border=0, align="C")
        pdf.cell(50, 10, "Reference Value", border=0, align="C")
        pdf.cell(50, 10, "Units", border=0, ln=1, align="C")  # ln=1 to move to the next line after headers

        # Add table rows without borders
        pdf.set_font("Arial", "", 10)
        for item in data:  # Iterate directly over the list of dictionaries
            pdf.cell(50, 10, item["Parameter"], border=0, align="C")
            pdf.cell(50, 10, str(item["Value"]), border=0, align="C")
            pdf.cell(50, 10, item["Reference Value"], border=0, align="C")
            pdf.cell(50, 10, item["Units"], border=0, ln=1, align="C")

        # Add Diagnosis section separately with color
        pdf.ln(10)  # Add space before diagnosis
        pdf.set_text_color(*diagnosis_color)
        pdf.set_font("Arial", "B", 14)
        pdf.cell(0, 10, f"Diagnosis: {heart_diagnosis}", border=0, ln=1, align="C")
        
        # Save PDF to a BytesIO object for download
        pdf_output = pdf.output(dest='S').encode('latin1')
        st.download_button(
            label="Download Report as PDF",
            data=pdf_output,
            file_name="heart_disease_report.pdf",
            mime="application/pdf"
        )
else:
    st.warning("Please enter all the details to get the prediction and download option.")
