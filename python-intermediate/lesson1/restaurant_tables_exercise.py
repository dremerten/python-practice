tables = {
  1: ['Jiho', False],
  2: [],
  3: [],
  4: [],
  5: [],
  6: [],
  7: [],
}

def assign_table(table_number, name, vip_status=False):
    if not isinstance(table_number, int):
        raise TypeError("table_number must be int")
    if not isinstance(name, str):
        raise TypeError("name must be string")
    if not isinstance(vip_status, bool):
        raise TypeError("vip_status must be boolean")
    tables.update({table_number: [name, vip_status]})
    return tables

yoni = assign_table(6, "Yoni", False)
martha = assign_table(table_number=3, name="Martha", vip_status=True)
karla = assign_table(4, "Karla")
print(tables)

result = assign_table(2, "joe", True)
print(result)