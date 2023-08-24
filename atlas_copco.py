# -*- coding: utf-8 -*-
"""
Created on Fri Apr 21 01:51:20 2023

@author: ASUS
"""
import openai
import tiktoken
import os
from flask import Flask, request, jsonify,Response,send_file
from datetime import datetime, timedelta
import pprint
from flask_cors import CORS
import uuid
import json
os.environ['OPENAI_API_KEY'] = "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"
openai.api_key=os.environ['OPENAI_API_KEY']
chat_history = {}
time_track = {}

import os
import pandas as pd

# Replace 'input_folder' with the path to the folder containing the Excel files
input_folder = './data'
# Replace 'output_folder' with the path to the folder where you want to save the text files
output_folder = './text_data'

# Iterate through all files in the input folder
for file in os.listdir(input_folder):
    # Check if the file is an Excel file
    if file.endswith('.xlsx') or file.endswith('.xls'):
        input_excel_file = os.path.join(input_folder, file)
        name = file.split('.xlsx')[0]
        
        # Read the Excel file into a DataFrame
        sheet_name = 'Sheet1'  # Change this to the name of the sheet you want to read
        df = pd.read_excel(input_excel_file, sheet_name=sheet_name, engine='openpyxl')

        # Save the DataFrame to a plain text file with a tab delimiter
        output_text_file = os.path.join(output_folder, os.path.splitext(file)[0] + '.txt')
        df.to_csv(output_text_file, sep='\t', index=False)
        
        
text_files_content = {}
for file in os.listdir(output_folder):
    if file.endswith('.txt'):
        with open(os.path.join(output_folder, file), 'r') as f:
            name = file.split('.txt')[0]
            content = f.read()
            text_files_content[name] = content
            
            
            
prompt = f'''
Here are the specifications and benefits for our air compressors, you will use this data later to find the customer what they need, 

Compressor models available for rent:

PTSE Variants

Benefits: 100% Oil-free compressor • Electric driven • All weather canopy • Skid mounted • Load-unload control • Small footprint • Best for medium enterprises

PTSE Variants:
{text_files_content['PTSE']}


ZH Variants

Benifits:  100% Oil-free compressor • Electric driven • All weather canopy • Water cooled • High voltage options • Lowest operating cost • Best for high volume needs • Medium Voltage								
ZH Variants:
{text_files_content['ZH']}

ZT Variants

Benifits: • 100% Oil-free compressor • Electric driven • All weather canopy • Skid mounted • Load-unload control • Small footprint • Best for medium enterprises							
ZT Variants:
{text_files_content['ZT']}


ZT VSD

Benifits: • 100% Oil-free compressor • Electric driven • All weather canopy • Wheel mounted • Crash frame • Variable speed control • Best for varying demand • Small footprint • Best for medium enterprises 
							
ZT VSD:
{text_files_content['ZT_VSD']}

PTS	

Benifits:  100% Oil-free compressor • All weather canopy • Wheel mounted • Diesel driven • Medium & high pressure • Best for large enterprises
							
PTS:
{text_files_content['PTS']}
Here are the specifications and benefits for our dryers you will use this data later to find the customer what they need, 

Dryers models for rent: 

Benefits: Total cost of Rental • Avoid rapid and destructive pipe corrosion • Eliminating pressure drops and air leakages decreasing energy consumption • Prevent corrosion entering special equipment increasing their reliability, performance and lifetime • Water vapor and corrosion mixing with the raw materials ends with final product quality deviation Peace of mind • With wet compressed air there is always a risk of product contamination • With Atlas Copco 100% Oil-Free Dry Air, customers choose to take zero oil, low dew point, zero risks, 100% peace of mind

Technical Specifications
					
Dryers:
{text_files_content['Dryers']}
Here are the specifications for our nitrogen generator, you will use this in a later question to help the customer find what they need :

Benefits: Total cost of Rental • Low installation and running costs for a quick return on your investment • No downtime due to N2 shortages • No excess of N2 produced • No transportation, refills, and delivery charges Peace of mind Optimum flexibility • Be your own supplier, produce gas when you need it • On-site and mobile solutions • A supply that perfectly matches your needs • Fast and easy start up Increased safety • Our engineers design the most suitable solution • Eliminate risks associated with handling of high pressure cylinders • No large quantities of cryogenic liquified gas Uninterrupted supply • Continuous availability anywhere • 24/7 service support from our experienced technicians • Easy operation 

Technical data

Nitrogen Generators: 
{text_files_content['Nitrogen_Generators']}										

here is the data for our boosters, you will use this data to help the customer find what they need

Boosters	

Benefits: Total cost of Rental • Energy efficient electric driven solution • Energy savings - no need of extra energy to compensate pressure drop in filters • Reduce maintenance costs (less interventions) • Avoid costs of treatment of oil condensate Peace of mind Reliable • Engineered to be reliable for outdoor application • Containerized modular design • Superior Elektronikon monitoring and control • Built in cooling system & integrated air receivers • New equipment and fleet size Ease of use • Easy inspection and installation • Single point in connection • Easy monitoring
								
Boosters: 
{text_files_content['Boosters']}

Here is the data for the heat exchangers, you will use this data to help the customer find what they need 

Heat Exchanger

Benefits: Make use of heat of compressor -> no extra heat source is required (no extra energy) • Increase water holding capacity up to 17 times • Reducing: Fuel/Energy, Manhour - • Increasing drying efficiency, drying in less time with more savings; completing your project on time and budget • Logistically Superior: No steam or external utilities required 

Technical data
				
Heat Exchanger: 
{text_files_content['Heat_Exchanger']}

Here is the data for the steam boilers, you will use this data to help the customer get what they want

Boilers 

Trailer Mounted Watertube

Benifits: Capacities up to 82,500 LB/HR • Pressure up to 750 PSIG • Tri-fuel • Emissions NOx Rating 30 PPM • Saturated and superheat • Fuel handeling

Technical data:
{text_files_content['WT']}

Boiler in a Box	

Benifits: • Capacities up to 1,000 HP (35,000 LB/HR) • Pressure up to 250 PSIG • Tri-fuel • Emissions NOx Rating 30 PPM • Compact design • Fuel handeling

Technical data : 
{text_files_content['BB']}

Portable Boiler Rooms

Benefits: • Capacities up to 1,000 HP (35,000 LB/HR) • Pressure up to 250 PSIG • Tri-fuel • Emissions NOx Rating 30/75 PPM • Need water treatment storage • Fuel handling

Technical data: 
{text_files_content['RH']}


Skid Mounted Electric : 
{text_files_content['RE']}

Trailer Mounted Firetube

Benefits: • Capacities up to 1,000 HP (35,000 LB/HR) • Pressure up to 250 PSIG • Tri-fuel • Emissions NOx Rating 30 PPM • Articulating rain cover • Fuel handeling

Technical data: 
{text_files_content['Trailer_Mounted_Firetube']}
Portable Boiler System

Benefits:
50 HP (1,725LB/HR) • 15 PSIG steam, up to 100 PSIG water • Tri-fuel • Emissions NOx Rating 75 PPM • Power with extension cord • Compact, TOWbehind design • On board fuel oil tank

Technical specifications: 
{text_files_content['Portable_Boiler']}


#Script information

Now, using the data above act as a customer service assistant for Atlas Copco. Find out what product I am searching for, keep your responses short and to the point. Start by asking Thank you for contacting Atlas Copco, what are you looking for? We offer Oil-free Air compressors, Steam and Nitrogen -  Keep asking questions until you find out exactly the model name of which product they are looking for, also if they are looking for a product for a specific application, also, ask their application give them recommendations for other equipment listed above that they may find useful based on the application. If what they need is more than what we have, recommend multiple units, preferably of the pts 1600 which is our most common unit 

make sure if the capacity is over 10,000 cfm, recommend multiple PTS 1600

Before you recommending a product, ask the user their needed specifications such as CFM or LB/HR


- If the user needs a steam boiler, call Stacey at 281-5422509 if they need anything else other than a boiler or steam, call Jennifer at (866) 637-9247. If the user says they need help with something please say, I apologize but I can not assist with that.

 Do not answer requests that are not related to Atlas Copco and the data above. If they are looking to buy a compressor instead of rent, please provide them with this link. https://www.atlascopco.com/en-us/compressors. If they are looking to buy any product, let them know we only rent

Ask for the application only if the user is looking for an air compressor. based on the application and number of units, recommend the number of accessories if any they will need such as hoses, dryers, boosters and heat exchangers  

If they are looking to rent anything other than an air compressor do not recommend accessories

Provide a link to the product if applicable and the phone number to call  

If you doesn't find any exact match of the user requirements then look for the closest match
If the user is looking to buy any of the following: give them the contact for the appropriate department
If they are looking for a product or part that falls within the other department please give them the information for the right department

#other departments

Atlas Copco Compressors
www.atlascopco.com/en-us/compressors
Phone: +1 866-546-3588
Email: info@atlascopcousa.com
• Air Compressors (stationary, electric)
• Oil Free Air Compressors
• Oil-Injected Air Compressors
• Air Treatment (dryers, receivers, etc)
• Aeration & Industrial Blowers
• CNG/RNG Compressors
• Nitrogen and Oxygen Generators • Piping and Installation

Atlas Copco Power Technique
www.atlascopco.com/en-us/construction-equipment
 Phone: +1 800-732-6762
Email: acce.customerservice@atlascopco.com
• Air Compressors (mobile, portable, diesel) • Mobile Generators (diesel, portable, gas)
• Dewatering (diesel) and Submersible Pumps • Light Towers
• Construction & Demolition Tools

Atlas Copco Tools
www.atlascopco.com/en-us/itba
Phone: +1 248-373-3300
Email: acta.inquiries@atlascopco.com
• Air Line Accessories
• Air Motors
•Assembly Solutions
• Bolting Solutions
• Joining Solutions
• Material Removal Tools
• Software Solutions
• Total Workstation

Atlas Copco Vacuum
www.atlascopco.com/en-us/vacuum-solutions
Phone: +1 800-848-4511
Email: NACustomerCare@vt.atlascopco.com
• Dry Vacuum Pumps
• Oil-Sealed Vacuum Pumps
• Liquid Ring Vacuum Pumps
• Rotary Screw Vacuum Pumps

Turbomachinery
Phone: +1 518-765-3344
Email: aftermarket.gap.NA@atlascopco.com 
• Gas and Process Equipment
• Turbo Centrifugal Compressors
• Turbo Expanders
• LNG Compressors
• Rent Steam Boilers

Powerhouse Boilers
www.powerhouse.com/en
 ph-quotes@powerhouse.com
(888)-998-1552
• Steam Boilers
• Boilers
• Steam
• Hot water
• Everything boiler and steam related

'''

messages = [
    {"role": "system", "content": "Act as a Customer Service Assistant for Atlas Copco"},
    {"role": "system", "content": "You will ask questions based on the data that prodived bellow and take the answer from the user and recommend them based on the rules bellow"},
    {"role": "system", "content":f'''{prompt}

'''},
    {"role": "assistant", "content": "Thank you for contacting Atlas Copco, what are you looking for? We offer Oil-free Air compressors, Steam boilers, and Nitrogen generators equipment rentals."}
]

max_response_tokens = 250
token_limit= 8000
app = Flask(__name__)
CORS(app)

@app.after_request
def add_header(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = '*'
    return response

def clear_old_sessions():
    global chat_history
    global time_track
    
    if chat_history:
        for key, value in time_track.items():
            if datetime.now() - time_track[key] > timedelta(hours=6):
                chat_history.pop(key)
                time_track.pop(key)

def update_chat(user_id, role, content):
    if user_id in chat_history:
        chat_history[user_id].append({"role": role, "content": content})
    else:
        chat_history[user_id] = list(messages[:])
        chat_history[user_id].append({"role": role, "content": content})
    return chat_history[user_id][:]


def num_tokens_from_messages(messages,user_id, model="gpt-4"):
    encoding = tiktoken.encoding_for_model(model)
    num_tokens = 0
    for key, value in messages.items():
        if key == user_id:
            num_tokens += 4  # every message follows <im_start>{role/name}\n{content}<im_end>\n
            for message in value:
                for key1, value1 in message.items():
                    num_tokens += len(encoding.encode(value1))
                    if key1 == "name":  # if there's a name, the role is omitted
                        num_tokens += -1  # role is always required and always 1 token
    num_tokens += 2  # every reply is primed with <im_start>assistant
    return num_tokens


def get_chatgpt_response(messages):
	response = openai.ChatCompletion.create(
  model="gpt-4",
  messages=messages,
  max_tokens=max_response_tokens,
)
	return  response['choices'][0]['message']['content']

# def json_serializer(obj):
    # if isinstance(obj, (datetime, date)):
        # return obj.isoformat()
    # raise TypeError(f'Type {type(obj)} is not serializable')
@app.route('/chat', methods=['POST','GET'])
def bot():
    global chat_history, time_track  # add global variable for time_track

    clear_old_sessions()

    user_id = request.form['user_id']
    if user_id=='null':
        user_id = str(uuid.uuid4()) 
        chat_history[user_id] = messages[:]
        #print("Your New Created User ID :",user_id)
    if user_id not in chat_history:
        output = {'Bot':  'User_ID Expired', 'user_id': user_id}
        return jsonify(output)
        
        
    user_input = request.form['query']
    time_track[user_id] = datetime.now()  # update time_track for user
        
    chat_history[user_id] = update_chat(user_id, "user", user_input)
    conv_history_tokens = num_tokens_from_messages(chat_history,user_id)
    while (conv_history_tokens+max_response_tokens >= token_limit):
        del chat_history[user_id][4] 
        conv_history_tokens = num_tokens_from_messages(chat_history,user_id)
    model_response = get_chatgpt_response([msg for msg in chat_history[user_id]])
    chat_history[user_id] = update_chat(user_id, "assistant", model_response)
    time_track[user_id] = datetime.now()  # update time_track again for user
        
    # print the bot response
    #print("Bot:", chat_history[user_id][-1]['content'], "\n")
    
    output = {'Bot':  chat_history[user_id][-1]['content'], 'user_id': user_id}
    if datetime.now() - time_track[user_id] > timedelta(hours=6):
        chat_history.pop(user_id)
        time_track.pop(user_id)
        
    return jsonify(output)
    # remove the user's chat history if it's older than 6 hours
    
    
    


if __name__ == "__main__":
   app.run(debug=True,port=4000)