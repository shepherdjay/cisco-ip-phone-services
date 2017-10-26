import os

import xmltodict

import ciscoipphone


def get_path(filename):
    path = os.path.join(os.path.dirname(__file__), filename)
    return path


def get_test_file(filename):
    with open(get_path(filename), 'r') as file:
        return file.read()


def list_equal(list1, list2):
    for i in list1:
        try:
            list2_index = list2.index(i)
            i2 = list2[list2_index]
        except IndexError:
            return False

        if isinstance(i, dict):
            if not dictionary_equal(i, i2):
                return False
            else:
                continue

        if isinstance(i, list):
            if not list_equal(i, i2):
                return False
            else:
                continue

        if i != i2:
            return False
    return True


def dictionary_equal(dict1, dict2):
    for key, value in dict1.items():
        # Check if we can even get element
        try:
            dict2value = dict2[key]
        except KeyError:
            return False

        # If another dictionary loop
        if isinstance(value, dict) and isinstance(dict2value, dict):
            if not dictionary_equal(value, dict2value):
                return False
            else:
                continue

        # If list send to list equal comparator
        if isinstance(value, list) and isinstance(dict2value, list):
            if not list_equal(value, dict2value):
                return False
            else:
                continue

        # Must be regular value lets compare
        if value != dict2value:
            return False

    return True


class TestReadme(object):
    def test_generating_ciscoipphonemenu(self, capsys):
        expected = xmltodict.parse(get_test_file('readme_ciscoipphone_expected'), encoding='utf8',
                                   dict_constructor=dict)

        menu = ciscoipphone.services.Menu(prompt="Select a directory")
        menu.add_item("My Contacts", "http://server/directory/contacts")
        menu.add_item("Businesses", "http://server/directory/businesses")
        menu.prettify()
        received, err = capsys.readouterr()
        received = xmltodict.parse(received, encoding='utf8', dict_constructor=dict)

        assert dictionary_equal(received, expected)

    def test_generating_CiscoIpPhoneDirectory(self, capsys):
        expected = xmltodict.parse(get_test_file('readme_ciscoipphonedirectory_expected'), encoding='utf8', dict_constructor=dict)

        directory = ciscoipphone.services.Directory(prompt='Select a contact', title='My Contacts')
        directory.add_entry('Avon Barksdale', 18442391546)
        directory.add_entry('Stringer Bell', 18993712775)
        directory.add_softkey('Dial', 'SoftKey:Dial', 1)
        directory.prettify()
        received, err = capsys.readouterr()
        received = xmltodict.parse(received, encoding='utf8', dict_constructor=dict)

        assert dictionary_equal(received, expected)