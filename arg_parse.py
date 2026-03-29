#!/usr/bin/env python3
"""arg_parse - Lightweight argument parser with subcommands and validation."""
import sys

class Arg:
    def __init__(self, name, type=str, default=None, required=False, help=""):
        self.name = name; self.type = type; self.default = default
        self.required = required; self.help = help

class ArgParser:
    def __init__(self, name="", description=""):
        self.name = name; self.description = description
        self.args = []; self.flags = {}; self.subcommands = {}
    def add_argument(self, name, **kwargs):
        self.args.append(Arg(name, **kwargs))
    def add_flag(self, short, long, help=""):
        self.flags[long.lstrip("-")] = {"short": short, "long": long, "help": help}
    def add_subcommand(self, name, parser):
        self.subcommands[name] = parser
    def parse(self, argv):
        result = {"_flags": set(), "_positional": [], "_subcommand": None}
        for a in self.args:
            result[a.name] = a.default
        i = 0
        while i < len(argv):
            arg = argv[i]
            if arg in self.subcommands:
                sub_result = self.subcommands[arg].parse(argv[i+1:])
                sub_result["_subcommand"] = arg
                result.update(sub_result)
                return result
            is_flag = False
            for fname, finfo in self.flags.items():
                if arg == finfo["short"] or arg == finfo["long"]:
                    result["_flags"].add(fname)
                    is_flag = True
                    break
            if not is_flag:
                matched = False
                for a in self.args:
                    if a.name.startswith("--"):
                        if arg == a.name or arg.startswith(a.name + "="):
                            if "=" in arg:
                                result[a.name.lstrip("-")] = a.type(arg.split("=", 1)[1])
                            else:
                                i += 1
                                result[a.name.lstrip("-")] = a.type(argv[i])
                            matched = True
                            break
                if not matched:
                    result["_positional"].append(arg)
            i += 1
        # assign positional args
        pos_args = [a for a in self.args if not a.name.startswith("-")]
        for j, a in enumerate(pos_args):
            if j < len(result["_positional"]):
                result[a.name] = a.type(result["_positional"][j])
        return result

def test():
    p = ArgParser("test", "A test CLI")
    p.add_argument("file", type=str)
    p.add_argument("--count", type=int, default=1)
    p.add_flag("-v", "--verbose")
    r = p.parse(["input.txt", "--count", "5", "-v"])
    assert r["file"] == "input.txt"
    assert r["count"] == 5
    assert "verbose" in r["_flags"]
    # subcommands
    sub = ArgParser("sub")
    sub.add_argument("name")
    p2 = ArgParser("main")
    p2.add_subcommand("greet", sub)
    r2 = p2.parse(["greet", "Alice"])
    assert r2["_subcommand"] == "greet"
    assert r2["name"] == "Alice"
    print("OK: arg_parse")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        test()
    else:
        print("Usage: arg_parse.py test")
