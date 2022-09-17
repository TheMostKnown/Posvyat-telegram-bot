from autocorrect import Speller
spell = Speller('ru')

def handler_message(user_input, db_list):
    db_list_lower = [db_list[i].lower() for i in range(len(db_list))]  # lead to similar register
    user_input_lower = user_input.lower()
    user_input_corrected = spell(spell(spell(spell(user_input_lower))))

    if user_input_corrected in db_list_lower:
        return db_list[db_list_lower.index(user_input_corrected)]
    else:
        lengths = []  # the difference in the number of letters
        unmatches = []  # number of unmatches between letters in each position of word

        for word in db_list_lower:
            lengths.append(abs(len(word)-len(user_input_lower))+1)
            word_list = list(word)
            user_input_lower_list = list(user_input_lower)
            min_len = min(len(user_input_lower_list), len(word_list))
            count = 0
            for i in range(min_len):
                if word_list[i] == user_input_lower_list[i]:
                    count += 1
            unmatches.append(max(len(user_input_lower_list), len(word_list))-count+1)

        multiplied = [lengths[i]*unmatches[i] for i in range(len(lengths))]  # find multiplication of two parameters

        pre_result = []  # list with all parameters of minimum values
        min_multiplied = min(multiplied)
        for i in range(len(multiplied)):
            if min_multiplied == multiplied[i]:
                pre_result.append([lengths[i], unmatches[i], i])

        result = []  # list with id and unmatches between minimum in length values
        min_lengths = min(pre_result)
        for i in range(len(pre_result)):
            if min_lengths[0] == pre_result[i][0]:
                result.append([pre_result[i][1], pre_result[i][2]])

        return db_list[min(result)[1]]




print(handler_message("sobaka sutvylau", ["sobaka sutulaya", "konor", "vodka", "posvyat", "sobaka", "woRt"]))  # сотрите
