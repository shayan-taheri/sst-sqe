##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install sst-core
#
# You can edit this file again by typing:
#
#     spack edit sst-core
#
# See the Spack documentation for more information on packaging.
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
from spack import *


class SstCore(Package):
    """This is the SST-Core."""

    homepage = "http://sst-simulator.org/"
    url      = "https://github.com/sstsimulator/sst-core/releases/download/v7.2.0_Final/sstcore-7.2.0.tar.gz"

    version('7.2.0', '854dce217764d980f01766ad2469decd')
    version('7.1.0', '1b6c91920bf5b7d28ad2391ffc759b35')
    version('7.0.0', 'd4c0bc759838d103a5561fdc57b203ae')
    version('6.1.0', '9cc854a06d65a1607fab51e71f93979a')
    version('6.0.0', 'e310764ce5ffaeb52d0d935280f53eda')
    version('master', git='https://github.com/sstsimulator/sst-core.git', branch='master')
    version('devel', git='https://github.com/sstsimulator/sst-core.git', branch='devel')

    variant('openmpi', default=True, description='Defined MPI to use.')
    variant('zoltan', default=False, description='Enable Zoltan support.')
    variant('disable-mpi', default=False, description='Disable MPI support.')
    variant('debug', default=False, description='Enables additional debug output to be compiled by components and the SST core.')

    depends_on('zoltan -shared -fortran - parmetis -mpi', when='+zoltan')
    depends_on('openmpi@1.8.8')  # We depend on MPI but may disable if not needed
#    depends_on('openmpi', when='-disable-mpi')

    def install(self, spec, prefix):
        # Perform Autogen
        autogen = Executable('./autogen.sh')
        autogen()

        # Setup Configure arguments
        config_args = []

        if '+zoltan' in spec:
            config_args.append('--with-zoltan={0}'.format(spec['zoltan'].prefix))

        if '+disable-mpi' in spec:
            config_args.append('--disable-mpi')

        # Configure 
        configure("--prefix=" + prefix,
                  "--disable-silent-rules",
                  *config_args)
        
        # Make
        make()
        
        # Make Install
        make("install")
        
        
        
        
        
        
        