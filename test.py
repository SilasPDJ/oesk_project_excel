from datetime import datetime, timedelta, timezone
import sched
# mail.DeferredDeliveryTime = datetime(self.y(), self.m(), self.hj(), , tzinfo=timezone.utc)
a = datetime.now()
a = a.replace(hour=23, minute=0)
print(a + timedelta(hours=9))

sched.