import lupa

supported_sources = ["joystick"]
lua = lupa.LuaRuntime()


def loadRawDiffs(module):
    get_diff(module)
    return diffs


def convert_table_to_dict(table):
    dict_data = {}
    for k, v in table.items():
        if lupa.lua_type(v) == "table":
            vd = convert_table_to_dict(v)
        else:
            vd = v
        dict_data[k] = vd
    return dict_data


def get_diff(module):
    with open(module[0]) as f:
        diff_file = f.read()
    diff_file = diff_file[diff_file.index("{") : diff_file.rindex("}") + 1]
    lua_table = lua.eval(diff_file)
    diff = convert_table_to_dict(lua_table)
    return diff
