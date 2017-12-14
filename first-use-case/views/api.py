from flask import Blueprint, jsonify

from models.BundleHashModel import BundleHashModel
from models.AddressModel import AddressModel
from models.Transactions import TransactionModel
from cassandra.cqlengine.query import DoesNotExist
from cassandra.cqlengine.query import MultipleObjectsReturned

api = Blueprint("api", __name__)



@api.route("/")
def index():
    return "Hello Cassandra.."


@api.route("/hash-exists/<string:hashInput>")
def hashExists(hashInput):
    result = TransactionModel.objects(hash=hashInput)
    if result.count() > 0:
        return jsonify({"exists": "true", "count":result.count()})
    else:
        return jsonify({"exists": "false" , "count":result.count()})

# @api.route("/address-exists/<string:addressInput>")
# def addressExists(addressInput):
#     result = AddressModel.objects(address=addressInput)
#     if result.count() > 0:
#         return jsonify({"exists": "true", "count":result.count()})
#     else:
#         return jsonify({"exists": "false" , "count":result.count()})

@api.route("/transactions-by-address/<string:addressInput>")
def getTransactionByAddress(addressInput):
    result = AddressModel.objects(address=addressInput)
    return jsonify([res.get_address_data() for res in result])

@api.route("/address-info/<string:addressInput>")
def getAddressInfo(addressInput):
    isSpentFrom = isReceivedOnly = addressExists = False

    #Check if Address exists or not
    result = AddressModel.objects(address=addressInput)
    if result.count() > 0:
        addressExists = True
    else:
        return jsonify({
                        "exists" : addressExists,
                        "is_spent_from"  : isSpentFrom,
                        "is_received_only" : isReceivedOnly
                 })

    #Check if its is spent from or not.
    spent_from_query = result.filter(value__lt=0)
    try:
        spent_from_query.get()
        #if it returns one or multiple object then address is SPENT FROM
        #in case of multiple objects it will through MultipleObjectsReturned Exception.
        isSpentFrom = True
    except DoesNotExist as e:
        isSpentFrom = False
    except MultipleObjectsReturned as m:
        isSpentFrom = True



    if isSpentFrom == True:
        # if it spent_from address then It is not received only
        return jsonify({
                        "exists" : addressExists,
                        "is_spent_from"  : isSpentFrom,
                        "is_received_only" : isReceivedOnly
                })
    else:
        #If the address is not spent_from then further check if it is received only or not.
        #If it has received any token then it means is received only.
        #Otherwise its a no value transfer and value will be equal to 0 in that case.

        received_only_query = result.filter(AddressModel.value > 0)
        try:
            received_only_query.get()
            # if it returns one or multiple object then address is RECEIVED ONLY
            # in case of multiple objects it will through MultipleObjectsReturned Exception.
            isReceivedOnly = True
        except MultipleObjectsReturned:
            isReceivedOnly = True
            return jsonify({
                        "exists" : addressExists,
                        "is_spent_from"  : isSpentFrom,
                        "is_received_only" : isReceivedOnly
                })
        except DoesNotExist:
            return jsonify({
                        "exists" : addressExists,
                        "is_spent_from"  : isSpentFrom,
                        "is_received_only" : isReceivedOnly
                })

@api.route("/bundle/<string:bundle_hash_input>")
def getBundle(bundle_hash_input):
    result = BundleHashModel.objects(bundle_hash=bundle_hash_input)
    return jsonify([res.get_bundle_data() for res in result])