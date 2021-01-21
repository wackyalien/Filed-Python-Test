from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_cors import CORS, cross_origin
from datetime import datetime


app = Flask(__name__)
CORS(app)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class Creditcard(db.Model):
    CreditCardNumber = db.Column(db.String,primary_key = True)
    CardHolder = db.Column(db.String,nullable = False)
    ExpirationDate = db.Column(db.DateTime,nullable = False)
    SecurityCode = db.Column(db.String(3))
    Amount = db.Column(db.Numeric(10,2),nullable = False)

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def __repr__(self):
        return self.CreditCardNumber

# db.create_all()

credit_put_args = reqparse.RequestParser()
credit_put_args.add_argument("CreditCardNumber",type=str,help="Name of the video",required = True)
credit_put_args.add_argument("CardHolder",type=str,help="Likes on the video",required = True)
credit_put_args.add_argument("ExpirationDate",type=str,help="Views of the video",required = True)
credit_put_args.add_argument("SecurityCode",type=str)
credit_put_args.add_argument("Amount",type=float,help="Views of the video",required = True)


def PremiumPaymentGateway():
    return 'Premium Payment Done'

def ExpensivePaymentGateway():
    return  'Expensive Payment Done'

def CheapPaymentGateway():
    return 'Cheap Payment Done'


@app.route('/ProcessPayment', methods=['POST'])
@cross_origin()
def ProcessPayment():
    args = credit_put_args.parse_args()
    try:
        datetime_str = args['ExpirationDate']
        datetime_object = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S.%f')
        diff = datetime_object>datetime.now()
        if len(str(args['SecurityCode']))==3 or len(str(args['SecurityCode']))==4:
            if (args['Amount']>=0 and diff==True):

                if (args['Amount']>0 and args['Amount']<=20.0):
                    res=CheapPaymentGateway()
                elif (args['Amount']>21.0 and args['Amount']<=500.0):
                    res=ExpensivePaymentGateway()
                else:
                    res=PremiumPaymentGateway()    
                return make_response('Payment is processed: 200 OK')
            else:
                return make_response('The request is invalid: 400 bad request')
        else:
            return make_response('The request is invalid: 400 bad request')
    except Exception:
        return make_response('Any error: 500 internal server error')


if __name__ == "__main__":
    app.run(debug=True)
