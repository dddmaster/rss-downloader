import unittest
from rss_downloader import RssDownloader
import SimpleHTTPServer
import HeaderAddingHTTPRequestHandler
import SocketServer
from threading import Thread
import os
import shutil

global_refs = {}

# Here's our "unit tests".
class IsOddTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        PORT = 8080
        Handler = SimpleHTTPServer.SimpleHTTPRequestHandler
        httpd = SocketServer.TCPServer(("", PORT), Handler)
        print "serving at port", PORT
        try:
            thread = Thread(target=httpd.serve_forever)
            thread.start()
            global_refs['thread'] = thread
            global_refs['httpd'] = httpd
        except Exception:
            print "Could not start spoof server"

    def testDownloadsFilesFromTwoSources(self):
        test_path = "./build/test_dir"
        if os.path.exists(test_path):
            shutil.rmtree(test_path)
        os.makedirs(test_path)
        rss_downloader = RssDownloader(test_path,
                                       ["http://localhost:8080/test_responses/main.xml",
                                        "http://localhost:8080/test_responses/main2.xml"])
        rss_downloader.run()
        self.assertTrue(os.path.exists(test_path + "/entries/test_file_1"))
        self.assertTrue(os.path.exists(test_path + "/entries/test_file_2"))
        self.assertTrue(os.path.exists(test_path + "/entries/test_file_3"))
        self.assertTrue(os.path.exists(test_path + "/marked_as_read/dGVzdF9maWxlXzI="))
        self.assertTrue(os.path.exists(test_path + "/marked_as_read/dGVzdF9maWxlXzE="))
        self.assertTrue(os.path.exists(test_path + "/marked_as_read/dGVzdF9maWxlXzM="))

    @classmethod
    def tearDownClass(cls):
        global_refs['httpd'].server_close()
        global_refs['thread'].join(1)

def main():
    unittest.main()

if __name__ == '__main__':
    main()
