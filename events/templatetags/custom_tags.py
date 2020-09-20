from django import template
import datetime 
register = template.Library()



@register.filter(expects_localtime=True)
def is_older_than_today(value):
    if isinstance(value, datetime.datetime):
        value = value.date()
    delta = value - datetime.date.today()
    return delta.days >= 1

@register.filter(name='split')
def split(value, key):
  """
    Returns the value turned into a list.
  """
  return value.split(key)

  