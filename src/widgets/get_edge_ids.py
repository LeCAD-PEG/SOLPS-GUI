# Python 3.5

import getopt
import sys
import tarfile
try:
    import BytesIO
except ImportError as e:
    from io import BytesIO, StringIO

class GetIDS:
    def __init__(self, shot, run, user, machine, version):

        self.shot = shot
        self.run = run
        self.user = user
        self.machine = machine
        self.version = version

        self.ids = imas.ids(shot, run)
        self.state = self.open_ids()

    def open_ids(self):
        print('Opening IDS')
        self.ids.open_env(self.user, self.machine, self.version)
        if self.ids.isConnected():
            print('IDS opened OK!')
            return True
        else:
            print('IDS open failed!')
            return False

    def read_code_parameters(self):
        self.ids.edge_profiles.get()
        parameter_string = self.ids.edge_profiles.code.parameters.encode()
        return parameter_string.replace(b'\x01', b'\x00').decode()

    def extract_files(self):
        bstr = self.read_code_parameters().encode()

        tf = BytesIO()
        tf.write(bstr)
        tar = tarfile.TarFile(mode='r', fileobj=tf)
        print(tar.list(verbose=False))
        for member in tar:
            print('Member: ', member.name)





if __name__ == '__main__':
    try:
        import imas
    except ImportError as e:
        print('There is no imas module... exiting!')
        sys.exit()
    """
    python3.5 put_edge_ids.py --dirpath=/home/ITER/simicg/RUNS/demo/2171/baserun\
    <--user=simicg --run=1001 --shot=1001 --device=solps-iter --version=3
    """

    # user = "simicg"
    # run = 1005
    # shot = 1005
    # machine = "solps-iter"
    # version = "3"
    # x = GetIDS(shot, run, user, machine, version)
    # if x.state == 'False':
    #     sys.exit()
    # string = x.read_code_parameters()
    # print(string)
    # print(x.ids.edge_profiles)


    # For launching python script directly from treminal with python command
    try:
        opts, args = getopt.getopt(sys.argv[1:], "srutvh", ["dirpath=",
                                                            "shot=", "run=",
                                                            "user=", "device=",
                                                            "version=", "help"])
        for opt, arg in opts:
            #print opt, arg
            if opt in ("-s", "--shot"):
                shot = int(arg)
            elif opt in ("-r", "--run"):
                run = int(arg)
            elif opt in ("-u", "--user"):
                user = arg
            elif opt in ("-t", "--device"):
                device = arg
            elif opt in ("-v", "--version"):
                version = arg

            if opt in ("-h", "--help"):
                print("In order to run b2read file path, shot, run, user,"
                    "device and version variables must be defined."
                    "Example (terminal): "
                    "python3.5 put_edge_ids.py "
                    "baserun "
                    "--shot=1000 --run=1 --user=tomsicp --device=solps-iter "
                    "--version=3")
                sys.exit()

    except Exception:
        print ('Supplied option not recognized!')
        print ('For help: b2read -h / --help')
        sys.exit(2)

    # few paths to example files for testing
    # /home/ITER/tomsicp/solps-iter/runs/AUG_16151_D/baserun
    # /home/ITER/tomsicp/solps-iter-devel/runs/ITER_535_D+He+Ar/baserun
    # run: "imasdb solps-iter"
    # Example command:
    """
python3.5 get_edge_ids.py --dirpath=/home/ITER/simicg/RUNS/demo/2171/baserun --user=simicg --run=1001 --shot=1001 --device=solps-iter --version=3
    """
    ids = GetIDS(shot, run, user, device, version)
    if ids.state == False:
        sys.exit()
    string = ids.read_code_parameters()
    print(string[:500])
    ids.extract_files()
