import json
from django.http.response import JsonResponse
from api.models import Session
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi


def post(request):
    try:
        print(request.body)
        data = json.loads(request.body)
        session = Session()
        session.facebook_id = data['facebook_id']
        session.session_id = data['session_id']
        session.save()
        return JsonResponse({"message": "ok"}, safe=False)
    except Exception as e:
        return JsonResponse({"message": e}, safe=False)


def get(request, id):
    try:
        session = Session.objects.filter(facebook_id=id).values()
        return JsonResponse(list(session), safe=False)
    except Exception as e:
        return JsonResponse({"message": e}, safe=False)


def webhook(request):
    try:
        body = json.loads(request.body)
        print(body)
        if body["queryResult"]["intent"]["name"] == "projects/velaryonbot-naos/agent/intents/310350dc-3eaa-4c7e-bbeb-0cf8efaedf6f":
            return exists(request)
        else:
            # elif body["queryResult"]["intent"]["name"] == "projects/velaryonbot-naos/agent/intents/1f553fe6-3325-486b-b3f5-ef03b347686b":
            return saveClient(request)
    except Exception as e:
        raise e


def exists(request):
    # print(request.body)

    data = json.loads(request.body)
    itemExists = checkAlbumInDb(data)

    fulfillmentText = "Si lo tenemos disponible ¿deseas realizar un pedido?" if itemExists else "Disculpa, pero no tenemos ese ejemplar disponible. Pero si así lo desea, puede proporcionarnos sus datos para que le notifiquemos cuando el ejemplar que desea vuelva a estar disponible. ¿Le parece? 😄"
    outputContext = str(
        "/contexts/siDisponible") if itemExists else str("/contexts/noDisponible")

    rawResponse = {
        "fulfillmentMessages": [
            {
                "text": {
                    "text": [fulfillmentText]
                }
            }
        ],
        "outputContexts": [
            {
                "name": data['session'] + outputContext,
                "lifespanCount": 5,
            }
        ]
    }
    try:
        return JsonResponse(rawResponse, safe=False)
    except Exception as e:
        return JsonResponse({"message": e}, safe=False)


def checkAlbumInDb(body):
    try:
        parameters = {
            "name": body["queryResult"]["parameters"]["albumes"],
            "artist": body["queryResult"]["parameters"]["artista"],
            "presentation": body["queryResult"]["parameters"]["presentacion"]
        }
        client = MongoClient(
            "mongodb+srv://corlysvelaryon:test@mondongo-bot.zakwctm.mongodb.net/?retryWrites=true&w=majority",
            server_api=ServerApi('1'),
        )

        db = client["velaryon"]
        # print(parameters)
        album = db["album"].find_one(parameters)
        # print(album)
        if album is None:
            return False
        return True
    except Exception as e:
        print(e)
        return False


def saveClient(request):
    try:
        body = json.loads(request.body)
        parameters = {
            "first_name": body["queryResult"]["parameters"]["person"]["name"],
            "last_name": body["queryResult"]["parameters"]["apellido"],
            "email": body["queryResult"]["parameters"]["email"],
            "phone_number": body["queryResult"]["parameters"]["phone-number"]
        }

        client = MongoClient(
            "mongodb+srv://corlysvelaryon:test@mondongo-bot.zakwctm.mongodb.net/?retryWrites=true&w=majority",
            server_api=ServerApi('1'),
        )

        db = client["velaryon"]
        client = db["clients"].insert_one(parameters)
        return JsonResponse({"message": "ok"}, safe=False)
    except Exception as e:
        return JsonResponse({"message": e}, safe=False)
