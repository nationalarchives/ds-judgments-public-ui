import math
import re
from datetime import datetime

from caselawclient.Client import RESULTS_PER_PAGE, api_client
from requests_toolbelt.multipart import decoder

from .fixtures.stop_words import stop_words
from .models import SearchResults

MAX_RESULTS_PER_PAGE = 50


def format_date(date):
    if date == "" or date is None:
        return None

    time = datetime.strptime(date, "%Y-%m-%d")
    return time.strftime("%d-%m-%Y")


def perform_advanced_search(
    query=None,
    court=None,
    judge=None,
    party=None,
    order=None,
    neutral_citation=None,
    specific_keyword=None,
    date_from=None,
    date_to=None,
    page=1,
    per_page=RESULTS_PER_PAGE,
):
    response = api_client.advanced_search(
        q=query,
        court=",".join(court) if isinstance(court, list) else court,
        judge=judge,
        party=party,
        neutral_citation=neutral_citation,
        specific_keyword=specific_keyword,
        page=page,
        order=order,
        date_from=date_from,
        date_to=date_to,
        page_size=per_page,
    )
    multipart_data = decoder.MultipartDecoder.from_response(response)
    return SearchResults.create_from_string(multipart_data.parts[0].text)


def remove_unquoted_stop_words(query):
    """
    Remove stop words [the, and, of] from a search query, but only if they
    are part of an unquoted string AND are not the only word.
    If they are part of a quoted string, e.g.
    'body of evidence', or are the only word, they are left alone.
    """
    if query is None:
        return
    if (
        re.match(r"^\"|^\'", query) is None
        and re.match(r"\"$|\'$", query) is None
        and re.match(solo_stop_word_regex(stop_words), query) is None
    ):
        without_stop_words = re.sub(
            without_stop_words_regex(stop_words), "", query, re.IGNORECASE
        )
        return re.sub(r"\s+", " ", without_stop_words)
    return query


def without_stop_words_regex(stops):
    modified_stops = [f"(\\b{stop}\\b)" for stop in stops]
    regex = r"|".join(modified_stops)
    return regex


def solo_stop_word_regex(stops):
    modified_stops = [f"(^{stop}$)" for stop in stops]
    regex = r"|".join(modified_stops)
    return regex


def as_integer(number_string, minimum, maximum=None, default=None):
    """
    Return an integer for user input, making sure it's between the min and max,
    and if it's not a valid number, that it's the default (or minimum if not set).
    """

    if default is None:
        default = minimum
    if number_string is None:
        return default
    try:
        number = int(number_string)
    except ValueError:
        return default

    min_bounded = max(minimum, number)
    if maximum is not None:
        return min(min_bounded, maximum)
    else:
        return min_bounded


def paginator(current_page, total, size_per_page=RESULTS_PER_PAGE):
    current_page = as_integer(current_page, minimum=1)
    size_per_page = as_integer(
        size_per_page, minimum=1, maximum=MAX_RESULTS_PER_PAGE, default=RESULTS_PER_PAGE
    )
    number_of_pages = math.ceil(int(total) / size_per_page)
    next_pages = list(
        range(current_page + 1, min(current_page + 10, number_of_pages) + 1)
    )

    return {
        "current_page": current_page,
        "has_next_page": current_page < number_of_pages,
        "next_page": current_page + 1,
        "has_prev_page": current_page > 1,
        "prev_page": current_page - 1,
        "next_pages": next_pages,
        "number_of_pages": number_of_pages,
    }
