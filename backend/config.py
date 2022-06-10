from flask import Blueprint
import datetime


configapp = Blueprint('configapp', __name__)


@configapp.app_template_filter('dtime')
def dtime(s):
    return s.strftime("%d/%m/%Y")


@configapp.app_template_filter('dettime')
def dettime(s):
    s = datetime.datetime.fromtimestamp(s.timestamp())
    return s.strftime("%d %B %Y")


@configapp.app_template_filter('detailtime')
def detailtime(s):
    s = datetime.datetime.fromtimestamp(s.timestamp())
    return s.strftime("%d %B %Y, %H:%M:%S")


@configapp.app_template_filter('detailtime1')
def detailtime1(s):
    s = datetime.datetime.fromtimestamp(s.timestamp())
    # return s.strftime("%d %B %Y, %H:%M")
    return s.strftime("%d %B %Y, %H:%M")


@configapp.app_template_filter('detailtime2')
def detailtime1(s):
    now = datetime.datetime.now() + datetime.timedelta(seconds=60 * 3.4)
    s = datetime.datetime.fromtimestamp(s.timestamp())
    # waktu = s.strftime("%Y-%m-%d %H:%M:%S")
    return s.strftime("%Y-%m-%d %H:%M:%S")

    # return timeago.format(waktu, now, 'id_ID')


@configapp.app_template_filter('rupiah')
def rupiah(s):
    str_value = str(s)

    reverse = str_value[::-1]
    temp_reverse_value = ""

    for index, val in enumerate(reverse):
        if (index + 1) % 3 == 0 and index + 1 != len(reverse):
            temp_reverse_value = temp_reverse_value + val + "."
        else:
            temp_reverse_value = temp_reverse_value + val

    temp_result = temp_reverse_value[::-1]

    return "Rp. " + temp_result
