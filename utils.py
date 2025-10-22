def use_filters(data, filters):
    results = data

    if filters.get("is_palindrome") is not None:
        results = [x for x in results if x.is_palindrome == filters["is_palindrome"]]

    if filters.get("min_length") is not None:
        results = [x for x in results if x.length >= filters["min_length"]]

    if filters.get("max_length") is not None:
        results = [x for x in results if x.length <= filters["max_length"]]

    if filters.get("word_count") is not None:
        results = [x for x in results if x.word_count == filters["word_count"]]

    if filters.get("contains_char") is not None:
        char = filters["contains_char"].lower()
        results = [x for x in results if char in x.value.lower()]

    if filters.get("starts_with"):
        results = [x for x in results if x.value.lower().startswith(filters["starts_with"])]

    if filters.get("ends_with"):
        results = [x for x in results if x.value.lower().endswith(filters["ends_with"])]

    return results


""" def use_filters(data, filters):
    results = data

    if filters.get("is_palindrome") is not None:
        results = [x for x in results if x["properties"]["is_palindrome"] == filters["is_palindrome"]]

    if filters.get("min_length") is not None:
        results = [x for x in results if x["properties"]["length"] >= filters["min_length"]]

    if filters.get("max_length") is not None:
        results = [x for x in results if x["properties"]["length"] <= filters["max_length"]]

    if filters.get("word_count") is not None:
        results = [x for x in results if x["properties"]["word_count"] == filters["word_count"]]

    if filters.get("contains_char") is not None:
        char = filters["contains_char"].lower()
        results = [x for x in results if char in x["value"].lower()]

    return results
 """