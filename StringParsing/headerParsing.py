# first we split them at , and then we strip them and then we assess quality

def contruct_quality_obj(lang, quality=0):
    # lets split lang into language and locale
    split = lang.split("-")
    if len(split) == 2:
        language, locale = split
    else:
        language = split[0]
        locale = "US"
    return {"lang": language, "locale": locale,  "quality": quality}

def calculate_quality(arr):
    header_quality_arr = []
    for header in arr:
        splits = header.split(";")
        cleaned_splits = [s.strip() for s in splits]
        if len(cleaned_splits) == 2:
            name, quality_raw = cleaned_splits
            prefix, quality = quality_raw.split("=")
            if prefix == "q":
                try:
                    quality_val = float(quality)
                    header_quality_arr.append(contruct_quality_obj(name, quality_val))
                    continue
                except ValueError as e:
                    print(header, "does not contain valid quality so defaulting to 1")
        elif len(cleaned_splits) == 1 and not cleaned_splits[0]:
            continue

        name = cleaned_splits[0]
        header_quality_arr.append(contruct_quality_obj(name, 1.0))
    return header_quality_arr

def split_headers(headers):
    return headers.split(",")

def header_parsing(headers):
    # do check support for the * pattern
    header_arr = split_headers(headers)
    
    # calculate quality
    return calculate_quality(header_arr)

def sort_by_quality(arr):
    return sorted(arr, key=lambda x: x["quality"], reverse=True)

def compare_language(current, supported):
    lang = current.get("lang")

    for s in supported:
        if s.get("lang", "") == lang:
            return True
    return False

def filter_out_unsupported(langs_arr, supported_langs):
    return filter(lambda x: compare_language(x, supported_langs),langs_arr)

def normalise_supported(supported):
    return list(map(contruct_quality_obj,supported))

def check_support(headers, supported):
    lang_qualities = header_parsing(headers)
    sorted_langs = sort_by_quality(lang_qualities)

    # now we need to filter
    filtered_langs = filter_out_unsupported(sorted_langs, normalise_supported(supported))
    return next(filtered_langs)

headers="en-US;q=0.8, en;q=0.9, fr;q=yo,,"
supported=["fr", "en"]

print(header_parsing(headers))
print(check_support(headers, supported))