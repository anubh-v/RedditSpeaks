from functools import reduce

import nltk


def naive_name_detector(text):
    """
    Given a piece of text, return a list of names identified in the text.
    """
    # Create a tokenizer that creates tokens of only alphanumeric characters
    # i.e. sets of characters with punctuation do not appear as a token
    tokenizer = nltk.RegexpTokenizer(r'\w+')

    # use tokenizer to break the text into tokens
    tokens = tokenizer.tokenize(text)

    # use 'part-of-speech' tagging to determine meaning of each token
    tagged_tokens = nltk.pos_tag(tokens)

    """
    Now, we identify the names in the text.

    We assume that:
     (1) all tokens tagged as singular proper nouns are part of names
     (2) names are comprised of at most 2 singular proper nouns

    Hence, we identify names by identifying the singular proper nouns.
    If there are 2 consecutive singular proper nouns, they are considered to be
    1 name.
    """

    # 'NNP' is nltk's code for singular proper noun
    PROPER_NOUN_SINGULAR = 'NNP'

    # Create a list to store the final list of names associated with this text.
    completed_names = []

    # Create a list to store the name currently being tracked, as we iterate
    # through the tokens.
    current_name = []

    for tagged_token in tagged_tokens:

        # For each tagged token, retrieve the tag and the token string
        tag = tagged_token[1]
        token = tagged_token[0].lower()

        if tag == PROPER_NOUN_SINGULAR:
            # If the current token is a proper noun (singular), it is either
            # part of the current name being tracked, or the start of a
            # new name.
            if len(current_name) == 0:
                # If we are not currently tracking a name, consider the current
                # token to be the start of a new name.
                current_name.append(token)

            elif len(current_name) != 0:
                # If we are currently tracking a name, consider the current
                # token part of it.

                # Append token to the current name.
                current_name[0] = current_name[0] + " " + token

                # Assume each name will have at most 2 NNP tokens.
                completed_names.append(current_name[0])
                current_name = []

        elif current_name:
            # If the current token is NOT a proper noun (singular), it
            # signifies the end of the current name.
            completed_names.append(current_name[0])
            current_name = []

    return completed_names


def action_phrase_detector(text, name):
    tokenizer = nltk.RegexpTokenizer(r'\w+')

    # use tokenizer to break the text into tokens
    text = text.lower()
    tokens = tokenizer.tokenize(text)

    # use 'part-of-speech' tagging to determine meaning of each token
    tagged_tokens = nltk.pos_tag(tokens)

    for index, tagged_token in enumerate(tagged_tokens):
        if tagged_token[0] in name:
            tagged_tokens[index] = (tagged_token[0], "NAME")

    grammar = "phrase: {<NAME>+<V.*><.*>{0,4}<NN.*>}"

    cp = nltk.RegexpParser(grammar)

    phrases = []

    result = cp.parse(tagged_tokens)
    for subtree in result.subtrees():
        if subtree.label() == "phrase":
            phrase = reduce(lambda string_so_far, token2:
                            " ".join([string_so_far, token2[0]]),
                            subtree.flatten(),
                            "")

            phrases.append(phrase)

    if phrases:
        print(name)
        print(text)
        print(phrases)
    return phrases
