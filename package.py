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
    insts = [i.split(':')[1].split()[0] for i in inst_part]
    insts = [i for i in insts if len(i) == 8]
    if XLEN == 32:
        return insts
    else:
        insts64 = []
        if len(insts) % 2 == 1:
            insts.append("00000000")
        for i in range(0, len(insts), 2):
            insts64.append(insts[i+1] + insts[i])
        return insts64


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
