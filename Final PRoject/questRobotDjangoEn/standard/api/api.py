from django.shortcuts import redirect
from ..common.helper import *
from ..common.reply import returAnswer
from ..common.voice import reg


def index(request):
    '''
    main page
    :param request:
    :return:
    '''
    return redirect('/dist/pages/index.html')


def reply(request):
    # match answer from question list
    res = returAnswer(request.POST.get("content"))

    # if has result return to page
    if res:
        return jsonResponse(0, 'success', res)

    return jsonResponse(1, 'fail', ' I\'m still learning the relevant knowledge')


def audio(request):
    # receiver wav obj get result from api
    result = reg(obj=request.FILES["file"])

    if result:
        return jsonResponse(0, 'success', result)
    return jsonResponse(1, 'fail', ' I\'m still learning the relevant knowledge')


def logout(request):
    return redirect('/dist/admin/login.html')
