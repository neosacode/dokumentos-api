class KeyNotInResponseException(Exception):
	def __init__(self, key):
		super().__init__('Field "{}" not found in webhook response'.format(key))


class WordsListException(Exception):
	def __init__(self):
		super().__init__('Words response key should be a list')