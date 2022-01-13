from flask import Flask, render_template, request
import sqlite3 as sql
import pandas as pd
import numpy as np
import pickle
from sklearn.ensemble import RandomForestRegressor



app = Flask(__name__)
# load the pickel model
model = pickle.load(open("model4.pkl", "rb"))



@app.route('/')
def home():
   return render_template('page.html')

@app.route("/predict", methods = ['POST'])
def predict():
    features = []
    age_map = {'None': 0,
    'Above 20 years': 1,
    '15 to 20 years': 2,
    '10 to 15 years': 3,
    '5 to 10 years': 4,
    'Less than 5 years': 5,
    'New Construction': 6}

    power_map = {'Over 6 Hours Powercut': 0,
                '2 To 4 Hours Powercut': 1,
                'None': 2,
                'No/Rare Powercut': 3}


    water_map = {'12 Hours Available': 0, 'None': 1, '24 Hours Available': 2}


    Furnished = {'Unfurnished': 0, 'Semi-Furnished': 1, 'Furnished': 2}

    Tenants_Pre = {'Bachelors': 0, 'Family': 1, 'None': 2}
    addr = {'None': 0,
                'Wakad': 1,
                'Hinjewadi': 2,
                'Hadapsar': 3,
                'Wagholi': 4,
                'Kalyani Nagar': 5,
                'Kharadi': 6,
                'Pune': 7,
                'Magarpatta City': 8,
                'Wadgaon Sheri': 9,
                'Pimple Saudagar': 10,
                'Baner': 11,
                'Balewadi': 12,
                'Amanora Park Town': 13,
                'Dhanori': 14,
                'NIBM Road': 15,
                'Viman Nagar': 16,
                'Koregaon Park': 17,
                'Aundh': 18,
                'Wanowrie': 19}


    statu = {'Immediately': 0, 'Immediately Available': 1, 'None': 2}

    Overlook = {'Garden/Park': 0,
    'Garden/Park, Main Road': 1,
    'Garden/Park, Main Road, Pool': 2,
    'Garden/Park, Pool': 3,
    'Garden/Park, Pool, Main Road': 4,
    'Main Road': 5,
    'Main Road, Garden/Park': 6,
    'Main Road, Garden/Park, Pool': 7,
    'None': 8,
    'Pool': 9,
    'Pool, Garden/Park': 10,
    'Pool, Garden/Park, Main Road': 11,
    'Pool, Main Road': 12,
    'Pool, Main Road, Garden/Park': 13}



    other_tenant_preff = {'Non-Vegetarians': 0,
    'Non-Vegetarians, Pets allowed': 1,
    'Non-Vegetarians, Pets not allowed': 2,
    'Non-Vegetarians, With Company Lease, Pets not allowed': 3,
    'Non-Vegetarians, Without Company Lease': 4,
    'Non-Vegetarians, Without Company Lease, Pets allowed': 5,
    'Non-Vegetarians, Without Company Lease, Pets not allowed': 6,
    'None': 7,
    'Pets allowed': 8,
    'Pets not allowed': 9,
    'Vegetarians': 10,
    'Vegetarians, Pets not allowed': 11,
    'Vegetarians, With Company Lease, Pets not allowed': 12,
    'Vegetarians, Without Company Lease, Pets not allowed': 13,
    'With Company Lease': 14,
    'With Company Lease, Pets not allowed': 15,
    'Without Company Lease': 16,
    'Without Company Lease, Pets allowed': 17,
    'Without Company Lease, Pets not allowed': 18}


    Authority_App = {'City Municipal Corporation': 0,
    'Developer': 1,
    'Development Authority': 2,
    'None': 3}

    Type_of_Owner = {'Co-operative Society': 0, 'Freehold': 1, 'Leasehold': 2, 'None': 3}
    Bedroom = request.form['Bedroom']
    features.append(int(Bedroom))
    Bathroom = request.form['Bathroom']
    features.append(int(Bathroom))
    Balcony = request.form['Balcony']
    features.append(int(Balcony))
    
    Super_area = request.form['Super_area']
    if '.' in Super_area :
        x = float(Super_area)
        features.append(x)
    else:
        features.append(int(Super_area))
    Carpet_area = request.form['Carpet_area']
    if '.' in Carpet_area :
        x = float(Carpet_area)
        features.append(x)
    else:
        features.append(int(Carpet_area))
    Furnished_status = request.form['Furnished_status']
    features.append(Furnished[Furnished_status])
    Car_parking = request.form['Car_parking']
    features.append(int(Car_parking))
    Tenants_Preferred = request.form['Tenants_Preferred']
    features.append(Tenants_Pre[Tenants_Preferred])
    Water_Availability = request.form['Water_Availability']
    features.append(water_map[Water_Availability])
    Booking_Amount = request.form['Booking_Amount']
    if '.' in Booking_Amount :
        x = float(Booking_Amount)
        features.append(x)
    else:
        features.append(int(Booking_Amount))
   
    Address = request.form['Address']
    features.append(addr[Address])
    Status = request.form['Status']
    features.append(statu[Status])

    Overlooking = request.form['Overlooking']
    features.append(Overlook[Overlooking])
    Status_of_Electricity = request.form['Status_of_Electricity']
    features.append(power_map[Status_of_Electricity])

    Lifts = request.form['Lifts']
    features.append(int(Lifts))
    Other_Tenants_Preferred = request.form['Other_Tenants_Preferred']
    features.append(other_tenant_preff[Other_Tenants_Preferred])
    Age_of_Construction = request.form['Age_of_Construction']
    features.append(age_map[Age_of_Construction])
    Authority_Approval = request.form['Authority_Approval']
    features.append(Authority_App[Authority_Approval])
    Type_of_Ownership = request.form['Type_of_Ownership']
    features.append(Type_of_Owner[Type_of_Ownership])
    Amenities_no = request.form['Amenities_no']
    features.append(int(Amenities_no))
    feature = [np.array(features)]
    # df = pd.DataFrame(feature,columns = ['Bedroom', 'Bathroom', 'Balcony', 'Super_area', 'Carpet_area',
    #    'Furnished_status', 'Car_parking', 'Tenants_Preferred',
    #    'Water_Availability', 'Booking_Amount', 'Address', 'Status',
    #    'Overlooking', 'Status_of_Electricity', 'Lifts',
    #    'Other_Tenants_Preferred', 'Age_of_Construction', 'Authority_Approval',
    #    'Type_of_Ownership', 'Amenities_no'])

    
    prediction = model.predict(feature)


    
    return render_template("page.html", prediction_text = "The predicted rent is  :  {}".format(prediction))



if __name__ == '__main__':
    
     app.run(debug = True)
   
    
    

    




