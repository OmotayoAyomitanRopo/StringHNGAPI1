def use_filters(data, filters):
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
