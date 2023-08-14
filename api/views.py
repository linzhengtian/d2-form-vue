from ninja import Router

api_router = Router()

@api_router.get("/testuserinfo/")
def testuserinfo(request):
    return {'msg': "success"}
