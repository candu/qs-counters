import datetime
from qs_counters.models import Counter, Update

class Metrics(object):
  @classmethod
  def _getDuration(cls, presses):
      total = 0
      last_pressed = None
      for press in presses:
          if press.pressed:
              last_pressed = press.timestamp
          elif last_pressed is not None:
              dt = press.timestamp - last_pressed
              total += dt.seconds + 0.000001 * dt.microseconds
              last_pressed = None
      return total

  @classmethod
  def _midnightOnDate(cls, date):
      midnight = datetime.time()
      return datetime.datetime.combine(date, midnight)

  @classmethod
  def getMetrics(cls, counter_or_id):
      if isinstance(counter_or_id, int):
          counter = Counter.objects.get(id=counter_or_id)
      else:
          counter = counter_or_id
      if counter is None:
          raise Exception('invalid counter object/id')
      if counter.type == 'count':
          return cls.getCountMetrics(counter)
      if counter.type == 'duration':
          return cls.getDurationMetrics(counter)

  @classmethod
  def _getDayWeekStarts(cls):
      now = datetime.datetime.now()
      day_start = cls._midnightOnDate(now.date())
      week_start = cls._midnightOnDate(now - datetime.timedelta(days=6))
      return (day_start, week_start)

  @classmethod
  def getCountMetrics(cls, counter):
      day_start, week_start = cls._getDayWeekStarts()
      day_count = Update.objects.filter(
          counter__id=counter.id,
          timestamp__gte=day_start).count()
      week_count = Update.objects.filter(
          counter__id=counter.id,
          timestamp__gte=week_start).count()
      return (day_count, week_count)

  @classmethod
  def getDurationMetrics(cls, counter):
      day_start, week_start = cls._getDayWeekStarts()
      day_presses = Update.objects.filter(
          counter__id=counter.id,
          timestamp__gte=day_start)
      week_presses = Update.objects.filter(
          counter__id=counter.id,
          timestamp__gte=week_start)
      return (cls._getDuration(day_presses), cls._getDuration(week_presses))
