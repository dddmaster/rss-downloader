package(default_visibility = ["//visibility:public"])
load("@subpar//:subpar.bzl", "par_binary")
load("@my_deps//:requirements.bzl", "requirement")

par_binary (
    name = "rss_downloader",
    srcs = ["rss_downloader.py"],
    deps = [
      requirement("appdirs"),
      requirement("feedparser"),
      requirement("packaging"),
      requirement("pyparsing"),
      requirement("requests"),
      requirement("schedule"),
      requirement("six"),
    ]
)

py_test(
    name = "test_rss_downloader",
    srcs = ["test_cases.py"],
    data = ["test_responses"],
    deps = [":rss_downloader"],
    main = "test_cases.py"
)
