"""
A toolkit to work with list of dicts. All of the dicts needs to have the same keys.
Example of a list of dicts : [{"Prénom":"David", "Nom":"TOCAVEN"}, {"Prénom":"Rania", "Nom":"BOTEY"}]
"""
import copy


def default_fct_condition(val):
    """
    Default function used in remove_dict_if function. It's always return True, whatever val parameter value.
    :param val: needed by default_fct_condition usage into remove_dict_if.
    :return: Always True.
    """
    return True


def remove_keys_in_dicts(list_of_dicts: list[dict], keys: list[str], fct_condition=default_fct_condition):
    """
    remove all keys, values couples in all dicts of list_of_dicts according to the given list of keys and values
    according to fct_condition function.
    :param fct_condition: A function that can be defined. It allows you to add conditions for deletion of keys.
    It must have a parameter.
    :param list_of_dicts: The data in which the keys ore to be deleted.
    :param keys: list of keys that will be deleted.
    :return:
    """
    for a_dict in list_of_dicts:
        for a_key in keys:
            if default_fct_condition(""):  # TODO : change default_fct_condition to fct_condition
                a_dict.pop(a_key)


def remove_dict_if(list_of_dicts: list[dict], key_of_interest: str, fct_condition_to_remove_data):
    """
    Remove a dict of a list of dict under condition defined by fct_condition_to_remove_data
    :param list_of_dicts: The data in which the dicts has to be deleted.
    :param key_of_interest: the key in the dictionaries on which the condition will be based.
    :param fct_condition_to_remove_data: a Boolean function that must be defined. It has one parameter that is the value
    linked to the key_of_interest. If this function returns True, the dict is deleted.
    :return:
    """
    i_dict = 0
    removed_dict = []  # TODO : remove this unused list
    while i_dict < len(list_of_dicts):
        if fct_condition_to_remove_data(list_of_dicts[i_dict].get(key_of_interest)):
            removed_dict.append(list_of_dicts.pop(i_dict))
        else:
            i_dict += 1


def is_not_empty(val: str):
    """
    Boolean condition used with the remove_dict_if function. It returns True if the value val is empty, False otherwise.
    :param val: A string value.
    :return:
    """
    return val != ""


def is_not_validee(val):
    """
    Boolean condition used with the remove_dict_if function. It returns True if value val equals "Validée", False
    otherwise.
    :param val: A string value.
    :return:
    """
    return val == "Validée"


def print_list_of_dicts(list_of_dicts: list[dict]):
    """
    Console print of a list of dicts. It displays the dict index in the list then each key-value pairs
    indented with a tab.
    :param list_of_dicts:The data to print.
    :return:
    """
    i = 0
    for eleve_dict in list_of_dicts:
        print(f"{i}:")
        for k, v in eleve_dict.items():
            print(f"\t{k}: {v}")
        i += 1


def values_as_list(list_of_dicts: list[dict], key: str):
    """
    Extract as a list all associated with the key of in the dictionaries of list_of_dicts.
    :param list_of_dicts: The data in which the values will be found.
    :param key:
    :return:
    """
    # values = []
    # for a_dict in list_of_dicts:
    #     values.append(a_dict.get(key))
    # return values
    return [a_dict.get(key) for a_dict in list_of_dicts]  # TODO : to test


def remove_duplicates(list_of_dicts: list[dict],
                      keys: list[str] = [],
                      key_to_keep_if_duplicates: str = "Statut",
                      value_to_keep_if_duplicates: str = "Validée"):
    """
    Remove some dicts in list_of_dicts to have no duplicates. The dicts can be compared  only on keys pairs.
    :param value_to_keep_if_duplicates:
    :param list_of_dicts:
    :param keys: keys to consider. If no value given, all keys are compared.
    :return:
    """
    ## Create a copy of list_of_dicts to seach duplicates considering keys parameter
    cp_list_of_dicts = copy.deepcopy(list_of_dicts)

    # if there is specified keys
    if keys:
        # find keys to removed
        l_keys = [x for x in list_of_dicts[0].keys() if x not in keys]
        remove_keys_in_dicts(cp_list_of_dicts, l_keys)

    # a list that contains lists. Each lists contain indices of sames duplicates.
    list_of_duplicates = []
    # a list that contains indices to link into.
    # When a duplicate dicts ars found, the second index is removed to this list. This avoid
    searching_indices = list(range(len(cp_list_of_dicts)))

    # find duplicates
    i = 0
    j = 1
    while i < len(searching_indices):
        j = i + 1
        while j < len(searching_indices):
            if cp_list_of_dicts[searching_indices[i]] == cp_list_of_dicts[searching_indices[j]]:
                if searching_indices[j] == searching_indices[i] + 1:  # if first duplicate of i found
                    # add a new list into list_of_duplicates that contains i index
                    list_of_duplicates.append([searching_indices[i]])

                list_of_duplicates[-1].append(searching_indices[j])  # add j inside the last list of list_of_duplicates.
                searching_indices.pop(j)  # remove j index of searching_indices list.
            else:
                j += 1
        i += 1
    # print(list_of_duplicates)


    # chose a dict to keep and remove other duplicates.

    # reverse list_of_duplicates and sub lists
    list_of_duplicates.reverse()
    for li in list_of_duplicates:
        li.reverse()
    #
    for a_duplicate_list_of_indices in list_of_duplicates:
        # create a list of
        status_of_duplicates = values_as_list([list_of_dicts[i] for i in a_duplicate_list_of_indices],
                                              key_to_keep_if_duplicates)
        index_to_keep = 0  # the index in a_duplicate_list_of_indices that contains the index to keep into list_of_dicts
        if value_to_keep_if_duplicates in status_of_duplicates:
            # find the firs index of "Validée" statut
            index_to_keep = status_of_duplicates.index(value_to_keep_if_duplicates)
        # if there is no a value_to_keep_if_duplicates, it keeps the first index

        # remove all index_to_keep into a_duplicate_list_of_indices
        a_duplicate_list_of_indices.pop(index_to_keep)
        if index_to_keep != 0:
            for a in a_duplicate_list_of_indices:
                a -= 1
        # remove all dict of list_of_dicts that indices are in a_duplicate_list_of_indices
        print("list of indices to remove :", a_duplicate_list_of_indices)
        # a_duplicate_list_of_indices.reverse()  # to avoid that the removing of a dict modify the index of other ones
        for i in a_duplicate_list_of_indices:
            list_of_dicts.pop(i)
            # if i isnt the bi

    # print("len of list_of_dicts", len(list_of_dicts))
    # print_list_of_dicts(list_of_dicts)
    # exit()

    # duplicates_i = []
    # i = 0  # original list index
    # j = 1  # copied list index
    # while i < len(cp_list_of_dicts):  # until the end of cp_list_of_dicts
    #     j = i + 1
    #     while j < len(cp_list_of_dicts):  # until the end of cp_list_of_dicts
    #         if cp_list_of_dicts[i] == cp_list_of_dicts[j]:  # if dicts at i and j indices are equals
    #             if not (list_of_dicts[i].get("Status") == "Validée"):  # if the i dict status is not equal to "Validée"
    #                 list_of_dicts.pop(i)
    #                 # j += 1
    #             else:
    #                 list_of_dicts.pop(j)
    #         # else:
    #         j += 1
    #
    #     i += 1

    """
    Other way : 
    1. create a list that contains the lists of sames dict indices in list_of_dicts.
    2. in each list of sames dicts
        if one dict has Status equal "Validée", remove the other ones
        else, keep the first, delete the other ones.
    
    """


def reverse_keys_list_dict(list_of_dicts: list[dict]):
    """
    Reverse the order of keys into all dicts.
    :param list_of_dicts:
    :return:
    """
    for i in range(len(list_of_dicts)):
        list_of_dicts[i] = {k: list_of_dicts[i][k] for k in reversed(list_of_dicts[i].keys())}


def union_minus_intersection(dicts_list_1: list[dict], dicts_list_2: list[dict]):
    """
    Find dicts that are not both in dicts_list_1 and dicts_list_2 and return them as a list of dicts.
    math view : (dicts_list_2 / dicts_list_1) U (dicts_list_1 / dicts_list_2)
    :param dicts_list_1: a first list of dicts.
    :param dicts_list_2: a second list of dicts.
    :return:
    """
    # intersection between dicts_list_1 and dicts_list_2
    intersect = []
    for x in dicts_list_1:
        if x in dicts_list_2:
            intersect.append(x)
    # print(intersect)
    # dicts_list_1 / dicts_list_2
    not_common = [x for x in dicts_list_1 if x not in intersect]
    # dicts_list_2 / dicts_list_1
    not_common2 = [x for x in dicts_list_2 if x not in intersect]
    # (dicts_list_2 / dicts_list_1) U (dicts_list_1 / dicts_list_2)
    return not_common + not_common2


def add_key_all_dicts(list_of_dicts: list[dict], key: str, value: str):
    """
    Add a key-value pair in all dicts of list_of_dicts
    :param list_of_dicts: A list of dictionaries.
    :param key: The key to insert.
    :param value: The value to insert.
    :return: None
    """
    for a_dict in list_of_dicts:
        a_dict[key] = value


def reduce_data(list_of_dicts: list[dict], keys_to_keep: list[str]):
    """

    :param list_of_dicts:
    :param keys_to_keep:
    :return:
    """
    # extract list of unwanted keys
    if list_of_dicts:
        unwanted_keys = list(list_of_dicts[0].keys())
        for k in keys_to_keep:
            unwanted_keys.remove(k)

        # remove unwanted keys and values
        remove_keys_in_dicts(list_of_dicts, unwanted_keys)


if __name__ == "__main__":
    ldicts = [{"Nom": "TOC", "Prénom": "Da"},
              {"Nom": "TAC", "Prénom": "Pa"},
              {"Nom": "BLOC", "Prénom": "Car"}]
    k_keys = ["Nom"]
    print_list_of_dicts(ldicts)
    reduce_data(ldicts, k_keys)
    print_list_of_dicts(ldicts)
