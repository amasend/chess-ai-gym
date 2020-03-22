# chess-ai-gym

Requirements to install pygraphviz:

sudo apt-get install python3-dev graphviz libgraphviz-dev pkg-config
sudo apt-get install python-numpy python-scipy python-matplotlib





Dependencies to install graph-tool:

sudo apt-get install libboost-all-dev
sudo apt-get install libgmp-dev

sudo apt-get install libcgal-dev
sudo apt-get install libcairomm-1.0

pip install pycairo
sudo apt-get install libsparsehash-dev
sudo apt install python3-gi gobject-introspection gir1.2-gtk-3.0
sudo apt-get install libgtk-3-dev

https://download.gnome.org/sources/gtk+/3.0/
https://developer.gnome.org/gtk3/stable/gtk-building.html


gtk needs Glib >= version
here meson and ninja is needed
glib needs mount: sudo apt-get install libmount-dev
meson: https://mesonbuild.com/Getting-meson.html : here you should open meson from directory: path_to_meson/meson.py _build eg: ../meson-0.53.2/meson.py _build
ninja -C _build
sudo ninja -C _build install

pango > 1.41
https://download.gnome.org/sources/pango/1.42/
you need to install sudo apt install libfribidi-dev

1. `cd' to the directory containing the package's source code and type
     `./configure' to configure the package for your system.  If you're
     using `csh' on an old version of System V, you might need to type
     `sh ./configure' instead to prevent `csh' from trying to execute
     `configure' itself.

     Running `configure' takes awhile.  While running, it prints some
     messages telling which features it is checking for.

  2. Type `make' to compile the package.

  3. Optionally, type `make check' to run any self-tests that come with
     the package.

  4. Type `make install' to install the programs and any data files and
     documentation.

  5. You can remove the program binaries and object files from the
     source code directory by typing `make clean'.  To also remove the
     files that `configure' created (so you can compile the package for
     a different kind of computer), type `make distclean'.  There is
     also a `make maintainer-clean' target, but that is intended mainly
     for the package's developers.  If you use it, you may have to get
     all sorts of other programs in order to regenerate files that came
     with the distribution.
