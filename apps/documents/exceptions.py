class KeyNotInResponseException(Exception):
	def __init__(self, key):
		super().__init__('Field "{}" not found in webhook response'.format(key))