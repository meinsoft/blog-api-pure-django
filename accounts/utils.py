import json 
from django.http import JsonResponse


def parse_json_body(request):
	try:
		data = json.loads(request.body)
		return data,None
	except json.JSONDecodeError:
		return None,'invalid json'

def error_response(code,message,details=None,status=400):
	obj = 	{
    "success": False,
    "error": {
        "code": code,
        "message": message,
    	}
	}
	if(details is not None):
		obj['error']['details']=details
	return JsonResponse(obj,status=status)