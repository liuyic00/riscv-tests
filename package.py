import os
import shutil

isa_dir = "isa"
bin_dir = "riscv-tests"


def clean():
    for file_name in os.listdir(bin_dir):
        if file_name in ['README.md', 'LICENSE']:
            continue
        shutil.rmtree(os.path.join(bin_dir, file_name))


if __name__ == "__main__":
    clean()
    for file_name in os.listdir(isa_dir):
        if not "-p-" in file_name:
            continue
        tp = file_name.split("-")[0]
        inst = file_name.split("-")[2]
        type_dir = os.path.join(bin_dir, tp)
        if not os.path.exists(type_dir):
            os.makedirs(type_dir)
        shutil.move(os.path.join(isa_dir, file_name),
                    os.path.join(type_dir, "{}-{}".format(tp, inst))
                    )
