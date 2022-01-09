import os
import shutil

from os.path import join

isa_dir = "isa"
package_dir = "riscv-tests"
bin_dir = join(package_dir, "riscv-tests-bin")
hex_dir = join(package_dir, "riscv-tests-hex")


def clean():
    for dr in [bin_dir, hex_dir]:
        for file_name in os.listdir(dr):
            if file_name in ['README.md', 'LICENSE']:
                continue
            shutil.rmtree(join(dr, file_name))


def get_hex(s_path, XLEN):
    print(s_path)
    with open(s_path, "r") as f:
        file = f.read().splitlines()
    inst_part = [i for i in file if '\t' in i]
    addr_insts = [i.split('\t')[0:2] for i in inst_part]
    addr_insts = [[i[0][:-1], i[1].strip()] for i in addr_insts]
    addr_insts = [i for i in addr_insts if i[1] != '']
    # split `inst` into bytes, put in `insts` by `addr`
    insts = []
    for addinsr in addr_insts:
        addr = int(addinsr[0], 16) - int("80000000", 16)
        inst = addinsr[1]
        insts += ["00"] * (addr - len(insts))
        for i in range(len(inst), 0, -2):
            insts.append(inst[i-2: i])
    # fill 
    res = len(insts) % (XLEN//8)
    if res != 0:
        insts += ["00"] * (XLEN//8 - res)
    # merge bytes to 32-bits or 64-bits
    t_insts = []
    for i in range(0, len(insts), XLEN//8):
        t = ""
        for j in range(0, XLEN//8):
            t = insts[i+j] + t
        t_insts.append(t)

    return t_insts


if __name__ == "__main__":
    clean()
    # bin
    for file_name in os.listdir(isa_dir):
        if not "-p-" in file_name:
            continue
        tp = file_name.split("-")[0]
        back = file_name.split("-")[2]
        bin_type_dir = join(bin_dir, tp)
        if not os.path.exists(bin_type_dir):
            os.makedirs(bin_type_dir)
        shutil.copy(join(isa_dir, file_name),
                    join(bin_type_dir, "{}-{}".format(tp, back))
                    )
    # hex
    for file_name in os.listdir(isa_dir):
        if not ("-p-" in file_name and ".dump" in file_name):
            continue
        tp = file_name.split("-")[0]
        back = file_name.split("-")[2]
        hex_type_dir = join(hex_dir, tp)
        if not os.path.exists(hex_type_dir):
            os.makedirs(hex_type_dir)
        s_path = join(isa_dir, file_name)
        t_path = join(hex_type_dir, "{}-{}".format(tp, back))
        shutil.copy(s_path, t_path)

        inst = back.split(".")[0]
        h_path = join(hex_type_dir, "{}-{}.hex".format(tp, inst))
        if "rv32" in tp:
            hex = get_hex(s_path, 32)
        else:
            hex = get_hex(s_path, 64)
        with open(h_path, "w") as f:
            f.writelines(i + '\n' for i in hex)
