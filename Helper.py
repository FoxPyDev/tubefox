def clean_filename(filename):
    """
        Cleans a given filename by removing invalid characters.

        This function takes a filename as input and removes any invalid characters that are not allowed in filenames
        on certain file systems (e.g., Windows). The list of invalid characters includes backslash, forward slash, colon,
        asterisk, question mark, double quote, less than, greater than, and pipe.

        Parameters:
            filename (str): The input filename to be cleaned.

        Returns:
            str: The cleaned filename with invalid characters removed.

        Example:
            To clean a filename:
            >>> original_filename = "file*name?with/invalid:characters"
            >>> cleaned_filename = clean_filename(original_filename)
            >>> print(cleaned_filename)
            "filenamewithinvalidcharacters"
        """
    invalid_chars = ['\\', '/', ':', '*', '?', '"', '<', '>', '|']
    cleaned_filename = ''.join(char for char in filename if char not in invalid_chars)
    return cleaned_filename
