from flask import Flask, flash, request, redirect, render_template
from werkzeug.utils import secure_filename
import pandas as pd
import numpy as np
import skfuzzy as fuzz

data = pd.read_csv('Datanew.csv')
features = data.drop(['Total_Harga', 'Ukuran','Jumlah_item'], axis=1)
data_matrix = features.to_numpy().T
data_asli = data.to_numpy()
centers, membership, best_u0, best_d, best_jm, best_p, best_fpc = fuzz.cluster.cmeans(data_matrix, c=3, m=2, error=0.005, maxiter=1000, init=None)
best_cluster_membership = np.argmax(membership, axis=0)

def get_recommendations(input):
    global centers, best_cluster_membership
    cluster_membership = fuzz.cluster.cmeans_predict(input.reshape(1, -1).T, centers, m=2, error=0.005, maxiter=1000, init=None)[0]
    cluster = np.argmax(cluster_membership, axis=0)[0]
    cluster_products = []
    for idx, member in enumerate(best_cluster_membership):
        # print("{} vs {}".format(cluster, member))
        if cluster == member:
            cluster_products.append(idx)
    return cluster_products

app = Flask(__name__)
app.secret_key = "secrpet key"

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/hasil')
def form():
	return render_template('hasil.html')

@app.route('/hasil', methods=['POST'])
def process_form():
	question1 = request.form.get('question1')
	print(question1)

	question2 = request.form.get('question2')
	print(question2)

	question3 = request.form.get('question3')
	print(question3)
	question4 = request.form.get('question4')
	print(question4)

	question5 = request.form.get('question5')
	print(question5)

	question6 = request.form.get('question6')
	print(question6)

	question7 = request.form.get('question7')
	print(question7)

	jenis_kemasan = ""
	if(question6=="plastik"):
		jenis_kemasan = 1
	else:
		jenis_kemasan = 2

	varian_aroma = ""
	if(question7=="Blue fresh"):
		varian_aroma =6
	elif(question7=="Buble Gum"):
		varian_aroma =5
	elif(question7=="Vanilla"):
		varian_aroma =3
	elif(question7=="Coffee"):
		varian_aroma =4
	
	aroma_fresh = "" 
	if(question1=="iya"):
		aroma_fresh = 1
	else:
		aroma_fresh = 0
	
	aroma_coffee =""
	if(question2=="iya"):
		aroma_coffee = 1
	else:
		aroma_coffee = 0
	
	frangrance_oil =""
	if(question3=="iya"):
		frangrance_oil = 1
	else:
		frangrance_oil = 0
	
	charlodir=""
	if(question4=="iya"):
		charlodir= 1
	else:
		charlodir = 0
	
	benzalkonium=""
	if(question5=="iya"):
		benzalkonium= 1
	else:
		benzalkonium = 0
	
	input_data = np.array([
		varian_aroma,
		aroma_fresh,
		aroma_coffee,
		frangrance_oil,
		charlodir,
		benzalkonium,
		jenis_kemasan,
	])
	# print(input_data.reshape(1,-1).T)

	hasil = get_recommendations(input_data)
	global data_asli
	# print(data_asli[0])
	hasilcetak = []
	for id in hasil:
		# print(data_asli[id])
		harga = str("Rp ")+str(data_asli[id][0])
		ukuran = str(data_asli[id][1])+str(" ml")
		var_aroma = data_asli[id][2]
		varian_aroma = data_asli[id][2]
		varian_aroma = 'Vanilla' if varian_aroma == 3 else 'Coffe' if varian_aroma == 4 else 'Bubble Gum' if varian_aroma == 5 else 'Blue Fresh' 
		aroma_fresh = data_asli[id][3]
		aroma_fresh = 'Aroma Fresh' if aroma_fresh == 1 else 'Non Fresh'
		aroma_coffe = data_asli[id][4]
		aroma_coffe = 'Aroma Kopi' if aroma_coffe == 1 else 'Non Kopi'
		frangrance_oil = data_asli[id][5]
		frangrance_oil = 'Dengan Fragrance Oil' if frangrance_oil == 1 else 'Tanpa Fragrance Oil'
		charlodir = data_asli[id][6]
		charlodir = 'Dengan Charlodir' if charlodir == 1 else 'Tanpa Charlodir'
		benzalkonium = data_asli[id][7]
		benzalkonium = 'Dengan Benzalkonium' if benzalkonium == 1 else 'Tanpa Benzalkonium'
		jenis_kemasan = data_asli[id][8]
		jenis_kemasan = 'Kemasan Plastik' if jenis_kemasan == 1 else 'Kemasan Karton'
		hasilcetak.append([id,var_aroma,harga,ukuran,varian_aroma,aroma_fresh,aroma_coffe,frangrance_oil,charlodir,benzalkonium,jenis_kemasan])

	return render_template('hasil.html', hasilcetak=hasilcetak, cluster=varian_aroma)


@app.route('/product', methods=['GET'])
def product():
	global data_asli
	productid = request.args.get('id')
	print(productid)
	
	print(data_matrix.T[int(productid)])
	input_data = data_matrix.T[int(productid)]
	harga = str("Rp ")+str(data_asli[int(productid)][0])
	ukuran = str(data_asli[int(productid)][2])+str(" ml")
	varian_aroma = input_data[0]
	varian_aroma = 'Vanilla' if varian_aroma == 3 else 'Coffe' if varian_aroma == 4 else 'Bubble Gum' if varian_aroma == 5 else 'Blue Fresh' 
	aroma_fresh = input_data[1]
	aroma_fresh = 'Aroma Fresh' if aroma_fresh == 1 else 'Non Fresh'
	aroma_coffe = input_data[2]
	aroma_coffe = 'Aroma Kopi' if aroma_coffe == 1 else 'Non Kopi'
	frangrance_oil = input_data[3]
	frangrance_oil = 'Dengan Fragrance Oil' if frangrance_oil == 1 else 'Tanpa Fragrance Oil'
	charlodir = input_data[4]
	charlodir = 'Dengan Charlodir' if charlodir == 1 else 'Tanpa Charlodir'
	benzalkonium = input_data[5]
	benzalkonium = 'Dengan Benzalkonium' if benzalkonium == 1 else 'Tanpa Benzalkonium'
	jenis_kemasan = input_data[6]
	jenis_kemasan = 'Kemasan Plastik' if jenis_kemasan == 1 else 'Kemasan Karton'
	data_product = [productid,harga,ukuran,varian_aroma,aroma_fresh,aroma_coffe,frangrance_oil,charlodir,benzalkonium,jenis_kemasan]
	print(data_product)

	hasil = get_recommendations(input_data)
	# print(data_asli[0])
	hasilcetak = []
	counter = 1
	for id in hasil:
		# print(data_asli[id])
		harga = str("Rp ")+str(data_asli[id][0])
		ukuran = str(data_asli[id][1])+str(" ml")
		varian_aroma = data_asli[id][2]
		var_aroma = data_asli[id][2]
		varian_aroma = 'Vanilla' if varian_aroma == 3 else 'Coffe' if varian_aroma == 4 else 'Bubble Gum' if varian_aroma == 5 else 'Blue Fresh' 
		aroma_fresh = data_asli[id][3]
		aroma_fresh = 'Aroma Fresh' if aroma_fresh == 1 else 'Non Fresh'
		aroma_coffe = data_asli[id][4]
		aroma_coffe = 'Aroma Kopi' if aroma_coffe == 1 else 'Non Kopi'
		frangrance_oil = data_asli[id][5]
		frangrance_oil = 'Dengan Fragrance Oil' if frangrance_oil == 1 else 'Tanpa Fragrance Oil'
		charlodir = data_asli[id][6]
		charlodir = 'Dengan Charlodir' if charlodir == 1 else 'Tanpa Charlodir'
		benzalkonium = data_asli[id][7]
		benzalkonium = 'Dengan Benzalkonium' if benzalkonium == 1 else 'Tanpa Benzalkonium'
		jenis_kemasan = data_asli[id][8]
		jenis_kemasan = 'Kemasan Plastik' if jenis_kemasan == 1 else 'Kemasan Karton'
		hasilcetak.append([id,var_aroma,harga,ukuran,varian_aroma,aroma_fresh,aroma_coffe,frangrance_oil,charlodir,benzalkonium,jenis_kemasan])
		counter=counter+1
		if counter>5:
			break
	print(hasilcetak)
	return render_template('product.html', hasilcetak=hasilcetak, hasil=hasil, product=data_product, data=input_data)


 
if __name__ == "__main__":
    app.run(debug=True)
	