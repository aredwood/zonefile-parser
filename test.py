import re

# input is a string of quoted strings, there may or may not be a newline or space between quotes
sample_input = """
"v=DKIM1; t=s; p=MIIBIjANBg/kqhGGEEkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA2KXqtqfmWDgP6X7d2gKPCAl"
                        		"tlgbSstMhKj3+UA+VbGZomqyY1er7QqkIriQSuTQT2hkV7DHHFMhYx4MFUvDHbLtTTREtkkzKqRr2Z1TwuYmgS5kzo453lm0uiQIxQXXHLlUMST0VerzO/Jp+0Ix76g68DxSU2nWudW6rE"
                        		"7g3vADE20JDJqriUKjGBqKY0RR/CqdLCLsyBrvuF/Nefg8hB/oz/0a3Ae1AYVmqtEf2d9Z/seGQPVj+E/wqobRyYdEKo4BBdUfRb3Jaw6rpqQ5aVOTuOZF5zaozf0BtgKeo"
                        		"l4PzCcPLQUTWp42Vh+9aeCL/j34XJyFjN7+40L3itdequjc6v/Ose51wnSMtR4sWwIDAQAB"
"""


def help_me(input_string):

  pattern = re.compile(r'"(.*?)"')


  matches = re.findall(pattern,input_string)

  return "".join(matches)


print(help_me(sample_input))
# assert help_me(sample_input) == "123"
# print("thank u")