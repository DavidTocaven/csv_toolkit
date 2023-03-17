"""
Générer la liste des différences entre deux listes de noms et prénoms entre 2 fichiers CSV.
Format de sortie : un fichier CSV contenant
NOMS, PRÉNOMS

"""
# imports
import csv
import sys
import copy
import re


def replace_double_string_delimiter_by_simple(csv_filename: str, encoding: str):
    data = ""
    with open(csv_filename, mode="r", encoding=encoding) as file:
        data = file.read().replace('"', "").replace("'", "")
    with open(csv_filename, mode="w", encoding=encoding) as file:
        file.write(data)


def open_csv(csv_filename: str, csv_delimiter: str, encoding: str = 'utf-8-sig', string_delimiter: str = "'"):
    """ Safely opening and reading of the csv file.
    :param string_delimiter: ' or "
    :param encoding: encodage du fichier csv
    :param csv_filename str  the name and path of csv file that contains data to publipost
    :param csv_delimiter str the delimiter character between data elements.
    return csv content as list of dicts
    """

    with open(csv_filename, newline='', encoding=encoding) as csvfile:
        spamreader = csv.DictReader(csvfile, delimiter=csv_delimiter, quotechar=string_delimiter)
        data_list = []
        for line in spamreader:
            # print(line)
            data_list.append(line)

    return data_list


# def clean_dicts(list_of_dicts: list[dict]):
#     for a_dict in list_of_dicts:
#         for k, v in a_dict.items():
#             k_clean = str(k)
#             v_clean = str(v)
#             if not k_clean.isalnum():
#                 k_clean = k_clean.replace('"', "").replace("'", "")
#             if not v_clean.isalnum():
#                 v_clean = v_clean.replace('"', "").replace("'", "")
#             if str(k) != k_clean or str(v) != v_clean:
#                 a_dict.pop(k)
#                 a_dict[k_clean] = v_clean


def reduce_data(list_of_dicts: list[dict], keys_to_keep):
    # extract list of unwanted keys
    unwanted_keys = list(list_of_dicts[0].keys())
    i_key = 0
    while i_key < len(unwanted_keys):
        if unwanted_keys[i_key] in keys_to_keep:
            unwanted_keys.pop(i_key)
            i_key -= 1
        i_key += 1
    # print(unwanted_keys)
    # remove unwanted keys and values
    remove_keys_list_of_dicts(list_of_dicts, unwanted_keys)


def default_fct_condition(val: str):
    return True


def remove_keys_list_of_dicts(list_of_dicts: list[dict], keys: list[str], fct_condition=default_fct_condition):
    """
    remove all keys, values couples in all dicts of list_of_dicts according to the given list of keys.
    :param fct_condition:
    :param list_of_dicts:
    :param keys:
    :return:
    """
    for a_dict in list_of_dicts:
        for a_key in keys:
            if default_fct_condition(""):
                a_dict.pop(a_key)


def remove_dict_if(list_of_dicts: list[dict], key_of_interest: str, fct_condition_to_remove_data):
    """
    remove a dict of a list of dict under condition
    :param list_of_dicts: input data, modified.
    :param key_of_interest: the key inside the dict that is under condition
    :param fct_condition_to_remove_data: a Boolean function, if its return true, the key and value are removed
    :return:
    """
    i_dict = 0
    removed_dict = []
    while i_dict < len(list_of_dicts):
        if fct_condition_to_remove_data(list_of_dicts[i_dict].get(key_of_interest)):
            removed_dict.append(list_of_dicts.pop(i_dict))
        else:
            i_dict += 1
    # print(removed_dict)


# function used into remove_dict_if

def is_not_empty(val):
    """
    the boolean condition used in remove_dict_if
    :param val:
    :return:
    """
    if val != "":
        return True
    return False


def is_not_validee(val):
    return val == "Validée"


def split_name_surname(list_of_dicts: list[dict], column_name):
    for data in list_of_dicts:
        # get name and surname and  remove it from dict
        list_name = data.pop(column_name).split()
        # separate them into two str
        name = []
        surname = []
        for word in list_name:
            word = word.replace('"', "")
            word = word.replace("'", "")
            if word.isupper():
                name.append(word)
            else:
                surname.append(word)
        # add them to the dict
        data["Nom"] = ' '.join(name)
        data["Prénom"] = ' '.join(surname)


def print_list_of_dicts(classe: list[dict]):
    i = 0
    for eleve_dict in classe:
        print(f"{i}:")
        for k, v in eleve_dict.items():
            print(f"\t{k}: {v}")
        i += 1


def values_as_list(list_of_dicts: list[dict], key: str):
    values = []
    for a_dict in list_of_dicts:
        values.append(a_dict.get(key))
    return values


def remove_duplicates(list_of_dicts: list[dict], list_keys: list[str] = []):
    """
    Remove the dicts in list_of_dicts if they have duplicates, only considering list_keys keys.
    :param list_of_dicts:
    :param list_keys: keys to consider. If no value, all keys are used
    :return:
    """
    cp_list_of_dicts = copy.deepcopy(list_of_dicts)
    if list_keys:
        # find keys to removed
        l_keys = [x for x in list_of_dicts[0].keys() if x not in list_keys]
        remove_keys_list_of_dicts(cp_list_of_dicts, l_keys)

    duplicates_i = []
    i = 0
    j = 1
    while i < len(cp_list_of_dicts):
        j = i + 1
        while j < len(cp_list_of_dicts):
            if cp_list_of_dicts[i] == cp_list_of_dicts[j]:
                if not (list_of_dicts[i].get("Status") == "Validée"):
                    list_of_dicts.pop(i)
                    j += 1
                else:
                    list_of_dicts.pop(j)
            else:
                j += 1
        i += 1


def reverse_keys_list_dict(list_of_dicts: list[dict]):
    for i in range(len(list_of_dicts)):
        list_of_dicts[i] = {k: list_of_dicts[i][k] for k in reversed(list_of_dicts[i].keys())}


def not_intersection(dicts_list_1: list[dict], dicts_list_2: list[dict]):
    # TODO finir la fonction
    # reverse_keys_list_dict(dicts_list_1)
    intersect = []
    for x in dicts_list_1:
        if x in dicts_list_2:
            intersect.append(x)
    print(intersect)
    not_common = [x for x in dicts_list_1 if x not in intersect]
    not_common2 = [x for x in dicts_list_2 if x not in intersect]
    return not_common + not_common2


def save_csv(list_of_dict: list[dict], filename: str, delimiter: str = ";"):
    with open(filename, mode="w", encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=delimiter)
        writer.writerow(list_of_dict[0].keys())

        for a_dict in list_of_dict:
            writer.writerow(a_dict.values())


def add_suffix(filename: str, suffix: str):
    l_filename = filename.split(".")
    return ".".join(l_filename[0:-1]) + suffix + "." + l_filename[-1]


def clean_name_surname(list_of_dicts: list[dict], l_keys: list[str] = ["Nom", "Prénom"]):
    for a_dict in list_of_dicts:
        for k in l_keys:
            if not a_dict.get(k).isalpha():
                a_dict[k] = re.sub("[^a-zA-Z]+", " ", a_dict.get(k))
                # a_dict[k] = a_dict.get(k).replace("  ", " ")
                a_dict[k] = a_dict.get(k).strip()

def seconde_session(classe_csv_filename: str,
                    pix_result_csv_filename: str,
                    output_filename_suffix: str = "_seconde_session",
                    classe_repository: str = "classes/",
                    pix_result_repository: str = "resultats_pix/",
                    absent_repository: str = "abs/"):
    ## Variables
    classe_columns_of_interest = ["Élève", "Sortie"]

    pix_columns_of_interest = ["Nom", "Prénom", "Statut"]
    pix_final_columns = ["Nom", "Prénom"]

    diff_list_csv_filename = add_suffix(classe_csv_filename, output_filename_suffix)
    ## Code

    # Classe
    classe = open_csv(classe_repository + classe_csv_filename, ";")
    # print_list_of_dicts(classe)
    reduce_data(classe, classe_columns_of_interest)
    # print_list_of_dicts(classe)

    remove_dict_if(classe, "Sortie", is_not_empty)  # remove students that quited high-school
    remove_keys_list_of_dicts(classe, ["Sortie"])
    split_name_surname(classe, classe_columns_of_interest[0])
    clean_name_surname(classe)
    # print_list_of_dicts(classe)

    # Pix
    pix_result = open_csv(pix_result_repository + pix_result_csv_filename, ";", string_delimiter='"')
    # print_list_of_dicts(pix_result)
    reduce_data(pix_result, pix_columns_of_interest)
    clean_name_surname(pix_result)
    reverse_keys_list_dict(pix_result)
    remove_duplicates(pix_result, pix_final_columns)
    # print_list_of_dicts(pix_result)
    # for a_dict in pix_result:
    #     print(a_dict)
    # print("classe : ", classe)
    # print(pix_result)
    pix_not_validee = copy.deepcopy(pix_result)
    remove_dict_if(pix_not_validee, 'Statut', is_not_validee)
    reduce_data(pix_not_validee, pix_final_columns)
    reduce_data(pix_result, pix_final_columns)
    # print(pix_not_validee)
    # print("résultat pix : ", pix_result)
    list_not_common = not_intersection(pix_result, classe)
    # print("list_not_common : ", list_not_common)
    pix_do_it_again = list_not_common + pix_not_validee
    # print("pix_do_it_again : ")
    # print_list_of_dicts(pix_do_it_again)
    ## Affichage
    print(f"------------------------------------------\n"
          f"Fichier Pronote : {classe_csv_filename}\n"
          f"Fichier Pix : {pix_result_csv_filename}\n"
          f"Effectif Pronote : {len(classe)}\n"
          f"Effectif sur Pix : {len(pix_result)}\n"
          f"Nombre non validé : {len(pix_not_validee)}\n"
          f"Nombre a passer la seconde session : {len(pix_do_it_again)}\n"
          f"Fichier enregistré : {diff_list_csv_filename}\n"
          f""f"------------------------------------------\n")

    save_csv(pix_do_it_again, absent_repository + diff_list_csv_filename)
    return absent_repository + diff_list_csv_filename


def add_key_all_dicts(list_of_dicts: list[dict], key: str, value: str):
    for a_dict in list_of_dicts:
        a_dict[key] = value


def fusion_csvs(list_of_csv_filenames: list[str],
                remove_suffix_classnames: str):
    list_list_dict = []
    for csv_filename in list_of_csv_filenames:
        class_name = '.'.join(csv_filename.split('/')[-1].split(".")[0:-1])
        class_name = class_name.replace(remove_suffix_classnames, "")
        the_class = open_csv(csv_filename, ";", encoding="latin-1")
        add_key_all_dicts(the_class, "Classe", class_name)
        list_list_dict.extend(the_class)

    return list_list_dict


if __name__ == '__main__':
    # Variables
    COMPUTE_ALL = True
    COMPUTE_DEBUG = False
    abs_list_filenames = []
    a_output_filename_suffix = "_seconde_session"
    # if len(sys.argv) > 1:
    #     # Version avec paramètre directement sur l'appel du script dans un terminal
    #     classe_csv_filename = sys.argv[1]
    #     pix_result_csv_filename = sys.argv[2]
    # else:
    # Version avec le fichier files.csv qui contient une liste de 2 fichiers
    if COMPUTE_ALL:
        files = open_csv("files.csv", csv_delimiter=",")
        for a_class in files:
            # print(a_class)
            abs_list_filenames.append({"Filename": seconde_session(classe_csv_filename=a_class.get("Pronote"),
                                                                   pix_result_csv_filename=a_class.get("Pix"),
                                                                   output_filename_suffix=a_output_filename_suffix)})
        save_csv(abs_list_filenames, "abs_files.csv")
        if not abs_list_filenames:
            abs_list_filenames = open_csv("abs_files.csv")
        abs_list_filenames = values_as_list(abs_list_filenames, "Filename")
        all_abs = fusion_csvs(list_of_csv_filenames=abs_list_filenames,
                              remove_suffix_classnames=a_output_filename_suffix)
        save_csv(all_abs, filename="all_abs.csv", delimiter=";")

    if COMPUTE_DEBUG:
        # Test avec TG5
        classe_csv_filename = "TG5.csv"
        pix_result_csv_filename = "20230313_resultats_TG5.csv"

        # diff_list_csv_filename = "TG5_abs.csv"
        seconde_session(classe_csv_filename, pix_result_csv_filename)
