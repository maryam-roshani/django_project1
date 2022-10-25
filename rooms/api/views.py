from django.http import JsonResponse


def getRouts(reequest):
	routes = [
		'GET /api/rooms',
		'GET /api/rooms/:id'
	]
	return JsonResponse(routes, safe=False)