from irrp import IRRP

ir = IRRP(file="test", no_confirm=True)
ir.Playback(GPIO=23, ID="air:on")
ir.stop()