import os


def command(name):
#    os.system(f"convert {name} -alpha copy -fx '#000' {name}")
#    os.system(f"convert {name} -colorspace srgb -type truecolor  {name}")
    os.system(f"convert {name} -set colorspace RGB -colorspace gray {name}")   
command('checkbox.png')
command('down_arrow.png')
command('handle.png')
