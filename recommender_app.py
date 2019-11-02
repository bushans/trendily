from flask import Flask, jsonify, request, render_template, url_for, flash, redirect
from predict import Predict
from werkzeug.utils import secure_filename
import os
import stripe

app = Flask(__name__)

STRIPE_PUBLISHABLE_KEY = 'pk_test_1Hv3MowOs3l0jNrEmHITabcw002vq1NuIp'
STRIPE_SECRET_KEY = 'sk_test_DXWufFtOIxTe4ZeXrFxwqEyv00hwFNaNFr'

#stripe_keys = {
 #'secret_key': os.environ['STRIPE_SECRET_KEY'],
  #'publishable_key': os.environ['STRIPE_PUBLISHABLE_KEY']
#}

#if stripe_keys.get('secret_key') != -1:
    #stripe.api_key = stripe_keys['secret_key']
#else:

#stripe.api_key = stripe_keys['secret_key']
stripe.api_key = STRIPE_SECRET_KEY
    
p = Predict()

UPLOAD_FOLDER = 'static'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# @app.route('/')
# def index():
#    return render_template('index.html', key=stripe_keys['publishable_key'])

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        try:
            # render_template('charge.html', amount=amount)
            return  render_template('home.html')
        except:
            return 'There was an issue adding your task'

    else:
        return render_template('index.html', key=STRIPE_PUBLISHABLE_KEY)
        #return render_template('index.html', key=stripe_keys['publishable_key'])

@app.route('/charge', methods=['POST'])
def charge():
    try:
        amount = 500   # amount in cents
        customer = stripe.Customer.create(
            email='sample@customer.com',
            source=request.form['stripeToken']
        )
        stripe.Charge.create(
            customer=customer.id,
            amount=amount,
            currency='usd',
            description='Flask Charge'
        )
        # return render_template('charge.html', amount=amount)
        render_template('charge.html', amount=amount)
        return  redirect('/home') 
    except stripe.error.StripeError:
        return render_template('error.html')

@app.route('/home', methods=['GET'])
def render_home():
    return render_template('home.html')

@app.route('/data', methods=['GET'])
def render_data():
    return render_template('project_details.html')


@app.route('/data/model', methods=['GET'])
def render_datamodel():
    return render_template('data_model.html', img=url_for('static', filename='Attributes1000_head_arch.jpg'))


@app.route('/data/eda', methods=['GET'])
def render_dataeda():
    return render_template('data_eda.html')


@app.route('/data/rec-method', methods=['GET'])
def render_datarecmethod():
    return render_template('data_rec_method.html')


@app.route('/resources', methods=['GET'])
def render_resources():
    return render_template('resources.html')


@app.route('/recs', methods=['GET'])
def render_html():
    return render_template('get_inputs.html')


@app.route('/recs', methods=['POST'])
def make_recs():

    if 'img' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['img']
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        img_path = secure_filename(file.filename)
        file.save(os.path.join(UPLOAD_FOLDER, img_path))

    recs = p.get_recs('static/'+img_path)
    return render_template('show_rec_imgs.html', img_path=url_for('static', filename=img_path), images=recs[0], urls=recs[2])
