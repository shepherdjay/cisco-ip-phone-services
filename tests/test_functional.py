import ciscoipphone
import os


def get_path(filename):
    path = os.path.join(os.path.dirname(__file__), filename)
    return path


def get_test_file(filename):
    with open(get_path(filename), 'r') as file:
        return file.read()


class TestReadme(object):
    def test_generating_ciscoipphonemenu(selfs, capsys):
        expected = get_test_file('readme_ciscoipphone_expected')

        menu = ciscoipphone.services.Menu(prompt="Select a directory")
        menu.add_item("My Contacts", "http://server/directory/contacts")
        menu.add_item("Businesses", "http://server/directory/businesses")
        menu.prettify()
        received, err = capsys.readouterr()

        assert received == expected

    def test_generating_CiscoIpPhoneDirectory(self, capsys):
        expected = get_test_file('readme_ciscoipphonedirectory_expected')

        directory = ciscoipphone.services.Directory(prompt='Select a contact', title='My Contacts')
        directory.add_entry('Avon Barksdale', 18442391546)
        directory.add_entry('Stringer Bell', 18993712775)
        directory.add_softkey('Dial', 'SoftKey:Dial', 1)
        directory.prettify()
        received, err = capsys.readouterr()

        assert received == expected
