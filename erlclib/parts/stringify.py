from json import dumps
# UNUSED

def stringify(obj, separators=None, ensure_ascii=False):
  """
  Function to mimic JSON.stringify in Python

  Args:
      obj: The Python object to convert to a JSON string.
      separators: An optional tuple of (item_separator, key_separator).
      ensure_ascii: An optional boolean to control how non-ASCII characters are represented.

  Returns:
      A JSON string representation of the object.
  """
  return dumps(obj, separators=separators, ensure_ascii=ensure_ascii)