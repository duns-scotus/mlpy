"""Generated Python code from mlpy ML transpiler."""

# This code was automatically generated from ML source
# Modifications to this file may be lost on regeneration

# ============================================================================
# Runtime Whitelist Enforcement
# ============================================================================
from mlpy.runtime.whitelist_validator import safe_call as _safe_call

from mlpy.stdlib.builtin import builtin

def test_chr_ascii():
    results = {}
    results['chr_65'] = _safe_call(builtin.chr, 65)
    results['chr_90'] = _safe_call(builtin.chr, 90)
    results['chr_97'] = _safe_call(builtin.chr, 97)
    results['chr_122'] = _safe_call(builtin.chr, 122)
    results['chr_48'] = _safe_call(builtin.chr, 48)
    results['chr_57'] = _safe_call(builtin.chr, 57)
    results['chr_32'] = _safe_call(builtin.chr, 32)
    results['chr_33'] = _safe_call(builtin.chr, 33)
    results['chr_63'] = _safe_call(builtin.chr, 63)
    return results

def test_ord_ascii():
    results = {}
    results['ord_A'] = _safe_call(builtin.ord, 'A')
    results['ord_Z'] = _safe_call(builtin.ord, 'Z')
    results['ord_a'] = _safe_call(builtin.ord, 'a')
    results['ord_z'] = _safe_call(builtin.ord, 'z')
    results['ord_0'] = _safe_call(builtin.ord, '0')
    results['ord_9'] = _safe_call(builtin.ord, '9')
    results['ord_space'] = _safe_call(builtin.ord, ' ')
    results['ord_exclaim'] = _safe_call(builtin.ord, '!')
    results['ord_question'] = _safe_call(builtin.ord, '?')
    return results

def test_chr_ord_roundtrip():
    results = {}
    results['roundtrip_65'] = _safe_call(builtin.ord, _safe_call(builtin.chr, 65))
    results['roundtrip_97'] = _safe_call(builtin.ord, _safe_call(builtin.chr, 97))
    results['roundtrip_48'] = _safe_call(builtin.ord, _safe_call(builtin.chr, 48))
    results['roundtrip_A'] = _safe_call(builtin.chr, _safe_call(builtin.ord, 'A'))
    results['roundtrip_z'] = _safe_call(builtin.chr, _safe_call(builtin.ord, 'z'))
    results['roundtrip_5'] = _safe_call(builtin.chr, _safe_call(builtin.ord, '5'))
    return results

def test_alphabet_generation():
    results = {}
    uppercase = []
    for i in _safe_call(builtin.range, 65, 91):
        uppercase = (uppercase + [_safe_call(builtin.chr, i)])
    results['uppercase_count'] = _safe_call(builtin.len, uppercase)
    results['first_letter'] = uppercase[0]
    results['last_letter'] = uppercase[25]
    lowercase = []
    for i in _safe_call(builtin.range, 97, 123):
        lowercase = (lowercase + [_safe_call(builtin.chr, i)])
    results['lowercase_count'] = _safe_call(builtin.len, lowercase)
    results['first_lower'] = lowercase[0]
    results['last_lower'] = lowercase[25]
    return results

def test_digit_generation():
    results = {}
    digits = []
    for i in _safe_call(builtin.range, 48, 58):
        digits = (digits + [_safe_call(builtin.chr, i)])
    results['digit_count'] = _safe_call(builtin.len, digits)
    results['first_digit'] = digits[0]
    results['last_digit'] = digits[9]
    return results

def test_character_range_check():
    results = {}
    char_code = _safe_call(builtin.ord, 'B')
    is_uppercase = ((char_code >= 65) and (char_code <= 90))
    results['B_is_uppercase'] = is_uppercase
    char_code2 = _safe_call(builtin.ord, 'm')
    is_lowercase = ((char_code2 >= 97) and (char_code2 <= 122))
    results['m_is_lowercase'] = is_lowercase
    char_code3 = _safe_call(builtin.ord, '7')
    is_digit = ((char_code3 >= 48) and (char_code3 <= 57))
    results['seven_is_digit'] = is_digit
    return results

def test_case_conversion():
    results = {}
    upper_code = _safe_call(builtin.ord, 'A')
    lower_code = (upper_code + 32)
    results['A_to_a'] = _safe_call(builtin.chr, lower_code)
    lower_code2 = _safe_call(builtin.ord, 'z')
    upper_code2 = (lower_code2 - 32)
    results['z_to_Z'] = _safe_call(builtin.chr, upper_code2)
    return results

def test_character_arithmetic():
    results = {}
    code_A = _safe_call(builtin.ord, 'A')
    code_B = (code_A + 1)
    results['next_after_A'] = _safe_call(builtin.chr, code_B)
    code_Z = _safe_call(builtin.ord, 'Z')
    code_Y = (code_Z - 1)
    results['prev_before_Z'] = _safe_call(builtin.chr, code_Y)
    code_a = _safe_call(builtin.ord, 'a')
    code_c = (code_a + 2)
    results['skip_from_a'] = _safe_call(builtin.chr, code_c)
    return results

def test_caesar_cipher():
    results = {}
    message = 'ABC'
    encrypted = []
    for i in _safe_call(builtin.range, _safe_call(builtin.len, message)):
        code = (_safe_call(builtin.ord, 'A') + i)
        shifted = (code + 3)
        encrypted = (encrypted + [_safe_call(builtin.chr, shifted)])
    results['encrypted_len'] = _safe_call(builtin.len, encrypted)
    return results

def test_character_classification():
    results = {}
    uppercase_count = 0
    lowercase_count = 0
    digit_count = 0
    other_count = 0
    for i in _safe_call(builtin.range, 48, 123):
        if ((i >= 65) and (i <= 90)):
            uppercase_count = (uppercase_count + 1)
        elif ((i >= 97) and (i <= 122)):
            lowercase_count = (lowercase_count + 1)
        elif ((i >= 48) and (i <= 57)):
            digit_count = (digit_count + 1)
        else:
            other_count = (other_count + 1)
    results['uppercase'] = uppercase_count
    results['lowercase'] = lowercase_count
    results['digits'] = digit_count
    results['other'] = other_count
    return results

def main():
    all_results = {}
    all_results['chr_ascii'] = test_chr_ascii()
    all_results['ord_ascii'] = test_ord_ascii()
    all_results['roundtrip'] = test_chr_ord_roundtrip()
    all_results['alphabet'] = test_alphabet_generation()
    all_results['digits'] = test_digit_generation()
    all_results['range_check'] = test_character_range_check()
    all_results['case_conv'] = test_case_conversion()
    all_results['arithmetic'] = test_character_arithmetic()
    all_results['caesar'] = test_caesar_cipher()
    all_results['classification'] = test_character_classification()
    return all_results

test_results = main()

# End of generated code