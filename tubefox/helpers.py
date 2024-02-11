class TimeConvertor:
    """
    TimeConvertor class for converting time values to formatted strings.

    Args:
        start_value (float): The start time value in seconds.
        duration (float): The duration value in seconds.

    Attributes:
        start_value (float): The start time value in seconds.
        duration (float): The duration value in seconds.

    Methods:
        convert_start_time: Convert the start time value to a formatted string (HH:MM:SS,mmm).
        convert_end_time: Convert the end time value (start time + duration) to a formatted string (HH:MM:SS,mmm).
    """

    def __init__(self, start_value: float, duration: float) -> None:
        self.start_value: float = start_value
        self.duration: float = duration

    @property
    def convert_start_time(self) -> str:
        """
        Convert the start time value to a formatted string (HH:MM:SS,mmm).

        Returns:
            str: The formatted start time string.
        """
        hours = int(self.start_value / 3600)
        minutes = int((self.start_value % 3600) / 60)
        seconds = int((self.start_value % 3600) % 60)
        milliseconds = int((self.start_value % 1.0) * 1000)
        start_time = "{:02d}:{:02d}:{:02d},{:03d}".format(hours, minutes, seconds, milliseconds)
        return start_time

    @property
    def convert_end_time(self) -> str:
        """
        Convert the end time value (start time + duration) to a formatted string (HH:MM:SS,mmm).

        Returns:
            str: The formatted end time string.
        """
        end_value = self.start_value + self.duration
        hours = int(end_value / 3600)
        minutes = int((end_value % 3600) / 60)
        seconds = int((end_value % 3600) % 60)
        milliseconds = int((end_value % 1.0) * 1000)
        end_time = "{:02d}:{:02d}:{:02d},{:03d}".format(hours, minutes, seconds, milliseconds)
        return end_time


def clean_filename(filename: str) -> str:
    """
    Clean a given filename by removing invalid characters.

    This function takes a filename as input and removes any invalid characters that are not allowed in filenames
    on certain file systems (e.g., Windows). The list of invalid characters includes backslash, forward slash, colon,
    asterisk, question mark, double quote, less than, greater than, and pipe.

    Args:
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
