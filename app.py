from flask import Flask, request, render_template
from flask_cors import cross_origin
import sklearn
import pickle
import pandas as pd

app = Flask(__name__)
model = pickle.load(open("flight_price_rf_new.pkl", "rb"))


@app.route("/")
@cross_origin()
def home():
    return render_template("home.html")




@app.route("/predict", methods = ["GET", "POST"])
@cross_origin()
def predict():
    if request.method == "POST":
        try:
            # Date_of_Journey
            date_dep = request.form["Dep_Time"]
            Journey_day = int(pd.to_datetime(date_dep, format="%Y-%m-%dT%H:%M").day)
            Journey_month = int(pd.to_datetime(date_dep, format ="%Y-%m-%dT%H:%M").month)
            # print("Journey Date : ",Journey_day, Journey_month)

            # Departure
            Dep_hour = int(pd.to_datetime(date_dep, format ="%Y-%m-%dT%H:%M").hour)
            Dep_min = int(pd.to_datetime(date_dep, format ="%Y-%m-%dT%H:%M").minute)
            # print("Departure : ",Dep_hour, Dep_min)

            # Arrival
            date_arr = request.form["Arrival_Time"]
            Arrival_hour = int(pd.to_datetime(date_arr, format ="%Y-%m-%dT%H:%M").hour)
            Arrival_min = int(pd.to_datetime(date_arr, format ="%Y-%m-%dT%H:%M").minute)
            # print("Arrival : ", Arrival_hour, Arrival_min)

            # Duration
            dur_hour = abs(Arrival_hour - Dep_hour)
            dur_min = abs(Arrival_min - Dep_min)
            # print("Duration : ", dur_hour, dur_min)

            # Total Stops
            Total_stops = int(request.form["stops"])
            # print(Total_stops)

            Source = request.form["Source"]
            if (Source == 'Delhi'):
                s_Delhi = 1
                s_Kolkata = 0
                s_Mumbai = 0
                s_Chennai = 0

            elif (Source == 'Kolkata'):
                s_Delhi = 0
                s_Kolkata = 1
                s_Mumbai = 0
                s_Chennai = 0

            elif (Source == 'Mumbai'):
                s_Delhi = 0
                s_Kolkata = 0
                s_Mumbai = 1
                s_Chennai = 0

            elif (Source == 'Chennai'):
                s_Delhi = 0
                s_Kolkata = 0
                s_Mumbai = 0
                s_Chennai = 1

            elif (Source == 'Banglore'):
                s_Delhi = 0
                s_Kolkata = 0
                s_Mumbai = 0
                s_Chennai = 0


            Destination = request.form["Destination"]
            if (Destination == 'Cochin'):
                d_Cochin = 1
                d_Delhi = 0
                d_New_Delhi = 0
                d_Hyderabad = 0
                d_Kolkata = 0

            elif (Destination == 'Delhi'):
                d_Cochin = 0
                d_Delhi = 1
                d_New_Delhi = 0
                d_Hyderabad = 0
                d_Kolkata = 0

            elif (Destination == 'New_Delhi'):
                d_Cochin = 0
                d_Delhi = 0
                d_New_Delhi = 1
                d_Hyderabad = 0
                d_Kolkata = 0

            elif (Destination == 'Hyderabad'):
                d_Cochin = 0
                d_Delhi = 0
                d_New_Delhi = 0
                d_Hyderabad = 1
                d_Kolkata = 0

            elif (Destination == 'Kolkata'):
                d_Cochin = 0
                d_Delhi = 0
                d_New_Delhi = 0
                d_Hyderabad = 0
                d_Kolkata = 1

            elif (Destination == 'Banglore'):
                d_Cochin = 0
                d_Delhi = 0
                d_New_Delhi = 0
                d_Hyderabad = 0
                d_Kolkata = 0

            # print(
            #     d_Cochin,
            #     d_Delhi,
            #     d_New_Delhi,
            #     d_Hyderabad,
            #     d_Kolkata
            # )

            # Airline
            # AIR ASIA = 0 (not in column)
            predictions = list()
            Airlines = ["Jet Airways", "IndiGo", "Air India", "Multiple carriers", "SpiceJet", "Vistara", "Air Asia", "GoAir"]
            for i in Airlines:
                if( i =='Jet Airways'):
                    Jet_Airways = 1
                    IndiGo = 0
                    Air_India = 0
                    Multiple_carriers = 0
                    SpiceJet = 0
                    Vistara = 0
                    GoAir = 0

                elif (i=='IndiGo'):
                    Jet_Airways = 0
                    IndiGo = 1
                    Air_India = 0
                    Multiple_carriers = 0
                    SpiceJet = 0
                    Vistara = 0
                    GoAir = 0

                elif (i=='Air India'):
                    Jet_Airways = 0
                    IndiGo = 0
                    Air_India = 1
                    Multiple_carriers = 0
                    SpiceJet = 0
                    Vistara = 0
                    GoAir = 0
                
                elif (i=='Multiple carriers'):
                    Jet_Airways = 0
                    IndiGo = 0
                    Air_India = 0
                    Multiple_carriers = 1
                    SpiceJet = 0
                    Vistara = 0
                    GoAir = 0
                
                elif (i=='SpiceJet'):
                    Jet_Airways = 0
                    IndiGo = 0
                    Air_India = 0
                    Multiple_carriers = 0
                    SpiceJet = 1
                    Vistara = 0
                    GoAir = 0
                
                elif (i=='Vistara'):
                    Jet_Airways = 0
                    IndiGo = 0
                    Air_India = 0
                    Multiple_carriers = 0
                    SpiceJet = 0
                    Vistara = 1
                    GoAir = 0

                elif (i=='GoAir'):
                    Jet_Airways = 0
                    IndiGo = 0
                    Air_India = 0
                    Multiple_carriers = 0
                    SpiceJet = 0
                    Vistara = 0
                    GoAir = 1

                elif (i == 'Air Asia'):
                    Jet_Airways = 0
                    IndiGo = 0
                    Air_India = 0
                    Multiple_carriers = 0
                    SpiceJet = 0
                    Vistara = 0
                    GoAir = 0

                prediction = model.predict([[Total_stops,
                        Journey_day,
                        Journey_month,
                        Dep_hour, Dep_min, Arrival_hour, Arrival_min, dur_hour,
                        dur_min,
                        Air_India,
                        GoAir,
                        IndiGo,
                        Jet_Airways,
                        Multiple_carriers,
                        SpiceJet,
                        Vistara,
                        s_Chennai,
                        s_Delhi,
                        s_Kolkata,
                        s_Mumbai,
                        d_Cochin,
                        d_Delhi,
                        d_Hyderabad,
                        d_Kolkata,
                        d_New_Delhi
                        ]])

                predictions.append(prediction)
            
            outputs = list()
            for i in range(8):
                output = predictions[i]
                outputr = round(output[0], 2)
                outputs.append(outputr)

                                                                                                        
            
            headings = ("Airlines", "Flight Fare (in Rs.)")
            
            data = ((Airlines[0], outputs[0]),
                    (Airlines[1], outputs[1]),
                    (Airlines[2], outputs[2]),
                    (Airlines[3], outputs[3]),
                    (Airlines[4], outputs[4]),
                    (Airlines[5], outputs[5]),
                    (Airlines[6], outputs[6]),
                    (Airlines[7], outputs[7]))
            
            return render_template('home.html',prediction_text="Predicted Flight Fare", headings = headings, data = data)

        except:
            return render_template('home.html',prediction_text="Error! Route not found. Please try again...")
            

    return render_template(".html")

if __name__ == "_main_":
    app.run(debug=True)