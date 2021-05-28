import sys, os, pathlib
sys.path.insert(0, os.getcwd())

import zonefile_parser



# this file had to be move out the source folder because it interacts
# with the fs and is therefore principally an integration test.


class TestIncludeDirective:
    def test_correctly_includes(self):
        this_folder = pathlib.Path(__file__).parent
        zonefile_parser.parseFile(this_folder + "/main.zone")
        assert 2==2
