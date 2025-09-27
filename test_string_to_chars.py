"""Generated Python code from mlpy ML transpiler."""

# This code was automatically generated from ML source
# Modifications to this file may be lost on regeneration

# ML Standard Library imports
from mlpy.stdlib.console_bridge import console
from mlpy.stdlib import getCurrentTime, processData

from mlpy.stdlib.string_bridge import string as ml_string

def test_string_to_chars():
    print('=== String toChars() Function Test ===')
    text = 'Hello'
    chars = ml_string.toChars(text)
    print('Text:', text)
    print('Characters:', chars)
    print('Character count:', ml_string.length(text))
    special_text = 'Hi! 123'
    special_chars = ml_string.toChars(special_text)
    print('\\nSpecial text:', special_text)
    print('Special characters:', special_chars)
    vowel_count = 0
    vowels = ml_string.toChars('aeiouAEIOU')
    for char in chars:
        for vowel in vowels:
            if (char == vowel):
                vowel_count = (vowel_count + 1)
    print("\\nVowel analysis for '", text, "':")
    print('Vowels found:', vowel_count)
    char_array = ml_string.toChars(text)
    print('\\nCharacter array processing:')
    print('Original chars:', char_array)
    print('First character:', char_array[0])
    print('Last character:', char_array[(ml_string.length(text) - 1)])
    empty_chars = ml_string.toChars('')
    print('\\nEmpty string test:')
    print('Empty chars:', empty_chars)
    print('Empty length:', ml_string.length(''))
    return {'original': text, 'characters': chars, 'vowel_count': vowel_count, 'char_array': char_array, 'special_test': special_chars}

result = test_string_to_chars()

print('\\n=== Test Results Summary ===')

print('Test completed successfully!')

print('Result object:', result)

# End of generated code