import subprocess
from subprocess import PIPE

class HexPlotter:
    datafile = "data.txt"
    def __init__(self, saver):
        self.__next_plot_id = 0
        self.saver = saver

    def data_preparation(self, label):
        length, keys = None, []
        data = self.saver.stats[label]
        for n, (key, nums) in enumerate(data.items()):
            if n == 0: dline = f"'{self.datafile}' u 1:{n+2}"
            else: dline += f", '' u 1:{n+2}"
            dline += f" w lines title '{key}'"
            if length: assert len(nums) == length
            else: length = len(nums)
            keys.append(key)
        with open(self.datafile, "w") as fd:
            dataline = ""
            for k in range(length):
                dataline = f"{k+1}"
                for key in keys:
                    num = data[key][k]
                    dataline += f" {num}"
                fd.write(f"{dataline}\n")
            return dline

    def set_plot_button(self, button):
        self.plot_button = button

    def get_next_label(self):
        groups = list(sorted(self.saver.stats.keys()))
        group = groups[self.__next_plot_id]
        return f"Plot {group} (p)"

    def plot(self):
        labels = list(sorted(self.saver.stats.keys()))
        label = labels[self.__next_plot_id]
        dline = self.data_preparation(label)
        script = f"""
        set terminal x11
        set grid
        set key out horiz
        set title '{label}'
        plot {dline}
        pause mouse keypress
        """
        cmd = ['gnuplot','-p']
        proc = subprocess.Popen(cmd, stdin=PIPE, shell=True)
        proc.communicate(script.encode('utf-8'))        
        self.__next_plot_id += 1
        self.__next_plot_id %= len(labels)
        label = self.get_next_label()
        self.plot_button.set_label(label)