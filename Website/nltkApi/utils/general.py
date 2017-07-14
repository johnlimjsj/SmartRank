

def translate(value, in_min, in_max, out_min, out_max, mode):
	# Figure out how 'wide' each range is
	in_span = in_max - in_min
	out_span = out_max - out_min

	if mode == 1: #normal
		return out_min + out_span * (value - in_min) / in_span
	elif mode == 2: #reverse mapping
		return out_max - out_span * (value - in_min) / in_span

	return None
