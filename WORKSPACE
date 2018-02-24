git_repository(
    name = "subpar",
    remote = "https://github.com/google/subpar",
    tag = "1.0.0",
)

git_repository(
    name = "io_bazel_rules_python",
    remote = "https://github.com/bazelbuild/rules_python.git",
    commit = "3175797bd07aac4ff35fa711f0a82285f2005e42",
)

load("@io_bazel_rules_python//python:pip.bzl", "pip_repositories")

pip_repositories()

load("@io_bazel_rules_python//python:pip.bzl", "pip_import")

pip_import(
   name = "my_deps",
   requirements = "//:requirements.txt"
)

load("@my_deps//:requirements.bzl", "pip_install")
pip_install()
