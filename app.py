import streamlit as st
from detector.detector import detect_plate_text
from database.database import check_plate_info


st.title('Licene Plate Recognition System')
uploaded_file = st.file_uploader("Upload an image", type=['jpg', 'png', 'jpeg'])

if uploaded_file is not None:

    st.image(uploaded_file, caption='Uploaded Image', use_column_width = True)
    with open('uploads/temp.jpg', 'wb') as f:
        f.write(uploaded_file.read())

    st.write('Detecting Licence Plate...')
    plate_number = detect_plate_text('uploads/temp.jpg')

    if plate_number:
        st.success(f'Detected Plate : {plate_number}')
        result = check_plate_info(plate_number)

        if result:
            st.write(f"**Owner:** {result['owner_name']}")
            st.write(f"**Fine Status:** {'Yes' if result['has_fine'] else 'No'}")
            # if result['has_fine']:
            #     st.write(f'**Fine Amount:** ${result['fine_amount']}')
        else:
            st.warning('Plate not found in database.')

    else:
        st.error('No plate detected or unreadable text.')
                       
    

