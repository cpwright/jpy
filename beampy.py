# Example for jpy

import os
import jpy

def _collect_classpath(path, classpath):
    for name in os.listdir(path):
        file = os.path.join(path, name)
        if name.endswith('.jar') or name.endswith('.zip') or os.path.isdir(file):
            classpath.append(file)

def _create_classpath():

    # todo: read 'beam_home' from a configuration file (beampy.ini)
    beam_home = os.getenv('BEAM_HOME', os.getenv('BEAM5_HOME'))

    invalid_beam_home = RuntimeError('BEAM_HOME environment variable must be set to a valid BEAM installation directors')

    if beam_home is None:
        raise invalid_beam_home

    beam_bin = os.path.join(beam_home, 'bin')
    beam_lib = os.path.join(beam_home, 'lib')
    beam_mod = os.path.join(beam_home, 'modules')

    print('beam_bin =', beam_bin, os.path.exists(beam_bin))
    print('beam_lib =', beam_lib, os.path.exists(beam_lib))
    print('beam_mod =', beam_mod, os.path.exists(beam_mod))

    if not (os.path.exists(beam_bin)
            and os.path.exists(beam_lib)
            and os.path.exists(beam_mod)):
        raise invalid_beam_home

    os.listdir(beam_lib)

    classpath = []
    _collect_classpath(beam_mod, classpath)
    _collect_classpath(beam_lib, classpath)
    _collect_classpath(beam_bin, classpath)

    return classpath


classpath = _create_classpath()

del _create_classpath
del _collect_classpath

#import pprint
#pprint.pprint(classpath)

# todo: read 'debug' and additional options from a configuration file (beampy.ini)
#debug = True
debug = False
jpy.create_jvm(options=['-Djava.class.path=' + os.pathsep.join(classpath), '-Xmx512M'], debug=debug)

try:
    # todo: read pre-defined types from a configuration file (beampy.ini)
    ProductIO = jpy.get_jtype('org.esa.beam.framework.dataio.ProductIO')
    Product = jpy.get_jtype('org.esa.beam.framework.datamodel.Product')
    Band = jpy.get_jtype('org.esa.beam.framework.datamodel.Band')
    VirtualBand = jpy.get_jtype('org.esa.beam.framework.datamodel.VirtualBand')
    GeoCoding = jpy.get_jtype('org.esa.beam.framework.datamodel.GeoCoding')
except Exception:
    jpy.destroy_jvm()
    raise

