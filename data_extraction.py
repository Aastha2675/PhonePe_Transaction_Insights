# Required Libraries
import json
import os

# FLoader/Files Paths
insurance_path = 'insurance/country/india'
transaction_path = 'transaction/country/india'
user_path = 'user/country/india'

hover_transaction_path = 'transaction/hover/country/india'
hover_insurance_path = 'insurance/hover/country/india'
hover_user_path = 'user/hover/country/india'


# Data Extraction for aggregated data
def extract_data_agg(data,dir,location_info):
    extracted_data = []

    # Data Extraction For User
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


    return extracted_data




# Data Extraction code for map data
def extract_data_map(data,dir,location_info):
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


  if(dir == hover_transaction_path or dir == hover_insurance_path):

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



def extract_data_top(data, dir, location_info):
    extracted_data = []

    if not data or 'data' not in data or data['data'] is None:
        return extracted_data  # return empty list

    for key, value in data['data'].items():
        if value is None:
            continue

        if key == 'states':
            for state in value:
                if dir == insurance_path or dir == transaction_path:
                    record = {
                        "TopState": state["entityName"],
                        "StateCount": state["metric"]["count"],
                        "StateAmount": state["metric"]["amount"],
                        **location_info
                    }
                elif dir == user_path:
                    record = {
                        "TopState": state["name"],
                        "RegUsers": state["registeredUsers"],
                        **location_info
                    }
                else:
                    continue
                extracted_data.append(record)

        elif key == 'districts':
            for dist in value:
                if dir == insurance_path or dir == transaction_path:
                    record = {
                        "TopDistrict": dist["entityName"],
                        "DistCount": dist["metric"]["count"],
                        "DistAmount": dist["metric"]["amount"],
                        **location_info
                    }
                elif dir == user_path:
                    record = {
                        "TopDistrict": dist["name"],
                        "RegUsers": dist["registeredUsers"],
                        **location_info
                    }
                else:
                    continue
                extracted_data.append(record)

        elif key == 'pincodes':
            for pin in value:
                if dir == insurance_path or dir == transaction_path:
                    record = {
                        "TopPinCode": pin["entityName"],
                        "PinCount": pin["metric"]["count"],
                        "PinAmount": pin["metric"]["amount"],
                        **location_info
                    }
                elif dir == user_path:
                    record = {
                        "TopPinCode": int(pin["name"]),
                        "RegUsers": pin["registeredUsers"],
                        **location_info
                    }
                else:
                    continue
                extracted_data.append(record)

    return extracted_data


# Function to extact data from json files
def extract_data(data, datatype, dir, location_info):
    extracted_data = []

    if datatype == "aggregated":
        extracted_data = extract_data_agg(data, dir, location_info) or []
    elif datatype == "top":
        extracted_data = extract_data_top(data, dir, location_info) or []
    elif datatype == "map":
        extracted_data = extract_data_map(data, dir, location_info) or []

    return extracted_data



# Function for trversing the folders paths
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




# Calling the functions
# country level and state level data

# aggregated
country_agg_insurance , state_agg_insurance = process_data('./data', dir = insurance_path, datatype="aggregated")
country_agg_transaction , state_agg_transaction = process_data('./data', dir = transaction_path, datatype="aggregated")
country_agg_user , state_agg_user = process_data('./data', dir = user_path, datatype="aggregated")

# map
country_map_insurance , state_map_insurance = process_data('./data', dir = insurance_path, datatype="map")
country_hover_map_insurance , state_hover_map_insurance = process_data('./data', dir = hover_insurance_path, datatype="map")
country_hover_map_transaction , state_hover_map_transaction = process_data('./data', dir = hover_transaction_path, datatype="map")
country_hover_map_user , state_hover_map_user = process_data('./data', dir = hover_user_path, datatype="map")

# top
country_top_insurance , state_top_insurance = process_data('./data', dir = insurance_path, datatype="top")
country_top_transaction , state_top_transaction = process_data('./data', dir = transaction_path, datatype="top")
country_top_user , state_top_user = process_data('./data', dir = user_path, datatype="top")










