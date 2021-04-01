import os
from pathlib import Path
from io_utils import unpack, read_string
import sys
import glob

def read_header(f):
    return {
        'type': f.read(4).decode('ascii'),
        'file_info_size': unpack('I', f)[0],
        'constant': unpack('I', f)[0],
        'unk': unpack('I', f)[0],
        'file_count': unpack('I', f)[0],
    }

# The name of the sound file is 32 bytes in. Seems to be a null delimited string.
def get_vag_name(f):
    original_position = f.tell()
    f.seek(32, 1)
    name = read_string(f)
    f.seek(original_position, 0)
    return name

def main():
    print("VBNK Decoder by @HeyThereCoffeee")
    print("For Gauntlet Dark Legacy (PS2)")

    root_out = './out'
    # Create our root output directory
    path = Path(root_out)
    path.mkdir(parents=True, exist_ok=True)

    files = sys.argv[1:]

    # Assume they want to do every file
    if len(files) == 0:
        files = ['--all']

    if files[0] == "--all":
        files = glob.glob('*.vbk')

        if len(files) == 0:
            print("No files found, exiting...")
            return
        # End If
    # End If

    unknown_count = 0

    for file in files:
        print("Opening %s" % file)
        f = open(file, 'rb')

        header = read_header(f)

        # Grab the vbnk name
        vbnk_name = os.path.splitext(os.path.basename(file))[0]
        file_out = "%s/%s/" % (root_out, vbnk_name)
        # Create our path
        dir_name = os.path.dirname(file_out)
        out_path = Path(dir_name)
        out_path.mkdir(parents=True, exist_ok=True)

        # Skip past a lot of unknown stuff
        f.seek(header['file_info_size'], 1)

        for _i in range(header['file_count']):
            has_header_been_read = False
            name = get_vag_name(f)

            if name == "":
                name = "unk%d" % unknown_count
                unknown_count += 1
                print("Unknown VAG (%s) found in %s" % (name, vbnk_name))
            # End If

            file_name = "%s.vag" % name

            print("Extracting %s.vag to %s" % (name, vbnk_name))

            f_file = open("%s/%s" % (file_out, file_name), 'wb')

            while True:
                data = f.read(4)

                # Check for EOF
                if not data:
                    break
                # Check for sound header
                elif data == b'VAGp':
                    # Oh we hit another sound file, break!
                    if has_header_been_read:
                        f.seek(-4, 1)
                        break
                    else:
                        has_header_been_read = True
                    # End If
                
                f_file.write(data)
            # End While

            f_file.close()
        # End For
        f.close()

    print("Finished extracting files!")

    print("All done!")

# End Def


main()