import json
import os
import pandas as pd

# file paths
insurance_path = 'insurance/country/india'
transaction_path = 'transaction/country/india'
user_path = 'user/country/india'

hover_transcation_path = 'transaction/hover/country/india'
hover_insurance_path = 'insurance/hover/country/india'
hover_user_path = 'user/hover/country/india'


def extract_data(data, datatype, dir, location_info):
    extracted_data = []

    ## For Data Category Aggregated
    if(datatype == "aggregated"):

        # Data Extraction for User 
        if(dir == user_path):
            registered_users = None
            for key, value in data['data'].items():
                if key == 'aggregated':
                    registered_users = value.get("registeredUsers")
                elif key == "usersByDevice" and value is not None:
                    for user_data in value:
                        record = {
                            "Brand": user_data.get("brand"),
                            "Count": user_data.get("count"),
                            "RegisteredUsers": registered_users,
                            "Percentage": user_data.get("percentage")
                            }
                        record.update(location_info)
                        extracted_data.append(record)  

        # Data Extraction for Insurance
        elif(dir == insurance_path):
            for transaction in data['data']['transactionData']:
                for payment in transaction['paymentInstruments']:
                    if payment['type'] == 'TOTAL':
                        count = payment['count']
                        amount = payment['amount']
                        record = {
                            "InsuranceCount": count,
                            "InsuranceAmount" : amount
                        }
                        record.update(location_info)
                        extracted_data.append(record)

        # Data Extraction for Transcation data
        elif(dir == transaction_path):
            for transaction in data['data']['transactionData']:
                transaction_type = transaction['name']
                for instrument in transaction['paymentInstruments']:
                    if instrument['type'] == 'TOTAL':
                        count = instrument['count']
                        amount = instrument['amount']
                        record = {
                            'TransactionType': transaction_type,
                            'TransactionCount': count,
                            'TransactionAmount': amount
                        }
                        record.update(location_info)
                        extracted_data.append(record)
        
        else:
            print("Invalid Path") 


    ## For Data Category TOP        
    elif (datatype == "top"):

        # Data Extraction for Insurance, Transcation
        table1 = []
        table2 = []
        table3 = []
            
        for key, value in data['data'].items():
            if key == 'states' and value is not None:
                for state in value:
                    # Data for top Insurance and Transcation
                    if(dir == insurance_path or dir == transaction_path):
                        state_name = state["entityName"]
                        state_count = state["metric"]["count"]
                        state_amount = state["metric"]["amount"]
                        record1 = {
                           "TopState" : state_name,
                           "StateCount" : state_count,
                           "StateAmount" : state_amount
                        }
                    # Data for top Users
                    elif(dir == user_path):
                        state_name = state["name"]
                        reg_users = state["registeredUsers"]
                        record1 = {
                          "TopState" : state_name,
                          "RegUsers" : reg_users 
                        } 
                    else:
                        pass

                    record1.update(location_info)
                    table1.append(record1)

            if key == 'districts'and value is not None:
                for dist in value:
                    if (dir == insurance_path or dir == transaction_path):
                       dist_name = dist["entityName"]
                       dist_count = dist["metric"]["count"]
                       dist_amount = dist["metric"]["amount"]
                       record2 = {
                            'TopDistrict' : dist_name,
                            'DistCount' : dist_count,
                            'DistAmount' : dist_amount
                        }
                    elif(dir == user_path):
                        dist_name = dist["name"]
                        reg_users = dist["registeredUsers"]
                        record2 = {
                            'TopDistrict' : dist_name,
                            'RegUsers' : reg_users
                        }
                    else:
                        record2 = {}
                    record2.update(location_info)
                    table2.append(record2)

            if key == 'pincodes' and value is not None:
                for pin in value:
                    if(dir == insurance_path or dir == transaction_path):
                        pincode = pin["entityName"]
                        pin_count = pin["metric"]["count"]
                        pin_amount = pin["metric"]["amount"]
                        record3 = {
                            'TopPinCode' : pincode,
                            'PinCount' : pin_count,
                            'PinAmount' : pin_amount
                        }
                    elif(dir == user_path):
                        pincode = int(pin["name"])
                        reg_users = pin["registeredUsers"]
                        record3 = {
                            'TopPinCode' : pincode,
                            'RegUsers' : reg_users
                        }
                    else:
                        record3 = {}
                    record3.update(location_info)
                    table3.append(record3) 
        
        extracted_data.append(table1)
        extracted_data.append(table2)
        extracted_data.append(table3)
    

    ## For Map data
    elif(datatype == "map"):

        extracted_data = []
        
        if(dir == insurance_path ):
            for key, value in data['data'].items():
                if key == "data" and value is not None:
                    for elem in value['data']:
                        record = {
                            'lat':elem[0],
                            'lng':elem[1],
                            'metric':elem[2],
                            'label':elem[3]
                        }
                        record.update(location_info)
                        extracted_data.append(record)


        if(dir == hover_transcation_path or dir == hover_insurance_path):

            for key, value in data['data'].items():
                if key == "hoverDataList":
                    for dict in value:
                        HoverName = dict['name']
                        if dict['metric'][0]['type'] == "TOTAL":
                            HoverTransCount = dict['metric'][0]['count']
                            HoverTranscAmt = dict['metric'][0]['count']
                            record = {
                                "name" : HoverName,
                                "count" : HoverTransCount,
                                "amount" : HoverTranscAmt
                            }
                            record.update(location_info)
                            extracted_data.append(record)


        if(dir == hover_user_path):
            for key, value in data['data'].items():
                if key == 'hoverData':
                    for name , data in value.items():
                        HoverName = name
                        RegUser = data['registeredUsers'] 
                        record = {
                            "HoverName" : HoverName,
                            "RegUser" : RegUser
                        }
                        record.update(location_info)
                        extracted_data.append(record)

    return extracted_data


def process_data(basedir,dir,datatype):

    path = os.path.join(basedir,datatype,dir)

    extracted_data = []
    extracted_data_state = []

    for item in os.listdir(path):
        item_path = os.path.join(path, item)

        # Country-level
        if os.path.isdir(item_path) and item != 'state':
            for c_file in os.listdir(item_path):
                if c_file.endswith('.json'):
                    quarter = int(c_file.split('.')[0])
                    with open(os.path.join(item_path, c_file), 'r') as f:
                        data = json.load(f)
                        extracted_data += extract_data(data, datatype, dir,{
                            "Year": int(item),
                            "Quarter": quarter
                        })

        # State-level
        elif item == 'state':
            for state in os.listdir(item_path):
                state_path = os.path.join(item_path, state)
                if os.path.isdir(state_path):
                    for year in os.listdir(state_path):
                        year_path = os.path.join(state_path, year)
                        if os.path.isdir(year_path):
                            for file in os.listdir(year_path):
                                if file.endswith('.json'):
                                    quarter = int(file.split('.')[0])
                                    with open(os.path.join(year_path, file), 'r') as f:
                                        data = json.load(f)
                                        extracted_data_state += extract_data(data, datatype, dir, {
                                            "State": state,
                                            "Year": int(year),
                                            "Quarter": quarter
                                        })

    return extracted_data, extracted_data_state


country_agg_insurance , state_agg_insurance = process_data('./data', dir = insurance_path, datatype="aggregated")
country_agg_transaction , state_agg_transaction = process_data('./data', dir = transaction_path, datatype="aggregated")
country_agg_user , state_agg_user = process_data('./data', dir = user_path, datatype="aggregated")


country_map_insurance , state_map_insurance = process_data('./data', dir = insurance_path, datatype="map")
country_map_transaction , state_map_transaction = process_data('./data', dir = transaction_path, datatype="map")
country_map_user , state_map_user = process_data('./data', dir = user_path, datatype="map")


country_top_insurance , state_top_insurance = process_data('./data', dir = insurance_path, datatype="top")
country_top_transaction , state_top_transaction = process_data('./data', dir = transaction_path, datatype="top")
country_top_user , state_top_user = process_data('./data', dir = user_path, datatype="top")

