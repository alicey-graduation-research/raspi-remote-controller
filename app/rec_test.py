from irrp import IRRP

ir = IRRP(file="test", post=130, no_confirm=True)
ir.Record(GPIO=22, ID="air:on")
ir.stop()