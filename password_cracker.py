import string
import re
from itertools import product


class PasswordCracker:
    PASSWORD_INGREDIENTS = {char.lower() for char in string.ascii_letters + string.digits}

    # def __init__(self):
    @classmethod
    def create_products(cls, char_set: set | None, repetitions: int = 3):
        """
        Generate all possible combinations of characters from the given set, repeated a specified number of times.

        This method uses itertools.product to create Cartesian products of the character set,
        then joins each combination into a string. If no character set is provided, it defaults
        to cls.PASSWORD_INGREDIENTS.

        :param char_set: (set | None) A set of characters to use for generating combinations.
          If None, uses cls.PASSWORD_INGREDIENTS.
        :param repetitions: (int, optional) The number of times to repeat the character set in each combination.
          Defaults to 3.

        :return:
            Generator[str]: A generator yielding strings, each representing a unique combination
            of characters from the set, repeated 'repetitions' times.

        Example:
            list(cls.create_products({'a', 'b'}, 2))
            ['aa', 'ab', 'ba', 'bb']
        """
        if char_set is None:
            char_set = cls.PASSWORD_INGREDIENTS
        return (''.join(x) for x in product(char_set, repeat=repetitions))

    @classmethod
    def generate_case_combination(cls, password: str) -> list[str]:
        """
        Generate all possible case combinations for the given password string.

        For each alphabetic character in the password, this method creates combinations
        where the character can be either uppercase or lowercase. Non-alphabetic characters
        remain unchanged. If the password contains no alphabetic characters, it returns
        the password as a single-element list.

        :param password: (str) The input string for which to generate case combinations.

        :returns:
            list[str]: A list of strings, each representing a unique case combination of the input password.
            If no alphabetic characters are present, returns [password].

        :raises TypeError: If password is not a string.

        Example:
        PasswordCracker.generate_case_combination("Ab")
        ['Ab', 'AB', 'aB', 'ab']
        PasswordCracker.generate_case_combination("123")
        ['123']
        """
        if type(password) is not str:
            try:
                password = str(password)
            except TypeError:
                raise TypeError('Password must be a string')
        if re.search(r'[a-zA-Z]+', password):
            return list(map(''.join, product(*zip(password.upper(), password.lower()))))
        else:
            return [password]

    @classmethod
    def get_combinations_from_file(cls, filename: str) -> set[str]:
        """
        Read passwords from a file and generate all unique case combinations for each,
        ensuring global uniqueness across all passwords.

        The method opens the specified file, reads it line by line, strips whitespace
        from each line (treating each as a password), and generates case combinations
        using the `cls.generate_case_combination` method. For each password, it collects
        unique combinations in a set to avoid duplicates within that password, then
        adds them to a result set for global deduplication. The final result is a set
        of all unique combinations from the entire file.

        :param filename: (str) The path to the file containing passwords, one per line.

        :return: set[str]: A set of all unique case combinations generated from all passwords in the file.

        :raises TypeError: If the filename is not a string
        :raises FileNotFoundError: If the specified file does not exist.

        Example:
            Assuming a file 'passwords.txt' with contents:
            Ab
            ab
            123
            PasswordGenerator.get_combinations_from_file('passwords.txt')
            {'Ab', 'AB', 'aB', 'ab', '123'}  # Note: 'ab' appears only once due to global uniqueness
        """
        if type(filename) is not str:
            raise TypeError('Password must be a string')

        result = []
        try:
            with open(filename) as file:
                for line in file:
                    current_password = line.strip()
                    unique_combinations = set(cls.generate_case_combination(current_password))
                    result.extend(unique_combinations)
        except FileNotFoundError:
            raise FileNotFoundError(f'File "{filename}" not found')

        return set(result)
