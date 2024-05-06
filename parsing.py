from bs4 import BeautifulSoup
from datetime import datetime
import os
import json

data_in = 'deliveroo/'
files = os.listdir(data_in)

captures = []
for file in files:
    doc = data_in + file
    with open(doc, 'r', encoding='utf-8') as fl:
        html_content = fl.read()
        soup = BeautifulSoup(html_content, 'html.parser')
        title = soup.find('title').text

    allp = soup.find_all('p')
    allp = [x.text.strip() for x in allp]
    spot_question = allp.index('Des questions sur votre commande ?')
    try:
        spot_delivery = allp.index('Frais de livraison')
    except(ValueError) as e:
        spot_delivery = -1

    order_nb = int(allp[spot_question+7][39:][::-1][1:][::1])
    order_total = float(allp[spot_question-1][1:])
    if(spot_delivery == -1):
        order_fee = .0
    else:
        order_fee = allp[spot_delivery+1]
        if(order_fee == "Free"):
            order_fee = .0
        else:
            order_fee = float(order_fee[1:])
    order_date = datetime.strptime(file_name[0:24], "%a_%d_%b_%Y_%H_%M_%S").strftime("%d/%m/%Y %H:%M")

    restau_name = allp[1]
    restau_rue = allp[2]
    restau_ville = allp[3]
    restau_cp = allp[4]
    restau_phone = allp[5]

    cus_name = allp[6]
    cus_rue = allp[7]
    cus_ville = allp[8]
    cus_cp = allp[9]
    cus_phone = allp[10]

    item_list = allp[14:spot_question-10]
    item_quant = []
    item_name = []
    item_price = []
    for i,x in enumerate(item_list):
        if(x[1] == 'x' and len(x) <= 3):
            item_quant.append(int(x[::-1][1:][::-1]))
            item_name.append(item_list[i+1])
            if(i != 0):
                if(item_list[i-1] == 'Free'):
                    item_price.append(0)
                elif(item_list[i-1][0] == '€'):
                    item_price.append(float(item_list[i-1][1:].replace(',', '.')))
                else:
                    item_price.append(float(item_list[i-1][::-1][2:][::-1].replace(',', '.')))
        if(i == len(item_list)-1):
            if(x == 'Free'):
                    item_price.append(0)
            elif(x[0] == '€'):
                    item_price.append(float(x[1:].replace(',', '.')))
            else:
                item_price.append(float(x[::-1][2:][::-1].replace(',', '.')))

    capture = {}
    capture['order'] = {}
    capture['restaurant'] = {}
    capture['customer'] = {}
    capture['order_items'] = []
    
    capture['order']['order_datetime'] = order_date
    capture['order']['order_number'] = order_nb
    capture['order']['delivery_fee'] = order_fee
    capture['order']['order_total_paid'] = order_total

    capture['restaurant']['name'] = restau_name
    capture['restaurant']['address'] = restau_rue
    capture['restaurant']['city'] = restau_ville
    capture['restaurant']['postcode'] = restau_cp
    capture['restaurant']['phone_number'] = restau_phone

    capture['customer']['name'] = cus_name
    capture['customer']['address'] = cus_rue
    capture['customer']['city'] = cus_ville
    capture['customer']['postcode'] = cus_cp
    capture['customer']['phone_number'] = cus_phone

    for i in range(len(item_quant)):
        item = {}
        item['name'] = item_name[i]
        item['quantity'] = item_quant[i]
        item['price'] = item_price[i]
        capture['order_items'].append(item)

    captures.append(capture)

json_string = json.dumps(captures)
with open('captures.json', 'w') as json_file:
    json_file.write(json_string)

"""
if __name__ == "__main__":
    ajoute les fonctions ici
"""