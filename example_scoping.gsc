[
    "sequenz",
    ["setzen", "x", "100"],
    ["func", "one", [], [["print", ["bekommen", "x"]]]],
    ["func", "two", [], [["setzen", "x", "42"], ["call", "one"]]],
    ["func", "main", [], [["call", "two"]]],
    ["call", "main"]
]