import pytoml as toml
import enscons
import json
import re

def merge(target=None, source=None, env=None):
    # first source is template, scan for "something { replace } something" lines
    template_filename = str(source[0])

    # remainder are .js function files to be encoded and included.
    replacement = {}
    for fn_node in source[1:]:
        fn_pathname = str(fn_node)
        fn_filename = fn_pathname.rsplit('/', 1)[-1]
        fn_name = fn_filename.split('.', 1)[0]
        with open(fn_pathname, 'r') as f:
            fn_content = f.read()
        replacement[fn_name] = fn_content

    with open(str(target[0]), 'w') as target_file:
        with open(template_filename, 'r') as template_file:
            for line in template_file:
                # We'll only do one replacement per line, avoiding recursion
                mo = re.search(r'\"\{\s*([a-z_]+)\s*}\"', line)
                if mo:
                    line = ''.join([
                        line[:mo.start()],
                        json.dumps(replacement[mo.group(1)]),
                        line[mo.end():]
                    ])
                line = re.sub(r'[ \t]+', ' ', line)
                target_file.write(line)


metadata = toml.load(open("pyproject.toml"))["project"]

full_tag = "py3-none-any"

env = Environment(
    tools=["default", "packaging", enscons.generate],
    PACKAGE_METADATA=metadata,
    WHEEL_TAG=full_tag,
)

ddoc_votes = env.Command('proportional_priority_voting/_design/votes.json',
                         ["design/votes.json.template"] + Glob("design/*.js"),
                         env.Action(merge))

py_source = Glob('proportional_priority_voting/*.py') + ddoc_votes

purelib = env.Whl("purelib", py_source, root=".")
whl = env.WhlFile(purelib)

# after the wheel
sdist = env.SDist(source=FindSourceFiles()
                  + ["PKG-INFO", "setup.py", "CHANGES"])
env.NoClean(sdist)
env.Alias("sdist", sdist)

develop = env.Command("#DEVELOP", enscons.egg_info_targets(env), enscons.develop)
env.Alias("develop", develop)

# needed for pep517 / enscons.api to work
env.Default(whl, sdist)
